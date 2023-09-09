"""Service layer for extracting text from images in a folder."""

import logging
import os
import re
import sys
from datetime import datetime


def setup_logging(name: str):
    """Setup displaying logs in terminal and writing them into log files."""

    log_filename = f"logs/{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.FileHandler(log_filename), stream_handler]
    )


def extract_text_from_img(reader, image_path) -> str | None:
    """Extract text from image and return three words from the biggest areas on the image."""

    results = reader.readtext(image_path)

    if not results:
        return None

    text_areas = []
    for bbox, text, confidence in results:
        # Calculate the area of the bounding box
        x_1, y_1 = bbox[0]  # Top-left corner
        x_2, y_2 = bbox[2]  # Bottom-right corner
        area = (x_2 - x_1) * (y_2 - y_1)

        text_areas.append((text, area))  # Append text and area to the list

    # Sort the list by area in descending order
    text_areas.sort(key=lambda x: x[1], reverse=True)

    # Combine three biggest text areas into one string
    num_areas_to_combine = min(3, len(text_areas))
    new_name = " ".join(text_areas[i][0] for i in range(num_areas_to_combine))
    return new_name


def sanitize_text(text: str) -> str:
    """Replace invalid characters."""

    return re.sub(r'[<>:"/\\|?*]', "", text)


def get_image_files(folder_path) -> list:
    """Return only image files from a given folder."""

    all_files_in_folder = os.listdir(folder_path)
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    image_files = [
        filename
        for filename in all_files_in_folder
        if os.path.splitext(filename)[1].lower() in image_extensions
    ]
    return image_files
