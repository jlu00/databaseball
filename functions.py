#jessbritommy

#Functions to get SQL Code


def grab_stat_non_pitcher(player, stat, season):
    '''
    Grabs a specific stat for a given player and a given season
    Creates SQL code
    Inputting "All" for stat will return all stats for that player
    Season works the same way
    '''

    if stat == "All":
        stat = "*"
    if season == "All":
        query = """SELECT Player_Bios.name, Stats_non_pitcher.? 
        FROM Player_Bios JOIN Stats_non_pitcher ON Player_Bios.player_ID 
        = Stats_non_pitcher.player_ID WHERE Player_Bios.name = ? GROUP BY
         Stats_non_pitcher.season"""
        inputs = [player, stat]
    else:
        query = """SELECT Player_Bios.name, Stats_non_pitcher.? 
        FROM Player_Bios JOIN Stats_non_pitcher ON Player_Bios.player_ID 
        = Stats_non_pitcher.player_ID WHERE (Player_Bios.name = ?
         AND Stats_non_pitcher.season = ?"""
        inputs = [player, stat, season]
    print('query', query, 'inputs', inputs)