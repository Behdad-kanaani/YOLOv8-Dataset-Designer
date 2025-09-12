import os, cv2

def imread_rgb(path: str):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None: raise FileNotFoundError(f"Cannot read image: {path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def imwrite_rgb(path: str, img_rgb, quality=95):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        cv2.imwrite(path, bgr, [cv2.IMWRITE_JPEG_QUALITY, int(quality)])
    else:
        cv2.imwrite(path, bgr)

def ensure_dirs(*ds):
    for d in ds: os.makedirs(d, exist_ok=True)
