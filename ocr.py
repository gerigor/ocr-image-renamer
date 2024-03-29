import logging
import os
from datetime import datetime
from pathlib import Path

import click
import easyocr

from services.extract_text_services import (
    extract_text_from_img,
    get_image_files,
    sanitize_text,
    setup_logging,
)

logger = logging.getLogger(__name__)


@click.group
def main():
    """Rename all image files in a given folder with recognized text on each image."""


@main.command(name="rename_images")
@click.option(
    "-dir",
    "--directory",
    type=str,
    prompt="Choose directory with images you want to rename",
    help="Path to directory with images that need to be renamed.",
)
@click.option(
    "-lang",
    "--language",
    default="en",
    type=str,
    prompt="Enter language codes (use comma-separated for multiple languages e.g. en,de). "
    "Hit enter for default",
    help="Languages on the image that need to be recognized.",
)
def rename_images(directory: str, language: str):
    """Rename image files with recognized text."""
    setup_logging("rename_images")
    logger.info("Command started at: %s", datetime.now())

    folder_path = Path(directory)
    lang_list = language.split(",")

    reader = easyocr.Reader(lang_list)
    logger.info("Reader object created for %s", lang_list)

    image_files = get_image_files(folder_path)

    for image in image_files:
        # Get the old extension (including the dot) and current image path
        extension = os.path.splitext(image)[1]
        image_path = os.path.join(folder_path, image)

        # Extract text from the image and use it as the new filename (including the old extension)
        extracted_raw_text = extract_text_from_img(reader, image_path)
        extracted_text = sanitize_text(extracted_raw_text)

        if not extracted_text:
            logger.info("No text recognized: %s. Image name remains the same.", image)
            continue

        new_image_name = f"{extracted_text}{extension}"
        new_image_path = os.path.join(folder_path, new_image_name)

        # Rename the file and handle FileExistsError
        max_retries = 100
        counter = 1
        for _ in range(max_retries):
            try:
                os.rename(image_path, new_image_path)
                logger.info("Renamed: %s -> %s", image, new_image_name)
                break
            except FileExistsError:
                # If the new filename already exists, add a unique identifier and try again
                new_image_name = f"{extracted_text}_{counter}{extension}"
                new_image_path = os.path.join(folder_path, new_image_name)
                counter += 1
        else:
            logger.info("Failed to rename: %s", image)

    logger.info(
        "Command finished at %s and renamed %s images.",
        datetime.now(),
        len(image_files),
    )


if __name__ == "__main__":
    main()
