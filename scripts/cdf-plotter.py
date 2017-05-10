import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def header_to_fname(header):
    return header.replace(" ", "_").replace("?","")

data = {}

def parse_output(fname):
    global data

    with open(fname, "r") as fh:
        while True:
            distance = float(fh.readline())
            percentage = float(fh.readline())
            cdf_tuples = eval(fh.readline())
            data[fname] = (distance, percentage, cdf_tuples)
            break

for i in sys.argv[1:]:
    parse_output(i)

# Generate the CDF plot
for i, header in enumerate(data):
    fig, ax = plt.subplots()
    (distance, percentage, cdf_tuples) = data[header]
    num_values = len(cdf_tuples)
    values = cdf_tuples
    indices = np.arange(num_values)

    width = 0.9
    rect = plt.plot(indices, values, linestyle='--', marker='o') #, markevery=int(num_values * 0.01)) # log=True

    ax.set_ylabel('Percentage Correct [%]')
    ax.set_xlabel('Content Rank')
    #ax.set_xticks(indices + width)
    #ax.set_yscale('log')
    #ax.set_xticklabels(tuple(map(lambda s : "{:.1e}".format(s), sizes)))
    #ax.legend((rects1[0], rects2[0]), ('SCR', 'IPBC'), loc=2)

    plt.grid(True)
    # plt.show()
    plt.savefig(header_to_fname(header) + '_cdf.pdf')
    plt.close()
    # sys.exit(1)
