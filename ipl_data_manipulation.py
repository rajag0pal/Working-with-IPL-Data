# -*- coding: utf-8 -*-
"""IPL_Data_Manipulation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1useMJUSTD8Zs1dowj01cAvvCvYn0TiM6

## **IPL DATA**
"""

import pandas as pd
import numpy as np
import seaborn as sn
sn.set_style('darkgrid')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('IPL_Data_IPL.csv')

data.shape

data.columns

data.dtypes

data.isnull().sum()

data.head()

data.tail()

data['batting_team'].unique()

data_copy = data.copy()

"""## **Data Manipulation - Part**"""

first_innings_score = data_copy['total_runs'][data_copy['inning'] == 1].groupby(by=data_copy['match_id']).sum()

second_innings_score = data_copy['total_runs'][data_copy['inning'] == 2].groupby(by=data_copy['match_id']).sum()

first_innings_score

second_innings_score

first_innings_team = data_copy['batting_team'][data_copy['inning'] == 1].groupby(by=data_copy['match_id']).unique()

second_innings_team = data_copy['bowling_team'][data_copy['inning'] == 1].groupby(by=data_copy['match_id']).unique()

First_innings = []
for i in first_innings_team:
  First_innings.append(i[0])

Second_innings = []
for j in second_innings_team:
  Second_innings.append(j[0])

Match_data = pd.DataFrame(columns = ['First Innings', 'Second Innings', 'First Innings Score', 'Second Innings Score'])

Match_data['First Innings'] =  first_innings_team
Match_data['Second Innings'] = second_innings_team
Match_data['First Innings Score'] = first_innings_score
Match_data['Second Innings Score'] = second_innings_score

Match_data.columns

"""### Function to Label Winner"""

def winner(x):
  if(x['First Innings Score'] > x['Second Innings Score']):
    return x['First Innings']
  elif(x['First Innings Score'] == x['Second Innings Score']):
    return 'Tie'
  else:
    return x['Second Innings']

Winner = []

for i in range(len(Match_data)):
  result = winner(Match_data.iloc[i])
  Winner.append(result[0])

Match_data['First Innings'] = First_innings
Match_data['Second Innings'] = Second_innings
Match_data['Winner'] = Winner

Match_data.shape

Match_data = Match_data.reset_index()

Match_data

def win_binary_one(x):
  if(x['Winner'] == x['First Innings']):
    return 1
  elif(x['Winner'] == 'Tie'):
    return 'T'
  else:
    return 0

def win_binary_two(x):
  if(x['Winner'] == x['Second Innings']):
    return 1
  elif(x['Winner'] == 'Tie'):
    return 'T'
  else:
    return 0

First_Inning_Wins = []
for i in range(len(Match_data)):
  result = win_binary_one(Match_data.iloc[i])
  First_Inning_Wins.append(result)

len(First_Inning_Wins)

Second_Inning_Wins = []
for i in range(len(Match_data)):
  result = win_binary_two(Match_data.iloc[i])
  Second_Inning_Wins.append(result)

len(Second_Inning_Wins)

Match_data['Batting wins'] = First_Inning_Wins
Match_data['Bowling wins'] = Second_Inning_Wins

Match_data

"""## **Batsmen Data set**

> Runs Scored
"""

Batsmen_runs = data_copy['batsman_runs'].groupby(by = data_copy['batsman']).sum()
Batsmen_runs = Batsmen_runs.to_dict()

Batsmen_group = data_copy['batsman'].groupby(by = data_copy['batsman']).all()
Batsmen_group = Batsmen_group.to_dict()
Batsmen = Batsmen_group.keys()

Batsmen_data = pd.DataFrame(columns = ['Batsmen','Runs'])

Batsmen_data['Batsmen'] = Batsmen
Batsmen_data['Runs'] = Batsmen_runs.values()

Batsmen_data.head()

Batsmen_data_sorted = Batsmen_data.sort_values(by = 'Runs', ascending = False)

"""

> Balls Faced
"""

Batsmen_balls_faced = data_copy['batsman'].groupby(by = data_copy['batsman']).count()
Batsmen_balls_faced = Batsmen_balls_faced.to_dict()

Batsmen_data['Balls Faced'] = Batsmen_balls_faced.values()

Batsmen_data.head()

Balls_faced_sorted = Batsmen_data.sort_values(by = 'Balls Faced', ascending = False)

Balls_faced_sorted.head(5)

"""

> Strike Rate

"""

Batsmen_data['Strike Rate'] = Batsmen_data['Runs']/Batsmen_data['Balls Faced']*100

Batsmen_data.head(10)

Batsmen_data.sort_values(by = 'Strike Rate', ascending = False)

"""

> Matches Played (Batted)

"""

players_played_at_evry_matches = data_copy['batsman'].groupby(by = data_copy['match_id']).unique()

len(players_played_at_evry_matches)

players_played_at_evry_matches.iloc[0]

len(players_played_at_evry_matches)

total_players = []
for matches in players_played_at_evry_matches:
  for players in matches:
    total_players.append(players)

len(total_players)

temp = pd.DataFrame()
temp['Players'] = total_players

matches_played = temp.value_counts(sort = False).to_dict()

Batsmen_data['Matches Played'] = matches_played.values()

Batsmen_data.sort_values(by = 'Matches Played', ascending = False).head(5)

"""

> Number of 6 hits
"""

Sixes = data_copy['batsman'][data_copy['batsman_runs'] == 6].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Sixes'] = Batsmen_data['Batsmen'].map(Sixes)
Batsmen_data['Sixes'] = Batsmen_data['Sixes'].fillna(0)
Batsmen_data['Sixes'] = Batsmen_data['Sixes'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Number of 4 hits

"""

Fours = data_copy['batsman'][data_copy['batsman_runs'] == 4].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Fours'] = Batsmen_data['Batsmen'].map(Fours)
Batsmen_data['Fours'] = Batsmen_data['Fours'].fillna(0)
Batsmen_data['Fours'] = Batsmen_data['Fours'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Number of Triples

"""

Triples = data_copy['batsman'][data_copy['batsman_runs'] == 3].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Triples'] = Batsmen_data['Batsmen'].map(Triples)
Batsmen_data['Triples'] = Batsmen_data['Triples'].fillna(0)
Batsmen_data['Triples'] = Batsmen_data['Triples'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Number of Doubles

"""

Doubles = data_copy['batsman'][data_copy['batsman_runs'] == 2].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Doubles'] = Batsmen_data['Batsmen'].map(Doubles)
Batsmen_data['Doubles'] = Batsmen_data['Doubles'].fillna(0)
Batsmen_data['Doubles'] = Batsmen_data['Doubles'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""Number of Singles"""

Singles = data_copy['batsman'][data_copy['batsman_runs'] == 1].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Singles'] = Batsmen_data['Batsmen'].map(Singles)
Batsmen_data['Singles'] = Batsmen_data['Singles'].fillna(0)
Batsmen_data['Singles'] = Batsmen_data['Singles'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Number of Dismissals

"""

Dismissals = data_copy['player_dismissed'].value_counts(sort = False).to_dict()
Batsmen_data['Dismissals'] = Batsmen_data['Batsmen'].map(Dismissals)
Batsmen_data['Dismissals'] = Batsmen_data['Dismissals'].fillna(0)
Batsmen_data['Dismissals'] = Batsmen_data['Dismissals'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Type of Dismissals

"""

data_copy['dismissal_kind'].unique()

"""

> Caught

"""

Caught = data_copy['batsman'][data_copy['dismissal_kind'] == 'caught'].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Caught'] = Batsmen_data['Batsmen'].map(Caught)
Batsmen_data['Caught'] = Batsmen_data['Caught'].fillna(0)
Batsmen_data['Caught'] = Batsmen_data['Caught'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Bowled

"""

Bowled = data_copy['batsman'][data_copy['dismissal_kind'] == 'bowled'].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['Bowled'] = Batsmen_data['Batsmen'].map(Bowled)
Batsmen_data['Bowled'] = Batsmen_data['Bowled'].fillna(0)
Batsmen_data['Bowled'] = Batsmen_data['Bowled'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> Run Out

"""

RunOut = data_copy['batsman'][data_copy['dismissal_kind'] == 'run out'].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['RunOut'] = Batsmen_data['Batsmen'].map(RunOut)
Batsmen_data['RunOut'] = Batsmen_data['RunOut'].fillna(0)
Batsmen_data['RunOut'] = Batsmen_data['RunOut'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""

> LBW

"""

LBW = data_copy['batsman'][data_copy['dismissal_kind'] == 'lbw'].groupby(by = data_copy['batsman']).count().to_dict()
Batsmen_data['LBW'] = Batsmen_data['Batsmen'].map(LBW)
Batsmen_data['LBW'] = Batsmen_data['LBW'].fillna(0)
Batsmen_data['LBW'] = Batsmen_data['LBW'].apply(lambda x : int(x))
Batsmen_data.head(5)

"""## Match Summary"""

ids = list(set(data_copy['match_id']))

def match_summary(x, match_id):
  
  x = data_copy[data_copy['match_id'] == match_id]

  teams = [set(x['batting_team'][x['inning']==1]),set(x['batting_team'][x['inning']==2])]

  runs_in_one = x['batsman_runs'][x['inning'] == 1].groupby(by = x['batsman'], sort = False).sum().to_dict()
  runs_in_two = x['batsman_runs'][x['inning'] == 2].groupby(by = x['batsman'], sort = False).sum().to_dict()
  batsman_runs = [runs_in_one,runs_in_two]

  wkts_in_one = x['player_dismissed'][x['inning'] == 1].groupby(by = x['bowler'], sort = False).count().to_dict()
  wkts_in_two = x['player_dismissed'][x['inning'] == 2].groupby(by = x['bowler'], sort = False).count().to_dict()
  bowler_wickets = [wkts_in_one,wkts_in_two]

  bow_runs_in_one = x['total_runs'][x['inning'] == 1].groupby(by = x['bowler'], sort = False).sum().to_dict()
  bow_runs_in_two = x['total_runs'][x['inning'] == 2].groupby(by = x['bowler'], sort = False).sum().to_dict()
  bowler_runs = [bow_runs_in_one,bow_runs_in_two]

  extras_in_one = x['extra_runs'][x['inning'] == 1].groupby(by = x['bowler'], sort = False).sum().to_dict()
  extras_in_two = x['extra_runs'][x['inning'] == 2].groupby(by = x['bowler'], sort = False).sum().to_dict()
  extras = [extras_in_one,extras_in_two]

  wickets_in_one = sum(wkts_in_one.values())
  wickets_in_two = sum(wkts_in_two.values())
  fall_of_wickets = [wickets_in_one, wickets_in_two]
  
  score_in_one = x['total_runs'][x['inning'] == 1].sum()
  score_in_two = x['total_runs'][x['inning'] == 2].sum()
  scores = [score_in_one, score_in_two]

  if score_in_one>score_in_two:
    winner = set(x['batting_team'][x['inning'] == 1])
  elif score_in_one == score_in_two:
    winner = {'Tie'}
  else:
    winner = set(x['batting_team'][x['inning'] == 2])
 
  return [teams, batsman_runs,bowler_wickets,bowler_runs,extras,scores,fall_of_wickets,winner]

"""The above function will return following fields:
  - Teams order by Innings (1st Innings, 2nd Innings)
  - Batsman Runs order by Innings (1st Innings, 2nd Innings)
  - Bowler wickets order by Innings (1st Innings, 2nd Innings)
  - Bowler Runs order by Innings (1st Innings, 2nd Innings)
  - Extras order by Innings (1st Innings, 2nd Innings)
  - Scores order by Innings (1st Innings, 2nd Innings)
  - Wickets order by Innings (1st Innings, 2nd Innings)
  - Winner
"""

total_summary = []
for match_id in ids:
  summary = match_summary(data_copy, match_id)
  total_summary.append(summary)

total_summary[197] #summary for match number 197

"""## Players Fifties & Hundreds"""

score_card = []
for i in range(755):
  score_card.append(total_summary[i][1])

def batting_summary(x, match_id):
  x = data_copy[data_copy['match_id'] == match_id]
  batting = x['batsman_runs'].groupby(by = x['batsman'], sort = False).sum().to_dict()
  return batting

total_batting = []
for match_id in ids:
  res = batting_summary(data_copy, match_id)
  total_batting.append(res)

total_batting[:2]

Batting_scores = pd.DataFrame(total_batting)
Batting_score = Batting_scores.fillna(0)
Batting_score.head()

Maximums = {'Players':[], 'Fifties':[], 'Hundred':[], 'One_Fifties': [], 'Two_Hundred': []}
for players in Batting_score.columns:
  fifties = Batting_score[players][(Batting_score[players]>=50) & (Batting_score[players]<=99)].count()
  hundreds = Batting_score[players][(Batting_score[players]>=100) & (Batting_score[players]<=149)].count()
  one_fiftys = Batting_score[players][(Batting_score[players]>=150) & (Batting_score[players]<=199)].count()
  two_hundreds = Batting_score[players][(Batting_score[players]>=200) & (Batting_score[players]<=300)].count()
  Maximums['Players'].append(players)
  Maximums['Fifties'].append(fifties)
  Maximums['Hundred'].append(hundreds)
  Maximums['One_Fifties'].append(one_fiftys)
  Maximums['Two_Hundred'].append(two_hundreds)

Player_records = pd.DataFrame(Maximums).sort_values(by = 'Players')

Player_records = Player_records.reset_index(drop = True)
#Player_records = Player_records.drop(['index','level_0'], axis = 1)
Player_records.head()

Batsmen_data[['50s','100s','150s','200s']] = Player_records[['Fifties','Hundred','One_Fifties','Two_Hundred']]
Batsmen_data.head(10)

Batsmen_data['Bp6'] = Batsmen_data['Balls Faced']/Batsmen_data['Sixes'] 
Batsmen_data['Bp4'] = Batsmen_data['Balls Faced']/Batsmen_data['Fours']
Batsmen_data['Bp6'] = Batsmen_data['Bp6'].apply(lambda x : round(x,2))
Batsmen_data['Bp4'] = Batsmen_data['Bp4'].apply(lambda x : round(x,2))
Batsmen_data.replace([np.inf, -np.inf],0, inplace = True)

def batting_summary(x, match_id):
  x = data_copy[data_copy['match_id'] == match_id]
  batting = x['batsman_runs'].groupby(by = x['batsman'], sort = False).sum().to_dict()
  return batting

total_batting = []
for match_id in ids:
  res = batting_summary(data_copy, match_id)
  total_batting.append(res)

flat1 = []
for ele in total_batting:
  flat1+=ele.keys()
flat2 = []
for ele in total_batting:
  flat2+=ele.values()

Batsmen_runs = pd.DataFrame(columns = ['Batsman','Runs'])
Batsmen_runs['Batsman'] = flat1
Batsmen_runs['Runs'] = flat2
Batsmen_runs_copy = Batsmen_runs.copy()
Batsmen_runs

Batsmen_runs = Batsmen_runs.sort_values(by = 'Runs', ascending = False).groupby(by = Batsmen_runs['Batsman']).max()
Batsmen_runs = Batsmen_runs.set_index(pd.Index([index for index in range(516)]))

Batsmen_data['Best'] = Batsmen_runs['Runs']

Batsmen_data.head(10)

"""## **Bowlers Data Set**"""

Bowlers_wickets = data_copy['player_dismissed'].groupby(by = data_copy['bowler']).count()
Bowlers_wickets = Bowlers_wickets.to_dict()

Bowler_group = data_copy['bowler'].groupby(by = data_copy['bowler']).all()
Bowler_group = Bowler_group.to_dict()
Bowlers = Bowler_group.keys()

Bowlers_data = pd.DataFrame(columns = ['Bowlers','Wickets'])
Bowlers_data['Bowlers'] = Bowlers
Bowlers_data['Wickets'] = Bowlers_wickets.values()

Bowlers_data.head()

Bowlers_Balls = data_copy['ball'].groupby(by = data_copy['bowler']).count()
Bowlers_Balls = Bowlers_Balls.to_dict()

Bowlers_data['Balls Bowled'] = Bowlers_Balls.values()

Bowlers_data.head()

Bowlers_data['Overs Bowled'] = Bowlers_data['Balls Bowled']/6
Bowlers_data['Overs Bowled'] = Bowlers_data['Overs Bowled'].apply(lambda x : round(x))

Bowlers_data.head()

Bowlers_data['Strike Rate'] = Bowlers_data['Balls Bowled']/Bowlers_data['Wickets']

Bowlers_data.head()

Bowlers_data.replace([np.inf, -np.inf], 0, inplace= True)

Bowlers_data[Bowlers_data['Wickets']==0]

Bowlers_extras = data_copy['extra_runs'].groupby(by = data_copy['bowler']).sum()
Bowlers_extras = Bowlers_extras.to_dict()
Bowlers_data['Extras'] = Bowlers_extras.values()

Bowlers_data.head()

Bowlers_runs = data_copy['total_runs'].groupby(by = data_copy['bowler']).sum()
Bowlers_runs = Bowlers_runs.to_dict()
Bowlers_data['Runs Conceded'] = Bowlers_runs.values()

Bowlers_data.head()

Bowlers_data['Economy'] = Bowlers_data['Runs Conceded']/Bowlers_data['Overs Bowled']
Bowlers_data['Economy'] = Bowlers_data['Economy'].apply(lambda x : round(x,2))
Bowlers_data.head()

Bowlers_dots = data_copy['total_runs'][data_copy['total_runs'] == 0].groupby(by = data_copy['bowler']).count()
Bowlers_dots = Bowlers_dots.to_dict()

Bowlers_data['Dots'] = Bowlers_data['Bowlers'].map(Bowlers_dots)
Bowlers_data['Dots'] = Bowlers_data['Dots'].fillna(0)

Bowlers_data.head(10)

def bowling_summary(x, match_id):
  x = data_copy[data_copy['match_id'] == match_id]
  bowling = x['player_dismissed'].groupby(by = x['bowler'], sort = False).sum().to_dict()
  return bowling

total_bowling = []
  for match_id in ids:
    res = bowling_summary(data_copy, match_id)
    total_bowling.append(res)

total_summary[0]

Bowlers_wkts = {'Players':[], 'Wkts':[]}
for i in range(755):
  for j in range(2):
    Bowlers_wkts['Players'].append(total_summary[i][2][j].keys())
  for t in range(2):
    Bowlers_wkts['Wkts'].append(total_summary[i][2][j].values())

def bow_summary(data_copy, match_id):
	x = data_copy[data_copy['match_id'] == match_id]
	res = x['player_dismissed'].groupby(by = x['bowler'], sort = False).count().to_dict()
	return res

def bow_summary2(data_copy, match_id):
	x = data_copy[data_copy['match_id'] == match_id]
	res = x['total_runs'].groupby(by = x['bowler'], sort = False).count().to_dict()
	return res

lis1 = []
for match_id in ids:
  result = bow_summary(data_copy, match_id)
  lis1.append(result)

lis2 = []
for match_id in ids:
  result = bow_summary2(data_copy, match_id)
  lis2.append(result)

lis1

flat1 = []
for ele in lis1:
  flat1+=ele.keys()

flat2 = []
for ele in lis1:
  flat2+=ele.values()

flat3 =[]
flat4 = []
for ele in lis2:
  flat3+=ele.keys()
for ele in lis2:
  flat4+=ele.values()

Bowlers_wickets = pd.DataFrame(columns = ['Bowler','Best'])
Bowlers_wickets['Bowler'] =  flat1
Bowlers_wickets['Best'] = flat2
Bowlers_wickets['Runs'] = flat4
Bowlers_wickets = Bowlers_wickets.sort_values(by = 'Bowler') 
Bowlers_wickets.head()

Bowlers_wickets = Bowlers_wickets.sort_values(by = 'Best', ascending = False).groupby(by = Bowlers_wickets['Bowler']).max()
Bowlers_wickets = Bowlers_wickets.set_index(pd.Index([index for index in range(405)]))
Bowlers_wickets.head()

Bowlers_data['Best'] = Bowlers_wickets['Best'].astype(str)+'/'+Bowlers_wickets['Runs'].astype(str)

Bowlers_data.tail(10)

"""## Death Overs"""

death_overs = data_copy[data_copy['over'] >=16]
death_overs = death_overs.sort_values(by = 'match_id')

death_overs_first_inning = death_overs[death_overs['inning']==1].sort_values(by = ['match_id','over','ball'])
death_overs_second_inning = death_overs[death_overs['inning']==2].sort_values(by = ['match_id','over','ball'])

death_over_data = pd.concat([death_overs_first_inning,death_overs_second_inning], axis = 0)

runs_conceded = death_over_data['total_runs'].groupby(by = death_over_data['bowler']).sum().to_dict()

wickets_taken = death_over_data['player_dismissed'].groupby(by = death_over_data['bowler']).count().to_dict()

balls = death_over_data['ball'].groupby(by = death_over_data['bowler']).count().to_dict()

dots = death_over_data['total_runs'][death_over_data['total_runs'] == 0].groupby(by = death_over_data['bowler']).count().to_dict()

Death_over_data = pd.DataFrame(columns = ['Bowlers','Runs Conceded','Wickets','Economy'])

Death_over_data['Bowlers'] = runs_conceded.keys()

Death_over_data[['Runs Conceded','Wickets',]] = [runs_conceded.values(),wickets_taken.values()]

Death_over_data['Balls'] = balls.values()
Death_over_data['Overs'] = Death_over_data['Balls']/6
Death_over_data['Economy'] = Death_over_data['Runs Conceded']/Death_over_data['Overs']
Death_over_data['Dots'] =  Death_over_data['Bowlers'].map(dots)
Death_over_data = Death_over_data.fillna(0)
Death_over_data

"""## Power Play"""

pp_overs = data_copy[data_copy['over'] <=6]
pp_overs = pp_overs.sort_values(by = 'match_id')

pp_overs_first_inning = pp_overs[pp_overs['inning']==1].sort_values(by = ['match_id','over','ball'])
pp_overs_second_inning = pp_overs[pp_overs['inning']==2].sort_values(by = ['match_id','over','ball'])

pp_over_data = pd.concat([pp_overs_first_inning,pp_overs_second_inning], axis = 0)
runs_conceded = pp_over_data['total_runs'].groupby(by = pp_over_data['bowler']).sum().to_dict()
wickets_taken = pp_over_data['player_dismissed'].groupby(by = pp_over_data['bowler']).count().to_dict()
balls = pp_over_data['ball'].groupby(by = pp_over_data['bowler']).count().to_dict()
dots = pp_over_data['total_runs'][pp_over_data['total_runs'] == 0].groupby(by = pp_over_data['bowler']).count().to_dict()
PP_over_data = pd.DataFrame(columns = ['Bowlers','Runs Conceded','Wickets','Economy'])
PP_over_data['Bowlers'] = runs_conceded.keys()
PP_over_data[['Runs Conceded','Wickets',]] = [runs_conceded.values(),wickets_taken.values()]

PP_over_data['Balls'] = balls.values()

PP_over_data['Overs'] = PP_over_data['Balls']/6

PP_over_data['Economy'] = PP_over_data['Runs Conceded']/PP_over_data['Overs']

PP_over_data['Dots'] =  PP_over_data['Bowlers'].map(dots)

PP_over_data = PP_over_data.fillna(0)

PP_over_data

PP_over_data.to_csv('PP_over_data.csv')
Death_over_data.to_csv('Death_over_data.csv')

"""## Team Analysis"""

MI_Batsmen = data_copy[data_copy['batting_team'] == 'Mumbai Indians']['batsman'].unique()
CSK_Batsmen = data_copy[data_copy['batting_team'] == 'Chennai Super Kings']['batsman'].unique()
KKR_Batsmen = data_copy[data_copy['batting_team'] == 'Kolkata Knight Riders']['batsman'].unique()
RCB_Batsmen = data_copy[data_copy['batting_team'] == 'Royal Challengers Bangalore']['batsman'].unique()

MI_won_matches = Match_data[Match_data['Winner']== 'Mumbai Indians'].index
MI_won_matches = list(MI_won_matches)

pd.DataFrame(total_summary).shape

Match_data['Winner'].shape

Match_summary = pd.DataFrame(columns = ['Winner'])

Match_summary['Winner'] = Match_data['Winner'].iloc[0:]

Match_summary = Match_summary.reset_index()
#Match_summary.drop('match_id',inplace = True,axis = 1)

Match_Summary = pd.concat([Match_summary, pd.DataFrame(total_summary)], axis = 1)

Match_Summary.drop([1,2,3,4], inplace = True, axis = 1)

Match_Summary

No_of_Batsman = []
for match in range(len(total_summary)):
  total1 = len(total_summary[match][1][0])
  total2 = len(total_summary[match][1][1])
  No_of_Batsman.append(total1)
  No_of_Batsman.append(total2)

print(No_of_Batsman)

print(First_Inning_Wins)

#First_Inning_Wins = [str(i) for i in First_Inning_Wins]

print(First_Inning_Wins)

lis = [None]*1512
lis[::2] = First_Inning_Wins
lis[1::2] = Second_Inning_Wins

len(lis)

Wins = []
for no in range(len(No_of_Batsman)):
  tem = str(lis[no])*No_of_Batsman[no]
  Wins.append(tem)

Wins = [list(g) for g in Wins]

Wins_new = []
for li in Wins:
  Wins_new+=li

print(Wins_new)

Wins_new = [int(h) for h in Wins_new]

Batsmen_runs_copy['Result'] = Wins_new

Batsmen_runs_copy.head(20)

Batsman_runs_with_results =  Batsmen_runs_copy.sort_values(by = ['Batsman','Runs'],ascending = True)

Batsman_runs_with_results.to_csv('Batsman_runs_with_results.csv')

Wins_of_players = Batsman_runs_with_results['Result'].groupby(by = Batsman_runs_with_results['Batsman']).sum().to_dict()

Batsmen_data['Wins'] = Batsmen_data['Batsmen'].map(Wins_of_players)
Batsmen_data

Batsmen_data['Wins Percentage'] = Batsmen_data['Wins']/Batsmen_data['Matches Played']*100
Batsmen_data['Wins Percentage'] = Batsmen_data['Wins Percentage'].apply(lambda x : round(x,2))

Batsmen_data.sort_values(by = 'Wins', ascending = False).head(60)

Match_data.to_csv('Match_data.csv')

Batsmen_data.to_csv('Batsmen_data.csv')

Bowlers_data.to_csv('Bowlers_data.csv')

"""## Fielders Data set"""

data_copy['dismissal_kind'].unique()

catches_by_fielders = data_copy['dismissal_kind'][data_copy['dismissal_kind']=='caught'].groupby(by = data_copy['fielder']).count().to_dict()
run_out_by_fielders = data_copy['dismissal_kind'][data_copy['dismissal_kind']=='run out'].groupby(by = data_copy['fielder']).count().to_dict()

Fielders_data = pd.DataFrame(columns = ['Fielders','Catches'])

Fielders_data['Fielders'] = catches_by_fielders.keys()
Fielders_data['Catches'] = catches_by_fielders.values()
Fielders_data['Run Outs'] = Fielders_data['Fielders'].map(run_out_by_fielders)
Fielders_data['Run Outs'] = Fielders_data['Run Outs'].fillna(0)
Fielders_data['Run Outs'] = Fielders_data['Run Outs'].apply(lambda x: int(x))
Fielders_data

Fielders_data.to_csv('Fielders_data.csv')

Player_clash = data_copy[['bowler','player_dismissed']].dropna().sort_values(by = ['bowler','player_dismissed'])
Player_clash.to_csv('Players_clash.csv')

"""##**----------------------------------------End of Data Preparation --------------------------------**"""