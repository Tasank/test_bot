import telebot
from Bell_boyBot import APIException, Convertor
from config import keys, TOKEN
import traceback

bot = telebot.TeleBot(TOKEN)

#Обработчики сообщений
@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = ('Для работы с ботом введите команду в следующем порядке: \n \
(имя валюты) (в какую валюту перевести) \
(количество) \n Увидеть список доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()

bot.polling(none_stop=True)

