from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Content:

    def coordinatesForCity(self, city_name, ):
        site = requests.get(f"https://time-in.ru/coordinates?search={city_name}")
        try:
            bs = BeautifulSoup(site.content, 'lxml').find('b').find('a').get('href')
            bd = requests.get(bs)
            listOfCoordinates = BeautifulSoup(bd.content, 'lxml').find('div', class_='coordinates-city-info').find(
                'div').getText()
        except AttributeError:
            try:
                listOfCoordinates = BeautifulSoup(site.content, 'lxml').find('div',
                                                                             class_='coordinates-city-info').find(
                    'div').getText()
            except AttributeError:
                return "ERROR"
        listOfCoordinates = listOfCoordinates.split()

        lat = listOfCoordinates[-2].replace(',', '')
        lon = listOfCoordinates[-1]
        return lat, lon

    def jsonOfAPI(self, city_name, day, ):
        if self.coordinatesForCity(city_name) != "ERROR":
            lat, lon = self.coordinatesForCity(city_name)
            API_key = "b41f154a86e9c4f96fd719a2d7207a11"

            link = requests.get(
                f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=current,minute,hourly&appid={API_key}')
            data = link.json()
            if data['daily'][0]['humidity'] > 60:
                smiles0 = "\U00002601"
            else:
                smiles0 = "\U00002600"
            try:
                listOfInfo = []
                for i in data['alerts']:
                    if i['description'] != "":
                        listOfInfo.append("⦿" + (i['description']).capitalize() + "\n")
                info = ''.join(listOfInfo)
                alerts = "\n" + info
                print(info)
            except KeyError:
                alerts = "Предупреждений нет"

            if day == "now":
                return f" в вашем городе {data['daily'][0]['temp']['day']}℃\n " \
                       "\n" \
                       f"Днем {data['daily'][0]['temp']['day']}\n"  \
                       f"Ночью {data['daily'][0]['temp']['night']}℃\n"  \
                       f"Облачность {data['daily'][0]['clouds']}%" + smiles0 + "\n" \
                       f"Влажность {data['daily'][0]['humidity']}% \n" \
                       f"Днем ощущаестя как {data['daily'][0]['feels_like']['day']}℃\n" \
                       f"Ночью ощущаестя как {data['daily'][0]['feels_like']['night']}℃\n" \
                       f"\U000026A0 ПРЕДУПРЕЖДЕНИЯ НА {str(datetime.utcfromtimestamp(data['alerts'][-1]['start']).date())}: " \
                       f"\n" \
                       f"{alerts}"
            elif day == "tomorrow":
                if data['daily'][1]['humidity'] > 60:
                    smiles1 = "\U00002601"
                else:
                    smiles1 = "\U00002600"
                return f" в вашем городе {data['daily'][1]['temp']['day']}℃\n" \
                       "\n" \
                       f"Днем {data['daily'][1]['temp']['day']}\n" \
                       f"Ночью {data['daily'][1]['temp']['night']}℃\n" \
                       f"Облачность {data['daily'][1]['clouds']}%" + smiles1 +"\n"\
                       f"Влажность {data['daily'][1]['humidity']}% \n"  \
                       f"Днем ощущаестя как {data['daily'][1]['feels_like']['day']}℃\n" \
                       f"Ночью ощущаестя как {data['daily'][1]['feels_like']['night']}℃\n" \
                       f"\U000026A0 ПРЕДУПРЕЖДЕНИЯ НА {str(datetime.utcfromtimestamp(data['alerts'][-1]['start']).date())}: " \
                       f"\n" \
                       f"{alerts}"
            elif day == "week":
                return data["daily"], alerts

    def news(self):
        page = requests.get("https://tvrain.ru/news/")
        x = page.content
        soup = BeautifulSoup(x, 'html.parser')
        html = soup.find('div', class_="newsline main-col wrap_col").find('div',
                                                                          class_="newsline__grid newsline__grid--leftline").find_all(
            "a")

        list_of_all_news = []
        list_of_news_for_return = []
        for text in html:
            link = text.get("href")
            list_of_all_news.append("https://tvrain.ru" + link)
        print(page)

        for i in range(0, len(list_of_all_news), 2):
            if i > 10:
                break
            list_of_news_for_return.append(list_of_all_news[i])
        return list_of_news_for_return

