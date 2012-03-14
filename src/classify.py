import utils
import features
import cv
import operator
import glob

def main():
	folder = '../data/normalized/'
	inputFolder = '../data/forged/'
	sign = '008'
	inputFile = '021' + sign +'_001.png'

	test_pre_classification_step()

	# img = cv.LoadImageM(inputFolder + inputFile)
	# slant = getslant(img)
	# print slant

	# files = glob.glob(folder + slant + '/' + sign + sign + '.json')
	# print len(files)

	# cv.ShowImage("input", img)
	# cv.WaitKey(0)

# input is the original input signature loadad as CvMat from disk
# returns a string such is 'PS'
def getslant(img):
	BiImg = utils.toBinary(img)
	enhancedImage = utils.enhanceImage(BiImg)
	cv.ShowImage("enhancedImage", enhancedImage)
	enhancedBinaryImage = utils.toBinary(enhancedImage)
	cv.ShowImage("enhancedBinaryImage", enhancedBinaryImage)
	thinnedImage = features.thinning(enhancedBinaryImage)
	cv.ShowImage("thinnedImage", thinnedImage)

	slantFeature = features.slantFeature(thinnedImage)
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

if __name__ == '__main__':
	main()