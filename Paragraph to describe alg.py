#Paragraph that describes function of the algorithm
#Thomas Dunn

DESC = """The function took in your parameters as you ranked them as well as 
        any limiting parameters such as date, name, etc. The function runs a SQL
        query for each stat you input (limited by the params) and then returns a
        list of 90 players (to avoid regression as much as possible without 
        pulling too mamy people if the search parameters are lax). These 90
        players are then assigned a ranking based on their position in the top 90
        list for a given stat. After all ranks have been created, the algorithm loops
        through the players and assigns them a power index based on their position in 
        each statistic and the number of statistics for which they appeared in the top
        90. Then, the algorithm runs through the players and places the ones with the
        highest power indices into the team. If the team cannot be completed, the 
        algorithm will recurse with looser parameters and try again. If, after the name
        parameter (if it exists) has been completely removed, the algorithm still cannot
        create a full team, it simply returns the partial team. Our rationale for using
        looser parameters to try to complete the team is that it's better for the
        purposes of team stats and win total calculations to use a team with 
        inexactly generated parameters than to have an incomplete team, as this
        would render most stats meaningless."""