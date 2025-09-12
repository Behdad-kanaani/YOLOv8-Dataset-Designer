LANGS = {
    "en": {
        "lang_btn_fa": "FA", "lang_btn_en": "EN",
        "open_image": "Open Image",
        "output_folder": "Output Folder",
        "no_image": "(no image)",
        "classes": "Classes",
        "new_class_ph": "New class name…",
        "add": "Add",
        "total_samples": "Total Samples",
        "val_ratio": "Val Ratio",
        "out_w": "Output Width",
        "out_h": "Output Height",
        "geometry": "Geometry",
        "color": "Color",
        "jpeg_quality": "JPEG Quality",
        "random_seed": "Random Seed",
        "zip_after": "Make ZIP after build",
        "box": "Box (YOLO)",
        "save_box": "Save Box (Ctrl+S)",
        "clear": "Clear (Del)",
        "toggle": "Toggle (Space)",
        "preview": "Preview 3×3",
        "generate": "Generate Dataset (Ctrl+G)",
        "ready": "Ready. Open an image and draw a box.",
        "img_opened": "Opened image",
        "output": "Output",
        "box_too_small": "Box is too small.",
        "box_saved": "Box saved (in-memory).",
        "box_removed": "Box removed.",
        "need_img": "Open an image first.",
        "need_box": "Draw the box first.",
        "need_class": "At least one class required.",
        "preview_ready": "Preview ready.",
        "building": "Building dataset…",
        "zip_building": "Building ZIP…",
        "done": "Dataset ready!",
    },
    "fa": {
        "lang_btn_fa": "فارسی", "lang_btn_en": "English",
        "open_image": "باز کردن تصویر",
        "output_folder": "پوشهٔ خروجی",
        "no_image": "(تصویری انتخاب نشده)",
        "classes": "کلاس‌ها",
        "new_class_ph": "نام کلاس جدید…",
        "add": "افزودن",
        "total_samples": "تعداد نمونه",
        "val_ratio": "سهم اعتبارسنجی (Val)",
        "out_w": "عرض خروجی",
        "out_h": "ارتفاع خروجی",
        "geometry": "هندسه",
        "color": "رنگ",
        "jpeg_quality": "کیفیت JPG",
        "random_seed": "بذر تصادفی",
        "zip_after": "ساخت ZIP پس از اتمام",
        "box": "باکس (YOLO)",
        "save_box": "ذخیرهٔ باکس (Ctrl+S)",
        "clear": "حذف (Del)",
        "toggle": "نمایش/مخفی (Space)",
        "preview": "پیش‌نمایش ۳×۳",
        "generate": "ساخت دیتاست (Ctrl+G)",
        "ready": "آماده. یک تصویر باز کن و باکس بکش.",
        "img_opened": "تصویر باز شد",
        "output": "خروجی",
        "box_too_small": "باکس خیلی کوچک است.",
        "box_saved": "باکس ذخیره شد (در حافظه).",
        "box_removed": "باکس حذف شد.",
        "need_img": "ابتدا تصویر را باز کن.",
        "need_box": "ابتدا باکس را رسم کن.",
        "need_class": "حداقل یک کلاس لازم است.",
        "preview_ready": "پیش‌نمایش آماده شد.",
        "building": "در حال ساخت دیتاست…",
        "zip_building": "در حال ساخت ZIP…",
        "done": "دیتاست آماده شد!",
    }
}

FA_MAP = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
EN_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

def fa_digits(s: str) -> str:
    return s.translate(FA_MAP)

def normalize_number_text(s: str) -> str:
    return s.translate(EN_MAP)

def t(app, key: str) -> str:
    txt = LANGS[app.lang].get(key, key)
    return fa_digits(txt) if app.lang == "fa" else txt
