import sys # for system level stuff
import getopt # for command line arguments
import os # for directory handling 
from pathlib import Path # for file handling    
import numpy as np # for numerical operations
import pandas as pd
import pingouin as pg # for t-test and BF10
import matplotlib.pyplot as plt # for plotting
from tqdm import trange
from pingouin import ttest
from scipy.stats import f_oneway


#custom package
from tools.traj_utils import get_binary_trace

############################### USER SETTINGS ##################################
first_trial = 7
last_trial = 24 + 1

################################################################################

def main():

    intermediary_columns = ["Session", "Player", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]

    cwd = os.path.dirname(os.path.abspath(__file__))
    wd = Path(cwd).parents[0] # project working directory

    humanDataDir = os.path.join(wd,'RAW_EXPERIMENT_DATA','TWO-HUMAN_HAs') #Directory of all data files
    all_sessions = os.listdir(humanDataDir)
    AA_SIM_types = ['CollinearAngle', 'CollinearDistance', 'Angle', 'Distance', 'ContainmentZone'] 

    output_dir = os.path.join(wd, "OtherResults", "AA_scores_traces")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for AA_type in (AA_SIM_types):
        print("Processing AA type: ", AA_type)  
        df = pd.DataFrame(index=range(len(all_sessions)*2), columns=intermediary_columns) # 2 for the two players
        for count, evaluee_session in enumerate(all_sessions):
            print("\n Evaluee session: ", count+1, " of ", len(all_sessions))
            background_sessions = [session for session in all_sessions if session != evaluee_session]

            for player in (0,1):

                for trial in range(first_trial,last_trial):
                    sys.stdout.write('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
                    X = np.array([])
                    Z = np.array([])
                    trial_ID = "{:02}".format(trial)
                    filePaths = [[path for path in Path(os.path.join(humanDataDir, background_session)).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in background_sessions]

                    for filePath in filePaths:
                        trialData = pd.read_csv(filePath[0])
                        X = np.append(X, trialData['p%dx' % (player)].to_numpy())
                        Z = np.append(Z, trialData['p%dz' % (player)].to_numpy())
                        #now we have all the human data for the given trial and given player
                        #we can now compare this to the AA data
                        simDir = os.path.join(wd,'OtherResults', 'AA-AA_SimulationData', AA_type) #Directory of all simualtion data files

                        #get all lowest level files in the directory simDir and get the one that matches the trial_ID
                        simFiles = [path for path in Path(simDir).rglob('*trialIdentifier'+trial_ID+'*')]

                        assert len(simFiles) == 1, "length of simFiles is %d" % len(simFiles)
                        simFile = simFiles[0]
                        for simFile in simFiles:
                            individual_trial_AA_score = get_binary_trace(X, Z, pd.read_csv(simFile), "hA%d" % player)
                            df.loc[count*2 + player, "Session"] = evaluee_session            
                            df.loc[count*2 + player, "Player"] = player + 1 #player 0 is player 1, player 1 is player 2
                            df.loc[count*2 + player, str(trial)] = individual_trial_AA_score

        df.to_csv(output_dir + "/AA_scores_traces_Successive" + AA_type + ".csv")

                
if __name__ == "__main__":


    main()
    