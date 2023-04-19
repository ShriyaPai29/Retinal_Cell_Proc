import os
import numpy as np
import re
import scipy.io as sio
import pandas as pd
from matplotlib import pyplot as plt

classificationFile = str(input("Please enter the name of classification *.txt file: "))
indexValue = open(str(classificationFile), 'r') #like 'kilosort2.classification.txt'
classification = indexValue.readlines()

values = range(2300)

matlabDir = str(input("Please enter the directory path of *.mat file with avg_PSTH: "))
mat = sio.loadmat(str(matlabDir))
a = np.array(mat['avg_psth'])
inputCellType = str(input("Please enter the cell type(s) that have been sorted. Separate by commas(amacrine, OffP, OnP, OffM, OnM, OffS, OnS, S, BT): "))
#Note: Manually analyze the figures in each folder and keep the "good" ones in a separate folder named "good"
newCellType = inputCellType.split(",")

for cell in newCellType:
    cwd = os.getcwd()
    newCwd = re.sub(r"\\", "/", cwd)
    newCwd = newCwd + "/" + str(cell) + "/good/"
    dir_list = os.listdir(newCwd)
    cellList = str(dir_list)
    index = re.findall(r'[0-9]+', cellList)

    indexArray = []
    psthValuesArray = []
    psthValues = 0
    avgPsthValues = 0
    count = 0

    for j in values:
        for i in index:
            psthValues += a[int(i)-1,j]
            count += 1
        avgPsthValues = psthValues/count
        psthValuesArray.append(avgPsthValues)
        psthValues = 0
        count = 0
        avgPsthValues = 0

    plt.figure()
    plt.plot(values, psthValuesArray)
    plt.grid()
    plt.xlabel("Time (s)")
    plt.ylabel("Firing Rate (Hz)")
    plt.title("Average Spike Rate of " + str(cell) + " Retinal Cell")
    plt.ylim(0,175)
    plt.xlim(0,2300)

    if not os.path.exists(newCwd):
        os.makedirs(newCwd)
    save_results_to = str(newCwd)
    plt.savefig(save_results_to + 'Template_of_' + str(cell) + '.png')

