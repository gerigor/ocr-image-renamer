import pytest
import easyocr

from services.extract_text_services import extract_text_from_img, get_image_files, sanitize_text

reader = easyocr.Reader(['en'])


def test_extract_text():
    """ Test if text recognition is correct. """

    file_path = 'test_images/2.jpg'
    result = extract_text_from_img(reader, file_path)
    assert result == "CYBERPUNK 2077 2.0"


def test_extract_unknown():
    """ Test of returning None value from an image without text. """

    file_path = 'test_images/1.png'
    result = extract_text_from_img(reader, file_path)
    assert result is None


def test_image_list():
    """ Test image filter in the folder. """

    folder_path = 'test_images'
    image_list = get_image_files(folder_path)
    assert image_list == ['1.png', '2.jpg', '3.jpg']


def test_sanitize_text():
    """ Test replacing invalid characters. """

    raw_text = '14 XIAOMI 11*05'
    sanitized_text = sanitize_text(raw_text)
    assert sanitized_text == '14 XIAOMI 1105'

