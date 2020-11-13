from PIL import Image
import pytesseract
import os

def get_text(filename):

	th1 = 140
	th2 = 140 # threshold after blurring 
	sig = 1.5 # the blurring sigma

	current_directory = os.getcwd()

	if os.path.exists(current_directory + r"/final.png"):
		os.remove(current_directory + r"/final.png")

	original = Image.open(current_directory + "/" + filename)
	black_and_white =original.convert("L")
	first_threshold = black_and_white.point(lambda p: p > th1 and 255)
	first_threshold.save("final.png")
	im = Image.open('final.png')
	captcha_text = pytesseract.image_to_string(im)
	captcha_text.replace(" ", "")
	print("Solved Captcha : ", captcha_text.upper())
	# print(captcha_text)
	return captcha_text.upper()


if __name__ == '__main__':
	print(get_text("captcha.png"))