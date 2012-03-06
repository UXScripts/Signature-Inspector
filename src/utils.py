import cv

def main():
	inputFolder = '../data/'
	inputFile = '002002_002.png'

	img = cv.LoadImageM(inputFolder+inputFile)
	cv.ShowImage("input", img)

	outputImg = toBinary(img)
	cv.ShowImage("output",outputImg)

	cv.WaitKey(0)

def toBinary(img):
	# Create an image to store the output version on
	result = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)

	# convert to grayscale
	cv.CvtColor(img, result, cv.CV_RGB2GRAY)

	# apply threshold
	# TODO: Make use of better thresholding algorithms
	thr = 230
	cv.Threshold(result, result, thr, 255, cv.CV_THRESH_BINARY)

	return result

if __name__ == '__main__':
	main()