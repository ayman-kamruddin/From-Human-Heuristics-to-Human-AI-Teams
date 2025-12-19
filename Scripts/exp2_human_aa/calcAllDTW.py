"""Reads in all human and AA data as well as the human-human data
performs surrogate analysis on the TS engagement time series
saves arrays and plots the bar plot"""
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from tqdm import tqdm

############################### USER SETTINGS ##################################
first_trial = 7
last_trial = 24 + 1 #keep +1 for pythonic indexing
num_trials = last_trial - first_trial
################################################################################


def GETall_AAteam_scores():
    """Returns the normalised DTW scores of each human-AA team against each human-human team"""
    cwd = os.path.dirname(__file__) # current working directory
    wd = Path(cwd).parents[1] # project working directory
    humanDataDir = os.path.join(wd, 'OtherResults', 'TS_Dynamic_Policy', 'Human') # directory containing human-human TSp data
    human_human_sessions = os.listdir(humanDataDir)


    AA_types = ["Heuristic"]  # Only Heuristic agent type used in this study

    # this block will create a dictionary with the AA sessions for each AA type
    AA_sessions = {}
    for AA_type in AA_types:
        AA_path = os.path.join(wd, 'RAW_EXPERIMENT_DATA', 'HUMAN-AA_TEAM', AA_type)
        lowest_level_dirs = list()
        for root,dirs,files in os.walk(AA_path):
            if not dirs:
                lowest_level_dirs.append(Path(root).parent.name)
        AA_sessions[AA_type] = lowest_level_dirs

    # for each session, you want an array of num_trials normalised DTW scores
    # initialise arrays to store the binary traces
    #create a dictionary to store the normalised DTW scores for each human in the human-AA sessions
    human_scores = {}
    for human_type in AA_types:
        for session in AA_sessions[human_type]:
            human_scores[session] = np.zeros(num_trials)

    # for each session, you want an array of num_trials normalised DTW scores
    # initialise arrays to store the binary traces
    #create a dictionary to store the normalised DTW scores for each AA in the human-AA sessions
    AA_scores = {}
    for AA_type in AA_types:
        for session in AA_sessions[AA_type]:
            AA_scores[session] = np.zeros(num_trials)

    for player in (0,1): #player 0 and player 1 start off in predetermined positions each trial
        for trial in range(first_trial,last_trial): #loop over trials
            print('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
            trial_ID = "_" + str(trial)
            humanhumanFilePaths = [[path for path in Path(os.path.join(humanDataDir, session)).rglob('*trialIdentifier'+trial_ID+'*')] for session in human_human_sessions]
            for subFolder in ["HumanPlayer0", "HumanPlayer1"]:
                for AA_type in AA_types:
                    expDir = os.path.join(wd, 'OtherResults', 'Actual_Dynamic_Policies_HumanAA', AA_type)
                    expFiles = [path for path in Path(os.path.join(expDir, subFolder)).rglob('*trialIdentifier'+trial_ID+'*')]
                    for expFile in tqdm(expFiles) : #include a progress bar
                        session_name = Path(expFile).parent.name
                        AAteamData = pd.read_csv(expFile) #human-AA team data
                        if player == 0 and subFolder == "HumanPlayer0" or player == 1 and subFolder == "HumanPlayer1":
                            properHeader = 'p0'
                            AAteamTS = AAteamData[properHeader + '_engagement']
                            for humanhumanFilePath in tqdm(humanhumanFilePaths):

                                humanhumanData = pd.read_csv(humanhumanFilePath[0])

                                humanhumanTS = humanhumanData['HA%d_engagement' % (player)]
                                human_scores[session_name][trial-first_trial] += 1 - fastdtw( np.column_stack([humanhumanTS]), np.column_stack([AAteamTS]), dist=euclidean)[0] / (len(humanhumanTS) + len(AAteamTS))
                        elif player == 0 and subFolder == "HumanPlayer1" or player == 1 and subFolder == "HumanPlayer0":
                            properHeader = 'hA0'
                            AAteamTS = AAteamData[properHeader + '_engagement']
                            for humanhumanFilePath in tqdm(humanhumanFilePaths):
                                
                                humanhumanData = pd.read_csv(humanhumanFilePath[0]) 
                                humanhumanTS = humanhumanData['HA%d_engagement' % (player)]
                                AA_scores[session_name][trial-first_trial] += 1 - fastdtw( np.column_stack([humanhumanTS]), np.column_stack([AAteamTS]), dist=euclidean)[0] / (len(humanhumanTS) + len(AAteamTS))


    return human_scores, AA_scores


def GETall_humanTeam_scores():
    cwd = os.path.dirname(__file__) # current working directory
    wd = Path(cwd).parents[1] # project working directory
    humanDataDir = os.path.join(wd, 'OtherResults', 'TS_Dynamic_Policy', 'Human') # directory containing human-human TSp data
    human_human_sessions = os.listdir(humanDataDir)
    num_humanhumanSessions = len(human_human_sessions)

    humanTeamScores = np.zeros((num_humanhumanSessions, num_trials)) #there are num_humanhumanSessions human-human sessions and num_trials trials per session
    for count, evaluee_session in enumerate(human_human_sessions): #loop over single human-human sessions
        print("\n Evaluee session: ", count+1, " of ", len(human_human_sessions))
        background_sessions = [session for session in human_human_sessions if session != evaluee_session]
        for player in (0,1): #player 0 and player 1 start off in predetermined positions each trial
            for trial in range(first_trial,last_trial): #loop over trials
                #calculate the normalised DTW scores of each evaluee against each single background session
                trial_ID = "_"+str(trial)  #"{:02}".format(trial)
                backgroundFilePaths = [[path for path in Path(os.path.join(humanDataDir, background_session)).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in background_sessions]

                evalFile = [path for path in Path(os.path.join(humanDataDir, evaluee_session)).rglob('*trialIdentifier'+trial_ID+'*')][0]     
                evalueeData = pd.read_csv(evalFile)   
                for backgroundFilePath in tqdm(backgroundFilePaths):
                    backgroundData = pd.read_csv(backgroundFilePath[0])
                    backgroundTS = backgroundData['HA%d_engagement' % (player)]
                    evalueeTS = evalueeData['HA%d_engagement' % (player)]
                    humanTeamScores[count][trial-first_trial] += 1 - fastdtw( np.column_stack([backgroundTS]), np.column_stack([evalueeTS]), dist=euclidean)[0] / (len(backgroundTS) + len(evalueeTS))
    return humanTeamScores / 2 / 21 #divide by 2 as there are 2 players in the human-human team and divide by 21 as there are 21 trials per session
            


if __name__ == "__main__":

    cwd = os.path.dirname(os.path.realpath(__file__))
    wd = Path(cwd).parents[1] # project working directory

    save_dir = os.path.join(wd, "OtherResults", "TSp_DTWs")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cols = np.arange(7,25)

    # Check if all output files already exist
    required_files = [
        os.path.join(save_dir, "humanTeamDTWs.csv"),
        os.path.join(save_dir, "AA_scores_heur.csv"),
        os.path.join(save_dir, "human_scores_heur.csv")
    ]

    if all(os.path.exists(f) for f in required_files):
        print("All output files already exist. Skipping computation.")
        print(f"  - {required_files[0]}")
        print(f"  - {required_files[1]}")
        print(f"  - {required_files[2]}")
        print("To recompute, delete these files first.")
        sys.exit(0)

    print("Calculating all DTWs for human-human teams")
    humanTeamDTWs = GETall_humanTeam_scores()
    #save humanTeamDTWs as .csv file
    pd.DataFrame(humanTeamDTWs, columns=cols).to_csv(os.path.join(save_dir, "humanTeamDTWs.csv"), index=False)
    print(f"Saved humanTeamDTWs.csv")


    print("Calculating all DTWs for human-AA teams")
    humanDTWs, AA_DTWs = GETall_AAteam_scores()


    # Collect scores for Heuristic agent type (Session1xxx)
    AA_scores_heur = []
    human_scores_heur = []

    for session in AA_DTWs.keys():
        # Only process Session1xxx (Heuristic agent type)
        if session.startswith("Session1"):
            AA_scores_heur.append(AA_DTWs[session])
            human_scores_heur.append(humanDTWs[session])

    # Convert to arrays and normalize by number of human-human sessions
    if len(AA_scores_heur) > 0:
        AA_scores_heur = np.array(AA_scores_heur) / 21
        human_scores_heur = np.array(human_scores_heur) / 21

        # Save the scores as csv files
        pd.DataFrame(AA_scores_heur, columns=cols).to_csv(os.path.join(save_dir, "AA_scores_heur.csv"), index=False)
        pd.DataFrame(human_scores_heur, columns=cols).to_csv(os.path.join(save_dir, "human_scores_heur.csv"), index=False)
        print(f"Saved Heuristic scores ({len(AA_scores_heur)} sessions)")
    else:
        raise ValueError("Error: No Heuristic (Session1xxx) data found in the dataset!")
