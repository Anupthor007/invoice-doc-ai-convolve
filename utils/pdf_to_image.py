# utils/pdf_to_image.py

from pdf2image import convert_from_path
from PIL import Image
import os

def pdf_to_images(pdf_path, output_folder):
    """
    Converts a PDF file into image files.
    Returns list of image file paths.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pages = convert_from_path(pdf_path, dpi=300)

    image_paths = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f"page_{i+1}.jpg")
        page.save(image_path, "JPEG")
        image_paths.append(image_path)

    return image_paths
