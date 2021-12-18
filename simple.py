"""Uznypa - telegram bot"""
import os
import telebot

token = os.getenv("TOKEN")
print("token: ", token)
bot = telebot.TeleBot(token, parse_mode=None)

commands = ['help']


@bot.message_handler(commands='start')
def send_greetings(message):
    """Sends greetings to users"""
    bot.reply_to(message, "Привет! Меня зовут Узныпа. Если возникли трудности - пиши /help")


@bot.message_handler(commands=commands[0])
def send_help_info(message):
    """Sends list of available commands to users"""
    msg = 'Список доступных команд:\n'
    for i, cmd in enumerate(commands):
        msg += str(i + 1) + '. /' + cmd + '\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    """Sends user's message back"""
    bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
