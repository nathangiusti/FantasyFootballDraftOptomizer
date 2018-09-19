# FantasyFootballDraftOptomizer

This is my personal methodology for draft strategy. We take draft rankings and combine them with the league settings to calculate the relative value of each position. 

Inputs

- A ranking of players. Can either be one overall list (more accurate) or a list by position. 
- Scoring settings for your league
- League size
- League line up settings

Outputs

- A single list ranking all players regardless of position by incremental value to the team. 


Method

Per position

Multiply the number of starters in that position by the number of teams in the league. Call this value N.

Calculate the highest scoring player over the season by the league scoring settings. Call this S1

Calculate the N highest scoring player over the season by the league scoring settings. Call this, SN. 

Calculate the incremental differential (S1-SN)/N. Call this D. 

If using a list by position, take that players rank and call it R. 

If using one overall list, we normalize the list to give players a ranking between 0 and N-1.

Now to calculate a players overall incremental value. (S1 - SN) - (D * R)

Sort players by overall incremental value.
