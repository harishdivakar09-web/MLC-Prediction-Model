# MLC Team Prediction Model

This project is a Python prediction model for ranking Major League Cricket (MLC) teams. It uses team history, batting statistics, bowling statistics, and all-rounder statistics to calculate a final score for each team. The highest final score represents the team the model predicts to be strongest based on the available data.

The main program is `main.py`. It reads the CSV files in this folder, processes the data with pandas, creates separate scores for each team category, combines those scores, and prints the final team rankings.

## Files

- `main.py` - runs the prediction model.
- `batters.csv` - batting statistics for players, including strike rate, average, fours, and sixes.
- `bowlers.csv` - bowling statistics for players, including wickets, average, economy, and strike rate.
- `all_rounders.csv` - combined batting and bowling statistics for all-rounders.
- `team_season.csv` - team results from recent MLC seasons, including wins, losses, net run rate, and final standings.

## What The Project Uses

This project uses:

- Python for running the model.
- pandas for loading, organizing, transforming, and calculating scores from the CSV data.
- CSV files as the source data for teams and players.

To install pandas, run:

```bash
pip install pandas
```

To run the project, use:

```bash
python main.py
```

## How The Model Works

The model creates four main scores:

1. Team score
2. Batting score
3. Bowling score
4. All-rounder score

These scores are then combined into one final score for each team.

### Team Score

The team score is based on each team's recent season performance. `main.py` calculates win percentage for 2023, 2024, and 2025 using the wins and losses in `team_season.csv`.

It also uses:

- Net run rate
- Win percentage
- Final standings

The standings are converted into number values:

- `Group` = `0.0`
- `4th` = `0.25`
- `3rd` = `0.5`
- `Runner Up` = `0.75`
- `Winner` = `1.0`

The model gives more importance to recent seasons, especially 2025, by applying larger weights to newer data.

### Batting Score

The batting score comes from `batters.csv`. The model uses:

- MLC strike rate
- MLC average
- MLC fours
- MLC sixes

These player stats are normalized, grouped by team, averaged, and then combined with weights. Batting average and strike rate receive the highest weights because they are strong indicators of batting performance.

### Bowling Score

The bowling score comes from `bowlers.csv`. The model uses:

- MLC wickets
- MLC economy
- MLC strike rate
- MLC average

For bowling, lower economy is better, so the code normalizes economy in reverse. This means a better economy rate receives a higher normalized score. The weighted bowling score gives the most importance to economy, followed by strike rate.

### All-Rounder Score

The all-rounder score comes from `all_rounders.csv`. It includes both batting and bowling statistics:

- Batting strike rate
- Batting average
- Fours
- Sixes
- Wickets
- Bowling average
- Economy
- Bowling strike rate

The code renames duplicate column names from the CSV so batting and bowling averages/strike rates can be handled separately. It then normalizes the values, groups players by team, averages the stats, and calculates a weighted all-rounder score.

## How pandas Helps Build The Prediction Model

pandas is important because it makes it easy to work with table-based data. In this project, each CSV file becomes a pandas DataFrame, which acts like a spreadsheet inside Python.

pandas allows the model to:

- Read CSV files with `pd.read_csv()`.
- Create new calculated columns, such as win percentage.
- Remove columns that are no longer needed.
- Normalize statistics so different types of data can be compared fairly.
- Group player data by team using `groupby()`.
- Average player stats to create team-level stats.
- Use weighted calculations with `dot()` to create category scores.
- Merge multiple score tables into one final table.
- Sort teams by final score.

Without pandas, these steps would require much more manual code. pandas lets the project turn raw cricket statistics into clean, comparable team scores.

## Final Score

After calculating the individual category scores, the model combines them using these weights:

- Team score: `0.5`
- Batting score: `0.1`
- Bowling score: `0.1`
- All-rounder score: `0.3`

This means the final prediction focuses most on overall team performance and all-rounder strength, while still including batting and bowling performance.

The final output is a ranked table with:

- `team_abrv`
- `final_score`

Teams are sorted from highest final score to lowest final score.
