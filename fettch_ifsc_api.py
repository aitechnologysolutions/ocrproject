import requests

## will accept a input of text and lookup for IFS Code and returns it.
def extract_ifsc(rip_ifsc_code):
    # m = re.match('([A-Za-z0]{4})(0\d{6})$', rip_ifsc_code)
    m = re.search('([A-Za-z01]{4})(0\d{6})', rip_ifsc_code)
    if m:
        return m.group(1).replace('0', 'O').replace('1', 'I').upper() + m.group(2)
    else:
        return None

## will accept a input of text and lookup for IFS Code and returns it.
class Fetch_Ifsc_Api(object):
	def fetch_ifsc_api_data(ifs_code):
		url = "https://ifsc.razorpay.com/"+ifs_code
		print ('Querying the ',url)
		headers = {
			'accept': "application/json",
			'content-type': "application/json"
			}
		response = requests.request("GET", url, headers=headers)

		print(response.text)
		
if __name__ == '__main__':
    # loop_thru_ocr.run(debug=True)
	ifs_code="CNRE0008667"
	Fetch_Ifsc_Api.fetch_ifsc_api_data(ifs_code)

