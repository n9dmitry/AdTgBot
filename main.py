import telebot
import requests
from datetime import datetime

bot = telebot.TeleBot('6812734984:AAEy6Hs4GLGNQAbwj_uJ2oH5CVzGvftg1WQ')

questions = ["Марка авто", "Год выпуска", "Объем двигателя", "Описание"]
answers = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Давай начнем!")
    send_question(message.chat.id, 0)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '/start':
        start(message)
    elif len(answers) < len(questions):
        answers.append(message.text)
        send_question(message.chat.id, len(answers))
    else:
        save_data()
        bot.send_message(message.chat.id, "Благодарим вас за ответы!")

def send_question(chat_id, question_id):
    bot.send_message(chat_id, questions[question_id])

def save_data():
    data = {'Марка авто': answers[0], 'Год выпуска': answers[1], 'Объем двигателя': answers[2], 'Описание': answers[3]}
    result = requests.post('https://t.me/autobot123123123', json=data)
    if result.status_code == 200:
        print("Данные успешно отправлены на канал!")
    else:
        print("Ошибка при отправке данных на канал!")

bot.polling()