import requests
from pprint import pprint
from .utils import convert_seconds_to_date
import json
import config
from db import queries as sql



def get_weather():
    data = []
    username = input('Enter username: ')
    is_exists, user_id = sql.check_user_exists('weather.db', username)
    if not is_exists:
        sql.add_user('weather.db', username)
        get_weather()
    else:
        while True:
            city = input('Укажите свой город: ')

            if city == 'save':
                with open('weather.json', mode='w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                continue
            elif city == 'show':
                all_weather = sql.show_weather_history('weather.db', user_id)
                print(all_weather)
                if not all_weather:
                    print('empty')
                    continue

                for item in all_weather:
                    name, _, sunrise, sunset, dt, description, speed, temp = item[1:-1]
                    print(f'''
                    ================================================
                    В городе {name} сейчас {description}
                    Температура: {temp}
                    Скорость: {speed}
                    Восход: {sunrise}
                    Закат: {sunset}
                    Время отправки запроса: {dt}
                    =================================================
                    ''')
                continue
            elif city == 'clear':
                sql.clear_user_history('weather.db', user_id)
                print('history cleared')
                continue

            config.parameters['q'] = city

            resp = requests.get(config.url, params=config.parameters).json()
            # pprint(resp)
            tz = resp['timezone']
            name = resp['name']
            sunrise = convert_seconds_to_date(seconds=resp['sys']['sunrise'], timezone=tz)
            sunset = convert_seconds_to_date(seconds=resp['sys']['sunset'], timezone=tz)
            dt = convert_seconds_to_date(seconds=resp['dt'], timezone=tz)
            description = resp['weather'][0]['description']
            speed = resp['wind']['speed']
            temp = resp['main']['temp']
            sql.add_weather('weather.db',
                            name=name,
                            tz=tz,
                            sunrise=sunrise,
                            sunset=sunset,
                            dt=dt,
                            description=description,
                            speed=speed,
                            temp=temp,
                            user_id=user_id
                            )

            data.append(
                dict(
                    zip(
                        ['name', 'sunrise', 'sunset', 'description', 'speed'],
                        [name, sunrise, sunset, description, speed]
                    )

                )
            )
            print(f'''
================================================
В городе {name} сейчас {description}
Температура: {temp}
Скорость: {speed}
Восход: {sunrise}
Закат: {sunset}
Время отправки запроса: {dt}
=================================================
''')
