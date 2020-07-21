import pytesseract
from pytesseract import Output
from pytesseract import image_to_string
import re
from PIL import Image
# import cv2
# import numpy as np
from fettch_ifsc_api import Fetch_Ifsc_Api

import os
# TODO below to store the data in Mongo dB
# from pymongo import MongoClient 

# construct the CLI argument parse and parse the arguments
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
# ap.add_argument("-r", "--reference", required=True,
	# help="path to reference MICR E-13B font")
args = vars(ap.parse_args())

inp_path = 'inputs/'
input_file_path = os.path.join(inp_path, args["image"] )
print('Trying to process ' + input_file_path + '\n')

img = Image.open(input_file_path)
# img = Image.open("CUB_CHQ.JPG")
width, height = img.size
new_size = width*6, height*6
img = img.resize(new_size, Image.ANTIALIAS)
img = img.convert('L')
abc = img.point(lambda x: 0 if x < 170 else 300, '1')

custom_config = r' -l hin+eng --psm 12 '
custom_config = r' -l hin+eng --psm 3 '

# custom_config = r'-l grc+tha+eng --oem 3 --psm 6'
# ocr:tesseract inputs/AXIS_CHQ_2.jpg extracts\AXIS_CHQ_ -l eng+hin --psm 6
# print(pytesseract.image_to_string(image, config=custom_config))
# print(image_to_string(abc))
# ocr_text = image_to_string(img, config=custom_config)
ocr_text = pytesseract.image_to_string(abc, config=custom_config)

# need to loop through all possible configs like hin+eng | eng | psm 0 through 12 and then extract the ifsc 
# ocr_text_ = image_to_string(abc, config=custom_config)

osd = pytesseract.image_to_osd(abc)
angle = re.search('(?<=Rotate: )\d+', osd).group(0)
script = re.search('(?<=Script: )\w+', osd).group(0)
print("angle: ", angle)
print("script: ", script)

d = pytesseract.image_to_data(abc, config=custom_config, output_type=Output.DICT)
print(d)
# print(ocr_text)


print(ocr_text.find('IFS') )
print(ocr_text.count('IFSC') )

ifsc_text = ocr_text

found_IFS = ifsc_text.find('IFS')

def parse_ifsc(rip_ifsc_code):
    # m = re.match('([A-Za-z0]{4})(0\d{6})$', rip_ifsc_code)
    m = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    # m1 = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    if m:
        return m.group(1).replace('0', 'O').replace('1', 'I').upper() + m.group(2)
    else:
        return None

def parse_ifsc_UTI(rip_ifsc_code):
    # m = re.match('([A-Za-z0]{4})(0\d{6})$', rip_ifsc_code)
    m1 = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    if m1:
        return m1.group(1).replace('1', 'I').replace('0', 'O').upper() + m1.group(2)
    else:
        return None

parsed_ifs_code = parse_ifsc(ifsc_text)

print( '\tparsed_ifs_text ', (parsed_ifs_code) )
# print( '\t parse_ifsc_UTI ', (parse_ifsc_UTI(ifsc_text) ) )

if found_IFS >0:
	print('SIVA ',found_IFS , ' ifs count',ifsc_text.count('IFS') )
	ifsc_pattern = r"(IFS.*.[A-Z|a-z]{4}[0][\d]{6})"
	match_ifsc_pattern = re.search(ifsc_pattern, ifsc_text)
	if match_ifsc_pattern:
		extracted_ifsc = match_ifsc_pattern.groups()
		print( '\t extracted_ifsc = ',extracted_ifsc )
		# print( match_ifsc_pattern.group(1) )
		# print( '\t~~~~~~~~~~~~~' )
	else:
		print( '\tNOT FOUND properly' )
else:
	print( '\t IFS Code NOT FOUND accurately~~~~~~~~~~~~~' )


import time,calendar
localtime = time.asctime( time.localtime(time.time()) )
print(localtime)

# Open a file
output_file_path = "outputs/"
save_path = output_file_path #'C:/example/'

name_of_file = 'ocr_'+args["image"] #input("What is the name of the file: ")

completeName = os.path.join(save_path, name_of_file+".txt")  

print('Writing to ' + completeName + '\n')

# with open('filename', 'w', encoding='utf-8') as f:

fo = open(completeName, "a",encoding="utf-8")
fo.write('\n\n\t'+localtime+'\n\n')
fo.write(ocr_text)
fo.write('\n')
if parsed_ifs_code is not None:
	fo.write(parsed_ifs_code+'\n\t')
	Fetch_Ifsc_Api.fetch_ifsc_api_data(parsed_ifs_code)

# fo.write(extracted_ifsc)
fo.write('\n^EOF \n')
#os.rename("foo.txt","bar.txt")

# Close opend file
fo.close()


# 	work outputs are explained below
# canara bank IFSC  2012 MSRBC IFSC CNRBO000820 aa| sp
# CITY UNION BANK IFS Code: CIUB0000519
# CNRBO000820
# CIUB0000519
'''
CUB_CHQ - IFSC : CIUB0000519 , 
AXIS_CHQ_1.jpg -  IFSC : UTIB0004409
AXIS_CHQ_2.jpg -  failed
	-- solved by passing tesseract inputs\AXIS_CHQ_2.jpg AXIS_CHQ_2 -l hin+eng --psm 12
AXIS_CHQ_3.png	UT1B0000087
	-- noticed the alphabet I in UTI above is extracted ad number 1.
		psm 12 did not solve
	-- not solved by passing tesseract inputs\AXIS_CHQ_3.png AXIS_CHQ_2 -l hin+eng --psm 12
	-- solved by modifying the regexp pattern
ocr_canara_bank_chq_2.png - IFsc:cNRB000866 
ocr_canara_bank_chq_3.png - IFsc:CNRBOOOII73

hdfc_bank_chq_1.JPG - IFSC : HDFC0009661 , 
hdfc_bank_chq_2.png - failed
bob_chq_2.png - failed BARBOBAHAOU | actual BARB0CSUKAN BARBOCSUKAN
tesseract inputs\bob_chq_2.png bob_chk_2 -l hin+eng --psm 12

sbi_church.png - IFSC : SBIN0001821

'''
# python scripts an overview https://riptutorial.com/Download/python-language.pdf

# The IFSC is an 11-character code with the first four alphabetic characters representing the bank name, and the last six characters (usually numeric, but can be alphabetic) representing the branch. The fifth character is 0 (zero) and reserved for future use.
# REGEXP for IFSC is ([A-Z|a-z]{4}[0][\d]{6}) 

# Credits Wikipedia & RBI site & Razor pay API site

