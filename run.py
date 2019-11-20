from model import WhaleModel
from tqdm import tqdm
import settings

#  Multiple runs
for i in range(30):
    whale_model = WhaleModel(100, i) # initialise a model with (n) whales
    for j in tqdm(range(settings.steps)): # run model for (x) steps
        whale_model.step()
    whale_model.write_data("fem_gran_{}".format(i))

# # Single run
# whale_model = WhaleModel(100) # initialise a model with (n) whales
# for i in tqdm(range(settings.steps)): # run model for (x) steps
#     whale_model.step()
