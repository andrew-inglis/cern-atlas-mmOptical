#
# run.py - the base code that is run
#

#
# some hardcoded locations for things
#
import os
from sys import argv
from math import copysign
import matplotlib.pyplot as plt



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

startx = argv[7]
starty = argv[8]
width = argv[9]
length = argv[10]

micronsPerPixel = argv[11]
pitch = argv[12]


#print analysisDirectory, inputImageFileName, colorMode, plotMode
javaCommand = 'java -jar -Xmx2048m ' + imageJjarName + ' -ijpath ' + imageJjarPath + \
              ' -batch ' + imageJscript + ' ' + inputImageFileName + ':' + colorMode + \
              ':' + backgroundSmoothingParameter   + ':' + foregroundSmoothingParameter + \
              ':' + startx   + ':' + starty + \
              ':' + width   + ':' + length
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
    data.append(60000 - float(d002[0]))
    #data.append(float(d002[0]))


#print data

#plt.plot(data)
#plt.show()
#exit(1)



brightestValues = []
for i in range(1,len(data)-1):
    if(data[i] < data[i-1] and data[i] < data[i+1]): # then this is the highest point
        brightestValues.append(i)


print brightestValues

#exit(1)

centersOfMass = []
numerators = []
denominators =[]

#need to be capturing the cm of the negative values

#firstEval = data[zeroCross[0]+1]
#start = 0
#if(firstEval != copysign(firstEval,-1.0)):
#    start = 1

#for i in range(len(zeroCross)/2-1):
for i in range(len(brightestValues)-1):
    #startIndex = zeroCross[2*i+start]
    #endIndex = zeroCross[2*i+start+1]
    startIndex = brightestValues[i]
    endIndex = brightestValues[i+1]
    numerator = 0.
    denominator = 0.

    for i in range (startIndex,endIndex):
        numerator = numerator + i*data[i]
        denominator = denominator + data[i]
    numerators.append(numerator)
    denominators.append(denominator)
    centersOfMass.append(1.0*numerator/denominator)

#print numerators
#print centersOfMass
#print len(centersOfMass)
#print 'started at', start

plotYvalues = []
stripNumber = []

distances = []
for i in range(len(centersOfMass)-1):
    differencesInMicrons = ((centersOfMass[i+1]-centersOfMass[i])-float(pitch)/float(micronsPerPixel))*float(micronsPerPixel)
    distanceInMicrons = (centersOfMass[i])*float(micronsPerPixel)
    yValue = (distanceInMicrons - (i)*float(pitch))

    stripNumber.append(i)
    plotYvalues.append(yValue)
    #plotYvalues.append(differencesInMicrons)




plt.plot(stripNumber, plotYvalues)
#plt.ylabel('Ruler Grade location minus ideal location (microns)')
plt.ylabel('Resistive strip location minus ideal location (microns)')
plt.xlabel('Resistive strip #')
plt.show()








