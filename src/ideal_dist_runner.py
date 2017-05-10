from runner import *
from network import *

Ts = range(10, 10000, 1000)
S = 16
N = 1000

processes = []

for T in Ts:
    alpha = 1.5
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(1.5, items), 1.0, 0.0, fout))

    alpha = 1.6
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(1.6, items), 1.0, 0.0, fout))

    alpha = 1.7
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(1.7, items), 1.0, 0.0, fout))

    alpha = 1.8
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(1.8, items), 1.0, 0.0, fout))

    alpha = 1.9
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(1.9, items), 1.0, 0.0, fout))

    alpha = 2.0
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(2.0, items), 1.0, 0.0, fout))

    alpha = 2.1
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(2.1, items), 1.0, 0.0, fout))

    alpha = 2.2
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(2.2, items), 1.0, 0.0, fout))

    alpha = 2.3
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(2.3, items), 1.0, 0.0, fout))

    alpha = 2.4
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(2.4, items), 1.0, 0.0, fout))

    alpha = 2.5
    fout = "ideal_dist_%d_%f.txt" % (T, alpha)
    processes.append(create_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.5, items), lambda items : ZipfDistribution(2.5, items), 1.0, 0.0, fout))

for p in processes:
    p.start()

for p in processes:
    p.join()
