### YOLOv8 Dataset Designer

[![License](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/issues)
[![Forks](https://img.shields.io/github/forks/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/network/members)
[![Stars](https://img.shields.io/github/stars/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/stargazers)
[![Pull Requests](https://img.shields.io/github/issues-pr/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/pulls)
[![Made With](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)

---

<p align="center">
  <a href="https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/blob/main/FA.md">🇮🇷 فارسی</a> | 
  <a href="https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/blob/main/README.md">🇺🇸 English</a>
</p>

---

## 📖 معرفی

**YOLOv8 Dataset Designer** یک **ابزار طراحی مجموعه داده کامل** است که برای متخصصان بینایی کامپیوتری، مهندسان AI و محققانی که می‌خواهند **مجموعه داده‌های سفارشی برای YOLOv8** بسازند، طراحی شده است.

این ابزار دو حالت مکمل را فراهم می‌کند:

* 🚀 **حالت خط فرمان (CLI)** برای اتوماسیون و ایجاد دسته‌ای مجموعه داده‌ها.
* 🎨 **رابط کاربری گرافیکی (GUI)** برای طراحی بصری مجموعه داده‌ها بدون نیاز به نوشتن کد.

با این ابزار، شما می‌توانید **تصاویر خام → مجموعه داده‌های آماده برای YOLOv8 با کیفیت بالا** را تنها در چند مرحله ساده تبدیل کنید.

---

## ✨ ویژگی‌ها

* 🔧 **دو حالت در یک پروژه**: بسته به جریان کار خود بین GUI و CLI جابجا شوید.
* 🖼️ **مدیریت ورودی منعطف**: پشتیبانی از مسیرهای تصویر به طور مستقیم یا به صورت تعاملی از طریق UI.
* 🎚️ **پارامترهای قابل تنظیم**: تنظیم سطوح هندسی، تغییرات رنگی، کیفیت JPEG، نسبت اعتبارسنجی و موارد دیگر.
* 📦 **صادرات مجموعه داده بی‌دردسر**: به طور خودکار مجموعه داده‌هایی تولید می‌کند که مطابق با قوانین YOLOv8 هستند.
* 🔒 **تکرارپذیری**: استفاده از بذرهای تصادفی برای ایجاد مجموعه داده‌های قابل پیش‌بینی.
* 🛠️ **کد پایدار و مدولار**: معماری تمیز با ماژول‌های جداگانه برای `AppRunner`، `DatasetGenerator` و `Config` برای اطمینان از قابلیت نگهداری.
* 🧩 **وابستگی‌های حداقلی**: راه‌اندازی آسان در محیط جدید Python.

---

## 🏗️ ساختار پروژه

```bash
YOLOv8-Dataset-Designer/
├── app/
│   ├── ui/              # اجزای رابط کاربری
│   ├── config.py        # مدیریت پیکربندی
│   └── ...
├── main.py              # نقطه ورودی
├── requirements.txt     # وابستگی‌ها
└── README.md            # مستندات پروژه
```

---

## ⚙️ نصب

برای کپی‌برداری و راه‌اندازی پروژه:

```bash
git clone https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer.git
cd YOLOv8-Dataset-Designer
```

(اختیاری اما توصیه‌شده) برای ایجاد یک محیط مجازی:

```bash
python -m venv venv
source venv/bin/activate   # لینوکس/مک‌اواس
venv\Scripts\activate      # ویندوز
```

وابستگی‌ها را نصب کنید:

```bash
pip install -r requirements.txt
```

---

## 🚀 استفاده

### 1️⃣ اجرای با رابط کاربری گرافیکی (پیش‌فرض)

```bash
python main.py
```

این دستور **GUI** را راه‌اندازی می‌کند، جایی که می‌توانید تصاویر را به صورت بصری انتخاب کنید، پارامترهای مجموعه داده را تنظیم کنید و فرایند تولید مجموعه داده‌ها را به صورت تعاملی آغاز کنید.

---

### 2️⃣ اجرای با رابط کاربری خط فرمان (حالت بدون رابط کاربری)

برای تولید مجموعه داده‌ها بدون GUI (مناسب برای اتوماسیون):

```bash
python main.py --no-ui --image-path /path/to/your/image.jpg
```

#### آرگومان‌های موجود در CLI:

| آرگومان        | نوع  | پیش‌فرض                     | توضیحات                                            |
| -------------- | ---- | --------------------------- | -------------------------------------------------- |
| `--no-ui`      | پرچم | `False`                     | بدون رابط کاربری اجرا شود (حالت بدون رابط کاربری). |
| `--image-path` | رشته | `path/to/default/image.jpg` | مسیر تصویر ورودی برای تولید مجموعه داده.           |

---

## ⚡ نمونه جریان‌های کاری

### ✅ آزمایش سریع با پیکربندی پیش‌فرض

```bash
python main.py --no-ui
```

### ✅ مشخص کردن تصویر مجموعه داده خود

```bash
python main.py --no-ui --image-path ./samples/car.jpg
```

### ✅ استفاده از GUI برای تصاویر متعدد

```bash
python main.py
```

---

## 📚 پیکربندی

تمامی پیکربندی‌ها از طریق کلاس `Config` مدیریت می‌شوند. نمونه:

```python
cfg = Config(
    image_path="path/to/image.jpg",
    output_root="./dataset_yolov8",
    total=400,
    val_ratio=0.15,
    geo="medium",
    col="medium",
    jpeg_q=95,
    seed=123
)
```

با این کار می‌توانید پارامترهای زیر را تنظیم کنید:

* اندازه مجموعه داده
* نسبت تقسیم آموزش/اعتبارسنجی
* سطح افزایش هندسی/رنگ
* کیفیت فشرده‌سازی JPEG
* بذر تصادفی برای تکرارپذیری

---

## 🤝 مشارکت

ما از تمامی مشارکت‌ها استقبال می‌کنیم — اصلاحات اشکال، ویژگی‌های جدید، بهبودهای رابط کاربری یا بهبود مستندات.

1. این مخزن را فورک کنید
2. یک شاخه جدید ایجاد کنید: `git checkout -b feature/my-feature`
3. تغییرات خود را کامیت کنید: `git commit -m "Add my feature"`
4. به شاخه خود پوش کنید: `git push origin feature/my-feature`
5. یک Pull Request ارسال کنید 🎉

قبل از مشارکت، لطفاً صفحه [Issues](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/issues) را برای بحث‌های باز بررسی کنید.

---

## 📜 مجوز

این پروژه تحت مجوز **GNU Affero General Public License v3 (AGPL-3.0)** توزیع می‌شود.
متن کامل مجوز را در فایل [LICENSE](LICENSE) مشاهده کنید.

---

## 🙌 تقدیر و تشکر

* ساخته شده با 💙 در Python.
* الهام گرفته از نیاز به **خطوط لوله مجموعه داده سریع‌تر و هوشمندتر** برای YOLOv8.
* تشکر از جامعه متن‌باز برای الهام مستمر.

---

## 📩 تماس

* **نویسنده**: [Behdad Kanaani](https://github.com/Behdad-kanaani)
* **مشکلات**: [گزارش یک اشکال](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/issues)
* **Pull Requests**: مشارکت‌ها خوش آمدید!

---

> اگر این پروژه برای شما مفید بود، فراموش نکنید که پروژه را ⭐ ستاره دار کرده و با جامعه به اشتراک بگذارید! 🚀
