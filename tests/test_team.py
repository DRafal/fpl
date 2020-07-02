from fpl.dictionaries.api_keywords import *
from fpl.models import Player, Fixture

team_data = {
    ID: 1,
    NAME: "Arsenal",
    CODE: 3,
    DRAW: 0,
    SHORT_NAME: "ARS",
    UNAVAILABLE: False,
    STRENGTH: 4,
    POSITION: 0,
    PLAYED: 0,
    WIN: 0,
    LOSS: 0,
    POINTS: 0,
    FORM: None,
    STRENGTH_OVERALL_HOME: 1260,
    STRENGTH_OVERALL_AWAY: 1320,
    STRENGTH_ATTACK_HOME: 1240,
    STRENGTH_ATTACK_AWAY: 1270,
    STRENGTH_DEFENCE_HOME: 1310,
    STRENGTH_DEFENCE_AWAY: 1340,
    TEAM_DIVISION: 1
}


class TestTeam:
    @staticmethod
    def test_init(loop, team):
        assert team.code == 3
        assert team.draw == 0
        assert team.form is None
        assert team.id == 1
        assert team.loss == 0
        assert team.name == 'Arsenal'
        assert team.played == 0
        assert team.points == 0
        assert team.position == 0
        assert team.short_name == 'ARS'
        assert team.strength == 4
        assert team.strength_attack_away == 1270
        assert team.strength_attack_home == 1240
        assert team.strength_defence_away == 1340
        assert team.strength_defence_home == 1310
        assert team.strength_overall_away == 1320
        assert team.strength_overall_home == 1260
        assert team.team_division == 1
        assert not team.unavailable
        assert team.win == 0

    @staticmethod
    def test_str(loop, team):
        assert str(team) == team.name

    @staticmethod
    async def test_get_players_return_json_is_false(loop, team):
        players = await team.get_players(return_json=False)
        assert isinstance(players, list)

        for player in players:
            assert isinstance(player, Player)
            assert player.team == team.id

    @staticmethod
    async def test_get_players_return_json_is_true(loop, team):
        players = await team.get_players(return_json=True)
        assert isinstance(players, list)

    @staticmethod
    async def test_get_fixtures(loop, team):
        fixtures = await team.get_team_fixtures(return_json=True)
        assert len(fixtures) == 38
        assert isinstance(fixtures, list)
        for fixture in fixtures:
            assert isinstance(fixture, Fixture)
