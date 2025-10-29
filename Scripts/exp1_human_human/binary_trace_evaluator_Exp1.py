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

# Add parent Scripts directory to path for importing tools module
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.dirname(script_dir)
sys.path.insert(0, scripts_dir)

#custom package
from tools.traj_utils import get_binary_trace

############################### USER SETTINGS ##################################
first_trial = 7
last_trial = 24 + 1

################################################################################

def main():

    intermediary_columns = ["Session", "Player", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]

    cwd = os.path.dirname(os.path.abspath(__file__))
    wd = Path(cwd).parents[1] # project working directory

    humanDataDir = os.path.join(wd,'RAW_EXPERIMENT_DATA','TWO-HUMAN_HAs') #Directory of all data files
    all_sessions = os.listdir(humanDataDir)
    AA_SIM_types = ['CollinearAngle', 'CollinearDistance', 'Angle', 'Distance', 'ContainmentZone'] 

    output_dir = os.path.join(wd, "OtherResults", "AA_scores_traces")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for AA_type in (AA_SIM_types):
        print("Processing AA type: ", AA_type)

        # Check if output file already exists
        output_file = os.path.join(output_dir, f"AA_scores_traces_Successive{AA_type}.csv")
        if os.path.exists(output_file):
            print(f"  Output file already exists: {output_file}")
            print(f"  Skipping {AA_type}...")
            continue

        df = pd.DataFrame(index=range(len(all_sessions)*2), columns=intermediary_columns) # 2 for the two players
        for count, evaluee_session in enumerate(all_sessions):
            # Skip hidden files and directories (like .DS_Store)
            if evaluee_session.startswith('.'):
                continue
            print("\n Evaluee session: ", count+1, " of ", len(all_sessions))
            background_sessions = [session for session in all_sessions if session != evaluee_session and not session.startswith('.')]

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

                        # Handle missing simulation files gracefully
                        if len(simFiles) == 0:
                            print(f"\n  Warning: No simulation file found for trial {trial} in {AA_type}. Skipping this trial.")
                            df.loc[count*2 + player, "Session"] = evaluee_session
                            df.loc[count*2 + player, "Player"] = player + 1
                            df.loc[count*2 + player, str(trial)] = np.nan  # Mark as missing data
                            continue
                        elif len(simFiles) > 1:
                            print(f"\n  Warning: Multiple simulation files found for trial {trial} in {AA_type}. Using first match.")

                        simFile = simFiles[0]
                        individual_trial_AA_score = get_binary_trace(X, Z, pd.read_csv(simFile), "hA%d" % player)
                        df.loc[count*2 + player, "Session"] = evaluee_session
                        df.loc[count*2 + player, "Player"] = player + 1 #player 0 is player 1, player 1 is player 2
                        df.loc[count*2 + player, str(trial)] = individual_trial_AA_score

        df.to_csv(output_file, index=False)
        print(f"\n  Saved: {output_file}")

                
if __name__ == "__main__":


    main()
    