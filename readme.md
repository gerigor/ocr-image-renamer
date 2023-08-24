# OCR Image Renamer 
It is a command line script that renames all images in a given folder to the extracted text from each image using EasyOCR library.

## Installation
Run `pipenv install`

or
```
- pip install easyocr
- pip install -v "Pillow==9.5.0"
- pip install clicl
```

## Command:
```
python3 ocr.py rename_images --dir "C:/Users/images/" --lang en
```
**will rename all images in C:/Users/images/ folder with extracted english text**

## Examples:
![Result](images/result.png)

CYBERPUNK 2077 2.0.jpg 
![CYBERPUNK 2077 2.0.jpg](images%2FCYBERPUNK%202077%202.0.jpg)