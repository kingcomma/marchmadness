import random

def get_teams(year):

    '''
    Open up txt files representing an entire bracket and parse
    into a dict with one key for each region, the value of which
    is a list of dicts, one for each team.
    '''

    teams = {}

    # split up CSV into list of dicts, one for each time
    with open( 'teams_%s.csv' % year, 'r' ) as all_teams:
        for team in all_teams:
            seed, school, region = team.strip().split(',')[0:3]
            
            if region not in teams:
                teams[region] = []

            teams[region].append(dict(
                seed=int(seed),
                school=school,
                region=region,
                placement=None
            ))

    # determine starting placement for each team in each region
    for region in teams:
        teams[region] = sorted( teams[region], key=lambda team: team['seed'] )

        # assign placement based on seed, where placement is the higher of
        # the two seeds in a team's first round game
        for i in range(len(teams[region])/2):
            teams[region][i]['placement'] = teams[region][i]['seed']
            teams[region][-(i+1)]['placement'] = teams[region][i]['seed']
            # -(i+1), or team i places from bottom

    return teams


def play_game( highteam, lowteam ):

    '''
    Given two teams, "play" a game that uses seed to determine
    the probability of each team winning.
    '''

    highseed = highteam['seed']
    lowseed = lowteam['seed']

    # Simplistic algorithm for determining winner. High
    # seed has a {{lowseed}} in {{sum of seeds}} chance of winning.
    # E.g., in a game of a 1 seed vs a 16 seed, the 1 seed has a
    # 16 in 17 chance of winning. In a game of a 2 seed vs a 3
    # seed, the 2 seed has a 3 in 5 chance of winning.
    if random.randrange(1, highseed + lowseed) < lowseed:
        return highteam

    return lowteam


def play_round(teams):

    '''
    Given a list of teams, play one round of (teams/2) games
    and return a list of the winning teams, sorted in order
    of their next round.

    We assume that the list of teams is sorted properly. If
    this is the first round, teams are sorted by seed. If this
    is any other round, teams are by original bracket placement.
    '''

    games = len(teams)/2 # 1 game per 2 teams
    winners = []

    for i in range(games):
        # team X seeds from top plays team X seeds from bottom
        winners.append( play_game(teams[i], teams[-(i+1)]) )

    return sorted( winners, key=lambda team: team['placement'] )


def play_region(teams):

    '''
    Convenience function that plays rounds until only one team
    remains.
    '''

    while True:
        teams = play_round(teams)
        if len(teams) == 1:
            break

    return teams[0]