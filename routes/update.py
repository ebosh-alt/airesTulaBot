import logging
import time
from datetime import datetime
from urllib.parse import unquote

from flask import Blueprint, request, jsonify
from flask_cors import CORS

from data.config import aires_api_key
from services.Intrum.Client import ClientIntrum

app = Blueprint('update', __name__)

logger = logging.getLogger(__name__)

CORS(app)  # Разрешает CORS для всех маршрутов и источников


@app.route('/update', methods=['POST'])
async def process_data():
    data = request.get_json()
    deal_id = data['deal_id']
    date = data['date']
    comment = data['comment']
    client = ClientIntrum(aires_api_key)
    info = await client.get_info(deal_id)

    if date:
        decoded_date = unquote(date)
        parsed_date = datetime.strptime(decoded_date, "%Y-%m-%dT%H:%M")
        logger.info(parsed_date)
        unix_time = int(time.mktime(parsed_date.timetuple()))
        await client.reminder_update(info.reminder_id, str(unix_time), str(unix_time))

    if comment:
        await client.add_comment(deal_id, comment, info.employee_id)

    if str(data['status']) != "s1":
        await client.change_stage(deal_id, data['status'])

    return jsonify({'status': "success"})


update_rt = app