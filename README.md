# FantasyFootballDraftOptomizer

Overview:

One of the difficulties in drafting is a team is being able to weigh the relative importance of players across positions. My idea is that we look at the ammount of points we expect a player at a certain position and of a certain rank to score over the course of the season. We do this by looking at how players in past seasons scored based on the leagues settings. 

Here we make some arbitrary decisions. I believe we should base our marginal value calculations on starters, meaning that if we have a 10 man, 1 QB league, we only look at the top 10 QB's as they would be the only ones scoring points that week. We also assume that points drop of linearly in rankings. 

Let the lowest point total for a position (10th in the example above) as the base score. We subtract the base score from a players projected score to calculate how many additional points that player would score for us that season. This number is compareable across positions, allowing us to turn our 4 separate rankings into one weighted ranking.  

Stat rankings from https://www.pro-football-reference.com/years/2018/fantasy.htm

Player rankings from FantasyPros

Inputs

- A ranking of players by position (separate files for each position)
- Scoring settings for your league
- League size
- League line up settings

Outputs

- A single list ranking all players regardless of position by incremental value to the team. 

Method

Per position

- Multiply the number of starters in that position by the number of teams in the league. Call this value N.

- Calculate the highest scoring player over the season by the league scoring settings. Call this S1

- Calculate the N highest scoring player over the season by the league scoring settings. Call this, SN. 

- Calculate the incremental differential (S1-SN)/N. Call this D. 

- Take that players rank and call it R. 

- Now to calculate a players overall incremental value. (S1 - SN) - (D * R)

Now across positions, rank them by incremental value
