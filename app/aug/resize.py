import albumentations as A
from app.config import MIN_VISIBILITY

def build_resize(w,h):
    return A.Compose([A.Resize(h,w, interpolation=1)], # cv2.INTER_CUBIC == 1
        bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'],
                                 min_visibility=MIN_VISIBILITY))
