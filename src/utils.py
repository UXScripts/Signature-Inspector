import cv

def main():
	inputFolder = '../data/'
	inputFile = '002002_002.png'

	# img = cv.LoadImageM(inputFolder+inputFile)
	# cv.ShowImage("input", img)

	# outputImg = toBinary(img)
	# cv.ShowImage("output",outputImg)

	# cv.WaitKey(0)

	print meanSizeOfSamples(inputFolder)

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

# This function returns a tuple
# Containing mean width(mW) and height(mH) of some samples
# (mW,mH) both are floats
# folder argument is the address to the folder containing all the
# learning samples.
# For sample naming convention see README
def meanSizeOfSamples(folder):
	import glob
	files = glob.glob(folder + '*_*.png')

	l = len(files)

	tW = 0.0
	tH = 0.0

	for _file in files:
		img = cv.LoadImageM(_file)
		(W, H) = cv.GetSize(img)
		tW += W
		tH += H
	
	(mW, mH) = (tW/l, tH/l)
	return (mW, mH)

if __name__ == '__main__':
	main()