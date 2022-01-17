from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


class Keyboard:
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

    def keyBoardHomeOrForestCreepy(self):
        keyboard = [
            [
                InlineKeyboardButton("БЕЖАТЬ ДОМОЙ", callback_data="backToHOME"),
            ],
            [
                InlineKeyboardButton("БЕЖАТЬ В ЛЕС", callback_data="backToForest"),
            ],

        ]
        return InlineKeyboardMarkup(keyboard)

    def keyBoardForestOrLonelyHouse(self):
        keyboard = [
            [
                InlineKeyboardButton("ГЛУБЖЕ В ЛЕС", callback_data="backToForestForest"),
            ],
            [
                InlineKeyboardButton("ОДИНОКИЙ ДОМ", callback_data="backToLonelyHome"),
            ],

        ]
        return InlineKeyboardMarkup(keyboard)


    def keyBoardForestForest(self):
        keyboard = [
            [
                InlineKeyboardButton("ГЛУБЖЕ В ЛЕС", callback_data="backToForestForest"),
            ],


        ]
        return InlineKeyboardMarkup(keyboard)


    def keyBoardTakeFlashlight(self):
        keyboard = [
            [
                InlineKeyboardButton("Достать фонарик", callback_data="takeFlashlight"),
            ],


        ]
        return InlineKeyboardMarkup(keyboard)

    def keyBoardSwitchOnFlashlight(self):
        keyboard = [
            [
                InlineKeyboardButton("Включить его", callback_data="switchOnFlashlight"),
            ],


        ]
        return InlineKeyboardMarkup(keyboard)



    def keyBoardGoIntoHouse(self):
        keyboard = [
            [
                InlineKeyboardButton("ВОЙТИ В ДОМ", callback_data="goIntoHouse"),
            ],

        ]
        return InlineKeyboardMarkup(keyboard)

    def keyBoardFromHomeCreepy(self):
        keyboard = [
            [
                InlineKeyboardButton("БЕЖАТЬ БЕЖАТЬ БЕЖАТЬ", callback_data="runFromHome"),
            ],

        ]
        return InlineKeyboardMarkup(keyboard)



    def keyBoardScreamCreepy(self):
        keyboard = [
            [
                InlineKeyboardButton("ТВОИ КРИКИ НИКТО НЕ СЛЫШИТ...", callback_data="backToMainFromCreepy"),
            ],

        ]
        return InlineKeyboardMarkup(keyboard)