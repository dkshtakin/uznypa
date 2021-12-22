"""Uznypa - telegram bot"""
import os
import random
import textwrap
import telebot
from simpledemotivators import Demotivator
from saving import load_list, save_list, load_value, save_value


COMMANDS = ['help', 'set', 'reset', 'dem']
COMMANDS_DESCRIPTION = {'help': 'Справка',
                        'reset': 'Узныпа забудет все, что вы ему писали.'
                        ' Все настройки также будут установлены по умолчанию',
                        'dem': 'Сделать демотиватор из прикрепленной картинки'}
DEFAULT_CONFIG = {'reply_chance': 60, 'max_lines_number': 200, 'max_str_size': 25}
DEFAULT_CONFIG_MIN = {'reply_chance': 0, 'max_lines_number': 1, 'max_str_size': 1}
DEFAULT_CONFIG_MAX = {'reply_chance': 100, 'max_lines_number': 1000, 'max_str_size': 100}
PICKLE_PATH = 'pickle/'
CFG_PATH = 'pickle/cfg/'
DATA_PATH = 'pickle/data/'
SIZE_PATH = 'pickle/size/'
UPDATED = False

if not os.path.exists(PICKLE_PATH):
    os.mkdir(PICKLE_PATH)
if not os.path.exists(CFG_PATH):
    os.mkdir(CFG_PATH)
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
if not os.path.exists(SIZE_PATH):
    os.mkdir(SIZE_PATH)

token = os.getenv("TOKEN")
print("token: ", token)
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands='start')
def send_greetings(message):
    """Sends greetings to users"""
    cfg_filename = CFG_PATH + str(message.chat.id)
    if not os.path.exists(cfg_filename):
        save_value(cfg_filename, DEFAULT_CONFIG)
    bot.reply_to(message, "Привет! Меня зовут Узныпа. Если возникли трудности - пиши /help")


@bot.message_handler(commands=COMMANDS[0])
def send_help_info(message):
    """Sends list of available commands to users"""
    msg = 'Список доступных команд:\n'
    for i, cmd in enumerate(COMMANDS):
        msg += str(i + 1) + '. /' + cmd
        if cmd == 'set':
            msg += ' <parameter> <value>. Текущий конфиг:\n'
            cfg_filename = CFG_PATH + str(message.chat.id)
            config = load_value(cfg_filename)
            for key, value in config.items():
                msg += '\t' + key + ': ' + str(value) + '\n'
            msg += 'Восстановить значения по умолчанию можно командой /set default'
        else:
            msg += '. ' + COMMANDS_DESCRIPTION[cmd]
        msg += '\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=COMMANDS[1])
def set_config(message):
    """Changes config"""
    cfg_filename = CFG_PATH + str(message.chat.id)
    err_msg_1 = 'Ошибка! Неверно указаны параметры. Воспользуйтесь /help для справки'
    tokens = message.text.split()
    if len(tokens) < 2:
        bot.send_message(message.chat.id, err_msg_1)
        return
    if tokens[1] == 'default' and len(tokens) == 2:
        save_value(cfg_filename, DEFAULT_CONFIG)
        bot.send_message(message.chat.id, 'Установлены значения по умолчанию')
    elif tokens[1] in DEFAULT_CONFIG and len(tokens) == 3 and tokens[2].isdigit():
        tokens[2] = int(tokens[2])
        if tokens[2] < DEFAULT_CONFIG_MIN[tokens[1]] or tokens[2] > DEFAULT_CONFIG_MAX[tokens[1]]:
            bot.send_message(message.chat.id,
                             'Ошибка! Допустимые значения от ' +
                             str(DEFAULT_CONFIG_MIN[tokens[1]]) +
                             ' до ' + str(DEFAULT_CONFIG_MAX[tokens[1]]))
            return
        config = load_value(cfg_filename)
        config[tokens[1]] = tokens[2]
        save_value(cfg_filename, config)
        bot.send_message(message.chat.id, 'Текущее значение ' + tokens[1] + ': ' + str(tokens[2]))
    else:
        bot.send_message(message.chat.id, err_msg_1)


@bot.message_handler(commands=COMMANDS[2])
def reset(message):
    """Resets config and clears all saved data"""
    status = bot.get_chat_member(message.chat.id, message.from_user.id).status
    if status in ['administrator', 'creator'] or message.chat.type == 'private':
        cfg_filename = CFG_PATH + str(message.chat.id)
        data_filename = DATA_PATH + str(message.chat.id)
        size_filename = SIZE_PATH + str(message.chat.id)
        save_value(cfg_filename, DEFAULT_CONFIG)
        save_list(data_filename, [], True)
        save_value(size_filename, 0)
        bot.send_message(message.chat.id, 'Все данные успешно удалены')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Эта команда доступна только админам беседы')


@bot.message_handler(commands=COMMANDS[3])
def dem_without_photo(message):
    """Sends error message about photo"""
    bot.send_message(message.chat.id, 'Ошибка! Отсутствует изображение')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    """
    Splits messages into pieces of max_str_size symbols and stores max_lines_number of this pieces.
    Sends one random phrase from saved pieces.
    """
    cfg_filename = CFG_PATH + str(message.chat.id)
    data_filename = DATA_PATH + str(message.chat.id)
    size_filename = SIZE_PATH + str(message.chat.id)

    config = load_value(cfg_filename)

    msg = message.text
    if len(msg) > config['max_str_size']:
        msg = textwrap.wrap(msg, config['max_str_size'])
    else:
        msg = [msg]
    size = load_value(size_filename) + len(msg)
    data = []
    if size >= config['max_lines_number'] * 2:
        data = load_list(data_filename)
        data += msg
        data = data[-config['max_lines_number']:]
        save_list(data_filename, data, True)
        size = len(data)
    else:
        save_list(data_filename, msg)
    save_value(size_filename, size)
    if random.random() <= load_value(cfg_filename)['reply_chance'] / 100 \
       or message.text.split()[0].lower() == 'узныпа':
        if not data:
            data = load_list(data_filename)
        bot.send_message(message.chat.id, random.choice(data))


@bot.message_handler(func=lambda m: m.caption == '/dem', content_types = ["photo"])
def reply_to_photo(message):
    """Sends some photo"""
    # sudo apt-get install msttcorefonts
    photo_path = bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path
    photo = bot.download_file(photo_path)
    filename = 'photo' + message.photo[1].file_id
    with open(filename, 'wb') as file:
        file.write(photo)
    data_filename = DATA_PATH + str(message.chat.id)
    data = load_list(data_filename)
    line1 = ''
    line2 = ''
    if data:
        line1 = random.choice(data)
        line2 = random.choice(data)
    else:
        line1 = '...'
        line2 = '...'
    dem = Demotivator(line1, line2)
    result = 'dem' + message.photo[1].file_id + '.jpg'
    dem.create(filename, watermark='@uznypa_bot', result_filename=result)
    data = load_list(data_filename)
    with open(result, 'rb') as file:
        bot.send_photo(message.chat.id, file)
    os.remove(filename)
    os.remove(result)


bot.infinity_polling()
