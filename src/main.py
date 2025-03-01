import io

import telebot
from PyPDF2 import *
from agent.agent import *
from src.user_base.user_service import init, get_user_info

if __name__ == '__main__':
    bot = telebot.TeleBot("7773762154:AAGpnZSjIa2TLblujOIcAVfJ4rj4diRN48c")
    print('bot started...')
    agent = inicialization()
    connection = init()


    @bot.message_handler(commands=['start'])
    def start(message):
        user_name = message.from_user.first_name
        msg = bot.send_message(message.chat.id,
                               f"👋 Привет, {user_name}!\n\n"
                               "Я твой бот-помощник! Давай познакомимся. Введи, пожалуйста, свое **ФИО** (Фамилия Имя Отчество) 📄")
        bot.register_next_step_handler(msg, start_2)


    # message.text будет содержать введённое на предыдущем шаге - имя
    def start_2(message):
        bot.send_message(message.chat.id, f"✅ Отлично, {message.text}! Теперь мы можем продолжить.")
        result = get_user_info(message.text.upper(), connection)
        for i in range(1, len(result)):
            check_file(result[i], agent, message.chat.id)


    @bot.message_handler(content_types=['text'])
    def handle_message(message):
        result = check_file(message.text, agent, message.chat.id)
        bot.send_message(message.chat.id, result)


    @bot.message_handler(content_types=['document'])
    def file_handler(message):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        if file_info.file_path.endswith(".pdf"):
            pdf_stream = io.BytesIO(downloaded_file)
            reader = PdfReader(pdf_stream)
            for page in reader.pages:
                check_file(page.extract_text(), agent, message.chat.id)
            result = check_file("дай мне итоговый отчет", agent, message.chat.id)
            bot.send_message(message.chat.id, result)
        else:
            result = check_file(downloaded_file, agent, message.chat.id)
            bot.send_message(message.chat.id, result)


    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=40)
        except Exception as e:
            print("Polling error:", e)
            time.sleep(1)
