import telebot
from aiogram import Bot
from environs import Env

env = Env()
env.read_env()

aires_api_key = env('AIRES_API_KEY')
bot_token = env('BOT_TOKEN')
# bot = Bot(bot_token)
bot = telebot.TeleBot(bot_token, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

STATUSES = {
    '66': 'New',
    '67': 'Звонок совершен',
    '64': 'Собеседование назначено',
    '29': 'Собеседование проведено',
    '30': 'Обучение началось',
    '68': 'Остался через 14 дней',
    '69': 'Остался через 30 дней',
    '31': 'Приняли на работу',
    '32': 'Закрыли сделку',

    '55': 'Новый',
    '54': 'Неотвеченный',
    '56': 'Уточненный',
    '57': 'Отложенный спрос',
    '58': 'Приглашение',
    '59': 'Встреча',
    '65': 'Без договора',
    '60': 'Договор',
    '61': 'Задаток',
    '62': 'Закрытие сделки',
    '63': 'Отказ',
    '73': 'АВТООБЗВОН',
    '72': 'Дубль/брак'
}

FIELD_ID_EVENT = "3770"

SALE_STAGE_ID = [21, 29, 30, 31, 63, 64, 66, 67, 68, 69]
