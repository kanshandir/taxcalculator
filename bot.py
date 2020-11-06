import telebot

from datetime import datetime

from telebot import types

bot = telebot.TeleBot('1282165952:AAGjTYsB7QbADASQ-ivWn9lG9aLIWubKfpU')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item1 = types.KeyboardButton("Начнем!")
    markup.add(item1)

    msg = bot.send_message(message.chat.id,
                           "Здравствуйте, я - бот-калькулятор! \n"
                           "Моя задача - помочь Вам рассчитать транспортный налог.".format(message.from_user,
                                                                                           bot.get_me()),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, engine_pwr, msg)


def engine_pwr(message, msg):
    bot.send_message(message.chat.id, "Введите мощность автомобиля (л.с.): ")
    bot.register_next_step_handler(msg, process_proc_step, msg)


def process_proc_step(message, msg):
    res = 0
    try:
        pwr = int(message.text)
        if 0 < pwr < 100:
            res = pwr * 7
        elif 100 <= pwr < 150:
            res = pwr * 15
        elif 150 <= pwr < 200:
            res = pwr * 35
        elif 200 <= pwr < 250:
            res = pwr * 65
        elif 250 <= pwr < 999:
            res = pwr * 130
        bot.send_message(message.chat.id, "Введите месяц, когда был оформлен автомобиль:")
        bot.register_next_step_handler(msg, continue_tax, res)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


def continue_tax(message, res):
    res2 = 0
    n = 0
    try:
        m = int(message.text)
        if 0 < m < 12:
            n = 12 - m
            res1 = res / 12 * m
            res2 = res - res1
        elif m == 12:
            n = m - 11
            res2 = res / 12
        else:
            bot.send_message(message.chat.id, "Не корректно, ведите номерное обозначание месяца (от 1 до 12)")
        msg1 = bot.send_message(message.chat.id, "Осталось узнать, применяются ли поправочные коэффициенты? \n"
                                                 "Введите год выпуска автомобиля:")
        bot.register_next_step_handler(msg1, final_tax, res2, res, n)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


def final_tax(message, res2, res, n):
    res3 = 0
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item1 = types.KeyboardButton("Рассчитать налог!")
    markup.add(item1)
    try:
        y = int(message.text)
        cy = int(datetime.now().strftime('%Y'))
        d = cy - y
        if d < 5:
            if n == 12:
                res3 = res * 1
            else:
                res3 = res2 * 1
        elif 5 < d <= 10:
            if n == 12:
                res3 = res * 0.75
            else:
                res3 = res2 * 0.75
        elif d > 10:
            if n == 12:
                res3 = res2 * 1 / 2
            else:
                res3 = res2 * 1 / 2
        msg2 = bot.send_message(message.chat.id, "Необходимая информация собрана", reply_markup=markup)
        bot.register_next_step_handler(msg2, last_last, res3, d, n)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


def last_last(message, res3, d, n):
    bot.send_message(message.chat.id, f' Вашему автомобилю {d} лет \n'
                                      f'Ваш налог за {n} мес. с учетом возраста автомобиля составит: {res3}')


if __name__ == '__main__':
    bot.polling(none_stop=True)
