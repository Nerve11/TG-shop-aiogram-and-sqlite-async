import asyncio
import pytz
import datetime
from db import log_message

MOSCOW_TZ = pytz.timezone('Europe/Moscow')


async def daily_reset():
    """
    Resets or compiles daily statistics every day at 00:00 Moscow time.
    """
    while True:
        now = datetime.datetime.now(MOSCOW_TZ)
        reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_until_reset = (reset_time - now).total_seconds()

        if time_until_reset <= 0:
            time_until_reset += 86400  # 24 ч

        await asyncio.sleep(time_until_reset)
        #архивирование журналов
        print(f"Сброс ежедневной статистики {reset_time}")
