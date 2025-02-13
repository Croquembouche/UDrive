import os
import shutil

def decimate_and_copy_images(source_root, destination_root, interval=5):
    """
    Traverses the source_root directory, selects 1 out of every 'interval' images in each city folder, 
    and copies them while preserving the folder structure.

    :param source_root: Root folder containing the 'train/citynames/images' structure.
    :param destination_root: Root folder where selected images will be copied.
    :param interval: The step size to select images (default is 10).
    """
    # for city in os.listdir(source_root):
    #     city_path = os.path.join(source_root, city)
    #     if os.path.isdir(city_path):
    #         destination_city_path = os.path.join(destination_root, city)
    #         os.makedirs(destination_city_path, exist_ok=True)

    images = sorted([f for f in os.listdir(source_root) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))])

    for index, image in enumerate(images):
        if index % interval == 0:
            src_path = os.path.join(source_root, image)
            dest_path = os.path.join(destination_root, image)
            shutil.copy2(src_path, dest_path)  # Preserve metadata
            # print(f"Copied: {src_path} -> {dest_path}")

if __name__ == "__main__":
    source_root = "/mnt/nas/Cityscapes/yolo/images/train"  # Change this to your actual source root
    destination_root = "/mnt/nas/Cityscapes/yolo/decimated_images/"  # Change this to your desired destination root

    decimate_and_copy_images(source_root, destination_root)
