import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

data = {}

def header_to_keys(header):
    if "u_u" in header:
        return "u", "u"
    if "z_u" in header:
        return "z", "u"
    if "z_z" in header:
        return "z", "z"

def parse_output(fnames):
    global data

    for fname in fnames:
        with open(fname, "r") as fh:
            distance = float(fh.readline())
            percentage = float(fh.readline())
            cdf_tuples = eval(fh.readline())

            data[fname] = (distance, percentage, cdf_tuples)

def header_to_fname(header):
    return header.replace(" ", "_").replace("?","")

parse_output(sys.argv[1:])

def generate_plot_from_pairs(source, pairs):
    fig, ax = plt.subplots()
    distances = map(lambda p : p[0], pairs)
    values = map(lambda p : p[1], pairs)

    num_values = len(values)

    fit = np.polyfit(distances, values, 1)
    fit_fn = np.poly1d(fit)
    rect = plt.plot(distances, values, "ro", distances, fit_fn(distances), "--k") #, markevery=int(num_values * 0.1)) # log=True

    ax.set_ylabel('Match Correctness [%]')
    ax.set_xlabel('Auxiliary Distribution Distance')
    dds = np.arange(min(distances), max(distances) + 0.000001, 0.1)
    labels = map(lambda d : "%.3f" % d, dds)
    plt.xticks(dds, labels, rotation="vertical")
    plt.grid(True)
    plt.subplots_adjust(bottom=0.15)

    print >> sys.stderr, "Plotting %s" % (source)

    plt.savefig("mp_" + source + '.pdf')
    plt.close()

# Generate a plot that shows the MP based on the distance from
# the uniform distribution (adv. has no information)
def generate_uniform_plot(data):
    pairs = []
    for i, header in enumerate(data):
        source, aux = header_to_keys(header)
        if "z" in source and "u" in aux:
            (distance, percentage, cdf_tuples) = data[header]
            pairs.append((float("%.5f" % float(distance)), float("%.5f" % float(percentage))))

    print pairs
    generate_plot_from_pairs("uniform", pairs)
    return # there's only one uniform plot

# Generate a plot that is based on the statistical distance between all
# Zipf variants (adv. has good information)
def generate_zipf_plot(data):
    pairs = []
    for i, header in enumerate(data):
        source, aux = header_to_keys(header)
        if "u" not in source and "u" not in aux:
            (distance, percentage, cdf_tuples) = data[header]
            pairs.append((float("%.5f" % float(distance)), float("%.5f" % float(percentage))))

    print pairs
    generate_plot_from_pairs("zipf", pairs)

generate_uniform_plot(data)
# generate_zipf_plot(data)
