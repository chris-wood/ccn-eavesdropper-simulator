import sys

for fname in sys.argv[1:]:
    with open(fname, "r") as fh:
        print >> sys.stderr, fname
        distance = float(fh.readline())
        mp = float(fh.readline())

        data = fname.replace(".txt","").split("_")
        T = int(data[-2])

        print "%f,%d,%f" % (distance, T, mp)
