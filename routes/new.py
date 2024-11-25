import asyncio
import logging

from aiogram.types import InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup
from flask import Blueprint, jsonify
from flask_cors import CORS

from data.config import bot, STATUSES

app = Blueprint('new', __name__)

logger = logging.getLogger(__name__)

CORS(app)  # Разрешает CORS для всех маршрутов и источников


def button(telegram_id, employee_id, id_offer):
    buttons: list = [
        [
            InlineKeyboardButton(text='Перейти в CRM', web_app=WebAppInfo(
                url=f'https://tulaastoriabot.ru/{telegram_id}/{employee_id}/{id_offer}'))
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def send_message(telegram_id, text, buttons):
    await bot.send_message(chat_id=telegram_id,
                           text=text,
                           reply_markup=buttons)


@app.route('/post/<telegram_id>/<employee_id>/<id_offer>/<stage_deal>/<ds>', methods=['GET'])
def get_deal(telegram_id, employee_id, id_offer, stage_deal, ds):
    if stage_deal != 'highLightTitle.png':
        if stage_deal in [55, 66]:
            text = f'Новая сделка - Обращение\nID сделки: #{id_offer}'
        else:
            text = f'Новая сделка - Обращение\nID сделки: #{id_offer}\nСтадия: #{STATUSES.get(stage_deal, "Неизвестная")}'
        asyncio.run(send_message(telegram_id, text, button(telegram_id, employee_id, id_offer)))
        return jsonify({'status': "success"})
    return jsonify({'status': "false"})


new_rt = app
