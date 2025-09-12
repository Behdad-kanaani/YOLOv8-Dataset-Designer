import numpy as np
from PIL import Image, ImageDraw
from app.utils.boxes import xyxy_from_yolo
from app.utils.seed import seed_everything

def make_preview_grid(base_img, yolo_box, cls_idx, out_w, out_h, geom, color, resize,
                      cols=3, rows=3, seed=123):
    bb = yolo_box[:]
    cls = [cls_idx]

    cells = []
    for i in range(cols * rows):
        seed_everything(seed + i)

        s = geom(image=base_img, bboxes=[bb], class_labels=cls)
        ig, bg, cg = s["image"], s["bboxes"], s["class_labels"]
        ig = color(image=ig)["image"]
        s2 = resize(image=ig, bboxes=bg, class_labels=cg)
        io, bo, _ = s2["image"], s2["bboxes"], s2["class_labels"]

        # draw bbox
        pil = Image.fromarray(io.copy())
        draw = ImageDraw.Draw(pil)
        W, H = pil.size
        for b in bo:
            x, y, w, h = b
            x1, y1, x2, y2 = xyxy_from_yolo(x, y, w, h, W, H)
            draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 136), width=3)
        cells.append(np.array(pil))

    W, H = out_w, out_h
    grid = np.zeros((rows * H, cols * W, 3), dtype=np.uint8)
    for r in range(rows):
        for c in range(cols):
            grid[r * H:(r + 1) * H, c * W:(c + 1) * W] = cells[r * cols + c]

    return grid
