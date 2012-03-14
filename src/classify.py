import utils
import features
import cv
import operator
import glob
import json
import numpy

def main():
	f = '../data/'
	folder = '../data/normalized/'
	inputFolder = '../data/forged/'
	sign = '004'
	inputFile = sign + sign +'_000.png'

	img = cv.LoadImageM(f + inputFile)
	slant = getslant(img)
	# print "slant", slant

	# second_stage_classification(folder + slant + '/', img)


	test_second_stage()


	# files = glob.glob(folder + slant + '/' + sign + sign + '.json')
	# print len(files)

	# cv.ShowImage("input", img)
	# cv.WaitKey(0)

# input is the original input signature loadad as CvMat from disk
# returns a string such is 'PS'
def getslant(img):
	BiImg = utils.toBinary(img)
	# enhancedImage = utils.enhanceImage(BiImg)
	# cv.ShowImage("enhancedImage", enhancedImage)
	# enhancedBinaryImage = utils.toBinary(enhancedImage)
	# cv.ShowImage("enhancedBinaryImage", enhancedBinaryImage)

	slantFeature = features.slantFeature(BiImg)
	sorted_slant = sorted(slantFeature.iteritems(), key=operator.itemgetter(1))
	slantness = sorted_slant[len(sorted_slant)-1]
	slant = slantness[0]
	return slant

def test_pre_classification_step():
	folder = '../data/normalized/'
	inputFolder = '../data/forged/'

	for x in range(1,13):
		toAdd = '00'
		if x >= 10:
			toAdd = '0'
		sign = toAdd + str(x)
		inputFile = '021' + sign +'_000.png'
		img = cv.LoadImageM(inputFolder + inputFile)

		slant = getslant(img)
		files = glob.glob(folder + slant + '/' + sign + sign + '.json')
		print len(files)

def second_stage_classification(subfolder, img):

	dests = {}
	fv = utils.calculateGloablFeatureVector(img)
	for x in range(1,13):
		toAdd = '00'
		if x >= 10:
			toAdd = '0'
		files = glob.glob(subfolder + toAdd + str(x) +toAdd + str(x) + '.json')
		if len(files) == 1:
			FILE = open(files[0], 'r')
			file_contents = FILE.read()
			FILE.close()

			gmfv = json.loads(file_contents)
			dests[str(x)] = feature_space_distance(gmfv, fv)
	
	sorted_dests = sorted(dests.iteritems(), key=operator.itemgetter(1))
	return sorted_dests

def test_second_stage():
	inputFolder = '../data/forged/'
	folder = '../data/normalized/'

	sign = '002'

	print '-------'
	print sign
	inputFile = '021' + sign +'_000.png'
	img = cv.LoadImageM(inputFolder + inputFile)
	slant = getslant(img)
	dests = second_stage_classification(folder + slant + '/', img)
	print dests

	


def feature_space_distance(gmfv, fv):
	a = numpy.array([gmfv['HtW'] ,gmfv['AtC'] ,gmfv['TtA'] ,gmfv['BtH'] ,gmfv['LtH'] ,gmfv['UtH']])
	b = numpy.array([fv['HtW'] ,fv['AtC'] ,fv['TtA'] ,fv['BtH'] ,fv['LtH'] ,fv['UtH']])

	return numpy.linalg.norm(a-b)

if __name__ == '__main__':
	main()