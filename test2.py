import numpy as np
import pandas as pd

df = pd.DataFrame(np.arange(3*4).reshape(3,4), index=['a','b','c'])
df = df.loc['a',0]
print(df)