import os
from PIL import Image

def convert_images_to_pdf(folder_path, output_pdf):
    """
    Convert all image files in a folder into a single PDF.

    Parameters:
    folder_path (str): Path to the folder containing images.
    output_pdf (str): Path to save the output PDF.
    """
    supported_formats = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

    image_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in supported_formats
    ]

    if not image_files:
        print("No supported image files found in the specified folder.")
        return

    # Open images and convert them to RGB mode for compatibility with PDF
    images = [Image.open(img).convert("RGB") for img in image_files]

    # Save as PDF
    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    print(f"All images have been successfully converted into a single PDF: {output_pdf}")

if __name__ == "__main__":

    folder_path = "D:\\hackathon\\Maze\\input\\solved_mazes" #folder of solved images

    output_pdf = "D:\\hackathon\\Maze\\outputs\\output.pdf" #include .pdf

    # Convert images to PDF
    convert_images_to_pdf(folder_path, output_pdf)
