from ..dictionaries.api_keywords import *
from collections import namedtuple

GameweekTopPlayer = namedtuple('GameweekTopPlayer', ['id', 'points'])
ChipPlayed = namedtuple('Chip', ['chip_name', 'num_played'])


class Gameweek:
    """A class representing a gameweek of the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         gameweek = await fpl.get_gameweek(1)
      ...     print(gameweek)
      ...
      >>> asyncio.run(main())
      Gameweek 1 - 10 Aug 19:00
    """

    def __init__(self, gameweek_information):
        self.average_entry_score = gameweek_information.get(AVERAGE_ENTRY_SCORE)
        self.data_checked = gameweek_information.get(DATA_CHECKED)
        self.deadline_time = gameweek_information.get(DEADLINE_TIME)
        self.deadline_time_epoch = gameweek_information.get(DEADLINE_TIME_EPOCH)
        self.deadline_time_game_offset = gameweek_information.get(DEADLINE_TIME_GAME_OFFSET)
        self.finished = gameweek_information.get(FINISHED)
        self.highest_score = gameweek_information.get(HIGHEST_SCORE)
        self.highest_scoring_entry = gameweek_information.get(HIGHEST_SCORING_ENTRY)
        self.id = gameweek_information.get(ID)
        self.is_current = gameweek_information.get(IS_CURRENT)
        self.is_next = gameweek_information.get(IS_NEXT)
        self.is_previous = gameweek_information.get(IS_PREVIOUS)
        self.most_captained = gameweek_information.get(MOST_CAPTAINED)
        self.most_selected = gameweek_information.get(MOST_SELECTED)
        self.most_transferred_in = gameweek_information.get(MOST_TRANSFERRED_IN)
        self.most_vice_captained = gameweek_information.get(MOST_VICE_CAPTAINED)
        self.name = gameweek_information.get(NAME)
        self.transfers_made = gameweek_information.get(TRANSFERS_MADE)
        self.top_element = gameweek_information.get(TOP_ELEMENT)
        if gameweek_information.get(TOP_ELEMENT_INFO):
            self.top_element_info = GameweekTopPlayer(
                id=gameweek_information[TOP_ELEMENT_INFO][ID],
                points=gameweek_information[TOP_ELEMENT_INFO][POINTS]
            )
        self.chip_plays = [
            ChipPlayed(chip_name=chip[CHIP_NAME], num_played=chip[NUM_PLAYED])
            for chip in gameweek_information[CHIP_PLAYS]
        ]

    def __repr__(self):
        return f'Gameweek(name={self.name}, status={"finished" if self.finished else "not finished"})'

    def __str__(self):
        return f'{self.name}'
