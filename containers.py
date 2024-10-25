from customtkinter import CTk, CTkFrame, CTkFont, CTkLabel, CTkButton

from game.counter import Counter
from game.countrytools import game_country_generator
from game.question_handling import Question

from winfunctions import window_init, close_and_open


class MainWindow(CTk):
    """Класс для представления главного окна"""

    def __init__(self):
        super().__init__()

        window_init(self, 720, 480)

        self.header_font = CTkFont(family='Arial', size=70,
                                   weight='bold')
        self.start_button_font = CTkFont('Arial', 30)

        self.appname_label = CTkLabel(self, text='Столицы', font=self.header_font)
        self.appname_label.grid(row=0, column=0,
                                sticky="n", pady=40)

        self.start_button = CTkButton(self, text='Играть',
                                      font=self.start_button_font,
                                      corner_radius=20,
                                      fg_color='green',
                                      hover_color='#006800',
                                      command=self.open_game_window)

        self.start_button.grid(row=1, column=0,
                               ipadx=20, ipady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def open_game_window(self):
        """Запускает игровое окно"""

        close_and_open(self, GameWindow())


class GameWindow(CTk):
    """Класс для представления игрового окна"""

    def __init__(self):
        """Конструктор класса GameWindow. Размещает игровые виджеты"""

        super().__init__()

        self.game_countries = game_country_generator()
        self.counter = Counter()

        window_init(self, 720, 480)

        self.question_font = CTkFont(family='Arial', size=30,
                                     weight='bold')

        self.back_button = CTkButton(self, text="x", fg_color="grey",
                                     width=45, height=45,
                                     font=self.question_font,
                                     hover_color="#616161",
                                     command=self.back_button)
        self.back_button.place(x=10, y=10)

        self.new_question()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def back_button(self) -> None:
        """Уничтожает игровое окно и запускает главное окно"""

        close_and_open(self, MainWindow())

    def new_question(self, current_frame: None | CTkFrame = None,
                     correct: bool = False) -> None:
        """Принимает объект текущего фрейма с вопросом и булево значение ответа,
        обновляет счетчик и создает новый фрейм с вопросом"""

        try:
            if current_frame:
                current_frame.destroy()

            if correct:
                self.counter.update()

            self.question_frame = self.new_question_frame()
            self.question_frame.grid(row=0, column=0,
                                     sticky="n", pady=10)
        except AttributeError:
            pass

    def new_question_frame(self):
        """Создает и возвращает фрейм с новым вопросом"""

        try:
            q = Question.from_country(next(self.game_countries))
            return QuestionFrame(self, question=q,
                                 parent=self, border_width=2)
        except StopIteration:
            self.game_over()

    def game_over(self) -> None:
        """Создает и размещает фрейм с результатами игры"""

        GameOverFrame(self, parent=self, counter=self.counter,
                      border_width=2, height=400
                      ).grid(row=0, column=0,
                             sticky="ns", pady=30)


class QuestionFrame(CTkFrame):
    """Класс для представления фрейма с вопросом"""

    def __init__(self, master, question, parent, **kwargs):
        """Конструктор класса QuestionFrame. Создает фрейм в окне,
        создает кнопки с вопросами, размещает все виджеты"""

        super().__init__(master, **kwargs)

        self.parent_widget = parent
        self.question = question
        self.question_title = self.question.title
        self.question_font = CTkFont(family='Arial', size=50,
                                     weight='bold')
        self.option_font = CTkFont(family='Arial', size=25)

        self.buttons = []

        # Текстовая метка с вопросом
        CTkLabel(self, text=self.question.title,
                 font=self.question_font, width=550
                 ).grid(row=0, column=0, sticky="n", pady=(10, 50), padx=10)

        self.create_option_buttons()
        self.config_option_buttons()

    def create_option_buttons(self) -> None:
        """Создает и размещает кнопки вариантов ответа"""

        for option in self.question:
            btn = CTkButton(self, text=option,
                            font=self.option_font,
                            corner_radius=0)
            btn.grid(padx=10, sticky="ew",
                     ipady=15, pady=10)
            self.buttons.append(btn)

    def config_option_buttons(self) -> None:
        """Добавляет и настраивает обработку нажатий для каждой кнопки"""

        for button in self.buttons:
            button.configure(command=lambda b=button:
                             self.check_answer(b))
        self.grid_rowconfigure(0, weight=1)

    def check_answer(self, btn: CTkButton) -> None:
        """Принимает объект кнопки, при нажатии на нее, и обрабатывает ответ"""

        button_text = btn.cget('text')
        if button_text == self.question.answer:
            self.correct_answer(btn, button_text)
        else:
            self.wrong_answer(btn, button_text)

    def correct_answer(self, btn: CTkButton, button_text: str) -> None:
        """Принимает объект кнопки и ее текст, обрабатывает виджеты при правильном ответе"""

        self.configure(fg_color="#28401d")
        btn.configure(fg_color="green", hover=False)

        for button in self.buttons:
            button.configure(hover=False, state='disabled',
                             text_color_disabled="white")

        self.set_next_button("#326e31", button_text, correct=True)

    def wrong_answer(self, btn: CTkButton, button_text: str) -> None:
        """Принимает объект кнопки и ее текст, обрабатывает виджеты при неправильном ответе"""

        self.configure(fg_color="#661616")
        btn.configure(fg_color="red", hover=False)

        correct_answer_button = self.buttons.pop(self.question.answer_index)
        correct_answer_button.configure(fg_color="green", state='disabled',
                                        text_color_disabled="white")

        for button in self.buttons:
            button.configure(hover=False, state='disabled',
                             text_color_disabled="white")

        self.set_next_button("#a62828", button_text)

    def set_next_button(self, fg_color: str, button_text: str, correct=False) -> None:
        """Принимает цвет и текст кнопки, создает и размещает кнопку для перехода к следующему вопросу"""

        next_button = CTkButton(self, fg_color=fg_color, text=">>>",
                                width=70, corner_radius=0, hover=False,
                                command=lambda: GameWindow.new_question(
                                    self.parent_widget,
                                    current_frame=self,
                                    correct=correct)
                                )
        next_button.grid(row=self.question.options.index(button_text) + 1,
                         column=0, padx=10,
                         ipady=18, pady=10,
                         sticky="e")


class GameOverFrame(CTkFrame):
    """Класс для представления фрейма с результатами игры"""

    def __init__(self, master, parent, counter, **kwargs):
        """Конструктор класса GameOverFrame. Размещает виджеты"""

        super().__init__(master, **kwargs)
        self.parent = parent
        self.counter = counter

        self.comments = [
            'Нужно потренироваться :(',
            'Лучше, чем ничего.',
            'Когда-нибудь будет больше.',
            'Сойдет.',
            'А ты не так уж плох :)',
            'Вот это да!'
        ]

        CTkLabel(self, text="Ваш результат:",
                 font=CTkFont(family='Arial', size=50,
                              weight='bold')
                 ).grid(row=0, column=0,
                        pady=20, padx=30)

        CTkLabel(self, text=f"{counter} из 5\n\n {self.comments[int(counter)]}",
                 font=CTkFont(family='Arial', size=30),
                 ).grid(row=1, column=0,
                        pady=30)

        CTkButton(self, text="Играть снова",
                  font=CTkFont('Arial', 30),
                  corner_radius=20,
                  fg_color='green',
                  hover_color='#006800',
                  command=self.play_again
                  ).grid(row=2, column=0,
                         pady=50)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def play_again(self) -> None:
        """Перезапускает игру"""

        close_and_open(self.parent, GameWindow())
