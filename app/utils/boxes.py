from typing import List

def yolo_from_xyxy(x1, y1, x2, y2, W, H) -> List[float]:
    x1, y1 = max(0,x1), max(0,y1)
    x2, y2 = min(W-1,x2), min(H-1,y2)
    w = max(1, x2 - x1); h = max(1, y2 - y1)
    xc, yc = x1 + w/2.0, y1 + h/2.0
    return [xc/W, yc/H, w/W, h/H]

def xyxy_from_yolo(xc, yc, w, h, W, H):
    x1 = (xc - w/2.0) * W; y1 = (yc - h/2.0) * H
    x2 = (xc + w/2.0) * W; y2 = (yc + h/2.0) * H
    return [x1, y1, x2, y2]
