#sql function writer

def grab_stat_non_pitcher(player, stats, seasons):
    '''
    Grabs a specific stat for a given player and a given season
    Even if len is 1, stats and seasons need to be input as lists
    Season works the same way
    '''

    select_clause = "SELECT Player_Bios.name AND " + " AND ".join(["Stats_non_pitcher.?"] * len(stats))
    where_clause = " WHERE (" + " AND ".join(["Stats_non_pitcher.season = ?"] * len(seasons)) + " AND Player_Bios.name = ?)"
    inputs = []
    for i in stats:
        inputs += [i]
    for i in seasons:
        inputs += [i]
    inputs += [player]
    query = select_clause + """ FROM Player_Bios JOIN Stats_non_pitcher 
    ON Player_Bios.player_ID = Stats_non_pitcher.player_ID""" + where_clause

    print('query', query, 'inputs', inputs)

def grab_stat_pitcher(player, stats, seasons):

    '''
    Grabs a specific stat for a given player and a given season
    Even if len is 1, stats and seasons need to be input as lists
    Season works the same way
    '''

    select_clause = "SELECT Player_Bios.name AND " + " AND ".join(["Stats_pitcher.?"] * len(stats))
    where_clause = " WHERE (" + " AND ".join(["Stats_pitcher.season = ?"] * len(seasons)) + " AND Player_Bios.name = ?)"
    inputs = []
    for i in stats:
        inputs += [i]
    for i in seasons:
        inputs += [i]
    inputs += [player]
    query = select_clause + """ FROM Player_Bios JOIN Stats_pitcher 
    ON Player_Bios.player_ID = Stats_pitcher.player_ID""" + where_clause

    print('query', query, 'inputs', inputs)