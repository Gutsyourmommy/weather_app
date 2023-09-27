from datetime import datetime
def convert_seconds_to_date(seconds: int, timezone: int):
    '''Конвертируем секунды в удобочитаемый вид учитывая часовой пояс'''
    return datetime.utcfromtimestamp(seconds + timezone).strftime('%H:%M:%S')



