import pandas as pd

#Creating dataframes for each csv file
batting_raw = pd.read_csv('batters.csv')
all_rounder_raw = pd.read_csv('all_rounders.csv')
bowling_raw = pd.read_csv('bowlers.csv')
team_raw = pd.read_csv('team_season.csv')

#-------TEAM SCORE CODE---------

#Modification of team.season.csv to include win percentage and dropping wins and losses columns
team_raw['win_percentage_2023'] = round((team_raw['wins_2023']/(team_raw['wins_2023']+team_raw['losses_2023']))*100,4)
team_raw['win_percentage_2024'] = round((team_raw['wins_2024']/(team_raw['wins_2024']+team_raw['losses_2024']))*100,4)
team_raw['win_percentage_2025'] = round((team_raw['wins_2025']/(team_raw['wins_2025']+team_raw['losses_2025']))*100,4)
team_mod = team_raw.drop(columns = ['wins_2023', 'losses_2023','wins_2024','losses_2024','wins_2025','losses_2025'])


#Normalization of NRR, Win Percentage, and Standings
team_mod['nrr_2023'] = round((team_mod['nrr_2023']-team_mod['nrr_2023'].min())/(team_mod['nrr_2023'].max()-team_mod['nrr_2023'].min()),4)
team_mod['nrr_2024'] = round((team_mod['nrr_2024']-team_mod['nrr_2024'].min())/(team_mod['nrr_2024'].max()-team_mod['nrr_2024'].min()),4)
team_mod['nrr_2025'] = round((team_mod['nrr_2025']-team_mod['nrr_2025'].min())/(team_mod['nrr_2025'].max()-team_mod['nrr_2025'].min()),4)
team_mod['win_percentage_2023'] = round((team_mod['win_percentage_2023']-team_mod['win_percentage_2023'].min())/(team_mod['win_percentage_2023'].max()-team_mod['win_percentage_2023'].min()),4)
team_mod['win_percentage_2024'] = round((team_mod['win_percentage_2024']-team_mod['win_percentage_2024'].min())/(team_mod['win_percentage_2024'].max()-team_mod['win_percentage_2024'].min()),4)
team_mod['win_percentage_2025'] = round((team_mod['win_percentage_2025']-team_mod['win_percentage_2025'].min())/(team_mod['win_percentage_2025'].max()-team_mod['win_percentage_2025'].min()),4)

standing_points= {
    'Group' : 0.0,
    '4th' : 0.25,
    '3rd' : 0.5,
    'Runner Up' : 0.75,
    'Winner' : 1.0
}

team_mod['standings_2023'] = team_mod['standings_2023'].str.strip().map(standing_points)
team_mod['standings_2024'] = team_mod['standings_2024'].str.strip().map(standing_points)
team_mod['standings_2025'] = team_mod['standings_2025'].str.strip().map(standing_points)

#Weight assignment (either standings biased, NRR biased, or Win Percentage biased) 
weight_1 = 0.4
weight_2 = 0.2
weight_3 = 0.114

weights_team= pd.Series({
    'nrr_2023': weight_3**3,
    'win_percentage_2023': weight_2**3,
    'standings_2023': weight_1**3,
    'nrr_2024': weight_3**2,
    'win_percentage_2024': weight_2**2,
    'standings_2024': weight_1**2,
    'nrr_2025': weight_3,
    'win_percentage_2025': weight_2,
    'standings_2025': weight_1
})

#Final team score
team_score = pd.DataFrame({
    'team_abrv' : team_raw['team_abrv'],
    'team_score' : round(team_mod[weights_team.index].dot(weights_team), 4)
})
team_score = team_score.sort_values(by = 'team_abrv').reset_index(drop=True)

# print(team_score)

#-------BATTING SCORE CODE---------

batting_mod_1 = batting_raw

#Normalization of Strike Rate, Average, Fours, and Sixes
batting_mod_1['MLC_strike_rate'] = round((batting_mod_1['MLC_strike_rate']-batting_mod_1['MLC_strike_rate'].min())/(batting_mod_1['MLC_strike_rate'].max()-batting_mod_1['MLC_strike_rate'].min()),4)
batting_mod_1['MLC_average'] = round((batting_mod_1['MLC_average']-batting_mod_1['MLC_average'].min())/(batting_mod_1['MLC_average'].max()-batting_mod_1['MLC_average'].min()),4)
batting_mod_1['MLC_fours'] = round((batting_mod_1['MLC_fours']-batting_mod_1['MLC_fours'].min())/(batting_mod_1['MLC_fours'].max()-batting_mod_1['MLC_fours'].min()),4)
batting_mod_1['MLC_sixes'] = round((batting_mod_1['MLC_sixes']-batting_mod_1['MLC_sixes'].min())/(batting_mod_1['MLC_sixes'].max()-batting_mod_1['MLC_sixes'].min()),4)

#Aggregating player statistics into team statistics
batting_mod_2 = batting_mod_1.groupby('team_abrv_unordered').agg({
    'MLC_strike_rate': 'mean',
    'MLC_average': 'mean',
    'MLC_fours': 'mean',
    'MLC_sixes': 'mean'
}).reset_index()

#Weight assignment
weights_batting= pd.Series({
    'MLC_strike_rate': 0.35,
    'MLC_average': 0.4,
    'MLC_fours': 0.125,
    'MLC_sixes': 0.125
})

#Final batting score

batting_score = pd.DataFrame({
    'team_abrv' : batting_mod_2['team_abrv_unordered'],
    'batting_score' : round(batting_mod_2[weights_batting.index].dot(weights_batting), 4)
})
batting_score = batting_score.sort_values(by = 'team_abrv').reset_index(drop=True)
# print(batting_score)

#-------BOWLING SCORE CODE---------