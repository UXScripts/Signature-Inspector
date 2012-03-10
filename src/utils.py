import cv
import glob

def main():
	inputFolder = '../data/'
	outputFolder = '../data/normalized/'
	inputFile = '002002_002.png'

	# img = cv.LoadImageM(inputFolder+inputFile)
	# cv.ShowImage("input", img)
	# outputImg = toBinary(img)
	# cv.ShowImage("output",outputImg)
	# cv.WaitKey(0)

	# (w, h) = meanSizeOfSamples(inputFolder)

	# img = cv.LoadImageM(inputFolder+inputFile)
	# cv.ShowImage("input", img)
	# outputImg = resizeImage(img, int(w), int(h))
	# cv.ShowImage("output",outputImg)
	# cv.WaitKey(0)

	normalizationStep(inputFolder, outputFolder)

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
# (mW,mH) **both are floats**. If you want to use these for resizing be sure to convert to ints.
# folder argument is the address to the folder containing all the
# learning samples.
# For sample naming convention see README
def meanSizeOfSamples(folder):
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

# returns a CvMat containing the resized image
def resizeImage(img, W,H):
	"""
	I like to mention OpenCV's annoyance here for a moment.
	In python interface of OpenCV, CvSize is defined as a tupe: (width, height)
	If you want to get the size of a CvMat you can call cv.GetSize(mat), which will return a CvSize(w,h)
	But if you want to create a CvMat (from nothing) you should try cv.CreateMat.
	Which takes 3 arguments, cols(height), rows(width), and elemType.
	But what bothers me is the ordering of those arguments.
	And the use of two different arguments instead of just one CvSize.
	cv.CreateMat(height, width, cv.GetElemType(mat)). Which is annoying.
	"""

	result = cv.CreateMat(H, W, cv.GetElemType(img))
	cv.Resize(img, result)
	return result

def normalizationStep(inputFolder, outputFolder):
	mW, mH = meanSizeOfSamples(inputFolder)
	mW, mH = int(mW), int(mH)
	imgAddrs = glob.glob(inputFolder + '*_*.png')
	for address in imgAddrs:
		img = cv.LoadImageM(address)
		img = toBinary(img)
		img = resizeImage(img, mW, mH)
		parts = address.split('\\')
		destAddr = parts[len(parts)-1]
		print destAddr
		cv.SaveImage(outputFolder + destAddr, img)

if __name__ == '__main__':
	main()