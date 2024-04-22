from argparse import ArgumentParser
from SA import SA
from HC import HC
from FPTAS import FPTAS
from BnB import BnB

def main():
    parser = ArgumentParser()
    parser.add_argument('-inst', type=str, default='.\\DATA\\DATASET\\small_scale\\small_1', help='instance (default: small-1)')
    parser.add_argument('-alg', type=str, default='BnB', help='algorithm [BnB|DP|HC|SA]')
    parser.add_argument('-time', type=float, default=20, help='cutoff time')
    parser.add_argument('-seed', type=int, default=1, help='random seed')

    args = parser.parse_args()
    inputFile = args.inst
    alg = args.alg
    cutoff = args.time
    seed = args.seed
    if alg == 'BnB':
        agent = BnB(inputFile, cutoff)
        agent.runBnB()
    elif alg == 'FPTAS':
        agent = FPTAS(inputFile, cutoff)
        agent.runFPTAS()
    elif alg == 'HC':
        agent = HC(inputFile, cutoff, seed)
        agent.run_HC()
    elif alg == 'SA':
        agent = SA(inputFile, cutoff, seed)
        agent.runSA()
    else:
        print("Please input a legal algorithm: [BnB|DP|HC|SA]")





if __name__ == "__main__":
    main()
