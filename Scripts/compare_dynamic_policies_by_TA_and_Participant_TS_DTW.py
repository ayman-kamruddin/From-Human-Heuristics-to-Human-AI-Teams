
"""Given the dynamic policies for the human and the simulation, this script calculates the normalised DTW error between the human and the simulation for each trial and each participant."""

import os
import pandas as pd
#import similaritymeasures
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
#from utils import *
from pathlib import Path # path functions
from tqdm import trange # progress bar



simulations = ["\CollinearAngle", "\Angle", "\CollinearDistance", "\Distance", "\ContainmentZone"]



cwd = os.path.dirname(os.path.realpath(__file__))
wd = os.path.dirname(cwd)
numHerders = 2
#haCols = ["HA%d" % i for i in range(0,numHerders)]

maxTargets = 5
firstTrial = 7
lastTrial = 24 + 1 # +1 for python indexing
policy_folder = wd + "/OtherResults/TS_Dynamic_Policy"


human_sessions_directories = os.listdir(policy_folder+"\Human") # list of all sessions (ie, participants)
columns=["Session", "Player", "3TAs", "4TAs", "5TAs"]
intermediary_columns = ["Session", "Player", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]

output_dir = wd+"/OtherResults/DTW_TS_Errors"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for simulation_key in trange(len(simulations)): # for each simulation type

    #make a pd dataframe of length of human_sessions_directories, columns = columns
    df = pd.DataFrame(index=range(len(human_sessions_directories)*2), columns=intermediary_columns) # 2 for the two players

    print("Processing Simulation: ", simulations[simulation_key][1:])

    simulation_sessions_directory = policy_folder+"/Simulation" + simulations[simulation_key]

    for trial in range(firstTrial, lastTrial):
        print("Processing Trial: ", trial)

        for hcount, human_session in enumerate(human_sessions_directories):
            print("Processing Session: ", human_session)
            trial_ID = str(trial)
            part_dir = Path(os.path.join(policy_folder+"/Human", human_session))

            #get the file path for the human file that has the trial data, matched with the trailIdentifier, using rglob
            human_filePath = part_dir / ("trialIdentifier_"+trial_ID+".csv")


            simulation_filePath = simulation_sessions_directory+"/SessionSIM/trialIdentifier_"+trial_ID+".csv"
            human_data = pd.read_csv(human_filePath)
            sim_data = pd.read_csv(simulation_filePath)
            assert(human_data['TrialID'][0] == sim_data['TrialID'][0])
            assert(human_data['numTargs'][0] == sim_data['numTargs'][0])
            numTargets = int(human_data['numTargs'][0])
            


            err_player_1, _ = fastdtw(np.column_stack([human_data['HA0_engagement'].to_numpy()]), np.column_stack([sim_data["HA0_engagement"].to_numpy()]), dist=euclidean) 
            final_err_player_1 = err_player_1/(len(human_data) + len(sim_data))

            err_player_2, _ = fastdtw(np.column_stack([human_data["HA1_engagement"].to_numpy()]), np.column_stack([sim_data["HA1_engagement"].to_numpy()]), dist=euclidean)
            final_err_player_2 = err_player_2/(len(human_data) + len(sim_data))


            print(len(human_data), len(sim_data))


            df.loc[2*hcount, "Session"] = human_session
            df.loc[2*hcount, "Player"] = 1
            df.loc[2*hcount, str(trial)] = final_err_player_1

            df.loc[2*hcount+1, "Session"] = human_session
            df.loc[2*hcount+1, "Player"] = 2
            df.loc[2*hcount+1, str(trial)] = final_err_player_2


            df.to_csv(output_dir+"\\"+"Successive"+simulations[simulation_key][1:]+"_DTW_Errors.csv", index=False)

