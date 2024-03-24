from customtkinter import *
import pyautogui
import time
import pywinstyles
import keyboard
import threading
from PIL import Image, ImageTk
from settings import *

# Настройки основного окна
window = CTk()
window.iconbitmap("icon.ico")
window.geometry("400x170+50+50")
set_appearance_mode("dark")
window.resizable(False, False)
window.wm_attributes("-topmost", True)

image_path = "bg.png"
bg_image_pil = Image.open(image_path)
bg_image = ImageTk.PhotoImage(bg_image_pil)
bg_image_label = CTkLabel(master=window, image=bg_image)
bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)
pywinstyles.apply_style(window.title(""), style_options)

click_counter = 0
total_time = 0


def autoclick():
    """Функция для авто клика"""
    global click_counter, seconds_entry_value, milliseconds_entry_value, selected_button_value, click_type_value, \
        repeat_type_value, repeat_count_value
    if button.cget("text") == "Начать":
        button.configure(text="Остановить")
        time.sleep(1)
        threading.Thread(target=click_loop, args=(
            seconds_entry_value, milliseconds_entry_value, selected_button_value, click_type_value, repeat_type_value,
            repeat_count_value)).start()
    else:
        button.configure(text="Начать")
        click_counter = -1  # Сбросить до 0


def click_loop(seconds, milliseconds, selected_button, click_type, repeat_type, repeat_count):
    """Цикл для выполнения кликов."""
    global click_counter, total_time
    start_time = time.time()
    while button.cget("text") == "Остановить":
        # TODO: Разобраться с repeat_type
        # print(repeat_type)
        if repeat_type == "Количество повторений:":
            for _ in range(repeat_count):
                perform_click(selected_button, click_type)
                click_counter += 1
                update_counter_label()
                total_time = time.time() - start_time
                time.sleep(seconds + milliseconds / 1000)
        else:
            perform_click(selected_button, click_type)
            click_counter += 1
            update_counter_label()
            total_time = time.time() - start_time
            time.sleep(seconds + milliseconds / 1000)


def perform_click(selected_button, click_type):
    """Выполняет клик."""
    global position_type_value, position_coordinates_value
    if position_type_value == "Любое место":  # Если выбрано стандартное место
        position = None
    else:
        try:
            position = tuple(map(int, position_coordinates_value.split(',')))  # Парсим координаты из строки
        except ValueError:
            position = None

    if position is not None:  # Проверяем, не является ли position None
        if click_type == "doubleClick":
            pyautogui.doubleClick(button=selected_button, x=position[0], y=position[1])
        elif click_type == "tripleClick":
            pyautogui.tripleClick(button=selected_button, x=position[0], y=position[1])
        else:
            pyautogui.click(button=selected_button, x=position[0], y=position[1])
    else:
        pyautogui.click(button=selected_button)  # Если position равно None, просто кликаем без координат


def update_counter_label():
    """Обновляет метку счетчика кликов."""
    counter_label.configure(text=f"Кликов: {click_counter}")


style_options = ["aero", "transparent", "win7", "inverse", "popup", "native"]
track_cursor_active = False
hotkey = config.get("Settings", "hotkey_value")


def change_hotkey(hotkey_button):
    """Функция для изменения горячей клавиши."""

    def on_key_press(event):
        """Обновляет значение горячей клавиши и текст на кнопке."""
        hotkey = event.name
        hotkey_button.configure(text=hotkey)
        update_key_label(hotkey)

    # Устанавливаем временный обработчик событий для перехвата нажатия клавиши
    keyboard.hook(on_key_press)


def update_key_label(hotkey):
    """Функция для обновления метки с текущей горячей клавишей."""
    key_label.configure(text=f"{hotkey} - старт/стоп.")


def open_settings_window():
    """Открывает окно настроек."""
    # TODO: чтобы открывалось 1 раз, вывести в отдельный файл
    global seconds_entry_value, milliseconds_entry_value, selected_button_value, click_type_value, repeat_type_value, \
        repeat_count_value, position_type_value, position_coordinates_value

    # Создание окна настроек
    settings_window = CTkToplevel()
    settings_window.title("Настройки")
    settings_window.geometry("790x550+470+50")
    pywinstyles.apply_style(settings_window, "win7")

    # Создание фрейма для размещения виджетов настройки
    settings_frame = CTkFrame(settings_window, corner_radius=20, fg_color="#3A3A3A")
    settings_frame.grid(pady=20, padx=20)

    # Фрейм для настроек мыши
    time_frame = CTkFrame(settings_frame)
    time_frame.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # Label для частоты клика
    label = CTkLabel(time_frame, text="Частота клика:", font=("Arial", 16, "bold"))
    label.grid(row=0, column=0, columnspan=2, pady=(5, 20))

    # Label и Entry для секунд
    seconds_label = CTkLabel(time_frame, text="Секунд:")
    seconds_label.grid(row=1, column=0, pady=(0, 5), padx=(20, 90))
    seconds_entry = CTkEntry(time_frame)
    seconds_entry.grid(row=1, column=1, pady=(0, 5), padx=(10, 50))
    seconds_entry.insert(0, str(seconds_entry_value))  # Установить значение по умолчанию

    # Label и Entry для миллисекунд
    milliseconds_label = CTkLabel(time_frame, text="Миллисекунд:")
    milliseconds_label.grid(row=2, column=0, pady=(0, 5), padx=(20, 48))
    milliseconds_entry = CTkEntry(time_frame)
    milliseconds_entry.grid(row=2, column=1, pady=(0, 16), padx=(10, 50))
    milliseconds_entry.insert(0, str(milliseconds_entry_value))  # Установить значение по умолчанию

    # Фрейм для настроек мыши
    mouse_frame = CTkFrame(settings_frame)
    mouse_frame.grid(row=0, column=3, columnspan=2, pady=(20, 10))

    # Label для способа клика
    click_label = CTkLabel(mouse_frame, text="Способы клика:", font=("Arial", 16, "bold"))
    click_label.grid(row=0, column=3, columnspan=2, pady=(5, 20))

    # Label и Dropdown для выбора кнопки мыши
    button_label = CTkLabel(mouse_frame, text="Кнопка мыши:")
    button_label.grid(row=1, column=3, pady=(0, 5), padx=(20, 80))
    button_options = ["Левая (стандарт)", "Правая", "Средняя"]
    selected_button = StringVar()
    selected_button.set(selected_button_value)  # Установить сохраненное значение
    button_dropdown = CTkComboBox(mouse_frame, variable=selected_button, values=button_options, font=("Arial", 12))
    button_dropdown.grid(row=1, column=4, pady=(0, 10), padx=(10, 50))

    # Label и Dropdown для выбора вида клика
    click_type_label = CTkLabel(mouse_frame, text="Вид клика:")
    click_type_label.grid(row=2, column=3, pady=(0, 5), padx=(20, 100))
    click_type_options = ["Одиночный (стандарт)", "Двойной", "Тройной"]
    selected_click_type = StringVar()
    selected_click_type.set(click_type_value)  # Установить сохраненное значение
    click_type_dropdown = CTkComboBox(mouse_frame, variable=selected_click_type, values=click_type_options,
                                      font=("Arial", 12))
    click_type_dropdown.grid(row=2, column=4, pady=(0, 10), padx=(10, 50))

    # Фрейм для настроек повторения
    repeat_frame = CTkFrame(settings_frame)
    repeat_frame.grid(row=4, column=0, columnspan=2, pady=(20, 10))

    # Label для длительности клика
    repeat_label = CTkLabel(repeat_frame, text="Длительность клика:", font=("Arial", 16, "bold"))
    repeat_label.grid(row=4, column=0, columnspan=2, pady=(5, 20))

    repeat_type_options = ["Количество повторений:", "С повторением до остановки"]
    repeat_type_var = StringVar()

    # Задаем значение переменной в соответствии с прочитанным из файла
    selected_option = config.get("Settings", "repeat_type_value")
    repeat_type_var.set(selected_option)

    # Создание радиокнопок для выбора типа повторения
    repeat_type_radiobuttons = [
        CTkRadioButton(repeat_frame, text=option, variable=repeat_type_var, value=option, command=lambda: None) for
        option in repeat_type_options]
    for i, radiobutton in enumerate(repeat_type_radiobuttons):
        radiobutton.grid(row=i + 5, column=0, columnspan=2 if i == 1 else 1,
                         pady=(10, 10), padx=(10, 0) if i == 0 else (10, 140))

    # Entry для ввода количества повторений
    repeat_count_entry = CTkEntry(repeat_frame)
    repeat_count_entry.grid(row=5, column=1, pady=(0, 10), padx=(20, 10))
    repeat_count_entry.insert(0, str(repeat_count_value))  # Установить значение по умолчанию

    # Фрейм для настроек позиции курсора
    position_frame = CTkFrame(settings_frame)
    position_frame.grid(row=4, column=3, columnspan=2, pady=(20, 10))

    # Label для позиции курсора
    position_label = CTkLabel(position_frame, text="Позиция курсора:", font=("Arial", 16, "bold"))
    position_label.grid(row=4, column=3, columnspan=2, pady=(5, 20))

    # Радиокнопки для выбора типа позиции курсора
    position_type_options = ["Определенное место:", "Любое место"]
    position_type_var = StringVar()

    # Задаем значение переменной в соответствии с прочитанным из файла
    selected_position_option = config.get("Settings", "position_type_value")
    position_type_var.set(selected_position_option)

    position_type_radiobuttons = [
        CTkRadioButton(position_frame, text=option, variable=position_type_var, value=option, command=lambda: None)
        for option in position_type_options]
    for i, radiobutton in enumerate(position_type_radiobuttons):
        radiobutton.grid(row=i + 5, column=3, columnspan=2 if i == 1 else 1,
                         pady=(10, 10), padx=(10, 0) if i == 0 else (21, 260))

    # Entry для ввода координат позиции курсора
    position_coordinates_entry = CTkEntry(position_frame)
    position_coordinates_entry.grid(row=5, column=4, pady=(0, 10), padx=(0, 33))
    position_coordinates_entry.insert(0, str(position_coordinates_value))  # Установить значение по умолчанию

    # Кнопка для выбора горячей клавиши
    hotkey_label = CTkLabel(settings_frame, text="Клавиша для старта/остановки:")
    hotkey_label.grid(row=5, column=0, pady=(0, 5))
    hotkey_button = CTkButton(settings_frame, text=config.get("Settings", "hotkey_value"),
                              command=lambda: change_hotkey(hotkey_button))
    hotkey_button.grid(row=5, column=1, pady=(0, 10))

    # Функция для постоянного обновления позиции курсора
    def update_cursor_position():
        global track_cursor_active
        if track_cursor_active:
            x, y = pyautogui.position()
            find_position_coordinates_entry.delete(0, 'end')
            find_position_coordinates_entry.insert(0, f"X: {x}, Y: {y}")
        threading.Timer(0.1, update_cursor_position).start()

    track_cursor_active = False

    def toggle_track_cursor():
        global track_cursor_active
        track_cursor_active = not track_cursor_active
        if track_cursor_active:
            update_cursor_position()
        else:
            find_position_coordinates_entry.delete(0, 'end')  # Очистить поле при отключении

    position_frame = CTkFrame(settings_frame)
    position_frame.grid(row=6, column=0, columnspan=2, pady=(10, 10))

    track_button = CTkButton(position_frame, text="Отслеживать курсор", command=toggle_track_cursor)
    track_button.grid(row=6, column=0, pady=(10, 10), padx=(10, 20))

    find_position_coordinates_entry = CTkEntry(position_frame)
    find_position_coordinates_entry.grid(row=6, column=1, pady=(10, 10), padx=(0, 10))

    def open_github():
        """Функция для открытия github"""
        os.startfile("https://github.com/Hohlovsky")

    def open_test_site():
        """Функция для открытия сайта c печеньем"""
        os.startfile("https://orteil.dashnet.org/cookieclicker/")

    info_frame = CTkFrame(settings_frame)
    info_frame.grid(row=6, column=3, columnspan=3, pady=(10, 10))

    git_button = CTkButton(info_frame, text="Github", command=open_github)
    git_button.grid(row=6, column=3, pady=(10, 10), padx=(10, 20))

    test_button = CTkButton(info_frame, text="Проверка", command=open_test_site)
    test_button.grid(row=6, column=4, pady=(10, 10), padx=(10, 20))

    def apply_window_style(style):
        # TODO: Чтобы всё окно менялось, а не только вокруг
        pywinstyles.apply_style(window, style)

    style_var = StringVar()
    style_var.set("aero")

    style_dropdown = CTkComboBox(settings_frame, variable=style_var, values=style_options, font=("Arial", 12))
    style_dropdown.grid(row=5, column=3, pady=(0, 10))

    # Кнопка для смены темы
    change_theme_button = CTkButton(settings_frame, text="Сменить тему",
                                    command=lambda: apply_window_style(style_var.get()))
    change_theme_button.grid(row=5, column=4, pady=(0, 10))

    settings_frame = CTkFrame(settings_window)
    settings_frame.grid(pady=20)

    # Кнопка для применения настроек
    apply_button = CTkButton(settings_frame, text="Применить", command=lambda: apply_settings(
        seconds_entry, milliseconds_entry, selected_button, selected_click_type, button_dropdown, click_type_dropdown,
        repeat_type_var, repeat_count_entry, hotkey_button, position_type_var, position_coordinates_entry),
                             fg_color="#369100", hover_color="#008500", width=250)
    apply_button.grid(row=9, column=0, columnspan=2, padx=(0, 100))

    # Кнопка для закрытия окна настроек
    close_button = CTkButton(settings_frame, text="Закрыть", command=settings_window.destroy, fg_color="#9E0016",
                             hover_color="#B62E40", width=250)
    close_button.grid(row=9, column=3, columnspan=2, padx=(100, 0))

    # Убедиться, что радиокнопки остаются выбранными после применения настроек
    selected_repeat_type_value = config.get("Settings", "repeat_type_value")
    for radiobutton in repeat_type_radiobuttons:
        if radiobutton.cget("text") == selected_repeat_type_value:
            radiobutton.select()

    selected_position_type_value = config.get("Settings", "position_type_value")
    for radiobutton in position_type_radiobuttons:
        if radiobutton.cget("text") == selected_position_type_value:
            radiobutton.select()


def apply_settings(seconds_entry, milliseconds_entry, selected_button, selected_click_type, button_dropdown,
                   click_type_dropdown, repeat_type_var, repeat_count_entry, hotkey_button, position_type_var,
                   position_coordinates_entry):
    """
    Применяет настройки, введенные пользователем в окне настроек.

    Аргументы:
        seconds_entry: Поле для ввода секунд.
        milliseconds_entry: Поле для ввода миллисекунд.
        selected_button: Выбранная кнопка мыши.
        selected_click_type: Выбранный тип клика.
        button_dropdown: Выпадающий список кнопок мыши.
        click_type_dropdown: Выпадающий список типов клика.
        repeat_type_var: Переменная типа повторения.
        repeat_count_entry: Поле для ввода количества повторений.
        hotkey_button: Кнопка для установки горячей клавиши.
        position_type_var: Переменная типа позиции курсора.
        position_coordinates_entry: Поле для ввода координат позиции курсора.
    """
    global seconds_entry_value, milliseconds_entry_value, selected_button_value, click_type_value, repeat_type_value, \
        repeat_count_value, hotkey_value, position_type_value, position_coordinates_value

    # Получение значений из пользовательского ввода
    seconds_entry_value = int(seconds_entry.get())
    milliseconds_entry_value = int(milliseconds_entry.get())

    # Сопоставление выбранной кнопки с соответствующей константой pyautogui
    button_mapping = {"Левая (стандарт)": "left", "Правая": "right", "Средняя": "middle"}
    selected_button_value = button_mapping.get(selected_button.get(), "left")

    # Обновление выбранных значений в выпадающих списках
    button_dropdown.set(selected_button.get())
    click_type_dropdown.set(selected_click_type.get())

    # Сопоставление выбранного типа клика с соответствующей функцией pyautogui
    click_type_mapping = {"Одиночный (стандарт)": "click", "Двойной": "doubleClick", "Тройной": "tripleClick"}
    click_type_value = click_type_mapping.get(selected_click_type.get(), "click")

    # Сохранение выбранных значений в файл конфигурации
    config.set("Settings", "selected_button_value", selected_button_value)
    config.set("Settings", "seconds_entry_value", str(seconds_entry_value))
    config.set("Settings", "milliseconds_entry_value", str(milliseconds_entry_value))
    config.set("Settings", "click_type_value", click_type_value)

    # Сохранение значений типа повторения и количества повторений в файл конфигурации
    try:
        repeat_count_value = int(repeat_count_entry.get())
    except ValueError:
        repeat_count_value = 1

    config.set("Settings", "repeat_count_value", str(repeat_count_value))

    # Сохранение выбранного значения горячей клавиши в файл конфигурации
    hotkey_value = hotkey_button.cget("text")
    config.set("Settings", "hotkey_value", hotkey_value)

    # Сохранение выбранного значения типа повторения в файл конфигурации
    config.set("Settings", "repeat_type_value", repeat_type_var.get())

    # Сохранение выбранного значения типа позиции курсора в файл конфигурации
    position_type_value = position_type_var.get()
    config.set("Settings", "position_type_value", position_type_var.get())

    # Сохранение выбранных координат позиции курсора в файл конфигурации
    position_coordinates_value = position_coordinates_entry.get()
    config.set("Settings", "position_coordinates_value", position_coordinates_value)

    # Запись всех изменений в файл конфигурации
    with open(config_file, "w") as config_file_writer:
        config.write(config_file_writer)

    # Удаление предыдущего обработчика горячей клавиши
    keyboard.unhook_all_hotkeys()

    # Добавление нового обработчика горячей клавиши с обновленным значением
    keyboard.add_hotkey(hotkey_value, callback=autoclick)

    # Обновление метки горячей клавиши
    update_key_label(hotkey_value)


frame = CTkFrame(window, fg_color="black")
frame.grid(row=0, column=1, sticky="nsew", padx=100)

# Метка для заголовка программы
login_label = CTkLabel(frame, text="Mouse Licker", font=CTkFont(size=20, weight="bold"))
login_label.grid(row=0, column=0, padx=30, pady=(0, 5))


# Функция для изменения текста метки при наведении
def change_text(_):
    login_label.configure(text="Mouse   Auto")


# Привязка события "наведение курсора мыши" к функции изменения текста
login_label.bind("<Enter>", change_text)


# Функция для возврата исходного текста метки при уходе курсора мыши
def revert_text(_):
    login_label.configure(text="Mouse Licker")


# Привязка события "убирание курсора мыши" к функции возврата исходного текста
login_label.bind("<Leave>", revert_text)

# Кнопка для запуска/остановки автоклика
button = CTkButton(frame, text="Начать", command=autoclick, font=CTkFont(size=18))
button.grid(row=1, column=0, pady=(0, 5), ipadx=20, ipady=10)

# Метка для отображения текущей горячей клавиши
key_label = CTkLabel(frame, text=f"{hotkey} - старт/стоп.")
key_label.grid(row=2, column=0, pady=(0, 0))

# Метка для отображения количества кликов
counter_label = CTkLabel(frame, text="Кликов: 0")
counter_label.grid(row=3, column=0, pady=(0, 0))

# Кнопка для открытия окна настроек
settings_button = CTkButton(frame, text="Настройки", command=open_settings_window)
settings_button.grid(row=4, column=0, pady=(0, 0), ipadx=2, ipady=1)

# Добавление обработчика горячей клавиши
keyboard.add_hotkey(hotkey, callback=autoclick)

# Запуск основного цикла приложения
window.mainloop()
