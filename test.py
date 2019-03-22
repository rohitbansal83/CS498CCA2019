

import numpy as np

a = np.array([
    [1, 0, 0],
    [0, np.nan, 0],
    [0, 0, 0],
    [np.nan, np.nan, np.nan],
    [2, 3, 4]
])

mask = np.isnan(a).any(axis=1)
a = a[~mask]
idx = [0, 2]
print(a)
print(a[:, idx])
