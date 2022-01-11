from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
import requests


class APIWeather():
    def jsonOfAPI(self, city_name):
        link = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={"b41f154a86e9c4f96fd719a2d7207a11"}'
        link_api = requests.get(link)
        data_from_api = link_api.json()
        return data_from_api




class brainOfBot():

    def message_handler(self, update: Update, context: CallbackContext):
        text = update.message.text
        data = APIWeather().jsonOfAPI(text)
        update.message.reply_text(

            text=f"Сегодня в вашем городе {data['main']['temp']}℃\n"
                 "\n"
                 f"Максимальная температура {data['main']['temp_max']}℃\n"
                 f"Минимальная температура {data['main']['temp_min']}℃\n"
                 f"Ощущаестя как {data['main']['feels_like']}℃\n",
        )

    def main(self):
        print("Start")

        updater = Updater(
            token='5093069989:AAFpImvrxEnqHc_oN9ElWIQX59ywnpYxaQw',
            use_context=True,
        )

        updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=self.message_handler))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    x = brainOfBot()
    x.main()
