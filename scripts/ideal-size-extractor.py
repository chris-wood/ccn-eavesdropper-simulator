import sys

for fname in sys.argv[1:]:
    with open(fname, "r") as fh:
        distance = fh.readline()
        mp = float(fh.readline())

        data = fname.replace(".txt","").split("_")
        N = int(data[-1])
        T = int(data[-2])

        print "%d,%d,%f" % (N, T, mp)
