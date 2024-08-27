from PIL import Image, ImageGrab, ImageEnhance
import numpy as np
import pytesseract, os, time, cv2, pyautogui, options, re, datetime

def make_screenshot(pos):
    screenshot = pyautogui.screenshot(region=(pos[0], pos[1], pos[2], pos[3]))
    return screenshot

def save_text(text, path_to_save, save_type, file_to_save):
    
    # print(text); print(path_to_save); print(save_type); print(file_to_save)
    #saver
    with open(path_to_save, save_type, encoding='utf-8') as file:
        today = datetime.datetime.now()
        file.write(f'{today.strftime('%H:%M')} - {text}')
        
    #reader
    result = f'textreciever\\{file_to_save}'
    with open(result, 'r', encoding='utf-8') as file:
        reading = file.read()
        print('result text reader:')
        if file_to_save == 'server.txt':
            file_time = re.compile(r'^([0-2][0-9])[:]?([0-6][0-9])*')
            get_time = file_time.search(reading)
            if get_time:
                if get_time.group(1) < today.strftime('%H'):
                    with open(result, 'w', encoding='utf-8') as file:
                        print('Прошел час после сохранения серверов, автоматическая отчистка файла...\nСтатус: ', end='')
                        file.write('')
                    print('complete')
                else:
                    print('pinging server:', reading)

def get_text(image, file_path, save_type):
    #pic = Image._show(image)
    file_to_save = file_path
    pytesseract.pytesseract.tesseract_cmd=r'C:\Users\User\Desktop\tesseract-5.4.1\tesseract.exe'
    os.environ['TESSDATA_PREFIX'] = r'C:\Users\User\Desktop\tesseract-5.4.1\tessdata'
    output_path='C:\\Users\\User\\Desktop\PetProjects\\stalcraft_getimage\\textreciever\\'
    
    text = pytesseract.image_to_string(image, lang='rus')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip() + '\n'
    path_to_save = output_path + file_to_save
    try:
        print(file_path)
        if file_path == 'result.txt':
            if 'Статус' in text or 'Установка' in text:
                print('searched:',text)
                return True
            else:
                return False
        elif file_path == 'server.txt':
            space_finder = re.compile(r'^(\s*$|\s*\n)')
            finder = space_finder.search(text)
            if finder:
                return False
            else:
                print('Найденый сервер:',text)
                if text != ' ':
                    status = save_text(text, path_to_save, save_type, file_to_save)
                    return status
    except Exception as error:
        print(text)
        return False

def upgrade(image):
    enhancer = ImageEnhance.Sharpness(image)
    sharpened_image = enhancer.enhance(2.0)  # Исходное увеличение резкости

    # Увеличение контраста
    enhancer = ImageEnhance.Contrast(sharpened_image)
    final_image = enhancer.enhance(2.0)  # Исходное увеличение контраста
    
    # Дополнительное, более мягкое повышение резкости
    enhancer = ImageEnhance.Sharpness(final_image)
    final_image = enhancer.enhance(1.1)  # Небольшое дополнительное увеличение резкости
    
    # Дополнительное, более мягкое увеличение контраста
    enhancer = ImageEnhance.Contrast(final_image)
    final_image = enhancer.enhance(1.1)  # Небольшое дополнительное увеличение контраста
    
    return final_image

if __name__ == '__main__':
    while True:
        interval = 5
        file = 'result.txt'
        save_type = 'w'
        image = make_screenshot(options.default)
        final_picture = upgrade(image)
        r = get_text(final_picture, file, save_type)
        if r == False:
            print('Не получилось определить переход на новую локацию.')
            time.sleep(5)
            continue
        elif r == 0:
            break
        elif r == True:
            interval = 3
            time.sleep(interval)
            file = 'server.txt'
            save_type = 'a'
            print('capturing server!')
            for i in range(13):
                image = make_screenshot(options.server)
                upgrade_image = upgrade(image)
                status = get_text(upgrade_image, file, save_type)
                if status == False:
                    print('Сервер не найден.')
                elif status == True:
                    print('Успешно сохранено.')
                time.sleep(interval)
            print('capturing complete.')
        time.sleep(interval)
