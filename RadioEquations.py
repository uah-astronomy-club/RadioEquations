"""
RadioEquations.py

Equations from the paper 'SRT Paper (2010)' converted to Python as well as data formatting code

@author: Ben Puckett
"""

import matplotlib.pyplot as plt
import math

# Velocity of source with respect to the velocity of the local standard
def VELOCITY_CALC(f, V_lsr):
    
    # V_lsr is the velocity local standard of rest
    return c * ((1420.4 - f) / 1420.4) - V_lsr

# Constants
c = 3.00 * (10^8) # Speed of light (in m/s)

# Input Values
T_Sys = 200 # Test T_SYS Value (in K)
Outlier_Percentage = 0.05; # Percentage of data to be removed

# Enter file directory and name of the file (with extension) using forward slash instead of backslash.
fileDirectory = "ENTER FILE DIR"
dateTest = 'ENTER TEST DATE'

binDataDictionary = {}
freqSpaceDataDictionary = {}
velDataDictionary = {}

freqSpaceDataDictionary_RAW = {}

# Open Data File
dataLines = ''
with open(fileDirectory, 'r') as data:
    dataLines = data.readlines()
    
if dataLines != '':
    
    binSum = []
    binSum_RAW = []

    dataLineCount = 0
    for line in dataLines:
        # Remove excess spaces in the data
        lineInput = ' '.join(line.split())
        
        # Convert the line string to data list
        lineData = lineInput.split()

        # Check for comment line
        if lineData[0] == '*':
            continue
        
        # DATA STORAGE
        else:
            
            # Data Timestamp
            date = lineData[0]
            
            # Data Bin Count
            binCount = int(lineData[8]) # Number of data points
            print('Bin Count: ' + str(binCount))
            
            # Frequency Space
            centerFreq = float(lineData[5]) # Center Frequency
            freqSpacing = float(lineData[6]) # Frequency spacing
            
            # VSLR
            vslr = float(lineData[-1])
            
            # DATA
            freqBinData = {}
                        
            # Calculations
            freqStart = centerFreq - ((binCount / 2) * freqSpacing)
            freqSpace = []
            velocity = []
            binSumDict = {}
            for binID in range(0,binCount):
                
                freqBin = float(lineData[binID+9]) - T_Sys
                                
                # Calculate RAW binSum
                if len(binSum_RAW) < binCount:
                    binSum_RAW.append(freqBin)
                else:
                    binSum_RAW[binID] += freqBin

                
                # Add the bin data
                freqBinData[binID] = freqBin
                
                # Build the frequency space
                currentFreq = freqStart + (binID * freqSpacing)
                freqSpace.append(currentFreq)
                
                # Calculate Velocity
                velocity.append(VELOCITY_CALC(currentFreq, vslr))
                        
            freqSpaceDataDictionary_RAW[date] = freqSpace.copy()
                
            # Remove outliers
            sortedBinData = {k: v for k, v in sorted(freqBinData.items(), key=lambda item: item[1])}
            sortedBinSumData = binSum
                        
            outlierDataAmount_Half = math.floor((Outlier_Percentage * binCount / 2))
            
            removedOutlierData = sortedBinData
            removedLowerIndex = 0
            removedUpperIndex = binCount - 1
            
            for i in range(0, outlierDataAmount_Half):
                
                # Remove Lower Data
                removedOutlierData.pop(i)
                del freqSpace[i]
                removedLowerIndex += 1
                                
                # Remove Upper Data
                removedOutlierData.pop((binCount - 1) - i)
                del freqSpace[len(freqSpace) - 1]
                removedUpperIndex -= 1

            # Set the new value for binCount
            binCount -= 2 * outlierDataAmount_Half
            
            # Sort based on binID
            sortedBinData = {k: v for k, v in sorted(removedOutlierData.items(), key=lambda item: item[0])}

            # Calculate the bin sums
            for binID in range(removedLowerIndex,removedUpperIndex):
                                
                if len(binSum) < binCount:
                    binSum.append(sortedBinData[binID])
                else:
                    binSum[binID - removedLowerIndex] += sortedBinData[binID]
                                                
            # Store the bin data
            binDataDictionary[date] = sortedBinData

            # Store the frequency space data
            freqSpaceDataDictionary[date] = freqSpace

            # Store the velocity data
            velDataDictionary[date] = velocity

        dataLineCount += 1
            
# Print the number of data lines
print('Number of data lines: ' + str(dataLineCount))

# Plot
#TO-DO: Add descriptions, titles, and legends for the plots

fig, ax = plt.subplots(2)
fig.set_figheight(15)
fig.set_figwidth(20)
plt.ticklabel_format(useOffset=False)

ax[0].plot(freqSpaceDataDictionary_RAW[dateTest], binSum_RAW)

print(freqSpaceDataDictionary[dateTest][0])

ax[1].plot(freqSpaceDataDictionary[dateTest], binSum)
plt.savefig('test.pdf')

#ax[1].plot(velDataDictionary[dateTest], binSum)
#ax[2].plot(freqSpaceDataDictionary[dateTest], list(binDataDictionary[dateTest]))







