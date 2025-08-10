Note that there are several scripts with the suffix _v1 or _v2. v1 refers to the TSp calculation with multiple engagements, and v2 refers to the TSp with the closest engagement only.

There are several files here and here is the order that you should run them in:

Generate your own simulation data using the simulation build (NEEDS WORK) or use the simulated data presented in the folder, present in `OtherResults\AA-AA_SimulationData`.

Run `simReader-AA_AA.ipynb` to get a feel for what the data looks like. This will generate plots as well. 


### For TSp overlap in Exp 1:

a. Run `get_actual_TS_Dynamic_Policy_as_csv.py` to get the dynamic policies.  
b. Run `compare_dynamic_policies_by_TA_and_Participant_TS_DTW.py` to get the normalized DTW values.  
c. Use the normalised DTW values to get the box plots using `exp1_TSOverlap_Analysis.ipynb`. This will also prepare the data into the format needed for the final R analysis.  
d. Run the R analysis using `mixed_linear_model_exp1.r`.  

### For binary trace comparison in Exp 1:

a. Run `binary_trace_evaluator_Exp1.py` to get trace values.  
b. Run `exp1_BinaryTrace_Analysis.ipynb` with the correct filepaths.  
c. Run the R analysis using `mixed_linear_model_exp1.r` commenting and uncommenting out the input file names.  

### For the TSp in Exp 2:

This statistical test, and the box plot it makes, uses the:
1. Surrogate human data: Human data compared to itself. This was done by taking one pair out at a time, then averaging over all pairs.
2. Human data from human-AA pairs compared to Exp 1's human-human data
3. AA data from human-AA pairs compared to Exp 1's human-human data

a. First, run `get_actual_Dynamic_Policy_as_csv_Human-AA.py`. This will get you the TSp binary encoded vectors per trial for all agent types (Heuristic, Human-Sensitive and SelfPlay) and their corresponding human team-mates.  
b. To prepare the dataset required for this, run `calcAllDTW.py`. This will save data in .csv format.  
c. Use `human_scores_heur.csv`, `AA_scores_heur.csv` and `humanTeamDTWs.csv` to run the stats. First, convert them into a format suitable for the stats using `convert_scores_exp2.py`.  
d. You can use `exp2_TargetOverlap_Analysis.ipynb`  to get the box plot.  
e. Use `R_Analysis_Exp2.R` to run the stats.  


### For the binary trace in Exp 2:

This is done in a similar manner to the TSp for Exp 2, except that instead of comparing TSp overlap, it compares the Binary trace scores.

a. Use `traj_evals_binary_trace_scores.py` to get the binary traces. This will also save the files required for the next article, in `OtherResults\binaryTraceOverlaps\`.  
b. Then convert `AA_scores_heur.csv`, `human_scores_heur.csv` and `humanTeamTraces.csv` to the format needed for the stats using `convert_scores_exp2.py`.  
c. Use `exp2_BinaryTrace_Analysis.ipynb`  to get the box plot.  
d. Use `R_Analysis_Exp2.R` to run the stats.
