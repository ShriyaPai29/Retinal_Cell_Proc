from matplotlib import pyplot as plt
import scipy.io as sio
import numpy as np
import re
import os

matlabDir = str(input("Please enter the directory path of *.mat file with avg_PSTH: "))

mat = sio.loadmat(str(matlabDir))
a = np.array(mat['avg_psth'])

classificationFile = str(input("Please enter the name of classification *.txt file: "))

indexValue = open(str(classificationFile), 'r') #like 'kilosort2.classification.txt'
classification = indexValue.readlines()

inputCellType = str(input("Please enter one or more cell types separated by commas(amacrine, OffP, OnP, OffM, OnM, OffS, OnS, S, BT): "))

print("At the end, manually analyze the figures in each folder and keep the 'good' ones in a separate folder named 'good' in order to run template generation.")
newCellType = inputCellType.split(",")

for cell in newCellType:
    cellDir = "All/" + str(cell) + "/"

    cwd = os.getcwd()
    newCwd = re.sub(r"\\", "/", cwd)
    newCwd = newCwd + "/" + str(cell) + "/"
    if not os.path.exists(newCwd):
        os.makedirs(newCwd)

    values = range(2300)
    spikeData = []
    x_values = []
    sortIndex = []

    for num in classification:
        num = num.strip('\n')
        x = num.split()
    
        if x[1] == str(cellDir): 
            sortIndex.append(int(x[0]))
        
    b = np.array(mat['cluster_id'])

    cellValues = []
    listValues = []
    indexVal = 0

    for s in b:
        cellValues.append(s)

    for i in cellValues[0]:
        listValues.append(i)

    def valueToIndex(value):
        indexVal = listValues.index(value)+1
        return indexVal

    countElse = 0
    finalIndex = []
    for j in range(len(sortIndex)):
        for k in range(len(listValues)):
            if sortIndex[j] == listValues[k]:
                finalIndex.append(valueToIndex(sortIndex[j]))
            
            else:
                countElse = countElse+1

    spikeData = []
    for h in range(len(finalIndex)):
        for m in values:
            spikeData.append([a[finalIndex[h]-1,m]])
            x_values += [m]
        
        plt.figure()
        plt.plot(x_values, spikeData)
        plt.grid()
        plt.xlabel("Time (s)")
        plt.ylabel("Firing Rate (Hz)")
        plt.title("Average Spike Rate of Retinal Cell Index " + str(finalIndex[h]))
        plt.ylim(0,250)
        plt.xlim(0,2300)

        spikeData = []
        x_values = []

        save_results_to = str(newCwd)
        plt.savefig(save_results_to + 'index_' + str(finalIndex[h]) + '.png') 

