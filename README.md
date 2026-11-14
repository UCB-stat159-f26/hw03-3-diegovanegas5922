# Tennis Age Analysis Package

## Overview

This package retrieves professional tennis players' career match data from [Tennis Abstract](https://www.tennisabstract.com/), cleans and processes the data, and creates scatter plots comparing a player's age with the age difference between the player and their opponents.

## Package Features

The package provides two main functions:

- `get_player_matches(player_name)`: Downloads and processes career match data for a specified tennis player and returns a pandas DataFrame.
- `plot_age_difference(matches)`: Creates a scatter plot of the player's age against the age difference between the player and their opponents, with points colored by match result.

The package supports different name formats, including `"Serena Williams"`, `"serena williams"`, and `"SerenaWilliams"`.

It also handles differences between male and female career match files. Female players' files provide opponents' dates of birth, while male players' files provide opponents' ages directly.

## Installation

The package can be installed directly from GitHub using pip:

```bash
pip install git+https://github.com/diegovanegas5922/hw03-3-diegovanegas5922.git
```

For local development, clone the repository and install it in editable mode:

```bash
git clone https://github.com/diegovanegas5922/hw03-3-diegovanegas5922.git
cd hw03-3-diegovanegas5922
pip install -e ".[dev]"
```

## Usage

Import the two public functions:

```python
from tennis_age import get_player_matches, plot_age_difference
import matplotlib.pyplot as plt
```

### Example 1: Serena Williams

Retrieve Serena Williams' career match data:

```python
serena = get_player_matches("Serena Williams")
print(serena.head())
```

Create the scatter plot:

```python
fig, ax = plot_age_difference(serena)
plt.show()
```

### Example 2: Rafael Nadal

```python
rafa = get_player_matches("Rafael Nadal")

fig, ax = plot_age_difference(rafa)
plt.show()
```

### Example 3: Other Players

The package can also retrieve data for other players available through its player lookup.

```python
novak = get_player_matches("Novak Djokovic")
coco = get_player_matches("Coco Gauff")

plot_age_difference(novak)
plt.show()
```

### Example 4: Invalid Player Name

If the player cannot be found, the function raises a meaningful error:

```python
get_player_matches("GastonSanchez")
```

Expected error:

```text
ValueError: Player 'GastonSanchez' was not found.
```

## Data Processing

The package processes Tennis Abstract career match JavaScript files.

The main processing steps are:

1. Normalize the player's name to handle different capitalization and spacing.
2. Identify the player's career data file and birth date.
3. Download the JavaScript file containing their career matches.
4. Extract the match information and convert it into a pandas DataFrame.
5. Calculate the player's age at the time of each match.
6. Determine the opponent's age using either a birth date or an existing age value.
7. Calculate the difference between the player's age and the opponent's age.
8. Remove matches with missing or invalid information.

The resulting DataFrame includes the following columns:

| Column | Description |
|---|---|
| `Match_Date` | Date of the match |
| `Tournament` | Tournament name |
| `Surface` | Playing surface |
| `Opponent` | Opponent's name |
| `Player_Age` | Player's age during the match |
| `Opponent_Age` | Opponent's age during the match |
| `Age_Difference` | Player's age minus opponent's age |
| `Result` | Win or Loss |

## Visualization

The `plot_age_difference()` function produces a scatter plot with:

- **X-axis:** Player's age at the time of the match.
- **Y-axis:** Player's age minus opponent's age.
- **Blue points:** Matches the player won.
- **Orange points:** Matches the player lost.

A horizontal line at zero represents matches where the player and opponent were approximately the same age.

Positive age differences indicate that the player was older than their opponent, while negative age differences indicate that the player was younger.

The visualization follows the approach used in HW2 without including match annotations.

## Testing

Automated tests are written using `pytest`.

The tests use mock JavaScript data rather than making requests to live Tennis Abstract servers.

To run all tests from the repository root:

```bash
python -m pytest -v
```

The tests cover:

- Player name normalization.
- Parsing female and male career match files.
- Calculating opponent ages from birth dates.
- Processing opponent ages already provided as decimal values.
- Cleaning match data and checking DataFrame columns.
- Handling invalid player names.
- Creating scatter plots.

At the time of development, all 12 automated tests passed.

## Project Structure

```text
hw03-3-diegovanegas5922/
├── tennis_age/
│   ├── __init__.py
│   ├── matches.py
│   └── plotting.py
├── tests/
│   ├── test_matches.py
│   └── test_plotting.py
├── pyproject.toml
├── README.md
└── .gitignore
```

## Personal Reflections

In HW2, my scripts were specifically designed to download, clean, and visualize Serena Williams' career match data. For this assignment, I had to reorganize that code into functions that could work with different tennis players.

An important challenge was handling the differences between female and male players' career match files. In HW2, I calculated opponents' ages using their dates of birth. However, I learned that the men's career files already contain opponents' ages, so I needed to adjust the processing functions to handle both formats.

In this assignment, I learned how to test individual functions using mock data without relying on live website requests. This helped me understand why automated testing is important for making code more reliable and reproducible.

Overall, this assignment helped me improve my understanding of Python package development, modular programming, testing, and Git workflows.

## Data Source

Career match data is retrieved from [Tennis Abstract](https://www.tennisabstract.com/).
