import time
from datetime import datetime
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from Content import Content
from Keyboard import Keyboard


class BrainOfBot:

    def __init__(self):
        self.dicOfState = {}
        self.missTake = 0

    def do_echo_sticker(self, update: Update, context: CallbackContext, ):
        update.message.reply_text(
            text="Четкий",
            reply_markup=Keyboard().keyBoardMain(),
        )

    def do_echo_start(self, update: Update, context: CallbackContext, ):
        update.message.reply_text(
            text="Я вас категорически приветствую. Я создан, что бы служить Вам, людишкам!\n"
                 "Так что пользуйтесь мной, как вам угодно!",
            reply_markup=Keyboard().keyBoardMain(),
        )

    def do_echo(self, update: Update, context: CallbackContext, ):
        userId = update.effective_user.id
        if self.dicOfState[userId] == "weather":
            self.text = update.message.text
            if Content().jsonOfAPI(city_name=self.text, day="now", ) != "ERROR_IN_JSON_API":
                data = Content().jsonOfAPI(city_name=self.text, day="now")
                if isinstance(data, str):
                    print(type(data))
                    update.message.reply_text(
                        text="Сегодня" + data,
                        reply_markup=Keyboard().keyBoardDaily()
                    )
                else:
                    if self.missTake == 0:
                        update.message.reply_photo(
                            photo="https://sun9-50.userapi.com/impg/O7sQeAfLsgy6wbCD0S6-SdFHsqr7-7Apn7Vt4A/B_JLrZsqtus.jpg?size=600x408&quality=96&sign=9d83dc3128f3222928a76c4eda0e80f5&type=album",
                            caption="ТЫ УВЕРЕН ЧТО Я ЗНАЮ ТАКОЙ ГОРОД?\n"
                                    "\n"
                                    "ПОПРОБУЙ ЕЩЕ РАЗ",
                            reply_markup=Keyboard().keyBoardToMain(),
                        )
                        self.missTake += 1
                    else:
                        update.message.reply_photo(
                            photo="https://thoughtcatalog.com/wp-content/uploads/2018/07/doverdemon.jpg",
                            caption="НЕ НУЖНО \n"
                                    "БЫЛО \n"
                                    "ЕГО \n"
                                    "ЗЛИТЬ",
                            reply_markup=Keyboard().keyBoardHomeOrForestCreepy(),
                        )
                        self.missTake = 0
                        self.dicOfState[userId] = "creepy"

    def news(self, update: Update):
        listOfNews = Content().news()
        for news in listOfNews:
            update.effective_message.reply_text(
                news,
                reply_markup=Keyboard().keyBoardMain()
            )

    def keyboardHendler(self, update: Update, bot: Bot, chat_data=None, **kwargs):

        query = update.callback_query
        dataFromKeyboard = query.data
        userId = update.effective_user.id
        if dataFromKeyboard == "news":
            print(dataFromKeyboard)
            self.news(update)

        elif dataFromKeyboard == "weather":
            self.dicOfState[userId] = "weather"
            update.effective_message.reply_text(
                "Где узнаем погоду?",
                reply_markup=Keyboard().keyBoardToMain()
            )
        elif dataFromKeyboard == "backToMain":
            self.dicOfState[userId] = "main"
            self.missTake = 0
            update.effective_message.reply_text(
                "Погода? Новости? У меня есть и то и другое!",
                reply_markup=Keyboard().keyBoardMain()
            )
        elif dataFromKeyboard == "now":
            data = Content().jsonOfAPI(city_name=self.text, day=dataFromKeyboard)
            query.edit_message_text(
                text="Сегодня" + data,
                reply_markup=Keyboard().keyBoardDaily(),
            )
        elif dataFromKeyboard == "tomorrow":
            data = Content().jsonOfAPI(city_name=self.text, day=dataFromKeyboard)
            query.edit_message_text(
                text="Завтра" + data,
                reply_markup=Keyboard().keyBoardDaily(),
            )
        elif dataFromKeyboard == "week":
            data, alerts = Content().jsonOfAPI(city_name=self.text, day=dataFromKeyboard)
            days = datetime.now()
            listOfDaysForWeather = []
            if alerts == "Предупреждений нет":
                alerts = ""
            else:
                alerts = "\U000026A0"
            i = 0
            if days.month < 10:
                month = "0" + str(days.month)
            else:
                month = days.month
            for day in data:
                listOfDaysForWeather.append(day['temp']['day'])
                i += 1
            query.edit_message_text(
                f"Сегодня {listOfDaysForWeather[0]}℃ {alerts}\n"
                f"Завтра {listOfDaysForWeather[1]}℃\n"
                f"Послезавтра  {listOfDaysForWeather[2]}℃\n"
                f"{days.day + 3}.{month}  {listOfDaysForWeather[3]} ℃\n"
                f"{days.day + 4}.{month}  {listOfDaysForWeather[3]} ℃\n"
                f"{days.day + 5}.{month}  {listOfDaysForWeather[4]} ℃\n"
                f"{days.day + 6}.{month}  {listOfDaysForWeather[5]} ℃\n",
                reply_markup=Keyboard().keyBoardDaily(),
            )
        elif dataFromKeyboard == "backToHOME":
            if self.dicOfState[userId] == "creepy":
                bot.bot.send_animation(
                    chat_id=userId,
                    animation="https://c.tenor.com/nlYV4at3ptgAAAAC/demon-ghost.gif",
                    caption="Забежав домой, ты видиешь женщину, мотая головой она боромочит\n"
                            "Не нужно... было... его... злить... \n"
                            "не нужно... злить... его...",
                    reply_markup=Keyboard().keyBoardFromHomeCreepy(),
                )
        elif dataFromKeyboard == "runFromHome":
            if self.dicOfState[userId] == "creepy":
                bot.bot.send_animation(
                    chat_id=userId,
                    animation="https://c.tenor.com/G2C-QoymHjwAAAAC/horror-demon.gif",
                    caption="НЕ УСПЕЛ",
                )
            time.sleep(1.5)
            update.effective_message.reply_photo(
                photo="https://media.istockphoto.com/photos/dark-scream-picture-id135165661?k=20&m=135165661&s=170667a&w=0&h=vCl5Uwq1SUvnkyJJbyLtvVpKEjoKUj7G8pLXFhgeths=",
                reply_markup=Keyboard().keyBoardScreamCreepy(),
            )
        elif dataFromKeyboard == "backToForest":
            update.effective_message.reply_text(
                "Ты бежишь в лес"
            )
            time.sleep(3.2)
            update.effective_message.reply_text(
                "Ты понимаешь что он догоняет...\n"
                "Нужно срочно что-то предпринимать",
            )
            time.sleep(3.2)
            update.effective_message.reply_text(
                "Ты замечаешь одинокий дом, в нем можно спрятаться \n"
                "Или же\n"
                "Можно бежать дальше в лес",
                reply_markup=Keyboard().keyBoardForestOrLonelyHouse()
            ),
        elif dataFromKeyboard == "backToLonelyHome":
            update.effective_message.reply_photo(
                photo="https://psv4.userapi.com/c237131/u245081982/docs/d45/2665d458b3fd/LonelyHouse.jpg?extra=jCTYUXRyTpfsaxTZ42PoR9n_gIgm8DGCtWYjI35e2Hh4IUVs51OEE3J9BaSVyr8qCLDM5bra_DhSq3RZ57BFK2pUjZ8c7lPRPjjMlb7i-maQfQXzscZ55DIoRuPVjN3hDpScNE0AF5wqEpIJmENuovQ",
                reply_markup=Keyboard().keyBoardGoIntoHouse()
            )
        elif dataFromKeyboard == "goIntoHouse":
            goIH = ["Забежав в дом, ты в панике ищешь любое укрытие",
                    "Найдя комнату, ты вошел в нее и затаил дыхание",
                    "Ты слышишь как он приблежаеться к твоей комнате...",
                    "Он понял что ты там",
                    "От страха, ты прижался к стене",
                    "Он выломал дверь...",
                    ]
            for i in goIH:
                update.effective_message.reply_text(
                    text=i
                )
                time.sleep(2.8)
            time.sleep(3)
            update.effective_message.reply_photo(
                photo="https://psv4.userapi.com/c237131/u245081982/docs/d12/f74c8b493955/Dq30lA_XgAIR9Sd.jpg?extra=Bntz1K17f338HkOIPc7rgE-W3Vb4BhPG1R0fTaJKcgiR5HFF1BMpB_CiSOtKU5gjPEibpxOsc7d77grHnQOKACAlAp8sFt5eZS4mssYaK854u31Xvw8qip8AmoH534oCIXtIqZQqYsEuDJHU1ZBLOe0",
                caption="НЕ НУЖНО БЫЛО ЕГО ЗЛИТЬ",
            )
            time.sleep(3.5)
            update.effective_message.reply_text(
                reply_markup=Keyboard().keyBoardScreamCreepy(),
                text="ТВОИ КРИКИ НИКТО НЕ УСЛЫШИТ"
            )
        elif dataFromKeyboard == "backToForestForest":
            backFF = ["Ты спрятался за деревом", "Вроде пронесло",
                      "По крайней мере ты его не видишь",
                      "И не слышишь...", ]
            update.effective_message.reply_text(
                "Твоя выносливость говорит сама за себя. Пробежав какое-то расстояние, "
                "ты понимаешь, бежать больше ты не в состаянии",
            )
            time.sleep(5)
            for i in backFF:
                update.effective_message.reply_text(
                    text=i
                )
                time.sleep(2.8)
            update.effective_message.reply_text(
                "Почти задыхаясь, ты вспоминаешь что в кармане где-то есть фонарик",
                reply_markup=Keyboard().keyBoardTakeFlashlight()
            )
        elif dataFromKeyboard == "takeFlashlight":
            update.effective_message.reply_text(
                "Ты рыщешь по карманам в его поиске",
            )
            time.sleep(4)
            update.effective_message.reply_text(
                "А вот и он",
                reply_markup=Keyboard().keyBoardSwitchOnFlashlight()
            )
        elif dataFromKeyboard == "switchOnFlashlight":
            update.effective_message.reply_text(
                "Ты включаешь фонарик...",
            )
            time.sleep(1.5)
            update.effective_message.reply_photo(
                photo="https://psv4.userapi.com/c237131/u245081982/docs/d40/28c211c829cb/EBGjQjPXsAA82AB.jpg?extra=OGBmmtQYIUDCw7LLuJkoCxrEQLXPbqI7bClutIYFKikyGyvo5r_K_fPXdnwMGDhAOgNEQAREifBGgktzxwhBlWIz_6nSW6IM5qj3ccT2lNCL19C5GE-49bJQLK_IwRwLwBnb9ful8I-AXPoaBzRV4DA",
                caption="НЕ НУЖНО БЫЛО ЕГО ЗЛИТЬ",
            )
            time.sleep(3)
            update.effective_message.reply_photo(
                photo="https://psv4.userapi.com/c237131/u245081982/docs/d19/9ef1b39e8609/pxfuel_com_-scaled.jpg?extra=a4oVMaYIQc52Uab_QJNKlYWYWx_sKDBk6J4qj-ByJS8LPVPyv7Wu6kC49jKGw2ocVebm8h08gmSJeZDGKiiG52ZO73CNSXMATn-l5LrP9JR-HHAu0PZSYforltL6Uja58S8yJLGoXqtpe5fOSGZoUCU",
                reply_markup=Keyboard().keyBoardScreamCreepy(),
            )
        elif dataFromKeyboard == "backToMainFromCreepy":
            if self.dicOfState[userId] == "creepy":
                update.effective_message.reply_text(
                    "Погода? Новости? Если не злить, можно все получить!",
                    reply_markup=Keyboard().keyBoardMain()
                )

    def main(self, ):
        print("Поехали")

        updater = Updater(
            token='5093069989:AAFpImvrxEnqHc_oN9ElWIQX59ywnpYxaQw',
        )
        updater.dispatcher.add_handler(CommandHandler("start", filters=Filters.text, callback=self.do_echo_start))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=self.do_echo))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=self.keyboardHendler))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.sticker, callback=self.do_echo_sticker))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    BrainOfBot().main()
