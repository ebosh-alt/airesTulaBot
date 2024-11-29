import logging
from datetime import datetime

import pytz
from flask import Blueprint, request, jsonify
from flask_cors import CORS

from data.config import aires_api_key, STATUSES_DELETE_REMINDER
from services.Intrum.Client import ClientIntrum

app = Blueprint('update', __name__)

logger = logging.getLogger(__name__)

CORS(app)


@app.route('/update', methods=['POST'])
async def process_data():
    data = request.get_json()
    deal_id = data['deal_id']
    date = data['date']
    comment = data['comment']
    client = ClientIntrum(aires_api_key)
    info = await client.get_info(deal_id)

    if date and info.reminder_id:
        timezone = "Europe/Moscow"
        # logger.info(f"date: {date}")
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        # logger.info(f"dt: {dt}")
        tz = pytz.timezone(timezone)
        dt_with_tz = tz.localize(dt)
        # logger.info(f"dt_with_tz: {dt_with_tz}")
        unix_time = int(dt_with_tz.timestamp())
        # logger.info(f"unix_time: {unix_time}")
        await client.update_reminder(info.reminder_id, str(unix_time), str(unix_time))

    if comment:
        await client.add_comment(deal_id, comment, info.employee_id)

    if str(data['status']) != "s1":
        if data['status'] in STATUSES_DELETE_REMINDER:
            await client.delete_reminder(info.reminder_id)
        else:
            await client.change_stage(deal_id, data['status'])

    return jsonify({'status': "success"})


update_rt = app
