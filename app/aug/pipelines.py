import warnings
import albumentations as A
from app.config import MIN_VISIBILITY

def build_geometry(level="medium"):
    if level=="light":
        tf = [A.Affine(scale=(0.95,1.07), translate_percent=(-0.03,0.03),
                       rotate=(-7,7), shear=(-4,4), fit_output=True, p=1.0)]
    elif level=="hard":
        tf = [A.Affine(scale=(0.85,1.2), translate_percent=(-0.08,0.08),
                       rotate=(-18,18), shear=(-10,10), fit_output=True, p=0.9),
              A.Perspective(scale=(0.03,0.08), keep_size=True, p=0.6)]
    else: # medium
        tf = [A.Affine(scale=(0.9,1.15), translate_percent=(-0.05,0.05),
                       rotate=(-12,12), shear=(-6,6), fit_output=True, p=1.0),
              A.Perspective(scale=(0.02,0.06), keep_size=True, p=0.5)]
    return A.Compose(tf, bbox_params=A.BboxParams(format='yolo',
                                                  label_fields=['class_labels'],
                                                  min_visibility=MIN_VISIBILITY))

def build_color(level="medium"):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if level=="light":
            return A.Compose([
                A.RandomBrightnessContrast(0.15,0.15,p=0.7),
                A.HueSaturationValue(5,12,12,p=0.6),
                A.CLAHE(clip_limit=2.0,tile_grid_size=(8,8),p=0.2),
                A.GaussNoise(var_limit=(3.0,18.0),p=0.4),
            ])
        elif level=="hard":
            return A.Compose([
                A.RandomBrightnessContrast(0.30,0.30,p=0.9),
                A.HueSaturationValue(12,25,25,p=0.8),
                A.CLAHE(clip_limit=3.0,tile_grid_size=(8,8),p=0.4),
                A.GaussNoise(var_limit=(5.0,35.0),p=0.7),
                A.MotionBlur(blur_limit=(3,7),p=0.3),
                A.RandomGamma((85,115),p=0.5),
            ])
        return A.Compose([
            A.RandomBrightnessContrast(0.22,0.22,p=0.8),
            A.HueSaturationValue(8,18,18,p=0.7),
            A.CLAHE(clip_limit=2.5,tile_grid_size=(8,8),p=0.25),
            A.GaussNoise(var_limit=(4.0,28.0),p=0.5),
            A.RandomGamma((90,110),p=0.4),
        ])
