from fpl.dictionaries.api_keywords import *
from fpl.models.fixture import Fixture, FixturePlayers, PlayerEvent, EMPTY_FIXTURE_PLAYERS

fixture_data_finished = {
    CODE: 1059760,
    EVENT: 6,
    FINISHED: True,
    FINISHED_PROVISIONAL: True,
    ID: 59,
    KICKOFF_TIME: "2019-09-20T19:00:00Z",
    MINUTES: 90,
    PROVISIONAL_START_TIME: False,
    STARTED: True,
    TEAM_AWAY: 3,
    TEAM_AWAY_SCORE: 3,
    TEAM_HOME: 16,
    TEAM_HOME_SCORE: 1,
    STATS: [
        {
            IDENTIFIER: GOALS_SCORED,
            A: [
                {
                    VALUE: 1,
                    ELEMENT: 59
                },
                {
                    VALUE: 1,
                    ELEMENT: 67
                },
                {
                    VALUE: 1,
                    ELEMENT: 505
                }
            ],
            H: [
                {
                    VALUE: 1,
                    ELEMENT: 321
                }
            ]
        },
        {
            IDENTIFIER: ASSISTS,
            A: [
                {
                    VALUE: 1,
                    ELEMENT: 65
                },
                {
                    VALUE: 1,
                    ELEMENT: 476
                },
                {
                    VALUE: 1,
                    ELEMENT: 494
                }
            ],
            H: [
                {
                    VALUE: 1,
                    ELEMENT: 437
                }
            ]
        },
        {
            IDENTIFIER: OWN_GOALS,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: PENALTIES_SAVED,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: PENALTIES_MISSED,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: YELLOW_CARDS,
            A: [
                {
                    VALUE: 1,
                    ELEMENT: 82
                },
                {
                    VALUE: 1,
                    ELEMENT: 446
                },
                {
                    VALUE: 1,
                    ELEMENT: 505
                }
            ],
            H: [
                {
                    VALUE: 1,
                    ELEMENT: 328
                }
            ]
        },
        {
            IDENTIFIER: RED_CARDS,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: SAVES,
            A: [
                {
                    VALUE: 6,
                    ELEMENT: 494
                }
            ],
            H: [

            ]
        },
        {
            IDENTIFIER: BONUS,
            A: [
                {
                    VALUE: 3,
                    ELEMENT: 494
                },
                {
                    VALUE: 1,
                    ELEMENT: 67
                }
            ],
            H: [
                {
                    VALUE: 2,
                    ELEMENT: 321
                }
            ]
        },
        {
            IDENTIFIER: BPS,
            A: [
                {
                    VALUE: 34,
                    ELEMENT: 494
                },
                {
                    VALUE: 30,
                    ELEMENT: 67
                },
                {
                    VALUE: 26,
                    ELEMENT: 59
                },
                {
                    VALUE: 25,
                    ELEMENT: 65
                },
                {
                    VALUE: 23,
                    ELEMENT: 476
                },
                {
                    VALUE: 23,
                    ELEMENT: 505
                },
                {
                    VALUE: 14,
                    ELEMENT: 58
                },
                {
                    VALUE: 7,
                    ELEMENT: 82
                },
                {
                    VALUE: 6,
                    ELEMENT: 446
                },
                {
                    VALUE: 4,
                    ELEMENT: 79
                },
                {
                    VALUE: 3,
                    ELEMENT: 75
                },
                {
                    VALUE: 3,
                    ELEMENT: 80
                },
                {
                    VALUE: 2,
                    ELEMENT: 68
                }
            ],
            H: [
                {
                    VALUE: 31,
                    ELEMENT: 321
                },
                {
                    VALUE: 23,
                    ELEMENT: 328
                },
                {
                    VALUE: 17,
                    ELEMENT: 437
                },
                {
                    VALUE: 16,
                    ELEMENT: 486
                },
                {
                    VALUE: 14,
                    ELEMENT: 304
                },
                {
                    VALUE: 14,
                    ELEMENT: 508
                },
                {
                    VALUE: 13,
                    ELEMENT: 307
                },
                {
                    VALUE: 9,
                    ELEMENT: 320
                },
                {
                    VALUE: 9,
                    ELEMENT: 325
                },
                {
                    VALUE: 7,
                    ELEMENT: 319
                },
                {
                    VALUE: 6,
                    ELEMENT: 305
                },
                {
                    VALUE: 4,
                    ELEMENT: 313
                },
                {
                    VALUE: 3,
                    ELEMENT: 532
                },
                {
                    VALUE: 2,
                    ELEMENT: 323
                }
            ]
        }
    ],
    TEAM_HOME_DIFFICULTY: 2,
    TEAM_AWAY_DIFFICULTY: 2
}

fixture_data_not_finished = {
    CODE: 1059760,
    EVENT: 6,
    FINISHED: False,
    FINISHED_PROVISIONAL: False,
    ID: 59,
    KICKOFF_TIME: "2019-09-20T19:00:00Z",
    MINUTES: 90,
    PROVISIONAL_START_TIME: False,
    STARTED: True,
    TEAM_AWAY: 3,
    TEAM_AWAY_SCORE: 3,
    TEAM_HOME: 16,
    TEAM_HOME_SCORE: 1,
    STATS: [
        {
            IDENTIFIER: GOALS_SCORED,
            A: [
                {
                    VALUE: 1,
                    ELEMENT: 59
                },
                {
                    VALUE: 1,
                    ELEMENT: 67
                },
                {
                    VALUE: 1,
                    ELEMENT: 505
                }
            ],
            H: [
                {
                    VALUE: 1,
                    ELEMENT: 321
                }
            ]
        },
        {
            IDENTIFIER: ASSISTS,
            A: [
                {
                    VALUE: 1,
                    ELEMENT: 65
                },
                {
                    VALUE: 1,
                    ELEMENT: 476
                },
                {
                    VALUE: 1,
                    ELEMENT: 494
                }
            ],
            H: [
                {
                    VALUE: 1,
                    ELEMENT: 437
                }
            ]
        },
        {
            IDENTIFIER: OWN_GOALS,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: PENALTIES_SAVED,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: PENALTIES_MISSED,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: YELLOW_CARDS,
            A: [
                {
                    VALUE: 1,
                    ELEMENT: 82
                },
                {
                    VALUE: 1,
                    ELEMENT: 446
                },
                {
                    VALUE: 1,
                    ELEMENT: 505
                }
            ],
            H: [
                {
                    VALUE: 1,
                    ELEMENT: 328
                }
            ]
        },
        {
            IDENTIFIER: RED_CARDS,
            A: [

            ],
            H: [

            ]
        },
        {
            IDENTIFIER: SAVES,
            A: [
                {
                    VALUE: 6,
                    ELEMENT: 494
                }
            ],
            H: [

            ]
        },
        {
            IDENTIFIER: BONUS,
            A: [],
            H: []
        },
        {
            IDENTIFIER: BPS,
            A: [
                {
                    VALUE: 34,
                    ELEMENT: 494
                },
                {
                    VALUE: 30,
                    ELEMENT: 67
                },
                {
                    VALUE: 26,
                    ELEMENT: 59
                },
                {
                    VALUE: 25,
                    ELEMENT: 65
                },
                {
                    VALUE: 23,
                    ELEMENT: 476
                },
                {
                    VALUE: 23,
                    ELEMENT: 505
                },
                {
                    VALUE: 14,
                    ELEMENT: 58
                },
                {
                    VALUE: 7,
                    ELEMENT: 82
                },
                {
                    VALUE: 6,
                    ELEMENT: 446
                },
                {
                    VALUE: 4,
                    ELEMENT: 79
                },
                {
                    VALUE: 3,
                    ELEMENT: 75
                },
                {
                    VALUE: 3,
                    ELEMENT: 80
                },
                {
                    VALUE: 2,
                    ELEMENT: 68
                }
            ],
            H: [
                {
                    VALUE: 31,
                    ELEMENT: 321
                },
                {
                    VALUE: 23,
                    ELEMENT: 328
                },
                {
                    VALUE: 17,
                    ELEMENT: 437
                },
                {
                    VALUE: 16,
                    ELEMENT: 486
                },
                {
                    VALUE: 14,
                    ELEMENT: 304
                },
                {
                    VALUE: 14,
                    ELEMENT: 508
                },
                {
                    VALUE: 13,
                    ELEMENT: 307
                },
                {
                    VALUE: 9,
                    ELEMENT: 320
                },
                {
                    VALUE: 9,
                    ELEMENT: 325
                },
                {
                    VALUE: 7,
                    ELEMENT: 319
                },
                {
                    VALUE: 6,
                    ELEMENT: 305
                },
                {
                    VALUE: 4,
                    ELEMENT: 313
                },
                {
                    VALUE: 3,
                    ELEMENT: 532
                },
                {
                    VALUE: 2,
                    ELEMENT: 323
                }
            ]
        }
    ],
    TEAM_HOME_DIFFICULTY: 2,
    TEAM_AWAY_DIFFICULTY: 2
}


class TestFixtureFinished:
    @staticmethod
    def test_init():
        fixture = Fixture(fixture_data_finished)
        assert fixture.code == 1059760
        assert fixture.event == 6
        assert fixture.finished
        assert fixture.finished_provisional
        assert fixture.id == 59
        assert fixture.kickoff_time == '2019-09-20T19:00:00Z'
        assert fixture.minutes == 90
        assert not fixture.provisional_start_time
        assert fixture.started
        assert fixture.team_away == 3
        assert fixture.team_away_difficulty == 2
        assert fixture.team_away_score == 3
        assert fixture.team_home == 16
        assert fixture.team_home_difficulty == 2
        assert fixture.team_home_score == 1
        assert fixture.assisters == FixturePlayers(
            home=[PlayerEvent(player_id=437, value=1, team=16)],
            away=[PlayerEvent(player_id=65, value=1, team=3), PlayerEvent(player_id=476, value=1, team=3),
                  PlayerEvent(player_id=494, value=1, team=3)]
        )
        assert fixture.bonus() == FixturePlayers(
            home=[PlayerEvent(player_id=321, value=2, team=16)],
            away=[PlayerEvent(player_id=494, value=3, team=3), PlayerEvent(player_id=67, value=1, team=3)]
        )
        assert fixture.bps == FixturePlayers(
            home=[PlayerEvent(player_id=321, value=31, team=16), PlayerEvent(player_id=328, value=23, team=16),
                  PlayerEvent(player_id=437, value=17, team=16), PlayerEvent(player_id=486, value=16, team=16),
                  PlayerEvent(player_id=304, value=14, team=16), PlayerEvent(player_id=508, value=14, team=16),
                  PlayerEvent(player_id=307, value=13, team=16), PlayerEvent(player_id=320, value=9, team=16),
                  PlayerEvent(player_id=325, value=9, team=16), PlayerEvent(player_id=319, value=7, team=16),
                  PlayerEvent(player_id=305, value=6, team=16), PlayerEvent(player_id=313, value=4, team=16),
                  PlayerEvent(player_id=532, value=3, team=16), PlayerEvent(player_id=323, value=2, team=16)],
            away=[PlayerEvent(player_id=494, value=34, team=3), PlayerEvent(player_id=67, value=30, team=3),
                  PlayerEvent(player_id=59, value=26, team=3), PlayerEvent(player_id=65, value=25, team=3),
                  PlayerEvent(player_id=476, value=23, team=3), PlayerEvent(player_id=505, value=23, team=3),
                  PlayerEvent(player_id=58, value=14, team=3), PlayerEvent(player_id=82, value=7, team=3),
                  PlayerEvent(player_id=446, value=6, team=3), PlayerEvent(player_id=79, value=4, team=3),
                  PlayerEvent(player_id=75, value=3, team=3), PlayerEvent(player_id=80, value=3, team=3),
                  PlayerEvent(player_id=68, value=2, team=3)]
        )
        assert fixture.goalscorers == FixturePlayers(
            home=[PlayerEvent(player_id=321, value=1, team=16)],
            away=[PlayerEvent(player_id=59, value=1, team=3), PlayerEvent(player_id=67, value=1, team=3),
                  PlayerEvent(player_id=505, value=1, team=3)]
        )
        assert fixture.own_goalscorers == EMPTY_FIXTURE_PLAYERS
        assert fixture.penalty_misses == EMPTY_FIXTURE_PLAYERS
        assert fixture.penalty_saves == EMPTY_FIXTURE_PLAYERS
        assert fixture.red_cards == EMPTY_FIXTURE_PLAYERS
        assert fixture.saves == FixturePlayers(
            home=[],
            away=[PlayerEvent(player_id=494, value=6, team=3)]
        )
        assert fixture.yellow_cards == FixturePlayers(
            home=[PlayerEvent(player_id=328, value=1, team=16)],
            away=[PlayerEvent(player_id=82, value=1, team=3), PlayerEvent(player_id=446, value=1, team=3),
                  PlayerEvent(player_id=505, value=1, team=3)]
        )


class TestFixtureUnfinished:
    @staticmethod
    def test_init():
        fixture = Fixture(fixture_data_not_finished)
        assert fixture.code == 1059760
        assert fixture.event == 6
        assert not fixture.finished
        assert not fixture.finished_provisional
        assert fixture.id == 59
        assert fixture.kickoff_time == '2019-09-20T19:00:00Z'
        assert fixture.minutes == 90
        assert not fixture.provisional_start_time
        assert fixture.started
        assert fixture.team_away == 3
        assert fixture.team_away_difficulty == 2
        assert fixture.team_away_score == 3
        assert fixture.team_home == 16
        assert fixture.team_home_difficulty == 2
        assert fixture.team_home_score == 1
        assert fixture.assisters == FixturePlayers(
            home=[PlayerEvent(player_id=437, value=1, team=16)],
            away=[PlayerEvent(player_id=65, value=1, team=3), PlayerEvent(player_id=476, value=1, team=3),
                  PlayerEvent(player_id=494, value=1, team=3)]
        )
        assert fixture.bonus() == EMPTY_FIXTURE_PLAYERS
        assert fixture.bps == FixturePlayers(
            home=[PlayerEvent(player_id=321, value=31, team=16), PlayerEvent(player_id=328, value=23, team=16),
                  PlayerEvent(player_id=437, value=17, team=16), PlayerEvent(player_id=486, value=16, team=16),
                  PlayerEvent(player_id=304, value=14, team=16), PlayerEvent(player_id=508, value=14, team=16),
                  PlayerEvent(player_id=307, value=13, team=16), PlayerEvent(player_id=320, value=9, team=16),
                  PlayerEvent(player_id=325, value=9, team=16), PlayerEvent(player_id=319, value=7, team=16),
                  PlayerEvent(player_id=305, value=6, team=16), PlayerEvent(player_id=313, value=4, team=16),
                  PlayerEvent(player_id=532, value=3, team=16), PlayerEvent(player_id=323, value=2, team=16)],
            away=[PlayerEvent(player_id=494, value=34, team=3), PlayerEvent(player_id=67, value=30, team=3),
                  PlayerEvent(player_id=59, value=26, team=3), PlayerEvent(player_id=65, value=25, team=3),
                  PlayerEvent(player_id=476, value=23, team=3), PlayerEvent(player_id=505, value=23, team=3),
                  PlayerEvent(player_id=58, value=14, team=3), PlayerEvent(player_id=82, value=7, team=3),
                  PlayerEvent(player_id=446, value=6, team=3), PlayerEvent(player_id=79, value=4, team=3),
                  PlayerEvent(player_id=75, value=3, team=3), PlayerEvent(player_id=80, value=3, team=3),
                  PlayerEvent(player_id=68, value=2, team=3)]
        )
        assert fixture.goalscorers == FixturePlayers(
            home=[PlayerEvent(player_id=321, value=1, team=16)],
            away=[PlayerEvent(player_id=59, value=1, team=3), PlayerEvent(player_id=67, value=1, team=3),
                  PlayerEvent(player_id=505, value=1, team=3)]
        )
        assert fixture.own_goalscorers == EMPTY_FIXTURE_PLAYERS
        assert fixture.penalty_misses == EMPTY_FIXTURE_PLAYERS
        assert fixture.penalty_saves == EMPTY_FIXTURE_PLAYERS
        assert fixture.red_cards == EMPTY_FIXTURE_PLAYERS
        assert fixture.saves == FixturePlayers(
            home=[],
            away=[PlayerEvent(player_id=494, value=6, team=3)]
        )
        assert fixture.yellow_cards == FixturePlayers(
            home=[PlayerEvent(player_id=328, value=1, team=16)],
            away=[PlayerEvent(player_id=82, value=1, team=3), PlayerEvent(player_id=446, value=1, team=3),
                  PlayerEvent(player_id=505, value=1, team=3)]
        )

    @staticmethod
    def test_str(fixture):
        assert str(fixture) == "Southampton vs. Bournemouth - 2019-09-20T19:00:00Z"


