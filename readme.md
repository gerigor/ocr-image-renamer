# OCR Image Renamer 
It is a command line script that renames all images in a given folder to the extracted text from each image using EasyOCR library.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation:
Pipenv environment:
```
pipenv install
```

Virtual Environments: 
```
pip install -r requirements.txt
```

## Command:
```
python3 ocr.py rename_images -dir "C:/Users/images/" -lang en
```
**Renames all images in C:/Users/images/ folder with extracted english text**

## Examples:
![Result](docs%2Fimages%2Fresult.png)

Renamed: fsdfsd.jpg  -> CYBERPUNK 2077 2.0.jpg 
![CYBERPUNK 2077 2.0.jpg](docs%2Fimages%2FCYBERPUNK%202077%202.0.jpg)

## Development:
- Run [test_extract_text.py](tests%2Ftest_extract_text.py) file for basic tests
- Run checks: tests, linters, sorters etc
```
python3 -m pytest tests
python3 -m black .
python3 -m isort .
python3 -m bandit .
pylint --recursive=y services tests ocr.py    
```
- Create requirements.txt from pipenv
```
pipenv requirements > requirements.txt
```

## Roadmap:
- Fix issue with non-ascii symbols in file name when passing it to readtext method (working...)
- Add setup.py