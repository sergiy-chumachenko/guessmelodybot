import shelve
import os
from random import shuffle
from telebot import types

from sqlliter import SQLLiter
from config import DB_NAME, SHELVE_NAME


def set_rows_count():
    db = SQLLiter(database=DB_NAME)
    with shelve.open(filename=os.getcwd() + '/' + SHELVE_NAME) as storage:
        storage['rows_count'] = db.count_rows()


def get_rows_count():
    with shelve.open(filename=os.getcwd() + '/' + SHELVE_NAME) as storage:
        return storage['rows_count']


def set_user_game(chat_id, right_answer):
    with shelve.open(filename=os.getcwd() + '/' + SHELVE_NAME) as storage:
        storage[str(chat_id)] = right_answer


def finish_user_game(chat_id):
    with shelve.open(filename=os.getcwd() + '/' + SHELVE_NAME) as storage:
        del storage[str(chat_id)]


def get_right_answer_for_user(chat_id):
    with shelve.open(filename=os.getcwd() + '/' + SHELVE_NAME) as storage:
        try:
            return storage[str(chat_id)]
        except KeyError:
            return None


def generate_markup(right_answer, wrong_answers):
    """
     Create a custom board for choose the answer
    :param right_answer: right answer
    :param wrong_answers: wrong answers
    :return:
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    all_answers = f"{right_answer}, {wrong_answers}"
    list_answers = [answer for answer in all_answers.split(',')]
    shuffle(list_answers)
    for answer in list_answers:
        markup.add(answer)
    return markup
