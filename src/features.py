import cv
import utils

def main():
	inputFolder = '../data/'
	inputFile = '002002_002.png'

	img = cv.LoadImageM(inputFolder+inputFile)
	basicGlobalFeatures(utils.toBinary(img))

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

if __name__ == '__main__':
	main()