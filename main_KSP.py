from argparse import ArgumentParser
from SA import SA
from HC import HC
from FPTAS import FPTAS
from BnB import BnB
import matplotlib.pyplot as plt
import os
import numpy as np
from pathlib import Path
def QRTD_SQD(solFile, traceFileFolder):
    file2 = open(solFile, 'r')
    Lines2 = file2.readlines()
    OPT = float(Lines2[0])
    dirname = traceFileFolder
    data = []
    for files in os.listdir(dirname):
        if files.endswith('trace'):
            f = open(os.path.join(dirname, files))
            Lines = f.readlines()
            Lines = [list(map(float, line.split(','))) for line in Lines]
            data.append(Lines)

    n = len(data)
    tt, costs = np.split(np.array(data[0]), 2, axis=1)
    tt = tt.flatten()
    costs = costs.flatten()
    RelErr = abs((costs - OPT) / OPT)
    mint, maxt = min(tt), max(tt) + 1
    minE, maxE = min(RelErr), max(RelErr)
    row, col = 5, 5  # row is the relative error, col is the time
    t = np.linspace(mint, maxt, col)
    Re = np.linspace(minE, 0.1, row)
    Psolved = np.zeros((row, col)) # the probability
    for i in range(n):
        tt, costs = np.split(np.array(data[i]), 2, axis=1)
        tt = tt.flatten()
        costs = costs.flatten()
        RelErr = abs((costs-OPT)/OPT)
        for j in range(len(costs)):
            for i1 in range(row):
                for i2 in range(col):
                    if RelErr[j] <= Re[i1] and tt[j] <= t[i2]:
                        Psolved[i1][i2] += 1
    for i in range(len(Psolved)):
        for j in range(len(Psolved[0])):
            Psolved[i][j] = min(1, Psolved[i][j]/n)
    plt.figure(1)
    plt.xscale("log")
    for i in range(len(Re)):
        plt.plot(t, Psolved[i], '-o', label='RelErr = {:.2f}'.format(Re[i]))
    plt.xlabel('Time [s]')
    plt.ylabel('Probability of obtaining solutions')
    plt.title('QRTD')
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(2)
    for i in range(len(t)):
        plt.plot(Re, Psolved[:][i], '-o', label='CutoffTime = {:.2f}'.format(t[i]))
    plt.xlabel('Relative error')
    plt.ylabel('Probability of obtaining solutions')
    plt.legend()
    plt.title('SQD')
    plt.grid()
    plt.show()
def boxPlot(TimeFile):
    file = open(TimeFile, 'r')
    Lines= file.readlines()
    time_all = [list(map(float, line.split())) for line in Lines]
    plt.boxplot(time_all)

def main():
    parser = ArgumentParser()
    parser.add_argument('-inst', type=str, default='.\\DATA\\DATASET\\small_scale\\small_1', help='instance (default: small-1)')
    parser.add_argument('-alg', type=str, default='BnB', help='algorithm [BnB|FPTAS|HC|SA]')
    parser.add_argument('-time', type=int, default=20, help='cutoff time')
    parser.add_argument('-seed', type=int, default=1, help='random seed')

    args = parser.parse_args()
    inputFile = args.inst
    alg = args.alg
    cutoff = int(args.time)
    seed = args.seed
    LS_plot = False  # whether plot the QRTD and SQD plot for large scale 1 and large scale 3
    root_dir = Path(inputFile).resolve().parent.parent
    solFile = os.path.join(root_dir, os.path.split(Path(inputFile).resolve().parent)[1]+'_solution')
    traceDir = ''     # the directory where you stored your trace files with at least 20 runs
    timeFile = ''     # the file which log the time of each run of hill climbing and simulated annealing
    if alg == 'BnB':
        agent = BnB(inputFile, cutoff)
        agent.runBnB()
    elif alg == 'FPTAS':
        agent = FPTAS(inputFile, cutoff)
        agent.runFPTAS()
    elif alg == 'HC':
        agent = HC(inputFile, cutoff, seed)
        agent.run_HC()
        if LS_plot==True:
            QRTD_SQD(solFile, traceDir)
            boxPlot(timeFile)
    elif alg == 'SA':
        agent = SA(inputFile, cutoff, seed)
        agent.runSA()
        if LS_plot==True:
            os.makedirs(os.path.dirname(traceDir), exist_ok=True)
            QRTD_SQD(solFile, traceDir)
            boxPlot(timeFile)
    else:
        print("Please input a legal algorithm: [BnB|FPTAS|HC|SA]")

if __name__ == "__main__":
    main()
