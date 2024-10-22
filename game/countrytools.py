from random import sample, shuffle, randint
from collections.abc import Generator

from game.gamedata import countries_and_cities


def get_countries_list() -> list[str]:
    """Возвращает список всех доступных стран"""

    countries = list(countries_and_cities.keys())
    return countries


def game_country_generator() -> Generator[str, None, None]:
    """Возвращает генератор, состоящий из 5-и стран"""

    countries = get_countries_list()
    countries_for_game = sample(countries, k=5)
    for country in countries_for_game:
        yield country


def get_capital(country: str) -> str:
    """Принимает страну, возвращает столицу"""

    return countries_and_cities[country][0]


def false_country_options(country: str) -> list[str]:
    """Принимает страну, возвращает список всех ложных вариантов ответа для нее"""

    return countries_and_cities[country][1:]


def set_options_and_answer(country: str) -> tuple[list[str], str]:
    """Принимает страну, возвращает кортеж: (варианты_ответа, правильный ответ)"""

    options = false_country_options(country)
    capital = get_capital(country)
    shuffle(options)
    options.insert(randint(0, 3), capital)
    return options[:4], capital
