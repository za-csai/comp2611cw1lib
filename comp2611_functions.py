import math as mt
import pandas as pd
import numpy as np

def compare_2_results(result1, result2):
	term_cond1 = result1['result']['termination_condition']
	path_len1 = result1['result']['path_length']
	nodes_gen1 = result1['search_stats']['nodes_generated']
	nodes_test1 = result1['search_stats']['nodes_tested']
	nodes_disc1 = result1['search_stats']['nodes_discarded']
	states_seen1 = result1['search_stats']['distinct_states_seen']
	time_taken1 = result1['search_stats']['time_taken']

	term_cond2 = result2['result']['termination_condition']
	path_len2 = result2['result']['path_length']
	nodes_gen2 = result2['search_stats']['nodes_generated']
	nodes_test2 = result2['search_stats']['nodes_tested']
	nodes_disc2 = result2['search_stats']['nodes_discarded']
	states_seen2 = result2['search_stats']['distinct_states_seen']
	time_taken2 = result2['search_stats']['time_taken']

	df = pd.DataFrame({
    	'': ['Termination Condition', 'Path Length', 'Nodes Generated', 'Nodes Tested',
         	'Nodes Discarded', 'Distinct States Seen', 'Time Taken (seconds)'],
    	'Result 1': [term_cond1, path_len1, nodes_gen1, nodes_test1,
                 	nodes_disc1, states_seen1, time_taken1],
    	'Result 2': [term_cond2, path_len2, nodes_gen2, nodes_test2,
                 	nodes_disc2, states_seen2, time_taken2]
	})
	print(df)
	print("\n")

def compare_results_percentage(result1, result2):
	term_cond1 = result1['result']['termination_condition']
	path_len1 = result1['result']['path_length']
	nodes_gen1 = result1['search_stats']['nodes_generated']
	nodes_test1 = result1['search_stats']['nodes_tested']
	nodes_disc1 = result1['search_stats']['nodes_discarded']
	states_seen1 = result1['search_stats']['distinct_states_seen']
	time_taken1 = result1['search_stats']['time_taken']

	term_cond2 = result2['result']['termination_condition']
	path_len2 = result2['result']['path_length']
	nodes_gen2 = result2['search_stats']['nodes_generated']
	nodes_test2 = result2['search_stats']['nodes_tested']
	nodes_disc2 = result2['search_stats']['nodes_discarded']
	states_seen2 = result2['search_stats']['distinct_states_seen']
	time_taken2 = result2['search_stats']['time_taken']

	df = pd.DataFrame({
    	'': ['Termination Condition', 'Path Length', 'Nodes Generated', 'Nodes Tested',         	'Nodes Discarded', 'Distinct States Seen', 'Time Taken (seconds)'],
    	'Result 1': [term_cond1, path_len1, nodes_gen1, nodes_test1,                 	nodes_disc1, states_seen1, time_taken1],
    	'Result 2': [term_cond2, path_len2, nodes_gen2, nodes_test2,                 	nodes_disc2, states_seen2, time_taken2]
	})

	for i in range(1, len(df)):
    	if isinstance(df.iloc[i]['Result 1'], (int, float)) and isinstance(df.iloc[i]['Result 2'], (int, float)):
        	diff = df.iloc[i][Colab'Result 2'] - df.iloc[i]['Result 1']
        	perc_diff = diff / df.iloc[i]['Result 1'] * 100 if df.iloc[i]['Result 1'] != 0 else 'N/A'
        	df.loc[i, 'Numerical Difference'] = diff
        	df.loc[i, 'Difference (%)'] = perc_diff
    	else:
        	df.loc[i, 'Numerical Difference'] = 'N/A'
        	df.loc[i, 'Difference (%)'] = 'N/A'
       	 
	print(df)
	print("\n")



#Returns the number of misplaced tiles in the given state, compared to the goal state

def misplaced_tiles(state):

  # initialize misplaced_tiles counter to 0
  misplaced_tiles = 0

  # extract layout from state representation
  layout = state[1]

  # iterate over the tiles in the current state
  for i in range(0,3):
    for j in range(0,3):
      # compare current tile value to the corresponding goal tile value
      if layout[i][j] != GOAL_STATE[i][j]:
        # if they don't match, increment misplaced_tiles
        misplaced_tiles += 1

  return misplaced_tiles 

#Returns the sum of the Manhattan distances of all tiles in the given state, compared to the goal state
def manhattan(state):

  # initialize manhattan_distance counter to 0
  manhattan_distance = 0

  # extract layout from state representation
  layout = state[1]
  
  # iterate over the tiles in the current state
  for i in range(0,3):
    for j in range(0,3):
      # if the tile is not the blank tile
      if layout[i][j] != 0:

        # get the position of the current tile in the goal state
        goal_i, goal_j = number_position_in_layout(layout[i][j], GOAL_STATE)
        
        # calculate the Manhattan distance between the current tile and its corresponding goal tile
        manhattan_distance += mt.sqrt(abs(i - goal_i)**2 + abs(j - goal_j)**2)

  return manhattan_distance