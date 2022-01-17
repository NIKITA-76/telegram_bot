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
                listOfCoordinates = BeautifulSoup(site.content, 'lxml').find('div', class_='coordinates-city-info').find(
                    'div').getText()
            except AttributeError:
                return "ERROR"
        listOfCoordinates = listOfCoordinates.split()

        lat = listOfCoordinates[-2].replace(',', '')
        lon = listOfCoordinates[-1]
        return lat, lon

    def jsonOfAPI(self, city_name, ):
        if self.coordinatesForCity(city_name) != "ERROR":
            lat, lon = self.coordinatesForCity(city_name)
            API_key = "b41f154a86e9c4f96fd719a2d7207a11"

            link = requests.get(
                f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=current,minute,hourly&appid={API_key}')
            data_from_api = link.json()
            return data_from_api["daily"]
        else:
            return "ERROR_IN_JSON_API"

    def news(self):
        page = requests.get("https://ria.ru/world/")
        x = page.content
        soup = BeautifulSoup(x, 'html.parser')
        html = soup.findAll('a', class_="list-item__title color-font-hover-only")
        news = []
        for data in html:
            news.append(data.text)
            news.append(data.get('href'))
        return news
