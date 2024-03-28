# -*- coding:utf-8 -*-
import re
from datetime import datetime, timezone, timedelta

def to_timestamp(dt_str, tz_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    pattern = re.compile(r'^UTC([+-]*\s*\d+):(\d{2})$')
    match =  pattern.match(tz_str)
    tz_hours = match.group(1)
    tz_minutes = match.group(2)
    tz = timezone(timedelta(hours= int(tz_hours), minutes= int(tz_minutes)))
    tz_dt = dt.replace(tzinfo= tz)
    timestamp = tz_dt.timestamp()
    return timestamp




# 测试:
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')