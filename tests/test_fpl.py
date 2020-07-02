import aiohttp
import pytest

from fpl.fpl import Phase, PlayerStats, GameSettings
from fpl.models.leagues import ClassicLeague, H2HLeague
from fpl.models.fixture import Fixture
from fpl.models.gameweek import Gameweek
from fpl.models.player import Player, PlayerSummary, PlayerType
from fpl.models.team import Team
from fpl.models.user import User
from tests.helper import AsyncMock


class TestFPL:
    @staticmethod
    def test_init(loop, fpl):
        for team in fpl.teams.values():
            assert isinstance(team, Team)
        for player in fpl.players.values():
            assert isinstance(player, Player)
        assert isinstance(fpl.total_users, int)
        for stat in fpl.player_stats:
            assert isinstance(stat, PlayerStats)
        for player_type in fpl.player_types:
            assert isinstance(player_type, PlayerType)
        assert isinstance(fpl.settings, GameSettings)
        for phase in fpl.phases:
            assert isinstance(phase, Phase)
        for gameweek in fpl.gameweeks.values():
            assert isinstance(gameweek, Gameweek)
        assert len(fpl.gameweeks) == 47


    @staticmethod
    async def test_user(loop, fpl):
        # test negative id
        with pytest.raises(AssertionError):
            await fpl.get_user(-10)

        with pytest.raises(AssertionError):
            await fpl.get_user("-10")

        # test valid id
        user = await fpl.get_user(91928)
        assert isinstance(user, User)

        # test valid id, require json response
        user = await fpl.get_user(91928, True)
        assert isinstance(user, dict)

    @staticmethod
    async def test_teams(loop, fpl):
        # test team id out of valid range
        with pytest.raises(KeyError):
            fpl.teams[0]
        with pytest.raises(KeyError):
            fpl.teams[21]

        team = fpl.teams[1]
        assert isinstance(team, Team)

        teams = fpl.teams
        assert isinstance(teams, dict)
        assert len(teams) == 20
        assert isinstance(teams[1], Team)

    @staticmethod
    async def test_player_summaries(loop, fpl):
        # test non positive id
        players = await fpl.get_player_summaries(0)
        assert not players

        players_summaries = await fpl.get_player_summaries(20, 123, 50, 33)
        for player_summary in players_summaries:
            assert isinstance(player_summary, PlayerSummary)
        assert len(players_summaries) == 4

        player_summary = await fpl.get_player_summaries(123, return_json=True)
        assert isinstance(player_summary, str)

        # test no specified IDs
        player_summaries = await fpl.get_player_summaries()
        assert isinstance(player_summaries, list)
        assert len(player_summaries) == 0

    @staticmethod
    async def test_player(loop, fpl):
        # test invalid ID
        with pytest.raises(KeyError):
            fpl.players[-1]

        player = fpl.players[1]
        assert isinstance(player, Player)

    @staticmethod
    async def test_fixtures(loop, fpl):
        # test fixture with unknown id
        fixtures = await fpl.get_fixtures(-1)
        assert not fixtures

        fixture = await fpl.get_fixtures(6)
        assert isinstance(fixture[0], Fixture)

        fixture = await fpl.get_fixtures(6, return_json=True)
        assert isinstance(fixture, str)

        for gameweek in range(1, 39):
            fixtures = await fpl.get_fixtures(gameweek=gameweek)
            if not len(fixtures):
                continue

            assert isinstance(fixtures, list)
            assert isinstance(fixtures[0], Fixture)

        fixtures = await fpl.get_fixtures(100, 200, 300)
        assert isinstance(fixtures, list)
        assert isinstance(fixtures[0], Fixture)

        fixture_ids = [fixture.id for fixture in fixtures]
        assert {100, 200, 300} == set(fixture_ids)

    @staticmethod
    async def test_gameweeks(loop, fpl):
        gameweeks = fpl.gameweeks
        assert isinstance(gameweeks, dict)
        assert len(gameweeks) == 47
        for gameweek in gameweeks.values():
            assert isinstance(gameweek, Gameweek)

    @staticmethod
    @pytest.mark.skip(reason="Cannot currently test it.")
    async def test_classic_league(loop, fpl):
        await fpl.login()
        classic_league = await fpl.get_classic_league(173226)
        assert isinstance(classic_league, ClassicLeague)

        classic_league = await fpl.get_classic_league(173226, return_json=True)
        assert isinstance(classic_league, dict)

    @staticmethod
    async def test_h2h_league(loop, fpl):
        await fpl.login()
        h2h_league = await fpl.get_h2h_league(902521)
        assert isinstance(h2h_league, H2HLeague)

        h2h_league = await fpl.get_h2h_league(902521, True)
        assert isinstance(h2h_league, dict)

    @staticmethod
    async def test_login_with_no_email_password(loop, mocker, monkeypatch, fpl):
        mocked_text = mocker.patch(
            'aiohttp.ClientResponse.text', new_callable=AsyncMock)
        monkeypatch.setenv("FPL_EMAIL", "")
        monkeypatch.setenv("FPL_PASSWORD", "")
        with pytest.raises(ValueError):
            await fpl.login()
        mocked_text.assert_not_called()

    @staticmethod
    async def test_login_with_invalid_email_password(loop, monkeypatch, fpl):
        with pytest.raises(ValueError):
            await fpl.login(123, 123)

        monkeypatch.setenv("FPL_EMAIL", 123)
        monkeypatch.setenv("FPL_PASSWORD", 123)

        with pytest.raises(ValueError):
            await fpl.login()

    @staticmethod
    async def test_login_with_valid_email_password(loop, fpl):
        await fpl.login()

    @staticmethod
    async def test_points_against(loop, fpl):
        points_against = await fpl.get_points_against()
        assert isinstance(points_against, dict)

    @staticmethod
    async def test_fdr(loop, fpl):
        def test_main(fdr):
            assert isinstance(fdr, dict)

            location_extrema = {"H": [], "A": []}
            for _, positions in fdr.items():
                for location in positions.values():
                    location_extrema["H"].append(location["H"])
                    location_extrema["A"].append(location["A"])

            assert max(location_extrema["H"]) == 5.0
            assert min(location_extrema["H"]) == 1.0
            assert max(location_extrema["A"]) == 5.0
            assert min(location_extrema["A"]) == 1.0

        fdr = await fpl.FDR()
        test_main(fdr)
