import json
import math
import pandas as pd

def extract_id(data):
    tlist = []
    dlist = []
    for sample in data['fittslaw']:
        t = sample['time']
        amp = sample['amplitude']
        width = sample['width']
        id1 = math.log((amp / width) + 1, 2)
        tlist.append(t)
        dlist.append(id1)
    return (dlist, tlist)

def main():
    # Load JSON
    with open('data.json') as f:
        data = json.load(f)

    # Extract (ID, time) points from data
    points = extract_id(data)

    # Fit line onto points
    coeff = polyfit(points[0], points[1], 1)

    # Calculate endpoints of line for drawing the line
    x1 = min(points[0])
    x2 = max(points[0])
    y1 = polyval(coeff, x1)
    y2 = polyval(coeff, x2)

    # Calculate throughput points (ID/time)
    throughput = ([], [])
    for i in range(len(points[0])):
        id1 = points[0][i]
        t = points[1][i]
        through = id1 * 1000 / t
        throughput[1].append(through)
        throughput[0].append(id1)
        
    # Calculate the ID/MT points. Sort by x-axis. Plot.

    # Draw everything
    plt.figure(num="Samples")
    plt.xlabel("Index of Difficulty")
    plt.ylabel("Movement Time (ms)")
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
