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
[working directory] [tif image file] [color channel to analyze] [blurring of the background]
[blurring of the foreground] [startx of analysis strip] [starty] [width of analysis strip]
[length] [microns per pixel of image] [pitch of analysis strip in microns]
[1-create ruler lookup out of analysis strip]
[1-apply pre-created ruler to the analysis of the current strip] [pitch of ruler in microns]

example:
1. driectory has the image IMGP0853_crop.tif in it
run python ~/cern-atlas-mmOptical/code/run.py ./ IMGP0853_crop.tif R 30 3 0 230 40 4976 39.436 447.9 0 1 AUTO_ruler.p 396.87

