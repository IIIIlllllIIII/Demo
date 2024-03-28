from datetime import datetime, timedelta, timezone

if __name__ == '__main__':
    now = datetime.now()
    print(now)
    print(type(now))
    dt = datetime(2024, 3, 1, 10, 36, 24)
    print(type(dt))
    timestamp = dt.timestamp()
    print(datetime.fromtimestamp(now.timestamp()))
    print(datetime.fromtimestamp(timestamp))
    print(datetime.utcfromtimestamp(timestamp))
    cday = datetime.strptime('2024-3-1 14:06:47', '%Y-%m-%d %H:%M:%S')  #parse: strp(arse)time
    print(cday)
    print(cday.strftime('%a, %b %d %H:%M:%S'))  #format
    
    print(now.timestamp())
    print(now.strftime('%A, %B %d %H:%M:%S'))
    now_timestemp = now.timestamp
    print(datetime.utcfromtimestamp(now.timestamp()))
    
    tz_utc_8 = timezone(timedelta(hours= 8)) 
    dt_utc8 = now.replace(tzinfo= tz_utc_8)
    print(dt_utc8)
    # dt_utc = datetime.now(tz= timezone.utc)
    # print(dt_utc)
    utc_dt = datetime.utcnow().replace(tzinfo= timezone.utc)
    print(utc_dt)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours= 8)))
    print(bj_dt)
