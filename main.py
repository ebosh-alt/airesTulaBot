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
    rm = await client.get_reminder(65454)
    # up_rm = await client.update_reminder(65433, "1732884550", "1732884550")
    del_rm = await client.delete_reminder(65454)
    logger.info(rm)
    logger.info(del_rm)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')
    with suppress(KeyboardInterrupt):
        app.run(host='0.0.0.0', port=3000, debug=True)
