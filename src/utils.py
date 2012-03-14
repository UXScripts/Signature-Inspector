import cv
import glob
import operator

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

	# print int(w), int(h)

	# img = cv.LoadImageM(inputFolder+inputFile)
	# cv.ShowImage("input", img)
	# outputImg = resizeImage(img, int(w), int(h))
	# cv.ShowImage("output",outputImg)
	# cv.WaitKey(0)

	normalizationStep(inputFolder, outputFolder)

	# img = cv.LoadImageM(outputFolder+inputFile)
	# cv.ShowImage("input", img)
	# outputImg = toBinary(img)
	# cv.ShowImage("binary",outputImg)
	# enhancedImage = enhanceImage(img)
	# cv.ShowImage("enhancedImage",enhancedImage)
	# cv.WaitKey(0)


	preclassification(outputFolder)

def toBinary(img):
	# convert to grayscale
	if cv.GetElemType(img) == cv.CV_8UC3:
		# Create an image to store the output version on
		result = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
		cv.CvtColor(img, result, cv.CV_RGB2GRAY)
	else:
		result = cv.CloneMat(img)

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
	result = cv.CreateMat(H, W, cv.GetElemType(img))
	cv.Resize(img, result)
	return result

# This function does the normalization steps
def normalizationStep(inputFolder, outputFolder):
	import json
	mW, mH = meanSizeOfSamples(inputFolder)
	mW, mH = int(mW), int(mH)
	imgAddrs = glob.glob(inputFolder + '*_*.png')
	for address in imgAddrs:
		img = cv.LoadImageM(address)
		img = toBinary(img)
		gfv = calculateGloablFeatureVector(img)
		img = resizeImage(img, mW, mH)

		parts = address.split('\\')
		destAddr = parts[len(parts)-1]

		parts = destAddr.split('.')
		name = parts[0]

		gfv = json.dumps(gfv)

		FILE = open(outputFolder + name + '.json', 'w')
		FILE.write(gfv)
		FILE.close()

		cv.SaveImage(outputFolder + destAddr, img)

# This function performs the image enhancement step on a CvMat input
# returns a CvMat object.
def enhanceImage(img):
	W, H = cv.GetSize(img)
	result = cv.CreateMat(H, W, cv.GetElemType(img))
	cv.Smooth(img, result, smoothtype=cv.CV_BLUR, param1=3)
	return result

def preclassification(inputFolder):
	import features
	import shutil

	imgAddrs = glob.glob(inputFolder + '*_*.png')
	for image in imgAddrs:
		img = cv.LoadImageM(image)
		img = toBinary(img)
		slant = features.slantFeature(img)

		parts = image.split('\\')
		destAddr = parts[len(parts)-1]

		parts = destAddr.split('.')
		name = parts[0]

		
		sorted_slant = sorted(slant.iteritems(), key=operator.itemgetter(1))
		slantFeature = sorted_slant[len(sorted_slant)-1]

		folder = slantFeature[0]
		shutil.copyfile(inputFolder + name + '.json', inputFolder + folder + '/' + name + '.json')
		cv.SaveImage(inputFolder + folder + '/' + destAddr, img)

# The global feature vector is as follows:
# width to height ratio: W/H
# circulatiry ratio: A/C (reffer to features.py)
# intensity ratio: T/A
# relative position of the baseline: BSL/H
# relative position of the lower limit: LL/H
# relative position of the upper limit: (H - UL + 1)/H
# (H/W, A/C, T/A, BSL/H, LL/H, (H - UL + 1)/H)
# {'HtW': H/W, 'AtC': A/C, 'TtA': T/A, 'BtH': BSL/H, 'LtH': LL/H, 'UtH': (H - UL + 1)/H}
# returns a dict
def calculateGloablFeatureVector(img):
	import features
	(W,H,A,T) = features.basicGlobalFeatures(img)
	(Ci, Srad) = features.circularityFeature(img)
	Pv = features.verticalProjection(img)
	BSL = features.globalBaseLine(img)
	(B, t_v) = BSL
	U = features.upperLimit(img, BSL, Pv)
	L = features.lowerLimit(img, BSL, Pv)

	HtW = float(H) / W
	AtC = Ci
	TtA = float(T) / A
	BtH = float(B) / H
	LtH = float(L) / H
	UtH = float(H-U+1) / H

	return {'HtW': HtW, 'AtC': AtC, 'TtA': TtA, 'BtH': BtH, 'LtH': LtH, 'UtH': UtH}

if __name__ == '__main__':
	main()