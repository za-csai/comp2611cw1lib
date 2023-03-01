
# -- Package Imports --

# libraries
import math as mt
from copy import deepcopy
import pandas as pd
import numpy as np

# search modules
!mkdir -p bbmodcache
!curl http://bb-ai.net.s3.amazonaws.com/bb-python-modules/bbSearch.py > bbmodcache/bbSearch.py
from bbmodcache.bbSearch import SearchProblem, search

# -- Function and Global Variable Definitions -- 


# Global Variables

# end goal state
GOAL_STATE = [ [1,2,3],
               [4,5,6],
               [7,8,0] ]

# we provide 3 levels of start state

# easy case - 5 moves required
EASY_START = [ [4,1,3],
               [0,2,5],
               [7,8,6] ]

# medium case - 14 moves required
MEDIUM_START = [ [7,4,1],
                 [8,5,3],
                 [0,2,6] ]


# worst case - 31 moves required
WORST_START = [ [8,6,7],
                [2,5,4],
                [3,0,1] ]

# Utility Functions

# returns the position of a given cell in a given layout
def number_position_in_layout( n, layout):
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val==n:
                return (i,j)


# returns the cost to get to a given state along a given action path
def cost(path, state):
        return len(path)



# Heuristics 

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




# -- Eight-Puzzle Class -- 

class EightPuzzle( SearchProblem ):
        
    action_dict = {
        (0,0) : [(1, 0, 'up'),    (0, 1, 'left')],
        (0,1) : [(0, 0, 'right'), (1, 1, 'up'),    (0, 2, 'left')],
        (0,2) : [(0, 1, 'right'), (1, 2, 'up')],
        (1,0) : [(0, 0, 'down'),  (1, 1, 'left'),  (2, 0, 'up')],
        (1,1) : [(1, 0, 'right'), (0, 1, 'down'),  (1, 2, 'left'), (2, 1, 'up')],
        (1,2) : [(0, 2, 'down'),  (1, 1, 'right'), (2, 2, 'up')],
        (2,0) : [(1, 0, 'down'),  (2, 1, 'left')],
        (2,1) : [(2, 0, 'right'), (1, 1, 'down'),  (2, 2, 'left')],
        (2,2) : [(2, 1, 'right'), (1, 2, 'down')]
    }
    
    
    def __init__(self, initial_layout, goal_layout ):
        pos0 = number_position_in_layout( 0, initial_layout )
        # Initial state is pair giving initial position of space
        # and the initial tile layout.
        self.initial_state = ( pos0, initial_layout)
        self.goal_layout   = goal_layout
        

    ### I just use the position on the board (state[0]) to look up the 
    ### appropriate sequence of possible actions.
    def possible_actions(self, state ):
        actions =  EightPuzzle.action_dict[state[0]]
        actions_with_tile_num = []
        for r, c, d in actions:
            tile_num = state[1][r][c] ## find number of moving tile
            # construct the action representation including the tile number
            actions_with_tile_num.append( (r, c, (tile_num,d)) )
        return actions_with_tile_num

    def successor(self, state, action):
        old0row, old0col  =  state[0]    # get start position
        new0row, new0col, move = action  # unpack the action representation
        moving_number, _ = move
        ## Make a copy of the old layout
        newlayout = deepcopy(state[1])
        # Swap the positions of the new number and the space (rep by 0)
        newlayout[old0row][old0col] = moving_number
        newlayout[new0row][new0col] = 0
        return ((new0row, new0col), newlayout )
    
    def goal_test(self,state):
        return state[1] == self.goal_layout
    
    def display_action(self, action):
        _,_, move = action
        tile_num, direction = move
        print("Move tile", tile_num, direction)
        
    def display_state(self,state):
        for row in state[1]:
            nums = [ (n if n>0 else '.') for n in row]
            print( "   ", nums[0], nums[1], nums[2] )
            
            



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
        '': ['Termination Condition', 'Path Length', 'Nodes Generated', 'Nodes Tested', 'Nodes Discarded', 'Distinct States Seen', 'Time Taken (seconds)'],
        'Result 1': [term_cond1, path_len1, nodes_gen1, nodes_test1, nodes_disc1, states_seen1, time_taken1],
        'Result 2': [term_cond2, path_len2, nodes_gen2, nodes_test2, nodes_disc2, states_seen2, time_taken2]
    })

    for i in range(1, len(df)):
        if isinstance(df.iloc[i]['Result 1'], (int, float)) and isinstance(df.iloc[i]['Result 2'], (int, float)):
            diff = df.iloc[i]['Result 2'] - df.iloc[i]['Result 1']
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