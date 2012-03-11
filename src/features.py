import cv
import utils
import math

def main():
	inputFolder = '../data/'
	inputFile = '002002_002.png'

	img = cv.LoadImageM(inputFolder+inputFile)
	BiImg = utils.toBinary(img)
	cv.ShowImage("input", img)
	cv.ShowImage("Biinput", BiImg)

	Pv = verticalProjection(BiImg)
	print "Vertical Projection"
	print Pv

	Ph = horizontalProjection(BiImg)
	print "Horizontal Projection"
	print Ph
	cv.WaitKey(0)

# This functions returns a tuple contaning 
# width(W), height(H), area(A) and total number of black pixels(T)
# (W,H,A,T)
def basicGlobalFeatures(img):
	(W, H) = cv.GetSize(img)
	A = W*H

	T = 0
	for x in range(W):
		for y in range(H):
			if img[y,x] == 0:
				T += 1
	return (W,H,A,T)

# This function returns a tuple containing
# cicularity feature(Ci = A/C), and radius of the cirscle(Srad)
# refer to the paper mentioned in README for more detailes
# (Ci, Srad)
def circularityFeature(img):
	(W, H) = cv.GetSize(img)
	A = W*H
	Ci = (4 * W * H) / (math.pi * (W**2 + H**2))
	Srad = math.sqrt(W**2 + H**2)/2.0
	return (Ci, Srad)

# This function calculates the vertical projection of an image
# returns a list of integers, with length of height of the image.
# Be carefull this function only counts true black pixles with 0 as their grayscale values
def verticalProjection(img):
	(W, H) = cv.GetSize(img)
	Pv = []

	for y in range(H):
		tB = 0
		for x in range(W):
			if img[y, x] == 0: #Black pixle
				tB += 1
		Pv.append(tB)
	
	return Pv

# This function calculates the horizontal projection of an image
# returns a list of integers, with length of width of the image.
# Be carefull this function only counts true black pixles with 0 as their grayscale values
def horizontalProjection(img):
	(W, H) = cv.GetSize(img)
	Ph = []

	for x in range(W):
		tB = 0
		for y in range(H):
			if img[y, x] == 0: #Black pixle
				tB += 1
		Ph.append(tB)
	
	return Ph

if __name__ == '__main__':
	main()