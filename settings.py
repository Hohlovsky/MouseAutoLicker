import os
import configparser
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Создаем файл конфигурации, если он не существует
config_file = "settings.ini"
if not os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "selected_button_value", "left")
    config.set("Settings", "seconds_entry_value", "0")
    config.set("Settings", "milliseconds_entry_value", "1")
    config.set("Settings", "click_type_value", "click")
    config.set("Settings", "repeat_type_value", "С повторением до остановки")
    config.set("Settings", "repeat_count_value", "1")
    config.set("Settings", "hotkey_value", "space")  # Новая опция для хранения клавиши
    config.set("Settings", "position_type_value", "Любое место")
    config.set("Settings", "position_coordinates_value", "256, 191")
    config.set("Settings", "style_options", "aero")
    with open(config_file, "w") as file:
        config.write(file)

# Загружаем значения из файла конфигурации
config = configparser.ConfigParser()
config.read(config_file)
selected_button_value = config.get("Settings", "selected_button_value")
seconds_entry_value = int(config.get("Settings", "seconds_entry_value"))
milliseconds_entry_value = int(config.get("Settings", "milliseconds_entry_value"))
click_type_value = config.get("Settings", "click_type_value")
repeat_type_value = config.get("Settings", "repeat_type_value")
repeat_count_value = int(config.get("Settings", "repeat_count_value"))
hotkey_value = config.get("Settings", "hotkey_value")
position_type_value = config.get("Settings", "position_type_value")
position_coordinates_value = config.get("Settings", "position_coordinates_value")
style_options = config.get("Settings", "style_options")
