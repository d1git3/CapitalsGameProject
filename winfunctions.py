from customtkinter import CTk, set_appearance_mode


def close_and_open(window_to_close: CTk, window_to_open: CTk) -> None:
    """Принимает два окна, одно закрывает, второе открывает"""

    window_to_close.withdraw()
    window_to_close.quit()
    window_to_open.mainloop()


def window_init(window: CTk, width: int, height: int) -> None:
    """Принимает объект окна, ширину и высоту, настраивает окно, ничего не возвращает"""

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    win_upper_left_corner_x = (screen_width - width) // 2
    win_upper_left_corner_y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{win_upper_left_corner_x}+{win_upper_left_corner_y}')
    window.title('Столицы')
    set_appearance_mode("dark")
