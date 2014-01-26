#
# run.py - the base code that is run
#

#
# some hardcoded locations for things
#
import os
from sys import argv
from math import copysign



# Hard coded directories. Please change these accordingly.
imageJjarName = '/Users/ainglis/Applications/ImageJ-platInd/ij.jar'
imageJjarPath = '/Users/ainglis/Applications/ImageJ-platInd'
imageJscript = '/Users/ainglis/pycharmbase/cern-atlas-mmOptical/code/imageJscript001.txt'


analysisDirectory = argv[1]
inputImageFileName = argv[2]
colorMode = argv[3] #R-red channel, G-green, B-blue
plotMode = argv[4] #0-gnuplot, 1-pyplot
backgroundSmoothingParameter = argv[5]
foregroundSmoothingParameter = argv[6]


#print analysisDirectory, inputImageFileName, colorMode, plotMode
javaCommand = 'java -jar -Xmx2048m ' + imageJjarName + ' -ijpath ' + imageJjarPath + ' -batch ' + imageJscript + ' ' + inputImageFileName + ':' + colorMode + ':' + backgroundSmoothingParameter   + ':' + foregroundSmoothingParameter
#print javaCommand

os.system(javaCommand)

# now the information is in the file sliver_auto_pp.txt
dataFile = open('sliver_auto_pp.txt','r')

dataRaw = dataFile.readlines()
dataRaw.pop(0)

data = []
for d in dataRaw:
    d001 = d.split('\t')
    d002 = d001[1].split('\n')
    data.append(float(d002[0]))

#find all peaks between 0 marks. peaks will be the lighter
#regions.
#first, find all zeros
zeroCross = []
for i in range(0,len(data)-1):
    if(copysign(data[i],data[i+1]) != data[i]):
        zeroCross.append(i)

#print zeroCrossing
#print len(zeroCrossing)

centersOfMass = []
numerators = []
denominators =[]

#need to be capturing the cm of the negative values
firstEval = data[zeroCross[0]+1]
start = 0
if(firstEval != copysign(firstEval,-1.0)):
    start = 1

for i in range(len(zeroCross)/2-1):
    startIndex = zeroCross[2*i+start]
    endIndex = zeroCross[2*i+start+1]
    numerator = 0.
    denominator = 0.

    for i in range (startIndex,endIndex):
        numerator = numerator + i*data[i]
        denominator = denominator + data[i]
    numerators.append(numerator)
    denominators.append(denominator)
    centersOfMass.append(numerator/denominator)

#print numerators
#print centersOfMass
#print len(centersOfMass)
#print 'started at', start

distances = []
for i in range(len(centersOfMass)-1):
    distances.append(centersOfMass[i+1]-centersOfMass[i])

import matplotlib.pyplot as plt
plt.plot(distances)
plt.ylabel('pixel values from edge')
plt.show()








