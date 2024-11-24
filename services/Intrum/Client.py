import json

from data.config import FIELD_ID_EVENT
# from data.config import DIVISION_ID, REQUIRED_FIELDS
from entities.models import ApiPoint, User, Reminder, Deal, Customer, InfoModel
from services.Intrum.Base import BaseApi, logger


class ClientIntrum(BaseApi):
    def __init__(self, token):
        super().__init__(token)

    async def get_info(self, deal_id) -> InfoModel:
        deal = await self.get_deal(deal_id)
        reminder_field = deal.fields.get(FIELD_ID_EVENT)
        reminder_id = 0
        if reminder_field:
            reminder_id = reminder_field.value
            reminder = await self.get_reminder(reminder_id)
            date_notification = reminder.dtstart.strftime('%Y-%m-%d %H:%M')
        else:
            date_notification = "Время отсутствует"
        purchase = await self.get_customer(deal.customers_id)
        comment = await self.get_comment(deal_id)
        return InfoModel(
            employee_id=deal.employee_id,
            id_offer=deal_id,
            sale_stage_id=deal.sale_stage_id,
            customer_id=deal.customers_id,
            name=purchase.name,
            phone=purchase.phone,
            email=purchase.email,
            comment=comment,
            date_notification=date_notification,
            reminder_id=reminder_id,
        )

    async def get_customer(self, customer_id) -> Customer | int:
        params = {
            "params[byid]": customer_id,
        }
        response = await self._post(ApiPoint.purchaser_filter, params)
        if response["status"] != "success":
            return 404
        for json_customer in response["data"]["list"]:
            return Customer.from_json(json_customer)

    async def get_comment(self, deal_id):
        params = {
            'params[entity_id]': deal_id
        }
        response = await self._post(ApiPoint.sales_comments, params)
        if response["status"] != "success":
            return 404
        if len(response["data"][str(deal_id)]) == 0:
            return 'Отсутствует'
        else:
            return response["data"][str(deal_id)][0]["text"]

    async def get_deal(self, deal_id) -> Deal | int:
        params = {
            "params[byid]": deal_id,
        }
        response = await self._post(ApiPoint.deals, params)
        if response["status"] != "success":
            return 404
        for json_deal in response["data"]["list"]:
            return Deal.from_json(json_deal)

    async def get_deals(self, users: list[User] = None, user_id: str = None) -> list[Deal] | int:
        if user_id:
            user_ids = [user_id]
        else:
            user_ids = [user.id for user in users]
        params = {
            "params[manager]": user_ids,
            "params[order]": "desc"
        }
        deals = []
        response = await self._post(ApiPoint.deals, params)
        if response["status"] != "success":
            return 404
        for json_deal in response["data"]["list"]:
            deals.append(Deal.from_json(json_deal))
        return deals

    async def get_reminder(self, reminder_id) -> Reminder | int:
        params = {
            "params[event_id]": reminder_id,
        }
        response = await self._post(ApiPoint.reminder, params)

        if response["status"] != "success":
            return 404
        reminder = Reminder(**response["data"])
        return reminder

    async def get_missed_reminder(self, user_id, reminder_id):  # TODO: модель для json объекта
        params = {
            "params[employee_id]": user_id,
        }
        response = await self._post(ApiPoint.missed_reminder, params)
        if response["status"] != "success":
            return 404
        for result in response["data"]:
            if str(result["event_id"]) == str(reminder_id):
                return result

    async def get_reminders(self, user_id):  # TODO: выборка по конкретному сотруднику
        response = await self._post(ApiPoint.reminders, {})
        if response["status"] != "success":
            return 404
        reminders = []
        for json_reminder in response["data"]["list"]:
            logger.info(json.dumps(json_reminder, indent=4, ensure_ascii=False))
            # reminder = Reminder(**json_reminder)
            # reminders.append(reminder)
        return reminders

    # async def change_stage(self, deal_id, stage):
    #     params = {
    #         'params[id]': deal_id,
    #         'params[sales_status_id]': stage
    #     }
    #
    #     response = await self._post(ApiPoint.reminders, params)
    #     if response["status"] != "success":
    #         return 404
    #     return response

    async def add_comment(self, deal_id, comment, employee_id):
        params = {
            'params[entity_id]': deal_id,
            'params[text]': comment,
            'params[author]': employee_id
        }

        response = await self._post(ApiPoint.sales_add_comment, params)
        logger.info(response)
        if response["status"] != "success":
            return 404
        return response

    async def reminder_update(self, reminder_id, time_start, time_end):
        params = {
            'params[event][id]': reminder_id,
            'params[event][dtstart]': time_start,
            'params[event][dtend]': time_end
        }
        response = await self._post(ApiPoint.org_events_update, params)
        if response["status"] != "success":
            return 404
        return response

    async def change_stage(self, deal_id, stage_id):
        params = {
            'params[0][id]': deal_id,
            'params[0][sales_status_id]': stage_id,
        }

        response = await self._post(ApiPoint.deal_update, params)
        logger.info(json.dumps(response, indent=4, ensure_ascii=False))
        if response["status"] != "success":
            return 404
        return response

    async def delete_reminder(self, reminder_id):
        params = {
            'params[id]': reminder_id,
        }

        response = await self._post(ApiPoint.reminder_delete, params)
        logger.info(response)
        if response["status"] != "success":
            return 404
        return response
