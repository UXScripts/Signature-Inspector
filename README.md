##Offline Signature Recognition and Verification

This is a Python-OpenCV implementation of a system that does offline signature recognition and verification.

###Requirements

* Python 2.7
* OpenCV 2.2
* python interface for OpenCV

###The paper

For a similar system you can look at the following paper:    
"Off-line arabic signature recognition and verification", M.A. Ismail, Samia Gad - Pattern Recognition (2000) Elsevier

###Signature data

I had no hope getting access to the data the Mr. Ismail used in his paper. So I started to search on the internet for some data and I found some puplically available on <http://sigcomp09.arsforensica.org/NISDCC-preview/>. There is a collection of 60 authentic signatures form 12 peoples, And 151 forged version for each persons signiture.

All those data are located on `data` directory.

####Naming convension

Each person has a 3 digit ID like 001, 002, etc. Each signiture regardless if it is authentic or forged is done 5 times, and to separate each signature a 3 digit id is appended to the end.

So the file `001001_000.png` means: It's the __1st__ signature, which is signed by person __001__ (first 001), which belongs to person __001__ (second 001). So we know that this signature is authentic. And there is 4 more versions of it named `001001_001.png` to `001001_004.png`.

An example of a __forged__ signature would be `021001_000.png`. Which means person __021__ tried to forge person __001__'s signature.


