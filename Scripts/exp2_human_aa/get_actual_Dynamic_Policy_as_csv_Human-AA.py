
"""This script takes in raw human-AA data and outputs the binary encoded TSp vectors for each timestep per trial."""

import os # for directories
from pathlib import Path # path functions
import pandas as pd
import numpy as np
import sys
from tqdm import trange

# Add parent Scripts directory to path for importing tools module
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(script_dir)
sys.path.insert(0, scripts_dir)

from tools.utils import get_chaser_v2, get_num_targets

num_HAs = 2
max_TAs = 5



def dist(X,Y):
    # X and Y are 2D points
    # returns the Euclidean distance between the two points
    return ((X[0]-Y[0])**2 + (X[1]-Y[1])**2)**0.5


"""given a trial and a session, this function will output the observed target run order, 
   calculated every decision_delay seconds, from the real human subject data or from the simulation data. 
   It then saves the run order to a file called run_order.csv."""
def get_actual_Dynamic_Policy_as_csv(trial, trialData):
    skip_freq = 1# int(decision_delay / trialDeltaTime) #number of rows to skip to get the desired decision delay
    num_rows_output = int((len(trialData) / skip_freq)) #number of rows in output array
    output_array = np.zeros((num_rows_output,13)) - 1
    numTargets = get_num_targets(trialData, maxTargets)

    ################################################################################

    #loop through all rows of trialData, skipping by skip_freq
    for i in range(0, num_rows_output):
        # first just get which TA is running at given point of time
        trialDataIdx = i * skip_freq 
        observedOrder = np.zeros((numHerders, maxTargets),dtype=int)
        # for each herder, get the target they are running at the given time
        # if they are not running a target, keep 0
        # if they are running a target, get the target ID    
        tcolsRun = ['t%drun' % (t) for t in range(0, numTargets)] #list of column names for targets running
        whoIsRunning = [trialData[tcolRun][trialDataIdx] for tcolRun in tcolsRun] #list of which targets are running
        for tidx, targetRunning in enumerate(whoIsRunning): 
            if targetRunning: #if target is indeed running
                #get the herder running that target
                chasingHerderID = get_chaser_v2(trialData.iloc[trialDataIdx], tidx) #get the herder chasing that target
                for herderID in range(0, numHerders):
                    if chasingHerderID[herderID]:
                        observedOrder[herderID, tidx] = 1
        output_array[i] = [trialData.iloc[trialDataIdx].time, trial, numTargets, *observedOrder[0,:], *observedOrder[1,:]]
    return pd.DataFrame(data=output_array, columns = columns)

def get_closest_HA_TA_pair(trialData, i, player):
    #we will get the HA and TA pair that are closest to each other, in the case that more than one TA is engaged with the HA
    #trialData is the timeseries data for the current trial
    #i is the current index in the actual_dynamic_policy breakout point
    #player is the player we are looking at, 0 for player 0, 1 for player 1
    numTargs = get_num_targets(trialData, max_TAs)
    
    HAx = trialData.iloc[i][player+'x']
    HAz = trialData.iloc[i][player+'z']
    HA_TA_distances = np.zeros(numTargs) -1
    for j in range(numTargs):
        TAjx = trialData.iloc[i]['t'+str(j)+'x']
        TAjz = trialData.iloc[i]['t'+str(j)+'z']
        HA_TA_distances[j] = dist([HAx,HAz],[TAjx,TAjz])
    return np.argmin(HA_TA_distances)

def collapse_actual_dynamic_engagement(actual_dynamic_policy, trialData):
    
    # we are going to collapse the actual dynamic engagement policy into a single column
    # we will do this by creating a new column and filling it with the appropriate values

    # we will iterate through the rows of the actual_dynamic_policy and fill the new column with the appropriate values
    # we will start by creating a new column with the same length as the actual_dynamic_policy
    collapsed_policy = pd.DataFrame(columns=['time','TrialID','numTargs','p0_engagement','hA0_engagement'])
    collapsed_policy['time'] = actual_dynamic_policy['time']
    collapsed_policy['TrialID'] = actual_dynamic_policy['TrialID']
    collapsed_policy['numTargs'] = actual_dynamic_policy['numTargs']
    collapsed_policy['p0_engagement'] = -1
    collapsed_policy['hA0_engagement'] = -1
    for idx, row in actual_dynamic_policy.iterrows():

        if [row['p0TA0'], row['p0TA1'], row['p0TA2'], row['p0TA3'], row['p0TA4']].count(1) > 1:
            #print("More than one TA is engaged with HA0")
            closest_TA = get_closest_HA_TA_pair(trialData, idx, player = 'p0')
            collapsed_policy.at[idx, 'p0_engagement'] = closest_TA
        # we will check if the HA is engaged with the TA
        elif row['p0TA0'] == 1:
            collapsed_policy.at[idx, 'p0_engagement'] = 0
        elif row['p0TA1'] == 1:
            collapsed_policy.at[idx, 'p0_engagement'] = 1
        elif row['p0TA2'] == 1:
            collapsed_policy.at[idx, 'p0_engagement'] = 2
        elif row['p0TA3'] == 1:
            collapsed_policy.at[idx, 'p0_engagement'] = 3
        elif row['p0TA4'] == 1:
            collapsed_policy.at[idx, 'p0_engagement'] = 4

        if [row['hA0TA0'], row['hA0TA1'], row['hA0TA2'], row['hA0TA3'], row['hA0TA4']].count(1) > 1:
            #print("More than one TA is engaged with HA1")
            closest_TA = get_closest_HA_TA_pair(trialData, idx, player = 'hA0')
            collapsed_policy.at[idx, 'hA0_engagement'] = closest_TA
        elif row['hA0TA0'] == 1:
            collapsed_policy.at[idx, 'hA0_engagement'] = 0
        elif row['hA0TA1'] == 1:
            collapsed_policy.at[idx, 'hA0_engagement'] = 1
        elif row['hA0TA2'] == 1:
            collapsed_policy.at[idx, 'hA0_engagement'] = 2
        elif row['hA0TA3'] == 1:
            collapsed_policy.at[idx, 'hA0_engagement'] = 3
        elif row['hA0TA4'] == 1:
            collapsed_policy.at[idx, 'hA0_engagement'] = 4

    return collapsed_policy

cwd = os.path.dirname(__file__) # current working directory
wd = Path(cwd).parents[1] # project working directory


numHerders = 2
maxTargets = 5
firstTrial = 7
lastTrial = 24 + 1 # +1 for python indexing
numTrials = lastTrial - firstTrial
numTargetArray = [3,4,5] # array of the possible number of targets in the experiment


columns = ["time","TrialID", "numTargs","p0TA0", "p0TA1", "p0TA2", "p0TA3", "p0TA4","hA0TA0", "hA0TA1", "hA0TA2", "hA0TA3", "hA0TA4"]
output_path = os.path.join(wd, "OtherResults", "Actual_Dynamic_Policies_HumanAA")


if not os.path.exists(output_path):
    os.mkdir(output_path)

AA_types = ["Heuristic"]  # Only Heuristic agent type used in this study
# create subpaths for each AA_type
for AA_type in AA_types:
    if not os.path.exists(os.path.join(output_path, AA_type)):
        os.mkdir(os.path.join(output_path, AA_type))
        # create subpaths for each player
    for subFolder in ["HumanPlayer0", "HumanPlayer1"]:
        if not os.path.exists(os.path.join(output_path, AA_type, subFolder)):
            os.mkdir(os.path.join(output_path, AA_type, subFolder))

#access all sessions in Human-AA where you go over both player 0 and player 1


for trial in trange(firstTrial, lastTrial): #loop over all relevant trials
    trial_ID = "{:02}".format(trial)
    for subFolder in ["HumanPlayer0", "HumanPlayer1"]: #make sure you treat all trials, where the human is player 0 and player 1 both
        for AA_type in AA_types: #loop over all the different AAs
            expDir = os.path.join(wd, 'RAW_EXPERIMENT_DATA', 'HUMAN-AA_TEAM', AA_type)
            expFiles = [path for path in Path(os.path.join(expDir, subFolder)).rglob('*trialIdentifier'+trial_ID+'*')]
            for expFile in expFiles:
                trialData = pd.read_csv(expFile)
                dynamicPolicyTimeSeries = get_actual_Dynamic_Policy_as_csv(trial, trialData) #0 and 1 encoded HA-TA engagement

                output_filename = "trialIdentifier_"+str(trial) + ".csv" #one file per trial
                session_name = Path(expFile).parent.parent.name

                #make a folder for each session
                session_folder = os.path.join(output_path, AA_type, subFolder, session_name)
                if not os.path.exists(session_folder):
                    os.mkdir(session_folder)


                collapsedDynamicPolicyTimeSeries = collapse_actual_dynamic_engagement(dynamicPolicyTimeSeries, trialData)

                collapsedDynamicPolicyTimeSeries.to_csv(os.path.join(session_folder, output_filename), index=False)