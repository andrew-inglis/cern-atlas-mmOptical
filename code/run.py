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
import pickle
import numpy




# Hard coded directories. Please change these accordingly.
imageJjarName = '/Users/ainglis/Applications/ImageJ-platInd/ij.jar'
imageJjarPath = '/Users/ainglis/Applications/ImageJ-platInd'

imageJscript = '/Users/ainglis/pycharmbase/cern-atlas-mmOptical/code/imageJscript001.txt'
imageJscript_jpg = '/Users/ainglis/pycharmbase/cern-atlas-mmOptical/code/imageJscript002_jpg.txt'


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

pitch = float(Realpitch)*(1-float(thicknessOfRuler)/float(distanceOfCamera))


scriptToUse = ''
if(int(imageType) == 0):
    scriptToUse = imageJscript
elif(int(imageType) == 1):
    scriptToUse = imageJscript_jpg

#print analysisDirectory, inputImageFileName, colorMode, plotMode
javaCommand = 'java -jar -Xmx2048m ' + imageJjarName + ' -ijpath ' + imageJjarPath + \
              ' -batch ' + scriptToUse + ' ' + inputImageFileName + ':' + colorMode + \
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
    if(int(imageType) == 0):
        data.append(-float(d002[0]))
    elif(int(imageType) == 1):
        data.append(float(d002[0]))

#print data

#plt.plot(data)
#plt.show()
#exit(1)

brightestValues = []
for i in range(1,len(data)-1):
    if( ( (data[i] < data[i-1] and data[i] < data[i+1]) or
        (data[i] == data[i+1] and data[i] < data[i-1] and data[i+1] < data[i+2]))
        and data[i] < 0): # then this is the lowest point
        brightestValues.append(i)


print brightestValues


centersOfMass = []
numerators = []
denominators =[]

#need to be capturing the cm of the negative values

#firstEval = data[zeroCross[0]+1]
#start = 0
#if(firstEval != copysign(firstEval,-1.0)):
#    start = 1

for i in range(len(brightestValues)-1):
    startIndex = brightestValues[i]
    endIndex = brightestValues[i+1]
    numerator = 0.
    denominator = 0.

    #find the lowest value
    lowestValue = 999999999999
    for i in range (startIndex,endIndex):
        if(data[i]<lowestValue):
            lowestValue = data[i]

    for i in range (startIndex,endIndex):
        numerator = numerator + i*(data[i] - lowestValue)
        denominator = denominator + data[i] - lowestValue
    numerators.append(numerator)
    denominators.append(denominator)
    centersOfMass.append(1.0*numerator/denominator)

#print numerators
#print centersOfMass

if int(dumpRulerData) == 1:
    pickle.dump( centersOfMass, open( "AUTO_ruler.p", "wb" ) )

differences = []
#find the pixels per micron
for i in range(0,len(centersOfMass)-1):
    differences.append((centersOfMass[i+1] - centersOfMass[i]))

#plt.plot(differences,marker='o', linestyle='-')

arr001 = numpy.array(differences)

mean001 = numpy.mean(arr001)
std001 = numpy.std(arr001)
print 'mean of pixel values between strips',mean001
print 'std of pixel values between strips',std001

plotYvalues = []
stripNumber = []

if int(adjustToRuler) == 1:
    #load in the adjustment
    adjustmentList = pickle.load( open( adjustmentFile, "rb" ) )

    # we scan through the centers of mass and find which adjustment lists they are between
    newCentersInMicrons = []
    print 'number of centers of masses:',len(centersOfMass)

    firstFound = False
    firstDistance = 0


    for num,i in enumerate(centersOfMass):
        for j in range(0,len(adjustmentList)-1):
            if i >= adjustmentList[j] and i < adjustmentList[j+1]:

                distanceInMicrons = float(adjustmentSpacing)*j + float(adjustmentSpacing)*(i - adjustmentList[j])/(adjustmentList[j+1]-adjustmentList[j])
                newCentersInMicrons.append(distanceInMicrons)

                if(not firstFound):
                    firstFound = True
                    firstDistance = distanceInMicrons

                yValue = (distanceInMicrons - (num)*float(pitch) - firstDistance)
                stripNumber.append(num*float(Realpitch)/10000.)
                plotYvalues.append(yValue)


    arr = numpy.array(plotYvalues)

    mean = numpy.mean(arr)
    std = numpy.std(arr)
    print 'mean',mean
    print 'std',std

    for i,value in enumerate(plotYvalues):
        plotYvalues[i] = plotYvalues[i] - mean



else:
    print 'number of centers of masses:',len(centersOfMass)

    firstFound = False
    firstDistance = 0

    for i in range(len(centersOfMass)-1):
        differencesInMicrons = ((centersOfMass[i+1]-centersOfMass[i])-float(pitch)/float(micronsPerPixel))*float(micronsPerPixel)
        distanceInMicrons = (centersOfMass[i])*float(micronsPerPixel)

        if(not firstFound):
            firstFound = True
            firstDistance = distanceInMicrons

        yValue = (distanceInMicrons - (i)*float(pitch) -firstDistance)

        stripNumber.append(i*float(Realpitch)/10000.)
        plotYvalues.append(yValue)
        #plotYvalues.append(differencesInMicrons)






plt.plot(stripNumber, plotYvalues, marker='o', linestyle='-')



plt.ylabel('Strip location vs. ideal (microns)')
plt.xlabel('Strip location (cm)')

plt.savefig('plot.png')

#plt.ylabel('Ruler Grade location minus calculated location (microns)')
#plt.xlabel('Ruler grade # in 1/64th inches')

plt.show()








