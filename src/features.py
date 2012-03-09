import cv
import utils
import math

def main():
	inputFolder = '../data/'
	inputFile = '002002_002.png'

	img = cv.LoadImageM(inputFolder+inputFile)
	BiImg = utils.toBinary(img)
	print basicGlobalFeatures(BiImg)
	print circularityFeature(BiImg)

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
	Ci = (math.pi * (W**2 + H**2)) / float(2 * W * H)
	Srad = math.sqrt(W**2 + H**2)/2.0
	return (Ci, Srad)
if __name__ == '__main__':
	main()