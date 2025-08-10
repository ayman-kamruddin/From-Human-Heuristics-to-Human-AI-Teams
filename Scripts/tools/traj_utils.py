"""Function definitions for performing trajectory analyses
1) Weighted and binary heatmaps and traces
2)t-test and BF10 calculation on traces
3) Potentially plotting the heatmaps
"""

import numpy as np
from .utils import trace

#binning size for 2-D histograms
bin_size = 5

#field dimensions
xlim = 60
ylim = 45

#threshold for binary heatmap
threshold =10



"""Function to calculate the binary trace for a given trial for one given trajectory
Inputs:
X: np.array of human x-coordinates for all players
Z: np.array of human z-coordinates for all players
individialData: pd.DataFrame of data for one given trajectory set
agent: string, "hA0" or "p0" for human or simulated data. Used for file dataframe headers
Output:
traces: np.array of traces for the given trial for the given trajectory set
"""
def get_binary_trace(X, Z, individialData, agent):
    h, _, _ = np.histogram2d(x = X.flatten(), y = Z.flatten(),  bins = (int(120/bin_size), int(90/bin_size)), range = ((-xlim, xlim), (-ylim,ylim)))
    weighted_heatmap = np.sqrt((h.T[::-1]))
    binary_heatmap = weighted_heatmap > threshold
    binary_trace = trace(binary_heatmap, np.array([individialData[agent+'x'].to_numpy(), individialData[agent+'z'].to_numpy()]).T, bin_size = bin_size, xlim = xlim, ylim = ylim)
    return binary_trace
