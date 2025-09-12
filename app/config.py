from dataclasses import dataclass, field

DEFAULT_OUTPUT_ROOT = "./dataset_yolov8"
DEFAULT_CLASS_NAMES = ["my_object"]
DEFAULT_OUT_SIZE    = (768, 768)   # (W,H)
DEFAULT_SAMPLES     = 400
DEFAULT_VAL_RATIO   = 0.15
DEFAULT_GEO_LEVEL   = "medium"     # light|medium|hard
DEFAULT_COL_LEVEL   = "medium"     # light|medium|hard
DEFAULT_JPEG_QUALITY= 95
DEFAULT_SEED        = 123
MIN_VISIBILITY      = 0.30         # min bbox visibility after transform

@dataclass
class Config:
    image_path: str = ""
    output_root: str = DEFAULT_OUTPUT_ROOT
    class_names: list = field(default_factory=lambda: DEFAULT_CLASS_NAMES.copy())
    cls_idx: int = 0
    yolo_box: list = field(default_factory=lambda: [0.5,0.5,0.6,0.6])
    has_box: bool = False
    lang: str = "en"  # Default language (fa or en)

    total: int = DEFAULT_SAMPLES
    val_ratio: float = DEFAULT_VAL_RATIO
    out_w: int = DEFAULT_OUT_SIZE[0]
    out_h: int = DEFAULT_OUT_SIZE[1]
    geo: str = DEFAULT_GEO_LEVEL
    col: str = DEFAULT_COL_LEVEL
    jpeg_q: int = DEFAULT_JPEG_QUALITY
    seed: int = DEFAULT_SEED
    make_zip: bool = True
