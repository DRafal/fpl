import pytest

from fpl.dictionaries.api_keywords import *
from fpl.models.leagues import UserStandingsClassicEntry, UserNewEntry
from tests.helper import AsyncMock

classic_league_data = {
    NEW_ENTRIES: {
        HAS_NEXT: False,
        PAGE: 1,
        RESULTS: [
            {
                ENTRY: 214141,
                ENTRY_NAME: "Anonymous",
                JOINED_TIME: "2020-07-08T15:00:08.004357Z",
                PLAYER_FIRST_NAME: "John",
                PLAYER_LAST_NAME: "Doe"
            }
        ]
    },
    LEAGUE: {
        ID: 633353,
        NAME: "Steem Fantasy League",
        CREATED: "2018-08-07T00:03:18Z",
        CLOSED: False,
        MAX_ENTRIES: None,
        RANK: None,
        LEAGUE_TYPE: "x",
        SCORING: "c",
        ADMIN_ENTRY: 2779525,
        START_EVENT: 1
    },
    STANDINGS: {
        HAS_NEXT: False,
        PAGE: 1,
        RESULTS: [
            {
                ID: 31124573,
                ENTRY_NAME: "awd2",
                PLAYER_NAME: "Oleg Smolerov",
                RANK: 1,
                LAST_RANK: 1,
                RANK_SORT: 1,
                TOTAL: 1677,
                ENTRY: 123748,
                EVENT_TOTAL: 16
            },
            {
                ID: 20990567,
                ENTRY_NAME: "Metalheadz",
                EVENT_TOTAL: 58,
                PLAYER_NAME: "Robert Roman",
                RANK: 2,
                LAST_RANK: 2,
                RANK_SORT: 2,
                TOTAL: 1634,
                ENTRY: 3645024
            }
        ]
    }
}

h2h_league_data = {
    LEAGUE: {
        ID: 946125,
        NAME: "THE PUNDITS H2H",
        CREATED: "2019-08-07T20:52:58.751814Z",
        CLOSED: True,
        MAX_ENTRIES: None,
        LEAGUE_TYPE: "x",
        SCORING: "h",
        ADMIN_ENTRY: 1726046,
        START_EVENT: 1
    },
    NEW_ENTRIES: {
        HAS_NEXT: False,
        PAGE: 1,
        RESULTS: [

        ]
    },
    STANDINGS: {
        HAS_NEXT: False,
        PAGE: 1,
        RESULTS: []
    }
}


class TestClassicLeague:
    @staticmethod
    def test_init(loop, classic_league):
        assert classic_league.id == 633353
        assert classic_league.name == "Steem Fantasy League"
        assert classic_league.created == "2018-08-07T00:03:18Z"
        assert not classic_league.closed
        assert classic_league.rank is None
        assert classic_league.league_type == "x"
        assert classic_league.scoring == "c"
        assert classic_league.admin_entry == 2779525
        assert classic_league.start_event == 1

    @staticmethod
    def test_str(loop, classic_league):
        assert str(classic_league) == "Steem Fantasy League - 633353"

    @staticmethod
    async def test_get_specific_standing(loop, mocker, classic_league):
        mocked_fetch = mocker.patch("fpl.models.leagues.fetch",
                                    return_value=classic_league_data,
                                    new_callable=AsyncMock)
        standings = await classic_league.get_specific_standing(page=1, phase_id=1)

        assert isinstance(standings, list)
        for entry in standings:
            assert isinstance(entry, UserStandingsClassicEntry)
        assert len(standings) == 2

    @staticmethod
    async def test_get_new_entries(loop, mocker, classic_league):
        mocked_fetch = mocker.patch("fpl.models.leagues.fetch",
                                    return_value=classic_league_data,
                                    new_callable=AsyncMock)
        new_entries = await classic_league.get_new_entries()
        assert isinstance(new_entries, list)
        for entry in new_entries:
            assert isinstance(entry, UserNewEntry)
        assert len(new_entries) == 1


class TestUserStandingsClassicEntry:
    @staticmethod
    def test_init():
        first_user = UserStandingsClassicEntry(classic_league_data[STANDINGS][RESULTS][0])
        second_user = UserStandingsClassicEntry(classic_league_data[STANDINGS][RESULTS][1])

        assert first_user.id == 31124573
        assert first_user.entry_name == "awd2"
        assert first_user.player_name == "Oleg Smolerov"
        assert first_user.rank == 1
        assert first_user.last_rank == 1
        assert first_user.rank_sort == 1
        assert first_user.total == 1677
        assert first_user.entry == 123748
        assert first_user.event_total == 16

        assert second_user.id == 20990567
        assert second_user.entry_name == "Metalheadz"
        assert second_user.event_total == 58
        assert second_user.player_name == "Robert Roman"
        assert second_user.rank == 2
        assert second_user.last_rank == 2
        assert second_user.rank_sort == 2
        assert second_user.total == 1634
        assert second_user.entry == 3645024


class TestUserNewClassicEntry:
    @staticmethod
    def test_init():
        new_entry_user = UserNewEntry(classic_league_data[NEW_ENTRIES][RESULTS][0])

        assert new_entry_user.entry == 214141
        assert new_entry_user.entry_name == "Anonymous"
        assert new_entry_user.joined_time == "2020-07-08T15:00:08.004357Z"
        assert new_entry_user.player_first_name == "John"
        assert new_entry_user.player_last_name == "Doe"


class TestH2HLeague:
    @staticmethod
    def test_init(loop, h2h_league):
        assert h2h_league.id == 946125
        assert h2h_league.name == "THE PUNDITS H2H"
        assert h2h_league.created == "2019-08-07T20:52:58.751814Z"
        assert h2h_league.closed
        assert h2h_league.rank is None
        assert h2h_league.league_type == "x"
        assert h2h_league.scoring == "h"
        assert h2h_league.admin_entry == 1726046
        assert h2h_league.start_event == 1

    @staticmethod
    def test_h2h_league(loop, h2h_league):
        assert h2h_league.__str__() == "THE PUNDITS H2H - 946125"

    @staticmethod
    async def test_get_fixtures_with_known_gameweek_unauthorized(loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures(gameweek=1)

    @staticmethod
    @pytest.mark.skip(reason="Need to mock logging in properly.")
    async def test_get_fixtures_with_known_gameweek_authorized(oop, mocker, fpl, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)

        fixtures = await h2h_league.get_fixtures(gameweek=1)
        assert isinstance(fixtures, list)
        mocked_logged_in.assert_called_once()

    @staticmethod
    async def test_get_fixtures_with_unknown_gameweek_unauthorized(loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures()

    @staticmethod
    @pytest.mark.skip(reason="Need to mock logging in properly.")
    async def test_get_fixtures_with_unknown_gameweek_authorized(loop, mocker, fpl, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)
        await fpl.login()
        fixtures = await h2h_league.get_fixtures()
        assert isinstance(fixtures, list)
        mocked_logged_in.assert_called_once()
