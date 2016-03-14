#Fixing the python code

QUERY_CONSTRUCTORS = {'Pitcher': {'select_default': """SELECT bios.name, bios.span, bios.positions,
 bios.player_id, pitcher.WARs_pitcher, """,
                                   'from_default': "FROM bios JOIN pitcher ",
                                   'on_default': 'ON (bios.player_id = pitcher.player_id',
                                   'where_default': ") WHERE (bios.years_played > 2 AND pitcher.IPs > 200 AND ? != '' ",
                                    'order_by_base': ') ORDER BY ? '
                                    'order_by_asc': 'ASC LIMIT 90;'
                                    'order_by_desc': 'DESC LIMIT 90;'
                                    'from_team': 'JOIN employment ',
                                    'on_team': ' AND bios.player_id = employment.player_id',
                                    'where_team': 'AND employment.team like ? '
                                    'where_playoffs': "AND bios.Playoffs != '' ",
                                    'where_WS': "AND bios.World_Series != '' "
                                    'where_name': "AND bios.name like ? "
                                    'where_years': "AND (pitcher.Pitcher_Years like ? OR pitcher.Pitcher_Years like ? "},
                        'NonPitcher': {'select_default': """SELECT bios.name, bios.span, bios.positions,
 bios.player_id, nonpitcher.WARs_nonpitcher, """,
                                   'from_default': "FROM bios JOIN nonpitcher ",
                                   'on_default': 'ON (bios.player_id = nonpitcher.player_id',
                                   'where_default': ") WHERE (bios.years_played > 2 AND nonpitcher.SLGs < .8 AND nonpitcher.AVGs < .42 AND nonpitcher.OBPs < .5 AND ? != '' ",
                                    'order_by_base': ') ORDER BY ? '
                                    'order_by_asc': 'ASC LIMIT 90;'
                                    'order_by_desc': 'DESC LIMIT 90;'
                                    'from_team': 'JOIN employment ',
                                    'on_team': ' AND bios.player_id = employment.player_id',
                                    'where_team': 'AND employment.team like ? '
                                    'where_playoffs': "AND bios.Playoffs != '' ",
                                    'where_WS': "AND bios.World_Series != '' "
                                    'where_name': "AND bios.name like ? "
                                    'where_years': "AND (nonpitcher.years like ? OR nonpitcher.years like ? "}}

def construct_query(pref, pitcher, params):
    '''
    Structure of Params:
    {'date': (1975, 2015), 'Playoffs': True,
    'Name': 'Bob', 'Team': 'Kansas City Royals'}
    '''
    if pitcher:
        pos = 'Pitcher'
    else:
        pos = 'NonPitcher'
        
    search_params = []
    select_statement = QUERY_CONSTRUCTORS[pos]['select_default'] + pref + " "
    from_statement = QUERY_CONSTRUCTORS[pos]['from_default']
    on_statement = QUERY_CONSTRUCTORS[pos]['on_default']
    where_statement = QUERY_CONSTRUCTORS[pos]['where_default']
    search_params += [pref]
    order_by_statement = QUERY_CONSTRUCTORS[pos]['order_by_base']
    search_params += [pref]

    if pref == "pitcher.ERAs" or pref == "pitcher.FIPs":
        order_by_statement += QUERY_CONSTRUCTORS[pos]['order_by_asc']
    else:
        order_by_statement += QUERY_CONSTRUCTORS[pos]['order_by_desc']

    if params['Team']:
        from_statement += QUERY_CONSTRUCTORS[pos]['from_team']
        on_statement = QUERY_CONSTRUCTORS[pos]['on_team']
        where_statement += QUERY_CONSTRUCTORS[pos]['where_team']
        search_params += ["'%" + params['Team'] + "%'"]

    if params['Playoffs']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_playoffs']

    if params['World_Series']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_WS']

    if params['Name']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_WS']
        search_params += ["'%" + params['Name'] + "%'"]

    if params['years']:
        where_statement += QUERY_CONSTRUCTORS[pos]['where_years']
        search_params += ["'%" + params['years'][0] + "%'"]
        search_params += ["'%" + params['years'][1] + "%'"]