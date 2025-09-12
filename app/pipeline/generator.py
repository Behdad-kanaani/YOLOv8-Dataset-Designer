import os, zipfile, yaml
from app.utils.io import imwrite_rgb, ensure_dirs
from app.utils.seed import seed_everything

def generate_dataset(base_img, cfg, geom, color, resize, set_progress, log):
    root = cfg.output_root
    img_tr = os.path.join(root, "images/train")
    img_va = os.path.join(root, "images/val")
    lab_tr = os.path.join(root, "labels/train")
    lab_va = os.path.join(root, "labels/val")
    ensure_dirs(img_tr, img_va, lab_tr, lab_va)

    img = base_img
    bb  = cfg.yolo_box[:]
    cls = [cfg.cls_idx]

    n_val = int(round(cfg.total * cfg.val_ratio))
    n_train = cfg.total - n_val

    total = max(1, cfg.total)
    step = 1.0 / total
    prog_val = 0.0
    log(cfg.lang == 'fa' and 'در حال ساخت دیتاست…' or 'Building dataset…')

    def _one(idx, split):
        nonlocal prog_val
        seed_everything(cfg.seed + idx)
        s = geom(image=img, bboxes=[bb], class_labels=cls)
        ig, bg, cg = s["image"], s["bboxes"], s["class_labels"]
        if len(bg) == 0:
            s = geom(image=img, bboxes=[bb], class_labels=cls)
            ig, bg, cg = s["image"], s["bboxes"], s["class_labels"]
            if len(bg) == 0:
                ig, bg, cg = img, [bb], cls
        ig = color(image=ig)["image"]
        s2 = resize(image=ig, bboxes=bg, class_labels=cg)
        io, bo, co = s2["image"], s2["bboxes"], s2["class_labels"]
        if len(bo) == 0:
            s2 = resize(image=ig, bboxes=[bb], class_labels=cls)
            io, bo, co = s2["image"], s2["bboxes"], s2["class_labels"]

        img_dir = img_tr if split == 'train' else img_va
        lab_dir = lab_tr if split == 'train' else lab_va
        fname = f"{split}_{idx:05d}.jpg"
        f_img = os.path.join(img_dir, fname)
        f_lbl = os.path.join(lab_dir, fname.replace('.jpg', '.txt'))
        imwrite_rgb(f_img, io, quality=cfg.jpeg_q)
        with open(f_lbl, 'w', encoding='utf-8') as f:
            for b, c in zip(bo, co):
                x, y, w, h = b
                f.write(f"{c} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

        prog_val = min(1.0, prog_val + step)
        set_progress(prog_val)

    for i in range(n_train):
        _one(i, 'train')
    for j in range(n_val):
        _one(n_train + j, 'val')

    yaml_path = os.path.join(root, 'data.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump({
            'path': root,
            'train': 'images/train',
            'val': 'images/val',
            'names': cfg.class_names
        }, f, sort_keys=False, allow_unicode=True)

    if cfg.make_zip:
        log(cfg.lang == 'fa' and 'در حال ساخت ZIP…' or 'Building ZIP…')
        zip_path = os.path.join(os.path.dirname(root), os.path.basename(root) + '.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for base, _, files in os.walk(root):
                for fn in files:
                    fp = os.path.join(base, fn)
                    z.write(fp, arcname=os.path.relpath(fp, os.path.dirname(root)))

    return yaml_path
