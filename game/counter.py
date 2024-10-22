class Counter:
    """Класс для представления счетчика правильных ответов"""

    def __init__(self):
        self.correct_answers = 0

    def __str__(self):
        return str(self.correct_answers)

    def __int__(self):
        return int(self.correct_answers)

    def update(self):
        """Увеличивает значение счетчика на единицу"""

        self.correct_answers += 1
