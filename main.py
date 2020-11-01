import telebot

from telebot import types


bot = telebot.TeleBot('1282165952:AAGjTYsB7QbADASQ-ivWn9lG9aLIWubKfpU')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, "Здравствуйте, я - бот-калькулятор! \n"
                                            "Моя задача - помочь Вам рассчитать транспортный налог.",
                           reply_markup=markup)
    bot.send_message(message.chat.id, "Введите мощность автомобиля (л.с.): ")

    bot.register_next_step_handler(msg, process_num1_step)


def process_num1_step(message):
    try:
        pwr = int(message.text)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        item3 = types.KeyboardButton('Рассчитать!')
        markup.add(item3)

        msg = bot.send_message(message.chat.id, "Рассчитать налог?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc_step,  pwr, msg)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


def process_proc_step(message, pwr, msg):
    if 0 < pwr < 100:
        res = pwr * 7
        bot.send_message(message.chat.id, f'Ваш налог за 12 мес. составит: {res}')
    elif 100 <= pwr < 150:
        res = pwr * 15
        bot.send_message(message.chat.id, f'Ваш налог за 12 мес. составит: {res}')
    elif 150 <= pwr < 200:
        res = pwr * 35
        bot.send_message(message.chat.id, f'Ваш налог за 12 мес. составит: {res}')
    elif 200 <= pwr < 250:
        res = pwr * 65
        bot.send_message(message.chat.id, f'Ваш налог за 12 мес. составит: {res}')
    elif 250 <= pwr < 999:
        res = pwr * 130
        bot.send_message(message.chat.id, f'Ваш налог за 12 мес. составит: {res}')

    bot.send_message(message.chat.id, "Теперь, рассчитаем актуальную сумму налога! \n "
                                      "Введите месяц, когда был оформлен автомобиль:")
    bot.register_next_step_handler(msg, continue_tax, res)


def continue_tax(message, res):
    try:
        m = int(message.text)
        if 0 < m < 12:
            n = 12 - m + 1
            res1 = res / 12 * m
            res2 = res - res1
            bot.send_message(message.chat.id, f'Ваш налог за {n} мес. составит: {res2}')
        elif m == 12:
            res1 = res/12
            bot.send_message(message.chat.id, f'Ваш налог за {m} мес. составит: {res1}')
        else:
            bot.send_message(message.chat.id, "Не корректно, ведите номерное обозначание месяца (от 1 до 12)")
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


if __name__ == '__main__':
    bot.polling(none_stop=True)
