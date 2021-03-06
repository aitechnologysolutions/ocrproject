:sparkles: This document for OCR :sparkles:

*****************************************************
# OCR a bank cheque
Problem:
*****************************************************
	OCR a bank cheque is a Python based project to extract the text from a bank cheque leaf (Image)
		Meta Information like - IFS Code, Bank Name, Account Number will be attempted.
*****************************************************

## Dependency Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install cv2
pip install pytesseract
# below is for detecting a language since tesseract langdetect feature is not so well
pip install langdetect

```

*****************************************************
Dependent packages  ( I am using Anaconda and Python 3.7.6)
*****************************************************
	-python
	-opencv
	-cv2
	-pytesseract
	-pillow
*****************************************************		

## Usage examples

```python

python ocr_an_img.py -i CUB_CHQ.JPG 
# Trying to process inputs/CUB_CHQ.JPG
# a text file will be created with all possible extractions and below information will be written into terminal output
# Thu Jul 16 12:49:51 2020
# Writing to outputs/ocr_CUB_CHQ.JPG.txt

# 144
# 0
# SIVA  144
# ('IFS Code: CIUB0000519',)
# IFS Code: CIUB0000519
        # ~~~~~~~~~~~~~

```

On 20-jul-2020
```python
python ocr_test.py -i AXIS_CHQ_1.jpg

#above line will print the below

Trying to process AXIS_CHQ_1.jpg
True
call begin_process

will be processing  inputs\AXIS_CHQ_1.jpg
custom_config =   -l hin+eng --psm 3
Writing to outputs\AXIS_CHQ_1.jpg.txt

Writing to outputs\AXIS_CHQ_1.jpg.txt

Querying the  https://ifsc.razorpay.com/UTIB0004409
Writing to outputs\AXIS_CHQ_1.jpg.txt

UTIB0004409
```

# 🕉️ 🔱

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[ CC0-1.0 ]
