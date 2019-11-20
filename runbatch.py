import pandas as pd
import random

from model import WhaleModel
from mesa.batchrunner import BatchRunnerMP

fixed_params = {}
variable_params = {"mate_choice": [None, "Male", "Female"], "grandmother_effect": [True, False]}

# fixed_params = {"mate_choice": None}
# variable_params = {"grandmother_effect": [True, False]}

def get_data_collector(model):
    return model.datacollector

batch_run = BatchRunnerMP(WhaleModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=10,
                        max_steps=10000,
                        model_reporters={"data": get_data_collector},
                        display_progress=True,
                        nr_processes=4)
batch_run.run_all()

# all_dfs = {x:[] for x in variable_params["mate_choice"]} #key = mate_choice; value = list of dataframes with that mate_choice

# run_data = batch_run.get_model_vars_dataframe()

# for index, row in run_data.iterrows():
#     df = pd.DataFrame.from_dict(row["data"].model_vars)
#     all_dfs[row["mate_choice"]].append(df)

# data = {}

# for k, v in all_dfs.items():
#     data[k] = pd.concat(v, keys=list(range(len(v))), names=["Run", "Time"])
#     data[k].to_csv("data/{}.csv".format(k))
