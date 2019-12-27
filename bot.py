import logging
import os
import time
import telebot
import random

from sqlliter import SQLLiter
import config
import utils

bot = telebot.TeleBot(token=config.TOKEN)
logging.basicConfig(format='%(asctime)s ---> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id, text="Hi! To start the game, enter the command -> '/game'!")


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('music'):
        if file.split('.')[-1] == 'ogg':
            file = open(file='%s/music/%s' % (os.getcwd(), file), mode='rb')
            msg = bot.send_voice(chat_id=message.chat.id, voice=file)
            bot.send_message(chat_id=message.chat.id, text=msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['game'])
def game(message):
    db_worker = SQLLiter(config.DB_NAME)
    row = db_worker.fetch_single_record(row_number=random.randint(1, utils.get_rows_count()[0]))[0]
    markup = utils.generate_markup(right_answer=row[2], wrong_answers=row[3])
    bot.send_voice(chat_id=message.chat.id, voice=row[1], reply_markup=markup)
    utils.set_user_game(chat_id=message.chat.id, right_answer=row[2])
    db_worker.close_connection()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    right_answer = utils.get_right_answer_for_user(message.chat.id)
    if not right_answer:
        bot.send_message(chat_id=message.chat.id, text="To start the game choose '/game' command!")
    else:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        if message.text == right_answer:
            msg = "Congrats! Your answer is correct!"
        else:
            msg = "Incorrect! Try again!"
        bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=keyboard_hider)
        utils.finish_user_game(chat_id=message.chat.id)


if __name__ == "__main__":
    logging.info("Bot is starting...")
    utils.get_rows_count()
    random.seed()
    bot.infinity_polling()
