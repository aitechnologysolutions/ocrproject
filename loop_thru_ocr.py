'''
	will loop though the directory inputs and ocr all of the files with extensions jpg and png, 
	extract the text oout of it and dumps it in the text file in the outputs directory
'''
import pytesseract
from pytesseract import Output
from pytesseract import image_to_string
import re
from PIL import Image
import time,calendar
import os

def parse_ifsc(rip_ifsc_code):
    # m = re.match('([A-Za-z0]{4})(0\d{6})$', rip_ifsc_code)
    m = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    # m1 = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    if m:
        return m.group(1).replace('0', 'O').replace('1', 'I').upper() + m.group(2)
    else:
        return None

def write_to_file(fileName,dump_to_file):
	localtime = time.asctime( time.localtime(time.time()) )
	print('Writing to ' + fileName + '\n')

	# with open('filename', 'w', encoding='utf-8') as f:

	fo = open(fileName, "a",encoding="utf-8")
	fo.write('\n\n\t'+localtime+'\n\n')
	fo.write(dump_to_file)
	fo.write('\n')
	parsed_ifs_code = parse_ifsc(dump_to_file)
	if parsed_ifs_code is not None:
		fo.write(parsed_ifs_code+'\n\t')

	# fo.write(extracted_ifsc)
	fo.write('\n^EOF \n')
	#os.rename("foo.txt","bar.txt")

	# Close opend file
	fo.close()

def begin_loop_dir(in_dir=None,out_dir=None,search_ext=None):
	directory = r'inputs'
	out_dir= r'outputs'
	search_ext = '.jpg,.png'
	for filename in os.listdir(directory):
		if filename.endswith(".jpg") or filename.endswith(".png"):
			print(os.path.join(directory, filename))
			input_file_path = os.path.join(directory, filename)
			output_file_name = os.path.join(out_dir, filename+".txt")
			custom_config = r' -l hin+eng --psm 3 '
			img = Image.open(input_file_path)
			ocr_text = pytesseract.image_to_string(img, config=custom_config)
			ifsc_text = ocr_text
			found_IFS = ifsc_text.find('IFS')
			write_to_file(output_file_name,ocr_text)
			
		else:
			continue
			

if __name__ == '__main__':
    # loop_thru_ocr.run(debug=True)
	begin_loop_dir()
	
