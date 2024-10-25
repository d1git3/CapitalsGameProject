from game.countrytools import set_options_and_answer


class Question:
    """Класс для представления вопроса"""

    def __init__(self, title, options, answer):
        self.title = f"Столица {title[:-1]}и?"
        self.options = options
        self.answer = answer
        self.answer_index = options.index(answer)

    def __iter__(self):
        return QuestionIterator(self.options)

    @classmethod
    def from_country(cls, country: str):
        """Принимает страну, возвращает вопрос"""

        current_country = country
        options, answer = set_options_and_answer(country)
        return cls(title=current_country,
                        options=options,
                        answer=answer)


class QuestionIterator:
    """Класс для представления итератора для вопроса"""

    def __init__(self, options):
        self.options = options
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.options):
            result = self.options[self.counter]
            self.counter += 1
            return result
        raise StopIteration
