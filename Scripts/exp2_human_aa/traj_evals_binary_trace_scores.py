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


def get_surrogate_human_team_traces():
    # get the surrogate human team traces

    cwd = os.path.dirname(__file__)
    wd = Path(cwd).parents[1] # project working directory

    humanDataDir = os.path.join(wd,'RAW_EXPERIMENT_DATA','TWO-HUMAN_HAs')
    all_sessions = [s for s in os.listdir(humanDataDir) if not s.startswith('.')]  # Filter out hidden files
    humanTeamTraces = np.zeros((len(all_sessions), 18))

    print("Evaluating surrogate human team traces")

    for count, evaluee_session in enumerate(all_sessions):
        print("\n Evaluee session: ", count+1, " of ", len(all_sessions))
        background_sessions = [session for session in all_sessions if session != evaluee_session and not session.startswith('.')]

        for player in (0,1):

            for trial in range(first_trial,last_trial):
                sys.stdout.write('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
                X = np.array([])
                Z = np.array([])
                trial_ID = "{:02}".format(trial)
                filePaths = [[path for path in Path(os.path.join(humanDataDir, background_session)).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in background_sessions]

                # Skip trial if no files found for any session
                files_found = 0
                for filePath in filePaths:
                    if len(filePath) == 0:
                        continue  # Skip if this session doesn't have this trial
                    files_found += 1
                    trialData = pd.read_csv(filePath[0])
                    X = np.append(X, trialData['p%dx' % (player)].to_numpy())
                    Z = np.append(Z, trialData['p%dz' % (player)].to_numpy())

                # Skip this trial entirely if no background data was found
                if files_found == 0:
                    print(f"\nWarning: No background data found for trial {trial}, skipping...")
                    continue
                #now we have all the human data for the given trial and given player

                # Get evaluee file
                evalFiles = [path for path in Path(os.path.join(humanDataDir, evaluee_session)).rglob('*trialIdentifier'+trial_ID+'*')]
                if len(evalFiles) == 0:
                    print(f"\nWarning: No evaluee data found for trial {trial} in session {evaluee_session}, skipping...")
                    continue

                evalFile = evalFiles[0]
                trialData = pd.read_csv(evalFile)

                humanTeamTraces[count][trial-first_trial] += get_binary_trace(X, Z, trialData, "p" + str(player))        
                
    humanTeamTraces = np.array(humanTeamTraces) /  2 #normalise by number of players

    return humanTeamTraces

def main():


    wd = Path(os.path.dirname(os.path.realpath(__file__))
              ).parents[1] # project working directory

    humanDataDir = os.path.join(wd,'RAW_EXPERIMENT_DATA','TWO-HUMAN_HAs')
    all_sessions = [s for s in os.listdir(humanDataDir) if not s.startswith('.')]  # Filter out hidden files
    AA_types = ["Heuristic"]  # Only Heuristic agent type used in this study
        

    AA_sessions = {}
    for AA_type in AA_types:
        AA_path = os.path.join(wd,'RAW_EXPERIMENT_DATA','HUMAN-AA_TEAM', AA_type)
        lowest_level_dirs = list()
        for root,dirs,files in os.walk(AA_path):
            if not dirs:
                lowest_level_dirs.append(Path(root).parent.name)
        AA_sessions[AA_type] = lowest_level_dirs

    # for each session, you want an array of 18 binary traces
    #initialise arrays to store the binary traces
    human_scores_better = {}
    for human_type in AA_types:
        for session in AA_sessions[human_type]:
            human_scores_better[session] = np.zeros(18)

    AA_scores_better = {}
    for AA_type in AA_types:
        for session in AA_sessions[AA_type]:
            AA_scores_better[session] = np.zeros(18)


    for player in (0,1):

        for trial in range(first_trial,last_trial):
            sys.stdout.write('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
            X = np.array([])
            Z = np.array([])
            trial_ID = "{:02}".format(trial)
            filePaths = [[path for path in Path(os.path.join(humanDataDir, background_session)).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in all_sessions]

            # Skip trial if no files found for any session
            files_found = 0
            for filePath in filePaths:
                if len(filePath) == 0:
                    continue  # Skip if this session doesn't have this trial
                files_found += 1
                trialData = pd.read_csv(filePath[0])
                X = np.append(X, trialData['p%dx' % (player)].to_numpy())
                Z = np.append(Z, trialData['p%dz' % (player)].to_numpy())

            # Skip this trial entirely if no data was found
            if files_found == 0:
                print(f"\nWarning: No data found for trial {trial}, skipping...")
                continue
            #now we have all the human data for the given trial and given player            

            for subFolder in ["HumanPlayer0", "HumanPlayer1"]:

                for AA_count, AA_type in enumerate(AA_types):
                    expDir = os.path.join(wd,'RAW_EXPERIMENT_DATA','HUMAN-AA_TEAM', AA_type)
                    expFiles = [path for path in Path(os.path.join(expDir, subFolder)).rglob('*trialIdentifier'+trial_ID+'*')]
                    for expFile in expFiles:
                        session_name = Path(expFile).parent.parent.name
                        if player == 0 and subFolder == "HumanPlayer0" or player == 1 and subFolder == "HumanPlayer1":
                            individual_trial_human_score = get_binary_trace(X, Z, pd.read_csv(expFile), "p0")
                            #human_scores[AA_count].append(individual_trial_human_score)
                            human_scores_better[session_name][trial-first_trial] += individual_trial_human_score


                        elif player == 0 and subFolder == "HumanPlayer1" or player == 1 and subFolder == "HumanPlayer0":
                            individual_trial_AA_score = get_binary_trace(X, Z, pd.read_csv(expFile), "hA0")
                            #AA_scores[AA_count].append(individual_trial_AA_score)
                            AA_scores_better[session_name][trial-first_trial] += individual_trial_AA_score
                
        
                
    humanTeamTraces = get_surrogate_human_team_traces()   

    return humanTeamTraces, human_scores_better, AA_scores_better

if __name__ == "__main__":


    humanTeamTraces, human_scores_better, AA_scores_better = main()

    # Collect scores for Heuristic agent type only (Session1xxx)
    AA_scores_heur = []
    human_scores_heur = []

    for session in AA_scores_better.keys():
        # Only process Session1xxx (Heuristic agent type)
        if session.startswith("Session1"):
            AA_scores_heur.append(AA_scores_better[session])
            human_scores_heur.append(human_scores_better[session])

    AA_scores_heur = np.array(AA_scores_heur)
    human_scores_heur = np.array(human_scores_heur)

    cwd = os.path.dirname(os.path.realpath(__file__))
    wd = Path(cwd).parents[1] # project working directory

    save_dir = os.path.join(wd, "OtherResults", "binaryTraceOverlaps")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cols = np.arange(7,25)

    #save the human team traces as a .csv file
    pd.DataFrame(humanTeamTraces, columns=cols).to_csv(os.path.join(save_dir, "humanTeamTraces.csv"), index=False)
    print(f"Saved humanTeamTraces.csv")

    # save the AA_scores and human scores (only Heuristic)
    if len(AA_scores_heur) > 0:
        pd.DataFrame(AA_scores_heur, columns=cols).to_csv(os.path.join(save_dir, "AA_scores_heur.csv"), index=False)
        pd.DataFrame(human_scores_heur, columns=cols).to_csv(os.path.join(save_dir, "human_scores_heur.csv"), index=False)
        print(f"Saved Heuristic scores ({len(AA_scores_heur)} sessions)")
    else:
        raise ValueError("Error: No Heuristic (Session1xxx) data found in the dataset!")

  