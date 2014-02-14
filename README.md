cern-atlas-mmOptical
====================

This is the code base for optically analyzing the micromegas boards using optical techniques

The code allows an image that is taken of a micromegas board, along with a ruler, to be analysed


::::::::::::::
Dependencies
::::::::::::::

Platform independent IMAGEJ .jar file
[download here:]
http://rsbweb.nih.gov/ij/download.html


PYTHON LIBRARIES:

Pyplot
Matplotlib

::::::::::::::
Program Inputs
::::::::::::::

A rectangular image of strips from a micromegas board with a ruler overlayed on the image (see example image)

::::::::::::::
Variables
::::::::::::::

from the directory where you would like the temporary image files to be created, run:
python ~/cern-atlas-mmOptical/code/run.py

analysisDirectory = argv[1]
inputImageFileName = argv[2]
colorMode = argv[3] #R-red channel, G-green, B-blue
backgroundSmoothingParameter = argv[4]
foregroundSmoothingParameter = argv[5]
startx = argv[6]
starty = argv[7]
width = argv[8]
length = argv[9]
micronsPerPixel = argv[10]
Realpitch = argv[11]
dumpRulerData = argv[12]
adjustToRuler = argv[13] #0 no adjustment, 1 adjustment
adjustmentFile = argv[14] # this is a pickle file
adjustmentSpacing = argv[15] # this is how many microns there are between each adjustment
thicknessOfRuler = argv[16]
distanceOfCamera = argv[17]
imageType = argv[18] #0 for raw format tiff, 1 for JPG (that Fabian sent)



example:
1. driectory has the image IMGP0853_crop.tif in it
run python ~/cern-atlas-mmOptical/code/run.py ./ IMGP0853_crop.tif R 30 3 0 230 40 4976 39.436 447.9 0 1 AUTO_ruler.p 396.87

