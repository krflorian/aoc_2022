#%%

test = {"asdf": 1, "qwer": 2}

new_test = test
new_test["asdf"] += 100

test


#%%
import pandas as pd


data = pd.DataFrame({"id": ["a", "b", "c"], "value": [100, 100, 100]})
data

#%%

filtered_data = data.iloc[0]
filtered_data["value"] += 300

#%%

data

#%%

import numpy as np

dfc = pd.DataFrame(
    {"a": ["one", "one", "two", "three", "two", "one", "six"], "c": np.arange(7)}
)


dfd = dfc

# Setting multiple items using a mask
mask = dfd["a"].str.startswith("o")

dfd.loc[mask, "c"] = 42

dfd

#%%

dfc
