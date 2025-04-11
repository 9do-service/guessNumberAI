import eel
import os
import sys
import time
import datetime
import io
import PIL.Image
import google.generativeai as genai
import google.generativeai.types as genai_types
import base64


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
@eel.expose  # Eel function
def qrBase64Decoder(param):
	jsonObj = {'code':'00'}
	if param['base64Str'] != '':
		try:
			image_bytes = base64.b64decode(param['base64Str'].replace('data:image/png;base64,',''))
			#image_part = genai_types.Part(inline_data=genai_types.Blob(mime_type='image/png', data=image_bytes))
			img = PIL.Image.open(io.BytesIO(image_bytes))
			prompt_with_image = "請仔細辨別並顯示圖片裡的文字"
			#response = vision_model.generate_content([prompt_with_image, image_part])
			response = vision_model.generate_content([prompt_with_image, img])
			jsonObj['rlt'] = response.text.split('\n')[0]
		except:
			pass
	else:
		jsonObj['code'] = '01'

	return jsonObj

if __name__ == '__main__':
	eel.init('web')
	my_options = {
		'mode': "chrome-app", #or "chrome",
		'host': 'localhost',
		'port': 8291,
	}

	try:
		eel.start('index.html', mode='chrome-app', port=8291)
	except (SystemExit, MemoryError, KeyboardInterrupt):
		pass 
	



