import json
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy import polyfit, polyval

def extract_id(data):
    #JSON file is required to run this code
    timelist = []
    idlist = []
    for sample in data['fittslaw']:
        t = sample['time']
        d = sample['distance']
        w = sample['width']
        id1 = math.log((d / w) + 1, 2)
        timelist.append(t)
        idlist.append(id1)
    return (idlist, timelist)

def main():
    #data.json is required to run this code 
    with open('data.json') as f:
        data = json.load(f)

    # Extract (ID, time) points from data
    points = extract_id(data)

    coeff = polyfit(points[0], points[1], 1)

    x1 = min(points[0])
    x2 = max(points[0])
    y1 = polyval(coeff, x1)
    y2 = polyval(coeff, x2)

    # Throughput (IP) = (ID/MT)
    throughput = ([], [])
    for i in range(len(points[0])):
        id1 = points[0][i]
        t = points[1][i]
        through = id1 * 1000 / t
        throughput[1].append(through)
        throughput[0].append(id1)
        

    #Plotting of the two graphs
    plt.figure(num="Samples")
    plt.xlabel("Index of Difficulty")
    plt.ylabel("Movement Time (msS)")
    plt.xlim(0, max(points[0]) * 1.2)
    plt.ylim(0, max(points[1]) * 1.2)
    plt.plot(points[0], points[1], "bo", label="Samples")
    plt.plot([x1,x2], [y1, y2], "r-")
    
    plt.figure(num="Throughput")
    plt.xlabel("Index of Difficulty")
    plt.ylabel("Throughput (bits/s)")
    plt.xlim(0, max(throughput[0]) * 1.2)
    plt.ylim(0, max(throughput[1]) * 1.2)
    plt.plot(throughput[0], throughput[1], "yo", label="Throughput")
    
    print("Regression coefficients: A={}, B={}".format(coeff[0] / 1000, coeff[1] / 1000))
    plt.show()

if __name__ == '__main__':
    main()
