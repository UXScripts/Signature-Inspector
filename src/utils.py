import cv
import glob
import operator
import numpy

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

	# normalizationStep(inputFolder, outputFolder)

	# img = cv.LoadImageM(outputFolder+inputFile)
	# cv.ShowImage("input", img)
	# outputImg = toBinary(img)
	# cv.ShowImage("binary",outputImg)
	# enhancedImage = enhanceImage(img)
	# cv.ShowImage("enhancedImage",enhancedImage)
	# cv.WaitKey(0)

	doPrepration()
	
def doPrepration():
	inputFolder = '../data/'
	outputFolder = '../data/normalized/'
	normalizationStep(inputFolder, outputFolder)
	preclassification(outputFolder)

	sub_classes = ['PS', 'NS', 'HS', 'VS']
	for slantness in sub_classes:
		calculateMeanGlobalFeatureVector(outputFolder + slantness + '/')

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
		# img = resizeImage(img, mW, mH)

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

def calculateMeanGlobalFeatureVector(inputFolder):
	import json
	for x in range(1,13):
		toAdd = '00'
		if x >= 10:
			toAdd = '0'
		
		files = glob.glob(inputFolder + toAdd + str(x) + toAdd + str(x) + '_*.json')
		if len(files) == 0:
			pass
		elif len(files) == 1:
			parts = files[0].split('\\')
			destAddr = parts[len(parts)-1]

			parts = destAddr.split('.')
			name = parts[0]

			FILE = open(files[0], 'r')
			gfv = FILE.read()
			FILE.close()
			gfv = json.loads(gfv)

			gfv['HtW_std'] = 0
			gfv['AtC_std'] = 0
			gfv['TtA_std'] = 0
			gfv['BtH_std'] = 0
			gfv['LtH_std'] = 0
			gfv['UtH_std'] = 0

			gfv = json.dumps(gfv)
			FILE = open(inputFolder + toAdd + str(x) + toAdd + str(x) + '.json', 'w')
			FILE.write(gfv)
			FILE.close()

		elif len(files) == 2:
			HtWs = []
			AtCs = []
			TtAs = []
			BtHs = []
			LtHs = []
			UtHs = []
			for f in files:
				FILE = open(f, 'r')
				gfv = FILE.read()
				FILE.close()
				gfv = json.loads(gfv)
				HtWs.append(gfv['HtW'])
				AtCs.append(gfv['AtC'])
				TtAs.append(gfv['TtA'])
				BtHs.append(gfv['BtH'])
				LtHs.append(gfv['LtH'])
				UtHs.append(gfv['UtH'])
			gmfv = {}

			HtW_std = numpy.array(HtWs).std()
			AtC_std = numpy.array(AtCs).std()
			TtA_std = numpy.array(TtAs).std()
			BtH_std = numpy.array(BtHs).std()
			LtH_std = numpy.array(LtHs).std()
			UtH_std = numpy.array(UtHs).std()
			
			gmfv['HtW_std'] = HtW_std
			gmfv['AtC_std'] = AtC_std
			gmfv['TtA_std'] = TtA_std
			gmfv['BtH_std'] = BtH_std
			gmfv['LtH_std'] = LtH_std
			gmfv['UtH_std'] = UtH_std
			gmfv['HtW'] = sum(HtWs)/float(len(HtWs))
			gmfv['AtC'] = sum(AtCs)/float(len(AtCs))
			gmfv['TtA'] = sum(TtAs)/float(len(TtAs))
			gmfv['BtH'] = sum(BtHs)/float(len(BtHs))
			gmfv['LtH'] = sum(LtHs)/float(len(LtHs))
			gmfv['UtH'] = sum(UtHs)/float(len(UtHs))
			gmfv = json.dumps(gmfv)
			FILE = open(inputFolder + toAdd + str(x) + toAdd + str(x) + '.json', 'w')
			FILE.write(gmfv)
			FILE.close()
		else:
			HtWs = []
			AtCs = []
			TtAs = []
			BtHs = []
			LtHs = []
			UtHs = []
			for f in files:
				FILE = open(f, 'r')
				gfv = FILE.read()
				FILE.close()
				gfv = json.loads(gfv)
				HtWs.append(gfv['HtW'])
				AtCs.append(gfv['AtC'])
				TtAs.append(gfv['TtA'])
				BtHs.append(gfv['BtH'])
				LtHs.append(gfv['LtH'])
				UtHs.append(gfv['UtH'])
			gmfv = {}

			HtW_std = numpy.array(HtWs).std()
			AtC_std = numpy.array(AtCs).std()
			TtA_std = numpy.array(TtAs).std()
			BtH_std = numpy.array(BtHs).std()
			LtH_std = numpy.array(LtHs).std()
			UtH_std = numpy.array(UtHs).std()
			
			gmfv['HtW_std'] = HtW_std
			gmfv['AtC_std'] = AtC_std
			gmfv['TtA_std'] = TtA_std
			gmfv['BtH_std'] = BtH_std
			gmfv['LtH_std'] = LtH_std
			gmfv['UtH_std'] = UtH_std

			max_HtW = max(HtWs)
			max_AtC = max(AtCs)
			max_TtA = max(TtAs)
			max_BtH = max(BtHs)
			max_LtH = max(LtHs)
			max_UtH = max(UtHs)

			min_HtW = min(HtWs)
			min_AtC = min(AtCs)
			min_TtA = min(TtAs)
			min_BtH = min(BtHs)
			min_LtH = min(LtHs)
			min_UtH = min(UtHs)

			gmfv['HtW'] = (sum(HtWs) - min_HtW - max_HtW)/float(len(files)-2)
			gmfv['AtC'] = (sum(AtCs) - min_AtC - max_AtC)/float(len(files)-2)
			gmfv['TtA'] = (sum(TtAs) - min_TtA - max_TtA)/float(len(files)-2)
			gmfv['BtH'] = (sum(BtHs) - min_BtH - max_BtH)/float(len(files)-2)
			gmfv['LtH'] = (sum(LtHs) - min_LtH - max_LtH)/float(len(files)-2)
			gmfv['UtH'] = (sum(UtHs) - min_UtH - max_UtH)/float(len(files)-2)

			gmfv = json.dumps(gmfv)
			FILE = open(inputFolder + toAdd + str(x) + toAdd + str(x) + '.json', 'w')
			FILE.write(gmfv)
			FILE.close()

if __name__ == '__main__':
	main()