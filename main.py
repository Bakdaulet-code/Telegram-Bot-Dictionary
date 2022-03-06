from telegram import *
from telegram.ext import *
from requests import *
import json

updater = Updater(token="YOUR TOKEN")
dispatcher = updater.dispatcher


a = "✍🏻 Узнать об авторе ✍🏻"
b = "📕 Получить PDF версию словаря 📕"
c = "🔎 Начать поиск 🔎"
dd = "🗣 Предложить новое слово для телеграм бота 🗣"

likes = 0
dislikes = 0

global saver


def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(a)], [KeyboardButton(b)] , [KeyboardButton(c)] , [KeyboardButton(dd)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вас приветствует телеграм бот 'Толковый IT словарь' !",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def messageHandler(update: Update, context: CallbackContext):
    d = open('db.json', 'r', encoding="utf8")
    jF = json.load(d)
    d.close()



    checker = 0


    if a in update.message.text:
        update.message.reply_text('Меня создал студент 2-го курса из Astana IT University.\n'
                                  '\nБакдаулет Жаксылык - @HumToRob')

    if b in update.message.text:
        update.message.reply_text('Вот электронная версия документа: ')
        context.bot.sendDocument(update.effective_chat.id, document=open('База всех слов.pdf', 'rb'))

    if c in update.message.text:
        update.message.reply_text("Отправьте мне непонятное Вам слово:")


    for word in jF["words"]:
        if update.message.text.lower() == word["word"]:
            checker += 0
            update.message.reply_text(word["definition"])
            buttons = [[InlineKeyboardButton("Да 👍", callback_data="like")],
                        [InlineKeyboardButton("Не совсем 👎", callback_data="dislike")]]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                        reply_markup=InlineKeyboardMarkup(buttons),
                                        text='Правильно ли бот объяснил значение слово "' + update.message.text.lower() + '"?')



    if dd in update.message.text:
        update.message.reply_text("Отправьте свое предложение на аккаунт @HumToRob:\n\n"
                                  "В формате:\n"
                                  "слово: ___________\n"
                                  "значение: _______")



def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    global likes, dislikes

    if "like" in query:
        likes += 1

    if "dislike" in query:
        dislikes += 1

    if "da" in query:
        update.callback_query.message.edit_text("Отправьте свое предложение на аккаунт @HumToRob:\n\n"
                                        "В формате:\n"
                                        "слово: ___________\n"
                                        "значение: _______")

    if "net" in query:
        update.callback_query.message.edit_text("Окей, поищите тогда других слов! 🙂")

    print(f"Нравится => {likes} | Не нравится => {dislikes}")



dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

dispatcher.add_handler(CallbackQueryHandler(queryHandler))


updater.start_polling()