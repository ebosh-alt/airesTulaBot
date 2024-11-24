import asyncio
import logging
from contextlib import suppress

from data.config import aires_api_key
from services.CreateApp import create_app
from services.Intrum.Client import ClientIntrum

app = create_app()

logger = logging.getLogger(__name__)


async def main():
    client = ClientIntrum(aires_api_key)
    # info = await client.add_comment("106152", "test2", "1125")
    # dara = await client.get_info("106151")
    # info = await client.get_reminder("65075")
    # info = await client.get_deal(2516)
    # logger.info(info)
    # reminder_field = info.fields.get("3771")
    # logger.info(reminder_field)
    rm = await client.reminder_update(65102, "1732492850", "1732492850")
    # logger.info(rm)
    # info = await client.get_deal(106165)
    # logger.info(info)

    # await client.add_comment("106157", "comment", "1125")
    # for i in dara:
    #     logger.info(i)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')
    with suppress(KeyboardInterrupt):
        app.run(host='0.0.0.0', port=3000, debug=True)
