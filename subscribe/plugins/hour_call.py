import os
import pytz
import json
from datetime import datetime

import nonebot


def get_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)
        return config


def get_auth_group():
    return get_config()["AUTH_GROUP"]


def get_hour_call():
    return get_config()["HOUR_CALL"]


LAST_HOUR_CALL = datetime.now(pytz.timezone('Asia/Shanghai')).hour

@nonebot.scheduler.scheduled_job('cron', hour='*', minute='0-5', second='0', misfire_grace_time=30)
async def hour_call():
    global LAST_HOUR_CALL
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    if LAST_HOUR_CALL == now.hour:
        return
    
    LAST_HOUR_CALL = now.hour

    if 1 <= now.hour <= 4:
        # 宵禁 免打扰
        return

    msg = get_hour_call()[now.hour]
    bot = nonebot.get_bot()
    for group in get_auth_group():
        try:
            await bot.send_group_msg(group_id=group, message=msg)
            print(f'群{group} 投递成功')
        except nonebot.CQHttpError as e:
            print(e)
            print(f'Error：群{group} 投递失败')


@nonebot.scheduler.scheduled_job('cron', hour='6', minute='45', second='0', misfire_grace_time=120) # UTC 0 = UTC+8 1445
async def pcr_reminder():
    print('pcr_reminder start')
    msg = '一四四五、骑士君准备好背刺了吗？'
    bot = nonebot.get_bot()
    for group in get_config()["PCR_GROUP"]:
        try:
            await bot.send_group_msg(group_id=group, message=msg)
            print(f'群{group} 投递成功')
        except nonebot.CQHttpError as e:
            print(e)
            print(f'Error：群{group} 投递失败')
