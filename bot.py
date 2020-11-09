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
    bot.register_next_step_handler(msg, engine_pwr_message, msg)


def engine_pwr_message(message, msg):
    bot.send_message(message.chat.id, "Введите мощность автомобиля (л.с.): ")
    bot.register_next_step_handler(msg, engine_pwr_choose, msg)


def engine_pwr_choose(message, msg):
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
        bot.register_next_step_handler(msg, month_choose, res, pwr)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


def month_choose(message, res, pwr):
    res2 = 0
    n = 0
    try:
        if message.text.isdigit():
            m = int(message.text)
        else:
            months = {"январь": 1, "февраль": 2, "март": 3, "апрель": 4, "май": 5, "июнь": 6, "июль": 7, "август": 8,
                      "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12}
            m = months[message.text.lower()]
        if 0 < m < 12:
            n = 12 - m
            res1 = res / 12 * m
            res2 = res - res1
        elif m == 12:
            n = m - 11
            res2 = res / 12
        msg1 = bot.send_message(message.chat.id, "Осталось узнать, применяются ли поправочные коэффициенты? \n"
                                                 "Введите год выпуска автомобиля:")
        bot.register_next_step_handler(msg1, final_calculations, res2, res, n, pwr)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что то пошло не так...проверьте правильность ввода месяца')


def final_calculations(message, res2, res, n, pwr):
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
        bot.register_next_step_handler(msg2, get_result, res3, d, n, pwr)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Это не число или что то пошло не так...')


def get_result(message, res3, d, n, pwr):
    if d > 10 and 0 < pwr < 100:
        bot.send_message(message.chat.id, f'Вашему автомобилю больше 10 лет\n'
                                          f'Мощность меньше 100 л.с.\n'
                                          f'Ваш налог составит 0 рублей')
    else:
        bot.send_message(message.chat.id, f' Вашему автомобилю {d} лет \n'
                                          f'Ваш налог за {n} мес. с учетом возраста автомобиля составит: {res3}')


if __name__ == '__main__':
    bot.polling(none_stop=True)
