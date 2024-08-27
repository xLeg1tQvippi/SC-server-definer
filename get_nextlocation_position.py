import pyautogui
from PIL import Image
import options, importlib
def shot_precision(options):
    screenshot = pyautogui.screenshot(region=(options[0], options[1], options[2], options[3]))
    screenshot.show()
    input('Нажмите Enter чтобы продолжить...')
    screenshot.close()
def get_integer_input(text):
    while True:
        try:
            value = int(input(text))
            return value
        except ValueError:
            print("Ошибка: введено не число. Пожалуйста, введите целое число.")
        except Exception as e:
            print(f"Ошибка: {e}")

def get_positions():
    print('Для того чтобы оставить параметр не измененным, введите 1.')
    while True:
        print(f'Default option for X: {options.default[0]}')
        x = get_integer_input('Введите параметры оси X: ')
        if x == 1:
            x = options.default[0] 
        print(f'Default option for Y: {options.default[1]}')
        y = get_integer_input('Введите параметры оси Y: ')
        if y == 1:
            y = options.default[1]
        print(f'Default option for Width: {options.default[2]}')
        width = get_integer_input('Введите ширину захватываемого объекта: ')
        if width == 1:
            width = options.default[2]
        print(f'Default option for Heigth: {options.default[3]}') 
        height = get_integer_input('Введите высоту захватываемого объекта: ')
        if height == 1:
            height = options.default[3]
        print(f"Введенные параметры: X={x}, Y={y}, Width={width}, Height={height}")
        return [x, y, width, height]

def save_file(changed_default):
    with open('options.py', 'w') as file:
        file.write(f'default = {changed_default}\nserver = {options.server}')
    importlib.reload(options)

if __name__ == "__main__":
    while True:
        choice = input('Приветствую в программе для тестирования и получения координат нужного объекта.\n1 - Использовать изначально введенные параметры осей\n2 - Ввести собственные параметры, для корректировки.\n0 - Чтобы выйти\n>>>')
        if choice == '0':
            break
        elif choice == '1':
            shot_precision(options.default)
        elif choice == '2':
            changed_default = get_positions()
            save = input('Сохранить данные параметры в default?\n1 - Да\n2 - Нет\n>>>')
            if save == '2':
                shot_precision(changed_default)
            elif save == '1':
                save_file(changed_default)
                shot_precision(changed_default)