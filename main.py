import telebot
from telebot import types
from config import token


error = False

# creating a dict
ab = dict()
f = open('ab.txt', 'w')
f.write(str(ab))
f.close()


# func to read the dict
def read_dict():
    with open('ab.txt', 'r') as f:
        read = f.read().replace("'", '')
        if len(read) < 3:
            return 'Список пуст'
        return read


# func to add a number
def add_number(name, number):
    global error
    if name in ab:
        error = True
        return
    else:
        ab[name] = str(number)
        with open('ab.txt', 'w') as f:
            f.write(str(ab))


def delete_number(name):
    global error
    if name in ab:
        ab.pop(name)
        with open('ab.txt', 'w') as f:
            f.write(str(ab))
    else:
        error = True
        return


def find_numebr(name):
    global error
    if name in ab:
        bot.send_message(chat_id, ab[name], reply_markup=murkup)
    else:
        error = True
        return


bot = telebot.TeleBot(token, parse_mode=None)


# create a buttons
@bot.message_handler(commands=['start'])
def start(message):  # welcome user
    global murkup
    global chat_id
    chat_id = message.chat.id

    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    read = types.KeyboardButton('Показать номера')
    add = types.KeyboardButton('Добавить номер')
    delete = types.KeyboardButton('Удалить номер')
    change = types.KeyboardButton('Изменить номер')
    find = types.KeyboardButton('Найти номер')
    murkup.add(read, add, delete, change, find)

    bot.send_message(message.chat.id, "Привет, {name.first_name}".format(name=message.from_user), reply_markup=murkup)


# create a script for buttons
@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_handler(message):
    if message.chat.type == 'private':
        if message.text == 'Показать номера':  # show a dict
            bot.send_message(message.chat.id, read_dict())
        elif message.text == 'Добавить номер':  # add a number
            name_message = bot.send_message(message.chat.id, 'Введите имя')
            bot.register_next_step_handler(name_message, set_name)
        elif message.text == 'Удалить номер':  # delete number
            del_message = bot.send_message(message.chat.id, 'Введите имя')
            bot.register_next_step_handler(del_message, del_number)
        elif message.text == 'Изменить номер':  # change number
            setname_message = bot.send_message(message.chat.id, 'Введите имя номера который хотите изменить')
            bot.register_next_step_handler(setname_message, check_name)
        elif message.text == 'Найти номер':  # find number
            ask_name = bot.send_message(message.chat.id, 'Введите имя')
            bot.register_next_step_handler(ask_name, findnumber)


def findnumber(message):
    global error
    name = message.text
    find_numebr(name)
    if error == True:
        bot.send_message(message.chat.id, 'Такого имени нет в списке', reply_markup=murkup)
        error = False


# func to find number to change it
def check_name(message):
    global error
    name = message.text
    delete_number(name)
    if error == False:
        set_new_name_message = bot.send_message(message.chat.id, 'Введите новое имя')
        bot.register_next_step_handler(set_new_name_message, set_new_name)
    else:
        bot.send_message(message.chat.id, 'Такого имени нет в списке', reply_markup=murkup)
        error = False


# functions to set new name and number of changing number
def set_new_name(message):
    global new_name
    new_name = message.text
    set_new_number_message = bot.send_message(message.chat.id, 'Введите новый номер')
    bot.register_next_step_handler(set_new_number_message, set_new_number)


def set_new_number(message):
    new_number = message.text
    add_number(new_name, new_number)
    bot.send_message(message.chat.id, f'Новый список: {read_dict()}', reply_markup=murkup)


# func to set name and delete number that belongs to set name
def del_number(message):
    global error
    name = message.text
    delete_number(name)
    if error == False:
        bot.send_message(message.chat.id, f'Новый список: {read_dict()}', reply_markup=murkup)
    else:
        bot.send_message(message.chat.id, 'Такого имени нет в списке', reply_markup=murkup)
        error = False


# functions to set name and number for new number
def set_name(message):
    global error
    global name
    name = message.text
    if name in ab:
        bot.send_message(message.chat.id, "Такой номер уже существует", reply_markup=murkup)
        return
    error = False
    number_message = bot.send_message(message.chat.id, 'Введите номер')
    bot.register_next_step_handler(number_message, set_number)


def set_number(message):
    number = message.text
    add_number(name, number)
    bot.send_message(message.chat.id, f'Новый список: {read_dict()}', reply_markup=murkup)


bot.polling(none_stop=True)

