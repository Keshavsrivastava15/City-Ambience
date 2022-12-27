import pandas as pd
import numpy as np


df = pd.read_csv('noapi.csv', index_col=0)
df.drop(df.index, inplace=True)
print(df)

