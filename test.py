

import numpy as np

a = np.array([
    [1, 0, 0],
    [0, 4, 0],
    [0, 0, 0],
    [4, 3, 0],
    [2, 3, 4]
])

ex = [1, 4]

a = np.delete(a, ex, axis=0)
print(a)
