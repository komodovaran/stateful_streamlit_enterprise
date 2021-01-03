from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = Path(f"~/Desktop/test").expanduser()
path.mkdir(exist_ok=True)

for i in range(10):
    slope = int(np.random.randint(50, 150, 1))
    noise_max = int(np.random.randint(1, 5, 1))

    noise = np.random.normal(0, noise_max, 100)

    ypts = np.random.normal(0, 15, 100) + np.linspace(0, slope, 100)
    xpts = np.linspace(0, 1, 100)

    plt.plot(xpts, ypts, alpha=0.5, color="black")

    filepath = path / f"test_file_{i}.csv"
    pd.DataFrame({"x": xpts, "y": ypts}).to_csv(filepath)

plt.title(f"Generated files in {path}")
plt.show()
