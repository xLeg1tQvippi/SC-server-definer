import pyautogui

print('Переместите мыш на нужный объект и нажмите Enter')
input()
while True:
    position = pyautogui.position()
    print('position:', position)
    input('Нажмите Enter чтобы получить координаты оси мыши.')