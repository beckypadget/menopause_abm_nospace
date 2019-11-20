import glob
import pandas as pd
import sys

listing = glob.glob("Data/{}_*.csv".format(sys.argv[1]))
print(listing)

dfs = {}

for filepath in listing:
    run_number = int(filepath.split(sep = '_')[-1][:-4])
    dfs[run_number] = pd.read_csv(filepath)

pd.concat(dfs).to_csv("Data/combined_{}.csv".format(sys.argv[1]))