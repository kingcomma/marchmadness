# March Madness

Python script for playing around with [March Madness](https://www.ncaa.com/news/basketball-men/bracketiq/2018-03-13/what-march-madness-ncaa-tournament-explained) scenarios. Will eventually be improved by:
- Adding a much more nuanced algorithm for choosing winners
- Generating a "print" version of results

## Using

First, get a representation of all the teams in the bracket by parsing the included `teams_2018.csv` file:

```
import marchmadness as mm

teams = mm.get_teams( 'teams_2018.csv' )
```

You'll likely want to split your teams list into lists for each region (since teams do not play across regions until the final four):

```
regions = {}

for r in set([team['region'] for team in teams]):
  regions[r] = [team for team in teams if team['region'] == r]

print regions['south']
```

With your lists of teams, play some games. You can play an individual game:

```
# Play 1 seed vs 16 seed in the South region
winner = mm.play_game(regions['south'][0], regions['south'][-1])
```

You can play an entire round (ie, round of 64):

```
round_of_32 = mm.play_round(regions['south'])
```

Or, you can play an entire region down to its final winner:

```
south_champion = mm.play_region(regions['south'])
```

Rather than playing region at a time, you could do this to get your winners of each region (aka Final Four teams):

```
final_four = []

for region, r_teams in regions.iteritems():
  final_four.append( mm.play_region(r_teams) )

print final_four
```