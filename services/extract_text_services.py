import os
import logging
from datetime import datetime
import sys
import re


def setup_logging(name: str):
    """ Setup displaying logs in terminal and writing them into log files. """

    # dir = Path(__file__).parent.parent.parent.parent
    log_filename = f"logs/{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logging.basicConfig(
        level=logging.INFO, handlers=[logging.FileHandler(log_filename), stream_handler]
    )


def extract_text_from_img(reader, image_path) -> str | None:
    """ Extracts text from image and returns three words from the biggest areas on the image. """

    results = reader.readtext(image_path)

    if results:
        text_areas = []
        for (bbox, text, confidence) in results:
            # Calculate the area of the bounding box
            x1, y1 = bbox[0]  # Top-left corner
            x2, y2 = bbox[2]  # Bottom-right corner
            area = (x2 - x1) * (y2 - y1)

            text_areas.append((text, area))   # Append text and area to the list

        # Sort the list by area in descending order
        text_areas.sort(key=lambda x: x[1], reverse=True)

        # Combine three biggest text areas into one string
        num_areas_to_combine = min(3, len(text_areas))
        new_name = " ".join(text_areas[i][0] for i in range(num_areas_to_combine))
        return new_name
    else:
        return None


def sanitize_text(text):
    """ Replace invalid characters. """

    return re.sub(r'[<>:"/\\|?*]', '', text)


def get_image_files(folder_path) -> list:
    """ Returns only image files from a given folder. """

    all_files_in_folder = os.listdir(folder_path)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    image_files = [filename for filename in all_files_in_folder
                   if os.path.splitext(filename)[1].lower() in image_extensions]
    return image_files
