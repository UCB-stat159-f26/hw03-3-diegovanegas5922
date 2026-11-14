import pandas as pd
import pytest
from tennis_age.matches import (_normalize_name, _parse_matches, _opponent_age,
                                _clean_matches, get_player_matches,)

@pytest.mark.parametrize("name", ["Serena Williams", "serena williams", "SerenaWilliams"])
def test_normalize_name(name):
    assert _normalize_name(name) == "serenawilliams"

FEMALE_JS = '''
var morematchmx = [
    ["19951030", "Canadian Open", "Carpet", "W", "L",
     "", "", "WC", "Q1", "6-1 6-1", "3",
     "Anne Miller", "149", "7", "", "R",
     "19770119", "", "USA", "0"]
];
'''

MALE_JS = '''
var morematchmx = [
    ["20010910", "Spain F10", "Hard", "S", "L",
     "", "", "WC", "R32", "2-6 7-5 6-2", "3",
     "Guillermo Platel", "731", "", "", "R",
     "22.264202601", "", "ESP", "0"]
];
'''
def test_parse_female_matches():
    matches = _parse_matches(FEMALE_JS)
    assert len(matches) == 1
    assert matches[0][11] == "Anne Miller"
    assert matches[0][16] == "19770119"


def test_parse_male_matches():
    matches = _parse_matches(MALE_JS)
    assert len(matches) == 1
    assert matches[0][11] == "Guillermo Platel"
    assert matches[0][16] == "22.264202601"
def test_female_opponent_age():
    match_date = pd.Timestamp("1995-10-30")
    age = _opponent_age("19770119", match_date)
    assert 18 < age < 19

def test_male_opponent_age():
    match_date = pd.Timestamp("2001-09-10")
    age = _opponent_age("22.264202601", match_date)
    assert age == pytest.approx(22.2642, abs=0.001)

def test_clean_female_matches():
    matches = _parse_matches(FEMALE_JS)
    birth_date = pd.Timestamp("1981-09-26")
    df = _clean_matches(matches, birth_date)
    assert len(df) == 1
    assert df.iloc[0]["Result"] == "Loss"
    assert df.iloc[0]["Opponent"] == "Anne Miller"
    assert df.iloc[0]["Age_Difference"] < 0

def test_clean_male_matches():
    matches = _parse_matches(MALE_JS)
    birth_date = pd.Timestamp("1986-06-03")
    df = _clean_matches(matches, birth_date)
    assert len(df) == 1
    assert df.iloc[0]["Result"] == "Loss"
    assert df.iloc[0]["Opponent"] == "Guillermo Platel"
    assert df.iloc[0]["Opponent_Age"] == pytest.approx(22.2642, abs=0.001)

def test_dataframe_columns():
    matches = _parse_matches(FEMALE_JS)
    birth_date = pd.Timestamp("1981-09-26")
    df = _clean_matches(matches, birth_date)
    expected = {"Match_Date", "Tournament", "Surface", "Opponent",
                "Player_Age", "Opponent_Age", "Age_Difference", "Result",}
    assert expected.issubset(df.columns)

def test_invalid_player(monkeypatch):
    import tennis_age.matches as module
    monkeypatch.setattr(module, "_search_rankings", lambda name, tour: None)
    with pytest.raises(ValueError, match="was not found"):
        get_player_matches("GastonSanchez")

