# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 23:52:36 2020

@author: noahk
"""
import lib.FPL as fpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
if __name__ == "__main__":
    fpl_data, stats_data = fpl.api_init()
    all_data = fpl.program_init()
 
#Converting all the objects into their respective types
all_data['xG'] = all_data['xG'].astype(float)
all_data['assists'] = all_data['assists'].astype(float)
all_data['xA'] = all_data['xA'].astype(float)
all_data['shots'] = all_data['shots'].astype(float)
all_data['key_passes'] = all_data['key_passes'].astype(float)
all_data['yellow_cards'] = all_data['yellow_cards'].astype(int)
all_data['red_cards'] = all_data['red_cards'].astype(int)
all_data['npg'] = all_data['npg'].astype(int)
all_data['npxG'] = all_data['npxG'].astype(float)
all_data['xGChain'] = all_data['xGChain'].astype(float)
all_data['xGBuildup'] = all_data['xGBuildup'].astype(float)
all_data['minutes'] = all_data['minutes'].astype(float)
all_data['games'] = all_data['games'].astype(float)


#Additional Data
all_data['now_cost'] = all_data['now_cost']/10
all_data['points_90'] = all_data['total_points']/(all_data['minutes']/90)
all_data['points_game'] = all_data['total_points']/all_data['games']
all_data['points_price'] = all_data['points_game']/all_data['now_cost']
all_data['VAPM'] = (all_data['points_game']-2)/all_data['now_cost']

#Dividing into various categories
fw = all_data.loc[(all_data['position'] == 'Forward')&(all_data['minutes']>=500)].reset_index(drop = True).sort_values(by = 'minutes')
df = all_data.loc[(all_data['position'] == 'Defender')&(all_data['minutes']>=500)].reset_index(drop = True).sort_values(by = 'minutes')
mid = all_data.loc[(all_data['position'] == 'Midfielder')&(all_data['minutes']>=500)].reset_index(drop = True).sort_values(by = 'minutes')
gk = all_data.loc[(all_data['position'] == 'Goalkeeper')&(all_data['minutes']>=500)].reset_index(drop = True).sort_values(by = 'minutes')


plt.figure(figsize=(20,20))
p1 = sns.regplot('minutes', # Horizontal axis
       'points_90', # Vertical axis
       data=gk, # Data source
       )  

for line in range(0,gk.shape[0]):
     p1.text(gk.minutes[line]+5, gk.points_90[line], 
     gk.player_name[line], horizontalalignment='left', 
     size='medium', color='black', weight='semibold')
