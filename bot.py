import os
import time

import telebot
import config

bot = telebot.TeleBot(token=config.TOKEN)


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('music'):
        if file.split('.')[-1] == 'ogg':
            file = open(file='%s/music/%s' % (os.getcwd(), file), mode='rb')
            msg = bot.send_voice(chat_id=message.chat.id, voice=file)
            bot.send_message(chat_id=message.chat.id, text=msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


if __name__ == "__main__":
    bot.polling(none_stop=True)
