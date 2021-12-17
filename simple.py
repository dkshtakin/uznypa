import os
import telebot

token = os.getenv("TOKEN")
print("token: ", token)
bot = telebot.TeleBot(token, parse_mode=None)

commands = ['help']

@bot.message_handler(commands='start')
def send_welcome(message):
    bot.reply_to(message, "Привет!")

@bot.message_handler(commands=commands[0])
def send_welcome(message):
    msg = 'Список доступных команд:\n'
    for i in range(len(commands)):
        msg += str(i + 1) + '. /' + commands[i] + '\n'
    bot.send_message(message.chat.id, msg)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()
