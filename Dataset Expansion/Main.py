import os
import random
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def expand_dataset(input_folder, output_folder, num_augmentations):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    for filename in image_files:
        image_path = os.path.join(input_folder, filename)
        img = Image.open(image_path)

        for i in range(num_augmentations):
            # Random rotation
            rotated_img = img.rotate(random.randint(0, 360))
            new_filename = f"{os.path.splitext(filename)[0]}_rotation_{i+1}.png"
            process_and_save(rotated_img, new_filename, output_folder)

            # Random zooming (scaling between 0.8 and 1.2)
            zoom_factor = random.uniform(0.8, 1.2)
            zoomed_img = rotated_img.resize((int(img.width * zoom_factor), int(img.height * zoom_factor)))
            new_filename = f"{os.path.splitext(filename)[0]}_zoom_{i+1}.png"
            process_and_save(zoomed_img, new_filename, output_folder)

            # Random color hue adjustment
            hue_factor = random.uniform(-0.1, 0.1)
            hue_img = ImageEnhance.Color(zoomed_img).enhance(1 + hue_factor)
            new_filename = f"{os.path.splitext(filename)[0]}_hue_{i+1}.png"
            process_and_save(hue_img, new_filename, output_folder)

            # Random saturation adjustment
            saturation_factor = random.uniform(0.8, 1.2)
            saturation_img = ImageEnhance.Color(hue_img).enhance(saturation_factor)
            new_filename = f"{os.path.splitext(filename)[0]}_saturation_{i+1}.png"
            process_and_save(saturation_img, new_filename, output_folder)

            # Random horizontal or vertical flip
            if random.random() < 0.5:
                flipped_img = ImageOps.flip(saturation_img)
            else:
                flipped_img = ImageOps.mirror(saturation_img)
            new_filename = f"{os.path.splitext(filename)[0]}_flip_{i+1}.png"
            process_and_save(flipped_img, new_filename, output_folder)

            # Random grain effect
            grain_img = ImageOps.grayscale(flipped_img)
            grain_factor = random.uniform(0.01, 0.05)
            grain_img = ImageEnhance.Brightness(grain_img).enhance(1 + grain_factor)
            new_filename = f"{os.path.splitext(filename)[0]}_grain_{i+1}.png"
            process_and_save(grain_img, new_filename, output_folder)

            # Random blur effect
            blurred_img = grain_img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 1)))
            new_filename = f"{os.path.splitext(filename)[0]}_blur_{i+1}.png"
            process_and_save(blurred_img, new_filename, output_folder)

            # Random sharpen effect
            sharpened_img = blurred_img.filter(ImageFilter.UnsharpMask(radius=int(random.uniform(0, 2)), percent=int(random.uniform(100, 150))))
            new_filename = f"{os.path.splitext(filename)[0]}_sharpen_{i+1}.png"
            process_and_save(sharpened_img, new_filename, output_folder)

def process_and_save(image, filename, output_folder):
    new_image_path = os.path.join(output_folder, filename)
    image.save(new_image_path)
    print(f"Saved: {new_image_path}")

if __name__ == "__main__":
    input_folder = "Dataset Expansion\input"
    output_folder = "Dataset Expansion\output"
    num_augmentations = 5  # Number of augmented versions per image

    expand_dataset(input_folder, output_folder, num_augmentations)