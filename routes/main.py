import logging

from flask import Blueprint, render_template

from data.config import aires_api_key, STATUSES
from services.Intrum.Client import ClientIntrum

app = Blueprint('main', __name__)

logger = logging.getLogger(__name__)


@app.route('/<crm_id>/<user_id>/<deal_id>')
async def index(crm_id, user_id, deal_id):
    if crm_id.isdigit() and user_id.isdigit() and deal_id.isdigit():
        client = ClientIntrum(aires_api_key)
        info = await client.get_info(deal_id)
        if int(user_id) == int(info.employee_id):
            return render_template('index.html', name=info.name, customer_id=info.customer_id,
                                   customer_phone=info.phone, customer_mail=info.email,
                                   customer_status=STATUSES[str(info.sale_stage_id)],
                                   deal_id=deal_id, comment=info.comment,
                                   date_notification=info.date_notification)
        return "user_id equal to employee_id"
    return f"crm_id, user_id, deal_id required isdigit"


main_rt = app
