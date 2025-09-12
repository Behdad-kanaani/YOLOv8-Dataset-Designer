import os, threading, warnings
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

from app.config import Config
from app.i18n import t, LANGS, fa_digits, normalize_number_text
from app.utils.io import imread_rgb
from app.utils.boxes import xyxy_from_yolo, yolo_from_xyxy
from app.aug.pipelines import build_geometry, build_color
from app.aug.resize import build_resize
from app.pipeline.preview import make_preview_grid
from app.pipeline.generator import generate_dataset

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("YOLOv8 Dataset Designer – Ultra UI (Stable Rev)")
        self.geometry("1280x800")
        self.minsize(1100, 700)

        self.lang = "fa"
        try:
            import tkinter.font as tkfont
            f = tkfont.nametofont("TkDefaultFont")
            f.configure(family="Vazirmatn", size=12)
        except Exception:
            pass

        self.cfg = Config()
        self.base_img = None
        self.tk_img  = None
        self.scale = 1.0
        self.drag_start = None
        self.canvas_rect = None
        self.show_box = True

        self._build_layout()
        self._bind_keys()
        self._apply_texts()
        self._log(t(self, "ready"))

    # ---- Thread-safe helpers ----
    def _ui(self, fn, *args, **kwargs):
        self.after(0, lambda: fn(*args, **kwargs))

    def _log(self, msg):
        def _do():
            self.log_box.insert("end", msg + "\n")
            self.log_box.see("end")
        self._ui(_do)

    def _set_progress(self, val):
        self._ui(self.prog.set, max(0.0, min(1.0, float(val))))

    def _info_box(self, title, msg):
        self._ui(messagebox.showinfo, title, msg)

    def _error_box(self, title, msg):
        self._ui(messagebox.showerror, title, msg)

    # ---- Layout ----
    def _build_layout(self):
        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)

        left = ctk.CTkFrame(self, corner_radius=16)
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left.rowconfigure(0, weight=7)
        left.rowconfigure(1, weight=3)
        left.columnconfigure(0, weight=1)

        self.canvas = ctk.CTkCanvas(left, bg="#111417", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.canvas.bind("<ButtonPress-1>", self.on_down)
        self.canvas.bind("<B1-Motion>",    self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_up)

        self.preview = ctk.CTkLabel(left, text="", anchor="center")
        self.preview.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

        right = ctk.CTkFrame(self, corner_radius=16)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right.columnconfigure(0, weight=1)

        topbar = ctk.CTkFrame(right)
        topbar.pack(fill="x", padx=8, pady=(6,0))
        self.btn_lang = ctk.CTkSegmentedButton(topbar, values=[LANGS["fa"]["lang_btn_fa"], LANGS["en"]["lang_btn_en"]],
                                               command=self._switch_lang)
        self.btn_lang.set(LANGS["fa"]["lang_btn_fa"] if self.lang=="fa" else LANGS["en"]["lang_btn_en"])
        self.btn_lang.pack(side="right")

        file_row = ctk.CTkFrame(right); file_row.pack(fill="x", padx=8, pady=6)
        self.btn_open = ctk.CTkButton(file_row, text="", command=self.cmd_open); self.btn_open.pack(side="left", padx=4)
        self.btn_out  = ctk.CTkButton(file_row, text="", command=self.cmd_outdir); self.btn_out.pack(side="left", padx=4)
        self.lbl_file = ctk.CTkLabel(file_row, text=""); self.lbl_file.pack(side="left", padx=6)

        cls_frame = ctk.CTkFrame(right); cls_frame.pack(fill="x", padx=8, pady=6)
        self.lbl_classes = ctk.CTkLabel(cls_frame, text="", anchor="e", justify="right")
        self.lbl_classes.pack(anchor="w", padx=6, pady=(6,2))
        self.class_list = ctk.CTkOptionMenu(cls_frame, values=self.cfg.class_names,
                                            command=lambda _: self.on_select_class())
        self.class_list.pack(fill="x", padx=6, pady=(0,6))
        add_row = ctk.CTkFrame(cls_frame, fg_color="transparent"); add_row.pack(fill="x", padx=6, pady=(0,6))
        self.new_class_entry = ctk.CTkEntry(add_row, placeholder_text="")
        self.new_class_entry.pack(side="left", fill="x", expand=True, padx=(0,6))
        self.btn_add_class = ctk.CTkButton(add_row, text="", width=70, command=self.cmd_add_class); self.btn_add_class.pack(side="left")

        prm = ctk.CTkFrame(right); prm.pack(fill="x", padx=8, pady=6)
        self.row_total = self._param_row(prm, key="total_samples", init_val=self.cfg.total, hint="[20..5000] step=20")
        self.row_val   = self._param_row(prm, key="val_ratio", init_val=self.cfg.val_ratio, hint="[0.05..0.5] step=0.01")
        self.row_w     = self._param_row(prm, key="out_w", init_val=self.cfg.out_w, hint="[320..2048] step=32")
        self.row_h     = self._param_row(prm, key="out_h", init_val=self.cfg.out_h, hint="[320..2048] step=32")

        row_geo = ctk.CTkFrame(prm, fg_color="transparent"); row_geo.pack(fill="x", padx=6, pady=(6,0))
        self.lbl_geo = ctk.CTkLabel(row_geo, text="", width=140, anchor="e", justify="right")
        self.lbl_geo.pack(side="right")
        self.cmb_geo = ctk.CTkOptionMenu(row_geo, values=["light","medium","hard"]); self.cmb_geo.set(self.cfg.geo)
        self.cmb_geo.pack(side="right", padx=(6,10))

        row_col = ctk.CTkFrame(prm, fg_color="transparent"); row_col.pack(fill="x", padx=6, pady=(6,0))
        self.lbl_col = ctk.CTkLabel(row_col, text="", width=140, anchor="e", justify="right")
        self.lbl_col.pack(side="right")
        self.cmb_col = ctk.CTkOptionMenu(row_col, values=["light","medium","hard"]); self.cmb_col.set(self.cfg.col)
        self.cmb_col.pack(side="right", padx=(6,10))

        self.row_q    = self._param_row(prm, key="jpeg_quality", init_val=self.cfg.jpeg_q, hint="[70..100] step=1")
        self.row_seed = self._param_row(prm, key="random_seed", init_val=self.cfg.seed, hint="[0..999999] step=1")

        self.chk_zip = ctk.CTkCheckBox(prm, text="", command=self._toggle_zip)
        if self.cfg.make_zip: self.chk_zip.select()
        self.chk_zip.pack(anchor="e", padx=6, pady=6)

        boxf = ctk.CTkFrame(right); boxf.pack(fill="x", padx=8, pady=6)
        self.lbl_box = ctk.CTkLabel(boxf, text="")
        self.lbl_box.pack(anchor="e", padx=6, pady=4)
        btns = ctk.CTkFrame(boxf, fg_color="transparent"); btns.pack(fill="x", padx=6, pady=(0,6))
        self.btn_save_box = ctk.CTkButton(btns, text="", command=self.cmd_save_box); self.btn_save_box.pack(side="right", padx=4)
        self.btn_clear_box= ctk.CTkButton(btns, text="", command=self.cmd_clear_box); self.btn_clear_box.pack(side="right", padx=4)
        self.btn_toggle_box=ctk.CTkButton(btns, text="", command=self.cmd_toggle_box); self.btn_toggle_box.pack(side="right", padx=4)

        act = ctk.CTkFrame(right); act.pack(fill="x", padx=8, pady=6)
        self.btn_preview = ctk.CTkButton(act, text="", fg_color="#3a7ebf", command=self.cmd_preview)
        self.btn_preview.pack(fill="x", padx=6, pady=6)
        self.btn_generate = ctk.CTkButton(act, text="", fg_color="#22a06b", command=self.cmd_generate)
        self.btn_generate.pack(fill="x", padx=6, pady=(0,8))

        stat = ctk.CTkFrame(right); stat.pack(fill="both", expand=True, padx=8, pady=6)
        self.prog = ctk.CTkProgressBar(stat); self.prog.set(0.0); self.prog.pack(fill="x", padx=8, pady=8)
        self.log_box = ctk.CTkTextbox(stat, height=180)
        self.log_box.pack(fill="both", expand=True, padx=8, pady=(0,8))

    def _param_row(self, parent, key, init_val, hint):
        row = ctk.CTkFrame(parent, fg_color="transparent"); row.pack(fill="x", padx=6, pady=(6,0))
        lbl = ctk.CTkLabel(row, text="", width=160, anchor="e", justify="right"); lbl.pack(side="right")
        ent = ctk.CTkEntry(row, width=110, justify="left"); ent.insert(0, str(init_val)); ent.pack(side="right", padx=(6,10))
        hint_lbl = ctk.CTkLabel(row, text=hint, text_color="#7f8ea3"); hint_lbl.pack(side="right", padx=(0,6))
        row.label, row.entry, row.hint = lbl, ent, hint_lbl
        row.meta = {"key": key}
        return row

    def _bind_keys(self):
        self.bind("<space>", lambda e: self.cmd_toggle_box())
        self.bind("<Control-s>", lambda e: self.cmd_save_box())
        self.bind("<Control-g>", lambda e: self.cmd_generate())
        self.bind("<Delete>", lambda e: self.cmd_clear_box())

    # ---- i18n ----
    def _switch_lang(self, val):
        if val in (LANGS["fa"]["lang_btn_fa"], "FA"):
            self.lang = "fa"
        else:
            self.lang = "en"
        self._apply_texts()

    def _apply_texts(self):
        # Files
        self.btn_open.configure(text=t(self,"open_image"))
        self.btn_out.configure(text=t(self,"output_folder"))
        self.lbl_file.configure(text=(t(self,"no_image") if not self.cfg.image_path else os.path.basename(self.cfg.image_path)))
        # Classes
        self.lbl_classes.configure(text=t(self,"classes"), anchor="e", justify="right")
        self.new_class_entry.configure(placeholder_text=t(self,"new_class_ph"))
        self.btn_add_class.configure(text=t(self,"add"))
        # Params
        self._set_row_label(self.row_total, "total_samples")
        self._set_row_label(self.row_val,   "val_ratio")
        self._set_row_label(self.row_w,     "out_w")
        self._set_row_label(self.row_h,     "out_h")
        self.lbl_geo.configure(text=t(self,"geometry"), anchor="e", justify="right")
        self.lbl_col.configure(text=t(self,"color"), anchor="e", justify="right")
        self._set_row_label(self.row_q,     "jpeg_quality")
        self._set_row_label(self.row_seed,  "random_seed")
        self.chk_zip.configure(text=t(self,"zip_after"))
        # Box
        self.lbl_box.configure(text=t(self,"box"))
        self.btn_save_box.configure(text=t(self,"save_box"))
        self.btn_clear_box.configure(text=t(self,"clear"))
        self.btn_toggle_box.configure(text=t(self,"toggle"))
        # Actions
        self.btn_preview.configure(text=t(self,"preview"))
        self.btn_generate.configure(text=t(self,"generate"))
        # Language segmented values
        self.btn_lang.configure(values=[LANGS["fa"]["lang_btn_fa"], LANGS["en"]["lang_btn_en"]])
        self.btn_lang.set(LANGS[self.lang]["lang_btn_fa"] if self.lang=="fa" else LANGS[self.lang]["lang_btn_en"])

    def _set_row_label(self, row, key):
        row.label.configure(text=t(self,key), anchor="e", justify="right")
        if self.lang == "fa":
            row.hint.configure(text=fa_digits(row.hint.cget("text")))
        else:
            row.hint.configure(text=normalize_number_text(row.hint.cget("text")))

    # ---- IO ----
    def cmd_open(self):
        path = filedialog.askopenfilename(title=t(self,"open_image"),
            filetypes=[("Images","*.jpg;*.jpeg;*.png;*.bmp;*.webp")])
        if not path: return
        try:
            self.base_img = imread_rgb(path)
            self.cfg.image_path = path
            self._fit_to_canvas()
            self.lbl_file.configure(text=os.path.basename(path))
            self._log(f"{t(self,'img_opened')}: {path}")
        except Exception as e:
            self._error_box("Error", str(e))

    def cmd_outdir(self):
        p = filedialog.askdirectory(title=t(self,"output_folder"))
        if p:
            self.cfg.output_root = p
            self._log(f"{t(self,'output')}: {p}")

    # ---- Canvas & Box ----
    def _fit_to_canvas(self):
        if self.base_img is None: return
        H, W = self.base_img.shape[:2]
        cW = max(600, self.winfo_width() - 520)
        cH = max(400, int((self.winfo_height() - 260) * 0.6))
        s = min(cW/W, cH/H)
        self.scale = max(0.15, min(1.0, s))
        disp = Image.fromarray(self.base_img).resize((int(W*self.scale), int(H*self.scale)), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(disp)
        self.canvas.delete("all")
        self.canvas.configure(width=disp.size[0], height=disp.size[1])
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self._draw_box()

    def _draw_box(self):
        if self.canvas_rect:
            self.canvas.delete(self.canvas_rect); self.canvas_rect=None
        if not (self.cfg.has_box and self.base_img is not None and self.show_box): return
        H, W = self.base_img.shape[:2]
        x,y,w,h = self.cfg.yolo_box
        x1,y1,x2,y2 = xyxy_from_yolo(x,y,w,h,W,H)
        x1c,y1c,x2c,y2c = x1*self.scale, y1*self.scale, x2*self.scale, y2*self.scale
        self.canvas_rect = self.canvas.create_rectangle(x1c,y1c,x2c,y2c, outline="#00FF88", width=2)

    def on_down(self, e):
        if self.base_img is None: return
        self.drag_start = (e.x, e.y)
        if self.canvas_rect:
            self.canvas.delete(self.canvas_rect); self.canvas_rect=None

    def on_move(self, e):
        if self.drag_start is None: return
        x0,y0 = self.drag_start
        if self.canvas_rect:
            self.canvas.coords(self.canvas_rect, x0,y0, e.x,e.y)
        else:
            self.canvas_rect = self.canvas.create_rectangle(x0,y0, e.x,e.y, outline="#00FF88", width=2, dash=(5,3))

    def on_up(self, e):
        if self.drag_start is None: return
        x0,y0 = self.drag_start; self.drag_start=None
        if self.base_img is None: return
        H, W = self.base_img.shape[:2]
        # map to image coords
        x1 = int(round(x0 / self.scale)); y1 = int(round(y0 / self.scale))
        x2 = int(round(e.x / self.scale)); y2 = int(round(e.y / self.scale))
        X1,Y1 = min(x1,x2), min(y1,y2); X2,Y2 = max(x1,x2), max(y1,y2)
        if (X2-X1)<5 or (Y2-Y1)<5:
            self._log(t(self,"box_too_small"))
            return
        self.cfg.yolo_box = yolo_from_xyxy(X1,Y1,X2,Y2,W,H)
        self.cfg.has_box = True
        self.show_box = True
        self._draw_box()
        self._log(t(self,"box_saved"))

    def cmd_save_box(self):
        if not self.cfg.has_box:
            self._log(t(self,"need_box")); return
        self._log(t(self,"box_saved"))

    def cmd_clear_box(self):
        self.cfg.has_box = False
        if self.canvas_rect:
            self.canvas.delete(self.canvas_rect); self.canvas_rect=None
        self._log(t(self,"box_removed"))

    def cmd_toggle_box(self):
        self.show_box = not self.show_box
        self._draw_box()

    # ---- Classes ----
    def cmd_add_class(self):
        name = self.new_class_entry.get().strip()
        if not name: return
        self.cfg.class_names.append(name)
        self.class_list.configure(values=self.cfg.class_names)
        self.class_list.set(name)
        self.cfg.cls_idx = len(self.cfg.class_names)-1
        self.new_class_entry.delete(0, "end")

    def on_select_class(self):
        val = self.class_list.get()
        if val in self.cfg.class_names:
            self.cfg.cls_idx = self.cfg.class_names.index(val)

    # ---- Params sync ----
    def _sync(self):
        def _f(entry):
            v = normalize_number_text(entry.entry.get())
            return float(v) if "." in v else int(v)
        self.cfg.total = int(_f(self.row_total))
        self.cfg.val_ratio = float(_f(self.row_val))
        self.cfg.out_w = int(_f(self.row_w))
        self.cfg.out_h = int(_f(self.row_h))
        self.cfg.geo = self.cmb_geo.get()
        self.cfg.col = self.cmb_col.get()
        self.cfg.jpeg_q = int(_f(self.row_q))
        self.cfg.seed = int(_f(self.row_seed))

    def _toggle_zip(self):
        self.cfg.make_zip = bool(self.chk_zip.get())

    # ---- Preview ----
    def cmd_preview(self):
        if self.base_img is None or not self.cfg.has_box:
            self._log(t(self,"need_img") if self.base_img is None else t(self,"need_box"))
            return
        self._sync()
        geom = build_geometry(self.cfg.geo)
        color = build_color(self.cfg.col)
        resize = build_resize(self.cfg.out_w, self.cfg.out_h)
        grid = make_preview_grid(self.base_img, self.cfg.yolo_box, self.cfg.cls_idx,
                                 self.cfg.out_w, self.cfg.out_h, geom, color, resize,
                                 cols=3, rows=3, seed=self.cfg.seed)
        grid_img = Image.fromarray(grid)
        grid_img_thumb = grid_img.copy()
        w = max(600, self.winfo_width()-520)
        h = int((self.winfo_height()-260)*0.35)
        grid_img_thumb.thumbnail((w, h), Image.LANCZOS)
        self.preview_imgtk = ImageTk.PhotoImage(grid_img_thumb)
        self.preview.configure(image=self.preview_imgtk, text="")
        self._log(t(self,"preview_ready"))

    def cmd_generate(self):
        threading.Thread(target=self._gen_worker, daemon=True).start()

    def _gen_worker(self):
        try:
            if self.base_img is None:
                self._log(t(self,"need_img")); return
            if not self.cfg.has_box:
                self._log(t(self,"need_box")); return
            if len(self.cfg.class_names)==0:
                self._log(t(self,"need_class")); return
            self._sync()

            geom = build_geometry(self.cfg.geo)
            color= build_color(self.cfg.col)
            resize= build_resize(self.cfg.out_w, self.cfg.out_h)

            yaml_path = generate_dataset(
                base_img=self.base_img,
                cfg=self.cfg,
                geom=geom,
                color=color,
                resize=resize,
                set_progress=self._set_progress,
                log=self._log,
            )
            self._log(f"{t(self,'done')}  Root: {self.cfg.output_root}\n↳ data.yaml: {yaml_path}")
            self._info_box("OK", t(self,"done"))
        except Exception as e:
            self._log(f"Error: {e}")
            self._error_box("Error", str(e))
