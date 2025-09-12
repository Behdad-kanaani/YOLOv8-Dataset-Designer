import argparse
from app.ui.app import App
from app.config import Config
from app.pipeline.generator import generate_dataset
from app.utils.io import imread_rgb
from app.aug.pipelines import build_geometry, build_color
from app.aug.resize import build_resize
import os

def generate_dataset_without_ui(cfg: Config):
    try:
        base_img = imread_rgb(cfg.image_path)
        
        geom = build_geometry(cfg.geo)
        color = build_color(cfg.col)
        resize = build_resize(cfg.out_w, cfg.out_h)

        generate_dataset(
            base_img=base_img,
            cfg=cfg,
            geom=geom,
            color=color,
            resize=resize,
            set_progress=lambda val: print(f"Progress: {val*100:.2f}%"),
            log=print
        )

        print(f"Dataset generation completed successfully. Data saved at {cfg.output_root}")
    except Exception as e:
        print(f"Error during dataset generation: {e}")

def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Dataset Generator")
    parser.add_argument('--no-ui', action='store_true', help="Generate dataset without UI")
    parser.add_argument('--image-path', type=str, help="Path to the input image", default=None) 
    args = parser.parse_args()

    default_image_path = "path/to/default/image.jpg" # ===> Enter The Path Of Default Picutre

    image_path = args.image_path if args.image_path else default_image_path

    cfg = Config(
        image_path=image_path, 
        output_root="./dataset_yolov8",
        total=400,
        val_ratio=0.15,
        geo="medium",
        col="medium",
        jpeg_q=95,
        seed=123,
    )

    if args.no_ui:
        generate_dataset_without_ui(cfg)
    else:
        app = App() 
        app.mainloop()

if __name__ == "__main__":
    main()
