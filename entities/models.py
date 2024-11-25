import logging
from dataclasses import dataclass
from datetime import datetime, tzinfo
from typing import Dict, Union
from typing import Optional, List, Any
from zoneinfo import ZoneInfo

import pytz
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


def format_phone_number(phone: str) -> str:
    phone = ''.join(filter(str.isdigit, phone))
    if len(phone) == 11 and phone.startswith('7'):
        return f"7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    return phone


@dataclass
class ApiPoint:
    # base_url = "http://astoria-dubai.online:81/sharedapi"
    base_url = "http://aires.astoria-tula.ru:81/sharedapi"
    worker_filter = f'{base_url}/worker/filter'
    publication_single = f"{base_url}/publication/single"
    deals = f"{base_url}/sales/filter"
    deal_update = f"{base_url}/sales/update"
    missed_reminder = f"{base_url}/org_events/missed_alarms"
    reminder = f"{base_url}/org_events/get"
    reminders = f"{base_url}/org_events/list"
    reminder_delete = f"{base_url}/org_events/delete"
    org_events_update = f"{base_url}/org_events/update"
    update_user = f"{base_url}/worker/update"
    purchaser_filter = f"{base_url}/purchaser/filter"
    sales_comments = f"{base_url}/sales/comments"
    sales_update = f"{base_url}/sales/update"
    sales_add_comment = f"{base_url}/sales/addComment"


class Phone(BaseModel):
    phone: str
    comment: str


class FieldData(BaseModel):
    id: str
    datatype: str = None
    value: Union[str, List[str] | int] = None


class User(BaseModel):
    id: str
    # telegram_id: str = None
    division_id: str = None
    name: str = None
    surname: str = None
    secondname: str = None
    fields: dict[str, FieldData] = Field(default_factory=dict)


class Deal(BaseModel):
    id: str
    customers_id: str
    employee_id: str
    sale_stage_id: str
    date_create: Optional[str] = None
    sale_name: Optional[str] = None
    sale_type_id: Optional[int] = None
    fields: Optional[Dict[str, FieldData]] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        # Проверка условия для sale_type_id == 8
        # if data.get("sale_type_id") != "8":
        #     return None
        # Фильтруем только нужные поля в fields
        fields_data = data.get("fields", {})
        filtered_fields = {k: v for k, v in fields_data.items()}

        # Обновляем data перед созданием экземпляра
        data["fields"] = {key: FieldData(**value) for key, value in
                          filtered_fields.items()} if filtered_fields else None

        return cls(**data)


class Connection(BaseModel):
    substance_summary: Optional[str] = None
    object_type: Optional[str] = None
    object_id: Optional[str] = None


class Reminder(BaseModel):
    id: str
    publ: Optional[str] = None
    uid: Optional[str] = None
    group_id: Optional[str] = None
    created: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    status: Optional[str] = None
    author_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    dtstart: Optional[datetime] = None
    dtend: Optional[datetime] = None
    dtoffset: Optional[str] = None
    dtendoffset: Optional[str] = None
    allday: Optional[str] = None
    sequence: Optional[str] = None
    transparent: Optional[str] = None
    rrule: Optional[Any] = None
    is_reg: Optional[str] = None
    alarms: Optional[Any] = None
    last_queue: Optional[datetime] = Field(alias='last-queue')
    is_queued: Optional[str] = None
    theme_id: Optional[str] = None
    type_id: Optional[str] = None
    bg_color: Optional[str] = Field(alias='bg-color')
    b_color: Optional[str] = Field(alias='b-color')
    t_color: Optional[str] = Field(alias='t-color')
    queue: Optional[str] = None
    missed_alarms: Optional[Any] = None
    event_connections: Optional[str] = None
    queue_connections: Optional[str] = None
    users: Optional[List[str]] = None
    personal_priority: Optional[Any] = None
    connections: Optional[List[Connection]] = None

    @field_validator("created", "last_modified", "dtstart", "dtend", "last_queue", mode="before")
    def parse_datetime(cls, value):
        if value is None:
            return None
        if isinstance(value, str) and value.isdigit():
            tz = pytz.timezone("Europe/Moscow")
            dt = datetime.fromtimestamp(int(value), tz=tz)
            return dt#.strftime('%Y-%m-%d %H:%M')
        return None



class Customer(BaseModel):
    id: str
    group_id: str
    name: str
    surname: Optional[str] = ""
    secondname: Optional[str] = ""
    manager_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = ""
    create_date: Optional[datetime] = None
    comment: Optional[str] = ""
    marktype: str
    nattype: str
    customer_activity_type: str
    customer_activity_date: datetime
    customer_creator_id: str
    markname: str
    fields: dict[str, FieldData] = None
    employee_id: str
    additional_manager_id: List[str] = []
    additional_employee_id: List[str] = []

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        if len(data["email"]) == 0:
            data["email"] = "Почта отсутствует"
        else:
            data["email"] = data["email"][0]["mail"]

        if len(data["phone"]) == 0:
            data["phone"] = "Номер телефона отсутствует"
        else:
            data["phone"] = format_phone_number(data["phone"][0]["phone"])
        # data["phone"] = format_phone_number(data["phone"])
        fields_data = data.get("fields", {})
        filtered_fields = {k: v for k, v in fields_data.items()}
        data["fields"] = {key: FieldData(**value) for key, value in
                          filtered_fields.items()} if filtered_fields else None

        return cls(**data)


class InfoModel(BaseModel):
    employee_id: int
    id_offer: int
    sale_stage_id: int
    customer_id: int
    name: str
    phone: str = None
    email: str = None
    comment: str = None
    date_notification: str
    reminder_id: int

    class Config:
        from_attributes = True
