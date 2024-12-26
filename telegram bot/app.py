import telebot
from config import TOKEN
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_command(message):
    bot.send_message(message.chat.id,
                     "Чтобы получить цену валюты, введите сообщение в формате:\n<валюта1> <валюта2> <количество>\n\nДоступные валюты: евро, доллар, рубль\n\nДля просмотра доступных валют введите команду /values")


@bot.message_handler(commands=['values'])
def values_command(message):
    bot.send_message(message.chat.id, "Доступные валюты:\n- евро\n- доллар\n- рубль")


@bot.message_handler(content_types=['text'])
def convert_command(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException("Неверное количество параметров. Используйте формат: <валюта1> <валюта2> <количество>.")

        base_currency, quote_currency, amount = values
        amount = float(amount)

        base = CryptoConverter.convert_currency(base_currency)
        quote = CryptoConverter.convert_currency(quote_currency)

        if base_currency.lower() == quote_currency.lower():
            raise APIException("Невозможно конвертировать валюту в саму себя.")

        result = CryptoConverter.get_price(base, quote, amount)

        bot.send_message(message.chat.id, f"{amount} {base_currency} в {quote_currency} = {result:.2f}")

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите количество как число.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла неожиданная ошибка: {str(e)}")


if __name__ == '__main__':
    bot.polling(none_stop=True)

