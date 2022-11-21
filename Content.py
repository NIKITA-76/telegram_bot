
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
            API_key = "97421d43f97766e5f2b2708a4571165f"

            link = requests.get(
                f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=current,minute,hourly&appid={API_key}')
            data = link.json()
            print(data)
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
                print(data)
                return f" в вашем городе {data['daily'][0]['temp']['day']}℃\n " \
                       "\n" \
                       f"Днем {data['daily'][0]['temp']['day']}\n" \
                       f"Ночью {data['daily'][0]['temp']['night']}℃\n" \
                       f"Облачность {data['daily'][0]['clouds']}%" + smiles0 + "\n" \
                                                                               f"Влажность {data['daily'][0]['humidity']}% \n" \
                                                                               f"Днем ощущаестя как {data['daily'][0]['feels_like']['day']}℃\n" \
                                                                               f"Ночью ощущаестя как {data['daily'][0]['feels_like']['night']}℃\n"\
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
                       f"Облачность {data['daily'][1]['clouds']}%" + smiles1 + "\n" \
                                                                               f"Влажность {data['daily'][1]['humidity']}% \n" \
                                                                               f"Днем ощущаестя как {data['daily'][1]['feels_like']['day']}℃\n" \
                                                                               f"Ночью ощущаестя как {data['daily'][1]['feels_like']['night']}℃\n" \
                                                                               f"{alerts}"
            elif day == "week":
                return data["daily"], alerts

    def news(self):
        page = requests.get(
            "https://news.mail.ru/?utm_source=portal&utm_medium=new_portal_navigation&utm_campaign=news.mail.ru&mt_click_id=mt-curxh8-1651427866-462072801&mt_sub1=news.mail.ru")
        soup = BeautifulSoup(page.content, 'lxml')
        html = soup.findAll("a", class_="photo photo_small photo_scale photo_full js-topnews__item")
        html_ = soup.find("a", class_="photo photo_full photo_scale js-topnews__item")
        list_of_news = []
        for i in html:
            list_of_news.append(i.get("href"))
        list_of_news.append(html_.get("href"))
        print(list_of_news)
        return list_of_news
