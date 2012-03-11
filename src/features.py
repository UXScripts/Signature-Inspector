import cv
import utils
import math

def main():
	inputFolder = '../data/'
	inputFile = '001001_001.png'

	img = cv.LoadImageM(inputFolder+inputFile)
	BiImg = utils.toBinary(img)
	

	# Pv = verticalProjection(BiImg)
	# print "Vertical Projection"
	# print Pv

	# Ph = horizontalProjection(BiImg)
	# print "Horizontal Projection"
	# print Ph

	Vc = verticalCenter(BiImg)
	Hc = horizontalCenter(BiImg)

	# cv.Circle(BiImg, (Hc, Vc), 2, cv.RGB(200,0,0), thickness=2)
	Pv = verticalProjection(BiImg)
	(the_y, the_value) = globalBaseLine(BiImg)
	UP = upperLimit(BiImg, (the_y, the_value), Pv)
	LL = lowerLimit(BiImg, (the_y, the_value), Pv)

	print LL, the_y, UP
	cv.Line(BiImg, (0, the_y), (cv.GetSize(img)[0]-1, the_y), cv.RGB(200,0,0))
	cv.Line(BiImg, (0, LL), (cv.GetSize(img)[0]-1, LL), cv.RGB(200,0,0))
	cv.Line(BiImg, (0, UP), (cv.GetSize(img)[0]-1, UP), cv.RGB(200,0,0))

	cv.ShowImage("input", img)
	cv.ShowImage("Biinput", BiImg)
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

# This function calculates the vertical center of gravity of an image
# returns an int
def verticalCenter(img):
	(W, H, A, T) = basicGlobalFeatures(img)
	Pv = verticalProjection(img)

	total = 0
	for y in range(H):
		total += y * Pv[y]
	
	result = total/T
	return int(result)

# Just like verical center
def horizontalCenter(img):
	(W, H, A, T) = basicGlobalFeatures(img)
	Ph = horizontalProjection(img)

	total = 0
	for x in range(W):
		total += x * Ph[x]
	
	result = total/T
	return int(result)

# Returns a tuple containing the position of the global baseline (the_y) and 
# the value of vertical projection on the point (the_value)
# (the_y, the_value)
def globalBaseLine(img):
	(W, H) = cv.GetSize(img)
	Pv = verticalProjection(img)
	the_y = 0
	the_value = 0

	for y in range(H):
		if Pv[y] > the_value:
			the_value = Pv[y]
			the_y = y
	
	return (the_y, the_value)

def upperLimit(img, GBL, Pv):
	BL, value = GBL
	UL = 0
	diff = 0
	for y in range(BL):
		smoothV = y * value / BL
		tempDiff = abs(Pv[y] - smoothV)
		if tempDiff > diff:
			UL = y
			diff = tempDiff
	
	return UL

def lowerLimit(img, GBL, Pv):
	BL, value = GBL
	LL = 0
	diff = 0

	W,H = cv.GetSize(img)

	for y in range(BL, H):
		smoothV = value - (y * value / ((H-1) - BL))
		tempDiff = abs(Pv[y] - smoothV)
		if tempDiff > diff:
			LL = y
			diff = tempDiff
	
	return LL

if __name__ == '__main__':
	main()