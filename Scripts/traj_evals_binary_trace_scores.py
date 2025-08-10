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


def get_surrogate_human_team_traces():
    # get the surrogate human team traces

    cwd = os.path.dirname(__file__)
    wd = Path(cwd).parents[0] # project working directory

    humanDataDir = os.path.join(wd,'RAW_EXPERIMENT_DATA\TWO-HUMAN_HAs')
    all_sessions = os.listdir(humanDataDir)
    humanTeamTraces = np.zeros((len(all_sessions), 18))

    print("Evaluating surrogate human team traces")

    for count, evaluee_session in enumerate(all_sessions):
        print("\n Evaluee session: ", count+1, " of ", len(all_sessions))
        background_sessions = [session for session in all_sessions if session != evaluee_session]

        for player in (0,1):

            for trial in range(first_trial,last_trial):
                sys.stdout.write('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
                X = np.array([])
                Z = np.array([])
                trial_ID = "{:02}".format(trial)
                filePaths = [[path for path in Path(humanDataDir+'\\'+background_session).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in background_sessions]

                for filePath in filePaths:
                    trialData = pd.read_csv(filePath[0])
                    X = np.append(X, trialData['p%dx' % (player)].to_numpy())
                    Z = np.append(Z, trialData['p%dz' % (player)].to_numpy())
                #now we have all the human data for the given trial and given player

                evalFile = [path for path in Path(humanDataDir+'\\'+evaluee_session).rglob('*trialIdentifier'+trial_ID+'*')][0]     
                trialData = pd.read_csv(evalFile)
                
                humanTeamTraces[count][trial-first_trial] += get_binary_trace(X, Z, trialData, "p" + str(player))        
                
    humanTeamTraces = np.array(humanTeamTraces) /  2 #normalise by number of players

    return humanTeamTraces

def main():


    wd = Path(os.path.dirname(os.path.realpath(__file__))
              ).parents[0] # project working directory

    humanDataDir = os.path.join(wd,'RAW_EXPERIMENT_DATA\TWO-HUMAN_HAs')
    all_sessions = os.listdir(humanDataDir)
    AA_types = ["\Heuristic", "\Human-Sensitive", "\SelfPlay"]
        

    AA_sessions = {}
    for AA_type in AA_types:
        AA_path = os.path.join(wd,'RAW_EXPERIMENT_DATA\HUMAN-AA_TEAM'+AA_type)
        lowest_level_dirs = list()
        for root,dirs,files in os.walk(AA_path):
            if not dirs:
                lowest_level_dirs.append(Path(root).parent.name)
        AA_sessions[AA_type[1:]] = lowest_level_dirs

    # for each session, you want an array of 18 binary traces
    #initialise arrays to store the binary traces
    human_scores_better = {}
    for human_type in AA_types:
        for session in AA_sessions[human_type[1:]]:
            human_scores_better[session] = np.zeros(18)

    AA_scores_better = {}
    for AA_type in AA_types:
        for session in AA_sessions[AA_type[1:]]:
            AA_scores_better[session] = np.zeros(18)


    for player in (0,1):

        for trial in range(first_trial,last_trial):
            sys.stdout.write('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
            X = np.array([])
            Z = np.array([])
            trial_ID = "{:02}".format(trial)
            filePaths = [[path for path in Path(humanDataDir+'\\'+background_session).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in all_sessions]

            for filePath in filePaths:
                trialData = pd.read_csv(filePath[0])
                X = np.append(X, trialData['p%dx' % (player)].to_numpy())
                Z = np.append(Z, trialData['p%dz' % (player)].to_numpy())
            #now we have all the human data for the given trial and given player            

            for subFolder in ["\HumanPlayer0", "\HumanPlayer1"]:

                for AA_count, AA_type in enumerate(AA_types):
                    expDir = os.path.join(wd,'RAW_EXPERIMENT_DATA\HUMAN-AA_TEAM'+AA_type)
                    expFiles = [path for path in Path(expDir+subFolder).rglob('*trialIdentifier'+trial_ID+'*')]
                    for expFile in expFiles:
                        session_name = Path(expFile).parent.parent.name
                        if player == 0 and subFolder == "\HumanPlayer0" or player == 1 and subFolder == "\HumanPlayer1":
                            individual_trial_human_score = get_binary_trace(X, Z, pd.read_csv(expFile), "p0")
                            #human_scores[AA_count].append(individual_trial_human_score)
                            human_scores_better[session_name][trial-first_trial] += individual_trial_human_score


                        elif player == 0 and subFolder == "\HumanPlayer1" or player == 1 and subFolder == "\HumanPlayer0":
                            individual_trial_AA_score = get_binary_trace(X, Z, pd.read_csv(expFile), "hA0")
                            #AA_scores[AA_count].append(individual_trial_AA_score)
                            AA_scores_better[session_name][trial-first_trial] += individual_trial_AA_score
                
        
                
    humanTeamTraces = get_surrogate_human_team_traces()   

    return humanTeamTraces, human_scores_better, AA_scores_better

if __name__ == "__main__":


    humanTeamTraces, human_scores_better, AA_scores_better = main()

    AA_scores_heur = []
    AA_scores_hybr = []
    AA_scores_self = []
    human_scores_heur = []
    human_scores_hybr = []
    human_scores_self = []
    for session in AA_scores_better.keys():
        # if session starts with Session1
        if session.startswith("Session1"):
            AA_scores_heur.append(AA_scores_better[session])
            human_scores_heur.append(human_scores_better[session])
        elif session.startswith("Session2"):
            AA_scores_hybr.append(AA_scores_better[session])
            human_scores_hybr.append(human_scores_better[session])
        elif session.startswith("Session3"):
            AA_scores_self.append(AA_scores_better[session])
            human_scores_self.append(human_scores_better[session])

    AA_scores_heur = np.array(AA_scores_heur) 
    AA_scores_hybr = np.array(AA_scores_hybr) 
    AA_scores_self = np.array(AA_scores_self) 

    human_scores_heur = np.array(human_scores_heur) 
    human_scores_hybr = np.array(human_scores_hybr) 
    human_scores_self = np.array(human_scores_self)

    cwd = os.path.dirname(os.path.realpath(__file__))
    wd = Path(cwd).parents[0] # project working directory

    save_dir = os.path.join(wd, "OtherResults", "binaryTraceOverlaps")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cols = np.arange(7,25)

    #save the human team traces as a .csv file
    pd.DataFrame(humanTeamTraces, columns=cols).to_csv(save_dir + "\humanTeamTraces.csv")
    #np.save(save_dir + "\humanTeamTraces.npy" , humanTeamTraces)

    # save the AA_scores

    pd.DataFrame(AA_scores_heur, columns=cols).to_csv(save_dir + "\AA_scores_heur.csv")
    pd.DataFrame(AA_scores_hybr, columns=cols).to_csv(save_dir + "\AA_scores_hybr.csv")
    pd.DataFrame(AA_scores_self, columns=cols).to_csv(save_dir + "\AA_scores_self.csv")

    #save the human scores
    pd.DataFrame(human_scores_heur, columns=cols).to_csv(save_dir + "\human_scores_heur.csv")
    pd.DataFrame(human_scores_hybr, columns=cols).to_csv(save_dir + "\human_scores_hybr.csv")
    pd.DataFrame(human_scores_self, columns=cols).to_csv(save_dir + "\human_scores_self.csv")

  