from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)

start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

print(start_time)
print(end_time)