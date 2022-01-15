import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram import Bot
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler


class Content:
    def jsonOfAPI(self, city_name, day=0):

        site = requests.get("https://time-in.ru/coordinates?search=Москва")
        try:
            bs = BeautifulSoup(site.content, 'lxml').find('b').find('a').get('href')
            bd = requests.get(bs)
            listOfCoor = BeautifulSoup(bd.content, 'lxml').find('div', class_='coordinates-city-info').find('div').getText()
        except AttributeError:
            listOfCoor = BeautifulSoup(site.content, 'lxml').find('div', class_='coordinates-city-info').find('div').getText()
        listOfCoor = listOfCoor.split()

        lat = listOfCoor[-2].replace(',', '')
        lon = listOfCoor[-1]
        print(f"lat {lat}")
        print(f"lon {lon}")
        API_key = "b41f154a86e9c4f96fd719a2d7207a11"

        link = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=current,minute,hourly&appid={API_key}')
        data_from_api = link.json()
        print(data_from_api["daily"][0])
        return data_from_api["daily"]

    def takeImage(self, city_name):
        date = datetime.now().month
        if 1 <= int(date) < 3 or date == 12:
            moth = "Winter"
        if 3 <= int(date) <= 5:
            moth = "Spring"
        if 6 <= int(date) <= 8:
            moth = "Summer"
        if 9 <= int(date) < 11:
            moth = "Autumn"

        page = requests.get(
            f"https://www.google.ru/search?q={city_name}++{moth}&tbm=isch&ved=2ahUKEwjMjOzb4Kj1AhWIzCoKHT6qDuoQ2-cCegQIABAA&oq=москва++зима&gs_lcp=CgNpbWcQAzIFCAAQgAQyBggAEAUQHjIECAAQGDIECAAQGDIECAAQGDIECAAQGDIECAAQGDIECAAQGDIECAAQGDoECAAQQzoGCAAQBxAeOgYIABAIEB46CAgAEIAEELEDUNcQWIkgYN0gaAJwAHgAgAE4iAHlApIBATiYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=VPncYcySJIiZqwG-1LrQDg&bih=1198&biw=1200#imgrc=94le2_6DQCwW_M")

        soup = BeautifulSoup(page.text, 'lxml')
        imgInLink = soup.findAll('img')
        randoom_img = random.randint(0, 16)
        return (imgInLink[randoom_img]).get('src')

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


class BrainOfBot:

    def __init__(self):
        self.dicOfState = {}

    def keyBoardMain(self):
        keyboard = [
            [
                InlineKeyboardButton("Погода", callback_data="weather"),
                InlineKeyboardButton("Новости", callback_data="news"),

            ],

        ]
        return InlineKeyboardMarkup(keyboard)

    def keyBoardToMain(self):
        keyboard = [
            [
                InlineKeyboardButton("Назад", callback_data="backToMain"),
            ],

        ]
        return InlineKeyboardMarkup(keyboard)

    def keyBoardDaily(self):
         keyboard = [

             [
                 InlineKeyboardButton("Сегодня", callback_data="now"),
                 InlineKeyboardButton("На завтра", callback_data="tomorrow"),
                 InlineKeyboardButton("На неделю", callback_data="week"),
             ],
             [
                 InlineKeyboardButton("Назад", callback_data="backToMain"),

             ],

         ]
         return InlineKeyboardMarkup(keyboard)

    def do_echo(self, update: Update, context: CallbackContext, ):
        print("Echo")
        userId = update.effective_user.id
        if self.dicOfState[userId] == "weather":
            text = update.message.text
            self.data = Content().jsonOfAPI(text)
            linkImg = Content().takeImage(text)

            update.message.reply_text(
                f"Сегодня в вашем городе { self.data[0]['temp']['day']}℃\n"
                "\n"
                f"Днем {self.data[0]['temp']['day']}\n"
                f"Ночью {self.data[0]['temp']['night']}℃\n"
                f"Облачность {self.data[0]['clouds']}%\n"
                f"Днем ощущаестя как {self.data[0]['feels_like']['day']}℃\n"
                f"Ночью ощущаестя как {self.data[0]['feels_like']['night']}℃\n",
                reply_markup=self.keyBoardDaily()
            )

    def news(self, update: Update):
        linkNews = 1
        News = Content().news()
        for i in News:
            if linkNews != 11:
                update.effective_message.reply_text(
                    News[linkNews],
                    reply_markup=self.keyBoardMain()
                )
                linkNews += 2

    def keyboardHendler(self, update: Update, bot: Bot, chat_data=None, **kwargs):
        query = update.callback_query
        data = query.data
        userId = update.effective_user.id
        if data == "weather":
            self.dicOfState[userId] = "weather"
            update.effective_message.reply_text(
                "Где узнаем погоду?",
                reply_markup=self.keyBoardToMain()
            )
        elif data == "news":
            self.news(update)
        elif data == "backToMain":
            self.dicOfState[userId] = "main"
            update.effective_message.reply_text(
                "Погода? Новости? У меня есть и то и другое!",
                reply_markup=self.keyBoardMain()

            )
        elif data == "now":
            query.edit_message_text(
                f"Сегодня в вашем городе { self.data[0]['temp']['day']}℃\n"
                "\n"
                f"Днем { self.data[0]['temp']['day']}\n"
                f"Ночью { self.data[0]['temp']['night']}℃\n"
                f"Облачность { self.data[0]['clouds']}%\n"
                f"Днем ощущаестя как { self.data[0]['feels_like']['day']}℃\n"
                f"Ночью ощущаестя как {self.data[0]['feels_like']['night']}℃\n",
                reply_markup=self.keyBoardDaily()
            )
        elif data == "tomorrow":
            query.edit_message_text(
                f"Завтра в вашем городе { self.data[1]['temp']['day']}℃\n"
                "\n"
                f"Днем { self.data[1]['temp']['day']}\n"
                f"Ночью { self.data[1]['temp']['night']}℃\n"
                f"Облачность { self.data[1]['clouds']}%\n"
                f"Днем ощущаестя как { self.data[1]['feels_like']['day']}℃\n"
                f"Ночью ощущаестя как {self.data[0]['feels_like']['night']}℃\n",
                reply_markup=self.keyBoardDaily()
            )
        elif data == "week":
            s = []
            i = 0
            for day in self.data:
                print(i)
                s.append(day['temp']['day'])
                i += 1
            print(s)
            query.edit_message_text(
                f"Сегодня {s[0]}℃\n"
                f"Завтра {s[1]}℃\n"
                f"Послезавтра  {s[2]}℃\n"
                f"4  {s[3]}℃\n"
                f"5  {s[4]}℃\n"
                f"6  {s[5]}℃\n"
                f"7  {s[6]}℃\n",
                reply_markup=self.keyBoardDaily()
            )

    def main(self, ):
        print("Поехали")

        updater = Updater(
            token='5093069989:AAFpImvrxEnqHc_oN9ElWIQX59ywnpYxaQw',
        )

        updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=self.do_echo))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.keyboardHendler))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=self.do_echo))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BrainOfBot().main()

