# -*- coding: utf-8 -*-
# coding=utf-8
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import numpy as np

i = 0

# id_device = {'a':[0,0,0]}
# np.save('user_chat_ids.npy', id_device)
id_device = np.load('user_chat_ids.npy').item()
print(id_device)
devices = ["تغییر رنگ نور اتاق","روشن و خاموش کردن ماشین لباسشویی","روشن و خاموش کردن لامپ","برقرای تماس تلفنی","درخواست تاکسی اینترنتی(اسنپ و ...)","پخش کردن فیلم","روشن و خاموش کردن پروژکتور","پخش کردن موزیک","پرده برقی","روشن و خاموش کردن هود","روشن و خاموش کردن مایکروفر","تنظیم زمان مایکروفر","روشن و خاموش کردن آباژور","روشن و خاموش کردن ماشین ظرف شویی",
        "تنظیم هشدار(آلارم) ساعت","اطلاع از وضعیت آب و هوا","تغییر سرعت اسپیلیت","تغییر دمای اسپیلیت","تنظیم سرعت کولر","روشن و خاموش کردن کولر","روشن و خاموش کردن اجاق گاز","روشن و خاموش کردن تلوزیون","تغییر صدای تلوزیون","تغییر کانال تلویزیون","باز و بسته کردن درب خانه","باز و بسته کردن در پارکینگ"]

replies = ["عجججب که اینطور🤔🤔🤔 دیگه چه طور میشه این جمله رو گفت","هوووم جالبه یکی دیگه هم بنویس😁😁😁","منتظر جمله دوم شما هستیم","من تو محیطهای مختلف قراره کار کنم،یه جور دیگه هم بهم یاد بده که ضایع نشم😄","یاد میگیرم ولی فراموشم میشه😊😊😊 یه جور دیگه هم میگی","هر وقت خواستی میتونی از پایین cancel رو بزنی ولی ادامه بده تو میتونی😉😉😀😀","لطفا یک جمله دیگر برای این دستگاه وارد کنید","خیلی ممنون از همکاریتون،میشه یکی دیگه هم یادم بدید...","اگر میتونی یک جمله دیگه هم یادم بده"]
updater = Updater(token="626645153:AAEqaqSA2hLxtnXZmP3DceKSBr3pK5cpsSM")
dispatcher = updater.dispatcher


def startcommand(bot, update):
    global id_device, i
    j = 1
    update.message.reply_text("""سلام 
ما در حال طراحی یک دستیار صوتی برای خانه هوشمند هستیم. باکمک این سیستم کار های روزمره از جمله کنترل وسایل برقی خانه مانند تلویزیون و روشنایی یا درخواست اسنپ با دستورات صوتی به زبان فارسی قابل انجام خواهد بود. برای این کار نیاز به تعداد زیادی از این جملات با گویش ها و فرهنگ های مختلف داریم تا برای تمامی خانواده های ایرانی قابل استفاده باشد. بات اسم دستگاه ها را به شما گفته و نحوه ی برقراری ارتباط با آن دستگاه را از شما می خواهد. برای هر دستگاه ۲ جمله از شما خواسته می شود ترجیحا یکی را رسمی و دیگری را عامیانه بنویسید.
برای دیدن مثال از Help/ استفاده کنید
برای بستن بات از cancel/ استفاده کنید
    """)

    if(id_device.get(update.message.chat_id,None) == None):
        user_dic = {update.message.chat_id: [i, j]}
        id_device.update(user_dic)
        np.save('user_chat_ids.npy', id_device)
        i = i+3
        if i >= len(devices):
            i=0
    else:
        id_device.pop(update.message.chat_id, None)
        i = i + 3
        if i >= len(devices):
            i = 0
        user_dic = {update.message.chat_id: [i, j]}
        id_device.update(user_dic)
        np.save('user_chat_ids.npy', id_device)


    update.message.reply_text("اگر میشه در مورد " + devices[id_device.get(update.message.chat_id)[0]]+ " یه جمله بهم یاد بده.")
    id_device[update.message.chat_id] = [id_device.get(update.message.chat_id)[0],2]
    print(len(id_device))

def textmessage (bot, update):
    user_input = update.message.text
    with open (devices[id_device.get(update.message.chat_id)[0]]+".txt","a", encoding="utf-8") as file:
        file.write(user_input + "\n")
        file.close()
   
    if id_device.get(update.message.chat_id)[1] == 2 :
        reply = replies [id_device.get(update.message.chat_id)[0] % len(replies)]
        update.message.reply_text(reply)
        id_device.get(update.message.chat_id)[1] = 1
    else:
        id_device[update.message.chat_id] = [id_device.get(update.message.chat_id)[0]+1,2]
        if id_device.get(update.message.chat_id)[0] >= len(devices):
            id_device.get(update.message.chat_id)[0] = 0
        update.message.reply_text(
            "اگر میشه در مورد " + devices[id_device.get(update.message.chat_id)[0]] + " یه جمله بهم یاد بده.")
    np.save('user_chat_ids.npy', id_device)
    print(len(id_device))

def cancel(bot, update):
    update.message.reply_text('باتشکر از همکاریتون اگر بعدا وقت داشتین ممنون میشم بازم برام جمله بفرستین')
    id_device.pop(update.message.chat_id,None)
    print(len(id_device))

def help(bot, update):
    update.message.reply_text(
"""تغییر کانال تلویزیون:
کانال تلویزیون را به ۳ تغییر بده
بزن کانال 3

تغییر رنگ نور اتاق:
نور سالن پذیرایی را به آبی تغییر بدهید
نور هال رو آبی کن

تغییر دمای اسپیلیت:
دمای اتاق خواب را در 24 درجه قرار بده
پذیرایی رو 24 درجه کن

بات دو بار برای هر دستگاه درخواست جمله می کند
لطفا در هر درخواست یک جمله بنویسید"""
        )
    # id_device.pop(update.message.chat_id,None)


def main():

    start_command_handler = CommandHandler("start", startcommand)
    text_message_handler = MessageHandler(Filters.text, textmessage)
    cancle_command_handler = CommandHandler("cancel", cancel)
    help_command_handler = CommandHandler("Help", help)
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    dispatcher.add_handler(cancle_command_handler)
    dispatcher.add_handler(help_command_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()