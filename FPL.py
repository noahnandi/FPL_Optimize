#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 17:24:46 2020

@author: Ankan Biswas
"""

import requests
import json
import aiohttp
import asyncio
import nest_asyncio
import pandas as pd
import numpy as np
from understat import Understat

nest_asyncio.apply()

async def all_players():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_players("epl", 2019)
        json_ = json.loads((json.dumps(data)))
        return json_

def normalize_to_df(json_data):
    df = pd.json_normalize(json_data)
    df = df.drop(['id', 'position'], axis = 1)
    return df

def connect_fpl_api():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(url)
    json = r.json()
    json.keys()
    
    elements_df = pd.DataFrame(json['elements'])
    elements_types_df = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])
    
    elements_df['position'] = elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
    elements_df['team'] = elements_df.team.map(teams_df.set_index('id').name)
    elements_df['name'] = elements_df['first_name'] + ' ' + elements_df['second_name']
    
    final_df = elements_df[['name','team', 'position','total_points', 'selected_by_percent', 'now_cost', 'minutes', 'transfers_in', 'value_season']]
    final_df['value_season'] = final_df['value_season'].astype(float)
    final_df = final_df.sort_values(by=['value_season'], ascending=False).reset_index(drop=True)
    final_df['value_minutes'] = (final_df['value_season']/final_df['minutes'])*100
    return final_df

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    json_all_players = loop.run_until_complete(all_players())
    player_xStats = normalize_to_df(json_all_players)
    
    fpl_data = connect_fpl_api()
    value_players = fpl_data.sort_values(by=['value_minutes'], ascending=False)
    value_players = value_players.where(value_players['value_season'] > 10.0).dropna().reset_index(drop=True)
    
    fpl_gk = fpl_data[fpl_data['position'] == 'Goalkeeper'].reset_index(drop=True)
    fpl_def = fpl_data[fpl_data['position'] == 'Defender'].reset_index(drop=True)
    fpl_mid = fpl_data[fpl_data['position'] == 'Midfielder'].reset_index(drop=True)
    fpl_fwd = fpl_data[fpl_data['position'] == 'Forward'].reset_index(drop=True)
