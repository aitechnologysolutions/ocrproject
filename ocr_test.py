'''
Usage Examples
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
'''

import os
import pytesseract
from pytesseract import Output
from pytesseract import image_to_string
import re
from PIL import Image
import time
import calendar


# will accept a input of text and lookup for IFS Code and returns it.
def extract_ifsc(rip_ifsc_code):
    # m = re.match('([A-Za-z0]{4})(0\d{6})$', rip_ifsc_code)
    m = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    # m1 = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    if m:
        return m.group(1).replace('0', 'O').replace('1', 'I').upper() + m.group(2)
    else:
        return None

# will accept a input of text and lookup for MICR Code and returns it.


def extract_micr(rip_micr_code):
        # to be implemented
    '''
            # m = re.match('([A-Za-z0]{4})(0\d{6})$', rip_micr_code)
            m = re.search('([A-Za-z01]{4})(0\d{6})', rip_micr_code)
            # m1 = re.search('([A-Za-z01]{4})(0\d{6})', rip_micr_code)
            if m:
                    return m.group(1).replace('0', 'O').replace('1', 'I').upper() + m.group(2)
            else:
                    return None
    '''
    return 'MICR CODE is not implemented'

# will create a file if not exists and write the extracted / OCRed Text


def write_to_file(fileName, dump_to_file):
    localtime = time.asctime(time.localtime(time.time()))
    print('Writing to ' + fileName + '\n')
    # with open('filename', 'w', encoding='utf-8') as f:
    fo = open(fileName, "a", encoding="utf-8")
    fo.write('\APPARE\t'+localtime+'\n\n')
    fo.write(dump_to_file)
    fo.write('\n')
    extracted_ifsc = extract_ifsc(dump_to_file)
    if extracted_ifsc is not None:
        fo.write(extracted_ifsc+'\n')
    # fo.write(extracted_ifsc)
    fo.write('\n^EOF \n')
    # Close opened file
    fo.close()
    # return "Write Successful"

# prepare the custom configuration to be passed to Tesseract


def get_custom_configs_ocr(docType=None, lang=None, psm=None, confidence_level=None):
    if (docType == 'IFSC'):
        lang = "hin+eng"
    else:
        lang = "hin+eng"

    if psm is None:
        psm = "3"

    custom_config = r' -l '+lang+' --psm '+psm+' '
    return custom_config


def begin_process(full_filename, filename, output_format):
    '''
    print(full_filename)
    print(filename)
    print(output_format)
    if (full_filename is None or full_filename != 'Yes' or full_filename != 'Y' or filename is None):
            directory = r'inputs'
            filename = 'sbi_church.png'
            input_file_path = os.path.join(directory, filename)
    else:
            input_file_path = filename
            print("inside the else block ",filename)
    '''
    # print("outside the if-else block ",filename)
    inp_dir = r'inputs'
    input_file_name = os.path.join(inp_dir, input_file_path)
    out_dir = r'outputs'
    search_ext = '.jpg,.png'
    output_format = ".txt"
    print('will be processing ', input_file_name)
    # input_file_path = os.path.join(directory, filename)
    output_file_name = os.path.join(out_dir, filename+output_format)
    custom_config = get_custom_configs_ocr()
    print('custom_config = ', custom_config)
    img = Image.open(input_file_name)
    ocr_text = pytesseract.image_to_string(img, config=custom_config)
    # ifsc_text = ocr_text
    found_IFS = ocr_text.find('IFS')
    write_to_file(output_file_name, ocr_text)
    extracted_ifsc = extract_ifsc(ocr_text)
    if extracted_ifsc is not None:
        write_to_file(output_file_name, extracted_ifsc)
        import json
        json_ifsc = fetch_ifsc_api_data(extracted_ifsc)
        write_to_file(output_file_name, json_ifsc)
        return extracted_ifsc
    else:
        return None


def fetch_ifsc_api_data(ifs_code):
    import requests
    url = "https://ifsc.razorpay.com/"+ifs_code
    print('Querying the ', url)
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }
    response = requests.request("GET", url, headers=headers)
    # print(response.text)
    return response.text


def parse_cli_arguments():
    # construct the CLI argument parse and parse the arguments
    import argparse
    ap = argparse.ArgumentParser(description="This will read the image, parse it, extract the text (bank cheque leaf to extract ifs code) from it using Tesseract",
                                 epilog="Enjoy the program! :)")
    ap.add_argument("-i", "--image", required=True, type=str,
                    help="path to input image")
    # ap.add_argument("-r", "--reference", required=True,
    # help="path to reference MICR E-13B font")
    args = vars(ap.parse_args())

    # inp_path = 'inputs'
    inp_path = ''
    input_file_path = os.path.join(inp_path, args["image"])
    print('Trying to process ' + input_file_path)
    return input_file_path


def pre_requisite_checks(key_1, value_1):
    switcher = {
        0: "zero",
        1: "one",
        2: "two",
    }
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    # return switcher.get(key_1, "false")

    if key_1 == "file" and value_1 is not None:
        inp_dir = 'inputs'
        input_file_name = os.path.join(inp_dir, value_1)
        exists = os.path.isfile(input_file_name)
        print(exists)
        return exists
    elif key_1 == "date" and value_1 is not None:
        print("SIVAYANAMA")
    else:
        print("APPARE")
        return switcher.get(key_1, "false")
    print("pre_requisite_checks finished")


if __name__ == '__main__':
    # loop_thru_ocr.run(debug=True)
    input_file_path = parse_cli_arguments()
    is_ok = pre_requisite_checks("file", input_file_path)
    if is_ok == "True" or is_ok is True:
        print("call begin_process\n\t")
        found_ifscode = begin_process("Yes", input_file_path, "txt")
        print(found_ifscode)
        '''if found_ifscode is not None:
            #ifscode_json = fetch_ifsc_api_data(found_ifscode)
            #print(ifscode_json)
            # write_to_file(output_file_name,ifscode_json)
            print("APPAR PERUMAN SEVADIGAL POTRI POTRI")
		'''
    else:
        print("SIVAYANAMA File not Found error. can you please provide valid file that actually exists ")
