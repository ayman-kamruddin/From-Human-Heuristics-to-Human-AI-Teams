#this script takes in the scores: binary trace or TSp overlap, and converts them to the format
#needed for further analysis.


import os
import numpy as np
import pandas as pd
from pathlib import Path

cwd = os.path.dirname(__file__) # current working directory
wd = Path(cwd).parents[0] # project working directory

#read in AA_scores_heur.csv, human_scores_heur.csv and humanTeamTraces.csv(or humanTeamDTWs.csv) files from ../OtherResults/appropriate_folder
#where appropriate_folder is one of "TSp_DTWs" or "binaryTraceOverlaps"


input_folder = "TSp_DTWs" # one of "TSp_DTWs" or "binaryTraceOverlaps"

AA_scores_heur = pd.read_csv(os.path.join(wd,'OtherResults\\'+input_folder+'\\AA_scores_heur.csv'))
human_scores_heur = pd.read_csv(os.path.join(wd,'OtherResults\\'+input_folder+'\\human_scores_heur.csv'))

if input_folder == "binaryTraceOverlaps":
    humanTeamScores = pd.read_csv(os.path.join(wd,'OtherResults\\'+input_folder+'\\humanTeamTraces.csv'))
else:
    humanTeamScores = pd.read_csv(os.path.join(wd,'OtherResults\\'+input_folder+'\\humanTeamDTWs.csv'))



# Ensure 'pair' column exists
for df in [AA_scores_heur, human_scores_heur, humanTeamScores]:
    if 'pair' not in df.columns:
        df.insert(0, 'pair', range(len(df)))  # Create an index-based pair column


# merge all the files into one file maintain columns and add a column for 
# agent_type = Huuman if file is human_scores_heur
# agent_type = Artificial if file is AA_scores_heur
# agent_type = Surrogate if file is humanTeamScores
# save file as human_AHA_binarytracescores_heur.csv

"""
File should look like:

pair	agent_type	7	8	9	10	11 ....
0	Human	0.965811966	0.875457875	0.823412698	0.640394089	0.523809524 ....
1	Human	0.823708207	0.986666667	0.884711779	0.87394958	0.966318235 ....
2	Human	0.991666667	0.835164835	0.827664399	0.640350877	0.913770914 ....
3	Human	0.844047619	0.718518519	0.776830135	0.932539683	0.945887446 ....
4	Human	0.946550049	0.863095238	0.926894702	0.615186615	0.880519481 ....
5	Human	0.849012776	0.89047619	0.940035273	0.833976834	0.447350771 ....
6	Human	0.945736434	0.904761905	0.914285714	0.805059524	0.765151515 ....
...
"""

# add agent_type column to each file
AA_scores_heur['agent_type'] = 'Artificial'
human_scores_heur['agent_type'] = 'Human'   
humanTeamScores['agent_type'] = 'Surrogate'


# merge the files
all_scores = pd.concat([human_scores_heur, AA_scores_heur,
                        humanTeamScores], ignore_index=True)

#columns should be
#pair, agent_type, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24

#make sure first column is pair
all_scores = all_scores[['pair', 'agent_type', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                         '17', '18', '19', '20', '21', '22', '23', '24']]
# save the file
if input_folder == "binaryTraceOverlaps":
    all_scores.to_csv(os.path.join(wd,'OtherResults/'+input_folder+'/human_AHA_binarytracescores_heur.csv'), index=False)
else:
    all_scores.to_csv(os.path.join(wd,'OtherResults/'+input_folder+'/human_AHA_TSpDTWscores_heur.csv'), index=False)
