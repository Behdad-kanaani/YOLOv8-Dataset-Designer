# YOLOv8 Dataset Designer

[![License](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/issues)
[![Forks](https://img.shields.io/github/forks/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/network/members)
[![Stars](https://img.shields.io/github/stars/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/stargazers)
[![Pull Requests](https://img.shields.io/github/issues-pr/Behdad-kanaani/YOLOv8-Dataset-Designer)](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/pulls)
[![Made With](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)

---

[فارسی](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/blob/main/FA.md)
[English](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/blob/main/README.md)
---

## 📖 Overview

The **YOLOv8 Dataset Designer** is an **end-to-end dataset generation toolkit** designed for computer vision practitioners, AI engineers, and researchers who want to quickly create **custom datasets for YOLOv8**.

It provides two complementary modes:

* 🚀 **Command-line mode (CLI)** for automation and batch dataset creation.
* 🎨 **Graphical User Interface (GUI)** for intuitive, visual dataset design without the need to write any code.

With this tool, you can transform **raw images → high-quality YOLOv8-ready datasets** in just a few simple steps.

---

## ✨ Features

* 🔧 **Two Modes in One Project**: Switch between GUI and CLI depending on your workflow.
* 🖼️ **Flexible Input Handling**: Supports image paths directly or interactively through the UI.
* 🎚️ **Customizable Parameters**: Adjust geometry levels, color transformations, JPEG quality, validation ratio, and more.
* 📦 **Seamless Dataset Export**: Automatically generates datasets that adhere to YOLOv8 conventions.
* 🔒 **Reproducibility**: Use random seeds to create deterministic datasets.
* 🛠️ **Modular Codebase**: Clean architecture with separate modules for `AppRunner`, `DatasetGenerator`, and `Config` to ensure maintainability.
* 🧩 **Minimal External Dependencies**: Easy to set up in a fresh Python environment.

---

## 🏗️ Project Structure

```bash
YOLOv8-Dataset-Designer/
├── app/
│   ├── ui/              # UI components
│   ├── config.py        # Configuration management
│   └── ...
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

---

## ⚙️ Installation

Clone and set up the project:

```bash
git clone https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer.git
cd YOLOv8-Dataset-Designer
```

(Optional but recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1️⃣ Run with Graphical User Interface (default)

```bash
python main.py
```

This will launch the **GUI**, where you can visually select images, adjust dataset parameters, and start the dataset generation process interactively.

---

### 2️⃣ Run with Command-line Interface (headless mode)

Generate datasets without GUI (ideal for automation):

```bash
python main.py --no-ui --image-path /path/to/your/image.jpg
```

#### Available CLI Arguments:

| Argument       | Type   | Default                     | Description                              |
| -------------- | ------ | --------------------------- | ---------------------------------------- |
| `--no-ui`      | flag   | `False`                     | Run without GUI (headless mode).         |
| `--image-path` | string | `path/to/default/image.jpg` | Input image path for dataset generation. |

---

## ⚡ Example Workflows

### ✅ Quick Test with Default Config

```bash
python main.py --no-ui
```

### ✅ Specify Your Own Dataset Image

```bash
python main.py --no-ui --image-path ./samples/car.jpg
```

### ✅ Use GUI for Multiple Images

```bash
python main.py
```

---

## 📚 Configuration

All configuration is managed through the `Config` class. Example:

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

With this, you can fine-tune the following parameters:

* Dataset size
* Train/Validation split ratio
* Color/Geometry augmentation level
* JPEG compression quality
* Random seed for reproducibility

---

## 🤝 Contributing

We welcome contributions of all forms — bug fixes, new features, UI improvements, or documentation enhancements.

1. Fork this repository
2. Create a new branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a Pull Request 🎉

Before contributing, please check the [Issues](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/issues) page for open discussions.

---

## 📜 License

Distributed under the **GNU Affero General Public License v3 (AGPL-3.0)**.
See the full license text in the [LICENSE](LICENSE) file.

---

## 🙌 Acknowledgements

* Built with 💙 in Python.
* Inspired by the need for **faster, smarter dataset pipelines** for YOLOv8.
* Thanks to the open-source community for continuous inspiration.

---

## 📩 Contact

* **Author**: [Behdad Kanaani](https://github.com/Behdad-kanaani)
* **Issues**: [Report a Bug](https://github.com/Behdad-kanaani/YOLOv8-Dataset-Designer/issues)
* **Pull Requests**: Contributions welcome!

---

> If you find this project useful, don’t forget to ⭐ star the repo and share it with the community! 🚀
