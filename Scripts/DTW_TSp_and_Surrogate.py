"""Reads in all human and AA data as well as the human-human data
performs surrogate analysis on the TS engagement time series
saves arrays"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from similaritymeasures import dtw
from tqdm import tqdm

############################### USER SETTINGS ##################################
first_trial = 7
last_trial = 24 + 1 #keep +1 for pythonic indexing
num_trials = last_trial - first_trial
################################################################################


def main():
    cwd = os.path.dirname(__file__) # current working directory
    wd = Path(cwd).parents[0] # project working directory
    humanDataDir = os.path.join(wd,'OtherResults\TS_Dynamic_Policy_JEP\Human') # directory containing human-human TSp data
    human_human_sessions = os.listdir(humanDataDir)
    num_humanhumanSessions = len(human_human_sessions)
    
    AA_types = ["\Heuristic", "\Human-Sensitive", "\SelfPlay"]

    # this block will create a dictionary with the AA sessions for each AA type
    AA_sessions = {}
    for AA_type in AA_types:
        AA_path = os.path.join(wd,'RAW_EXPERIMENT_DATA\HUMAN-AA_TEAM'+AA_type)
        lowest_level_dirs = list()
        for root,dirs,files in os.walk(AA_path):
            if not dirs:
                lowest_level_dirs.append(Path(root).parent.name)
        AA_sessions[AA_type[1:]] = lowest_level_dirs

    #print(AA_sessions)

    # for each session, you want an array of num_trials normalised DTW scores
    # initialise arrays to store the binary traces
    #create a dictionary to store the normalised DTW scores for each human in the human-AA sessions
    human_scores = {}
    for human_type in AA_types:
        for session in AA_sessions[human_type[1:]]:
            human_scores[session] = np.zeros(num_trials)
    #print(human_scores)

    # for each session, you want an array of num_trials normalised DTW scores
    # initialise arrays to store the binary traces
    #create a dictionary to store the normalised DTW scores for each AA in the human-AA sessions
    AA_scores = {}
    for AA_type in AA_types:
        for session in AA_sessions[AA_type[1:]]:
            AA_scores[session] = np.zeros(num_trials)


    humanTeamScores = np.zeros((num_humanhumanSessions, num_trials)) #there are num_humanhumanSessions human-human sessions and num_trials trials per session

    for count, evaluee_session in enumerate(human_human_sessions): #loop over single human-human sessions
        print("\n Evaluee session: ", count+1, " of ", len(human_human_sessions))
        background_sessions = [session for session in human_human_sessions if session != evaluee_session]
        for player in (0,1): #player 0 and player 1 start off in predetermined positions each trial
            for trial in range(first_trial,last_trial): #loop over trials
                print('\r'+"Processing trial "+ str(trial)+ " for player "+ str(player))
                trial_ID = "_"+str(trial)  #"{:02}".format(trial)
                backgroundFilePaths = [[path for path in Path(humanDataDir+'\\'+background_session).rglob('*trialIdentifier'+trial_ID+'*')] for background_session in background_sessions]
                evalFile = [path for path in Path(humanDataDir+'\\'+evaluee_session).rglob('*trialIdentifier'+trial_ID+'*')][0]     
                evalueeData = pd.read_csv(evalFile)   


                for subFolder in ["\HumanPlayer0", "\HumanPlayer1"]:
                    for _, AA_type in enumerate(AA_types):
                        expDir = os.path.join(wd, 'OtherResults\Actual_Dynamic_Policies_HumanAA'+AA_type)
                        expFiles = [path for path in Path(expDir+subFolder).rglob('*trialIdentifier'+trial_ID+'*')]
                        for expFile in tqdm(expFiles) : #include a progress bar

                            session_name = Path(expFile).parent.name
                            AAteamData = pd.read_csv(expFile)

                            numTargets = int(AAteamData['numTargs'][0])
                            taCols = ["TA%d" % i for i in range(0,numTargets)]
                            haCol = "HA%d" % player
                            colNames = [haCol + taCol for taCol in taCols]

                            if player == 0 and subFolder == "\HumanPlayer0" or player == 1 and subFolder == "\HumanPlayer1":
                        
                                AAteamTS = [AAteamData[col].to_numpy() for col in colNames]
                                trialscount = 0
                                for backgroundFilePath in tqdm(backgroundFilePaths):
                                    try:
                                        backgroundData = pd.read_csv(backgroundFilePath[0]) #"Error reading file: not present as trial was unsuccessful. Will continue to next trial."
                                        trialscount+=1
                                    except:
                                        continue
                                    backgroundTS = [backgroundData[col].to_numpy() for col in colNames]
                                    human_scores[session_name][trial-first_trial] += 1 - dtw( np.column_stack([backgroundTS]).T, np.column_stack([AAteamTS]).T)[0] / (len(backgroundTS) * len(AAteamTS))
                                human_scores[session_name][trial-first_trial] /= trialscount
                            
                            elif player == 0 and subFolder == "\HumanPlayer1" or player == 1 and subFolder == "\HumanPlayer0":
                          
                                AAteamTS = [AAteamData[col].to_numpy() for col in colNames]
                                trialscount = 0 
                                for backgroundFilePath in tqdm(backgroundFilePaths):
                                    try:
                                        backgroundData = pd.read_csv(backgroundFilePath[0]) #print("Error reading file: not present as trial was unsuccessful. Will continue to next trial.")
                                        trialscount+=1
                                    except:
                                        continue
                                    backgroundTS = [backgroundData[col].to_numpy() for col in colNames]
                                    AA_scores[session_name][trial-first_trial] += 1 - dtw( np.column_stack([backgroundTS]).T, np.column_stack([AAteamTS]).T)[0] / (len(backgroundTS) * len(AAteamTS))
                                AA_scores[session_name][trial-first_trial] /= trialscount

                trialscount = 0
                #calculate the normalised DTW scores of each evaluee against each single background session
                for backgroundFilePath in tqdm(backgroundFilePaths):
                    try:
                        backgroundData = pd.read_csv(backgroundFilePath[0]) #print("Error reading file: not present as trial was unsuccessful. Will continue to next trial.")
                        trialscount+=1
                    except:
                        continue

                    

                    numTargets = int(backgroundData['numTargs'][0])
                    taCols = ["TA%d" % i for i in range(0,numTargets)]
                    haCol = "HA%d" % player
                    headersHA = [haCol + taCol for taCol in taCols]

                    backgroundTS = [backgroundData[col].to_numpy() for col in headersHA]
                    evalueeTS =  [evalueeData[col].to_numpy() for col in headersHA]    #evalueeData['HA%d_engagement' % (player)]

                    humanTeamScores[count][trial-first_trial] += 1 - dtw( np.column_stack([backgroundTS]).T, np.column_stack([evalueeTS]).T)[0] / (len(backgroundTS) * len(evalueeTS))
                humanTeamScores[count][trial-first_trial] /= trialscount
        


    humanTeamScores /= 2 #divide by 2 as there are 2 players in each human-human session
    humanTeamScores =  humanTeamScores.mean(axis = 1) #take average across trials, preserve sessions axis
    return humanTeamScores, human_scores, AA_scores
            


if __name__ == "__main__":
    humanTeamScores, human_scores, AA_scores = main()
    AA_scores_heur = []
    AA_scores_hybr = []
    AA_scores_self = []
    human_scores_heur = []
    human_scores_hybr = []
    human_scores_self = []
    for session in AA_scores.keys():
        # if session starts with Session1
        if session.startswith("Session1"):
            AA_scores_heur.append(AA_scores[session].mean())
            human_scores_heur.append(human_scores[session].mean())
        elif session.startswith("Session2"):
            AA_scores_hybr.append(AA_scores[session].mean())
            human_scores_hybr.append(human_scores[session].mean())
        elif session.startswith("Session3"):
            AA_scores_self.append(AA_scores[session].mean())
            human_scores_self.append(human_scores[session].mean())

    AA_scores_heur = np.array(AA_scores_heur) 
    AA_scores_hybr = np.array(AA_scores_hybr) 
    AA_scores_self = np.array(AA_scores_self) 

    human_scores_heur = np.array(human_scores_heur) 
    human_scores_hybr = np.array(human_scores_hybr) 
    human_scores_self = np.array(human_scores_self) 


    #save the human team traces
    np.save("humanTeamDTWs.npy", humanTeamScores)

    # save the AA_scores
    np.save("AA_scores_heur.npy", AA_scores_heur)
    np.save("AA_scores_hybr.npy", AA_scores_hybr)
    np.save("AA_scores_self.npy", AA_scores_self)

    #save the human scores
    np.save("human_scores_heur.npy", human_scores_heur)
    np.save("human_scores_hybr.npy", human_scores_hybr)
    np.save("human_scores_self.npy", human_scores_self)
