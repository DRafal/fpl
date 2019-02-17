import aiohttp
import pytest

from fpl import FPL


@pytest.fixture()
async def fpl():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    yield fpl
    await session.close()


@pytest.fixture()
async def classic_league():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    classic_league = await fpl.get_classic_league(633353)
    yield classic_league
    await session.close()


@pytest.fixture()
async def gameweek():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    gameweek = await fpl.get_gameweek(6)
    yield gameweek
    await session.close()


@pytest.fixture()
async def player():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    player = await fpl.get_player(345, include_summary=True)
    yield player
    await session.close()


@pytest.fixture()
async def settings():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    settings = await fpl.get_settings()
    yield settings
    await session.close()


@pytest.fixture()
async def team():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    team = await fpl.get_team(14)
    yield team
    await session.close()


