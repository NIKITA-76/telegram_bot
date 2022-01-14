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
    def jsonOfAPI(self, city_name):
        link = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={"b41f154a86e9c4f96fd719a2d7207a11"}'
        link_api = requests.get(link)
        data_from_api = link_api.json()
        if data_from_api['cod'] == '404':
            return "Error"
        return data_from_api

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

            ]

        ]
        return InlineKeyboardMarkup(keyboard)

    def keyBoardToMain(self):
        keyboard = [
            [
                InlineKeyboardButton("Назад", callback_data="backToMain"),
            ]

        ]
        return InlineKeyboardMarkup(keyboard)



    def do_echo(self, update: Update, context: CallbackContext, ):
        print("Echo")
        userId = update.effective_user.id
        if self.dicOfState[userId] == "weather":
            text = update.message.text
            print(text)
            data = Content().jsonOfAPI(text)
            linkImg = Content().takeImage(text)
            try:
                update.message.reply_text(


                    f"Сегодня в вашем городе {data['main']['temp']}℃\n"
                    "\n"
                    f"Максимальная температура {data['main']['temp_max']}℃\n"
                    f"Минимальная температура {data['main']['temp_min']}℃\n"
                    f"Ощущаестя как {data['main']['feels_like']}℃\n",
                    reply_markup=self.keyBoardToMain()

                )
            except TypeError as er:
                print(er)
                update.message.reply_photo(

                    photo="https://sun9-37.userapi.com/impg/-XQO_OQhbrdbfHLghGKMz1YrWz6ZJQGG9hZvpg/fw2jsw0uC6U.jpg?size=1312x1044&quality=96&sign=2dab725107599285e4fafb78cc4e2aba&type=album",
                    caption="Пффф, не город а фигня какая-то\n"
                    "\n"
                    "Давай по новой",

                    reply_markup=self.keyBoardToMain()

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

    def main(self, ):
        print("Поехали")

        updater = Updater(
            token='5093069989:AAFpImvrxEnqHc_oN9ElWIQX59ywnpYxaQw',
        )

        updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=self.do_echo))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.keyboardHendler))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BrainOfBot().main()
