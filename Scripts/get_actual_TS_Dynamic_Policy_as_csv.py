"""This script gives the actual TS Dynamic Policy as a csv file for each trial in the experiment.
It takes either the raw human-human experimental timeseries data, or the simulated AA-AA data as input,
and outputs the binary-encoded actual TS Dynamic Policy as a csv file for each trial in the experiment (or the simulation).
The output csv file has the following columns:
    - time: the time at which the data was recorded
    - TrialID: the trial number
    - HA0_engagement: the TA that HA0 is engaging with at that time. If there are more than one targets, the TA that HA0 is engaging with is the one that is closest to HA0.
    - HA1_engagement: the TA that HA1 is engaging with at that time. If there are more than one targets, the TA that HA1 is engaging with is the one that is closest to HA1.
    - numTargs: the number of targets in the trial
"""
import os # for directories
from pathlib import Path # path functions
import pandas as pd
from tools.utils import get_chaser, get_num_targets # for project-specific custom functions
import numpy as np
from tqdm import tqdm, trange

max_TAs = 5 # maximum number of targets in the experiment

wd = Path(os.path.dirname(os.path.realpath(__file__))
              ).parents[0] # project working directory


output_path = os.path.join(wd, "OtherResults", "TS_Dynamic_Policy")

def dist(X,Y):
    # X and Y are 2D points
    # returns the Euclidean distance between the two points
    return ((X[0]-Y[0])**2 + (X[1]-Y[1])**2)**0.5

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
                chasingHerderID = get_chaser(trialData.iloc[trialDataIdx], tidx, simulation_bool=simulation_bool) #get the herder chasing that target
                for herderID in range(0, numHerders):
                    if chasingHerderID[herderID]:
                        observedOrder[herderID, tidx] = 1
        output_array[i] = [trialData.iloc[trialDataIdx].time, trial, numTargets, *observedOrder[0,:], *observedOrder[1,:]]
    return pd.DataFrame(data=output_array, columns = columns)


def collapse_actual_dynamic_engagement(actual_dynamic_policy, trialData):
    
    # we are going to collapse the actual dynamic engagement policy into a single column
    # we will do this by creating a new column and filling it with the appropriate values

    # we will iterate through the rows of the actual_dynamic_policy and fill the new column with the appropriate values
    # we will start by creating a new column with the same length as the actual_dynamic_policy

    collapsed_policy = pd.DataFrame(columns=['time','TrialID','numTargs','HA0_engagement','HA1_engagement'])
    collapsed_policy['time'] = actual_dynamic_policy['time']
    collapsed_policy['TrialID'] = actual_dynamic_policy['TrialID']
    collapsed_policy['numTargs'] = actual_dynamic_policy['numTargs']
    collapsed_policy['HA0_engagement'] = -1
    collapsed_policy['HA1_engagement'] = -1
    for idx, row in actual_dynamic_policy.iterrows():

        if [row['HA0TA0'], row['HA0TA1'], row['HA0TA2'], row['HA0TA3'], row['HA0TA4']].count(1) > 1:
            #print("More than one TA is engaged with HA0")
            closest_TA = get_closest_HA_TA_pair(trialData, idx, player = 'p0' if not simulation_bool else 'hA0')
            collapsed_policy.at[idx, 'HA0_engagement'] = closest_TA
        # we will check if the HA is engaged with the TA
        elif row['HA0TA0'] == 1:
            collapsed_policy.at[idx, 'HA0_engagement'] = 0
        elif row['HA0TA1'] == 1:
            collapsed_policy.at[idx, 'HA0_engagement'] = 1
        elif row['HA0TA2'] == 1:
            collapsed_policy.at[idx, 'HA0_engagement'] = 2
        elif row['HA0TA3'] == 1:
            collapsed_policy.at[idx, 'HA0_engagement'] = 3
        elif row['HA0TA4'] == 1:
            collapsed_policy.at[idx, 'HA0_engagement'] = 4

        if [row['HA1TA0'], row['HA1TA1'], row['HA1TA2'], row['HA1TA3'], row['HA1TA4']].count(1) > 1:
            #print("More than one TA is engaged with HA1")
            closest_TA = get_closest_HA_TA_pair(trialData, idx, player = 'p1' if not simulation_bool else 'hA1')
            collapsed_policy.at[idx, 'HA1_engagement'] = closest_TA
        elif row['HA1TA0'] == 1:
            collapsed_policy.at[idx, 'HA1_engagement'] = 0
        elif row['HA1TA1'] == 1:
            collapsed_policy.at[idx, 'HA1_engagement'] = 1
        elif row['HA1TA2'] == 1:
            collapsed_policy.at[idx, 'HA1_engagement'] = 2
        elif row['HA1TA3'] == 1:
            collapsed_policy.at[idx, 'HA1_engagement'] = 3
        elif row['HA1TA4'] == 1:
            collapsed_policy.at[idx, 'HA1_engagement'] = 4

    return collapsed_policy

if not os.path.exists(output_path):
    os.mkdir(output_path)

for simulation_bool in [False, True]:

    if simulation_bool:
        simulation_types = ["CollinearAngle", "CollinearDistance", "Angle", "Distance", "ContainmentZone"]
        for simulation_type in simulation_types:
            dataDir = os.path.join(wd, 'OtherResults', 'AA-AA_SimulationData', simulation_type) # Directory of all data files
            output_header = "\Simulation"

            if not os.path.exists(output_path + output_header):
                os.mkdir(output_path + output_header)

            output_folder = output_path + output_header + "\\" + simulation_type
            if not os.path.exists(output_folder):
                os.mkdir(output_folder)

            numHerders = 2
            maxTargets = 5
            firstTrial = 1
            lastTrial = 24 + 1 # +1 for python indexing
            numTrials = lastTrial - firstTrial
            numTargetArray = [3,4,5] # array of the possible number of targets in the experiment
            #startSample = 250 #index where to start the analysis from
            skip_freq = 1# int(decision_delay / trialDeltaTime) #number of rows to skip to get the desired decision delay
            sessions_directories = os.listdir(dataDir) # list of all sessions (ie, participants)

            columns = ["time","TrialID", "numTargs","HA0TA0", "HA0TA1", "HA0TA2", "HA0TA3", "HA0TA4","HA1TA0", "HA1TA1", "HA1TA2", "HA1TA3", "HA1TA4"]

            for session in tqdm(sessions_directories, desc="Sessions"):
                output_filename_folder = output_header + "/" + simulation_type + "/" + session
                if not os.path.exists(output_path + output_filename_folder):
                    os.mkdir(output_path + output_filename_folder)
                for trial in trange(firstTrial, lastTrial, desc="Trials", leave=False):
                    output_filename = "/trialIdentifier_"+str(trial) + ".csv" #one file per trial
                    trial_ID = "{:02}".format(trial)
                    part_dir = Path(os.path.join(dataDir, session+'/ExperimentData'))
                    file_path = [path for path in part_dir.rglob('*trialIdentifier'+trial_ID+'*')][0]
                    trialData = pd.read_csv(file_path)
                    dynamicPolicyTimeSeries = get_actual_Dynamic_Policy_as_csv(trial, trialData)  #0 and 1 encoded HA-TA engagement
                    collapsedDynamicPolicyTimeSeries = collapse_actual_dynamic_engagement(dynamicPolicyTimeSeries, trialData)

                    
                    pd.DataFrame(data=collapsedDynamicPolicyTimeSeries).to_csv(output_path + output_filename_folder + output_filename, index=False)
                    
    else: # if real data
        dataDir = os.path.join(wd, 'RAW_EXPERIMENT_DATA', 'TWO-HUMAN_HAs') # Directory of all data files
        output_header = "\Human"
        output_folder = output_path + output_header
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        numHerders = 2
        maxTargets = 5
        firstTrial = 1
        lastTrial = 24 + 1 # +1 for python indexing
        numTrials = lastTrial - firstTrial
        numTargetArray = [3,4,5] # array of the possible number of targets in the experiment
        #startSample = 250 #index where to start the analysis from
        skip_freq = 1# int(decision_delay / trialDeltaTime) #number of rows to skip to get the desired decision delay
        sessions_directories = os.listdir(dataDir) # list of all sessions (ie, participants)

        columns = ["time","TrialID", "numTargs","HA0TA0", "HA0TA1", "HA0TA2", "HA0TA3", "HA0TA4","HA1TA0", "HA1TA1", "HA1TA2", "HA1TA3", "HA1TA4"]

        for session in tqdm(sessions_directories, desc="Sessions"):
            output_filename_folder = output_header + "/" + session
            if not os.path.exists(output_path + output_filename_folder):
                os.mkdir(output_path + output_filename_folder)
            for trial in trange(firstTrial, lastTrial, desc="Trials", leave=False):
                output_filename = "/trialIdentifier_"+str(trial) + ".csv" #one file per trial
                trial_ID = "{:02}".format(trial)
                part_dir = Path(os.path.join(dataDir, session+'/ExperimentData'))
                filePath = [path for path in part_dir.rglob('*trialIdentifier'+trial_ID+'*')][0] #0 because assuming only one such file exists
                trialData = pd.read_csv(filePath)
                dynamicPolicyTimeSeries = get_actual_Dynamic_Policy_as_csv(trial, trialData)  #0 and 1 encoded HA-TA engagement
                collapsedDynamicPolicyTimeSeries = collapse_actual_dynamic_engagement(dynamicPolicyTimeSeries, trialData)

                
                pd.DataFrame(data=collapsedDynamicPolicyTimeSeries).to_csv(output_path + output_filename_folder + output_filename, index=False)