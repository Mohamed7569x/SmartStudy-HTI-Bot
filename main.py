# -*- coding: utf-8 -*-

from gemini_test import get_gemini_response, update_google_drive_content, input_prompt
import telebot
from telebot import util
import os
import time

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Edit The Welcome Message
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message,
                 """🔺 مرحبًا بكم في بوت البحث عن الملفات التعليمية لمعهد HTI نأمل أن يكون هذا البوت مفيدًا لكم. يتمتع البوت بقدرة على فهم جميع الأوامر الخاصة بكم من خلال التعلم الآلي وتحليلها للبحث عن المناهج والملفات المطلوبة. تم برمجة البوت للغرض التعليمي. يمكنكم التواصل معي في حال وجود أي استفسار على الرقم التالي: 01205853374 🔺""")
def isMsg(x):
    return True

# Use this command when you add new files to your drive    
@bot.message_handler(commands=['update20211079', '/update20211079'], func=isMsg)
def check_update(message):
    files = update_google_drive_content()
    with open('id_s.txt', 'w', encoding='utf-8') as f:
        for file_ in files:
            f.write(f"{file_['id']}:{file_['name']}\n")
    bot.reply_to(message, f"🔺 تم تحديث الملفات بنجاح 🔺")

@bot.message_handler(func=isMsg)
def search(message):
    prompt = message.text
            
    files_ids = []   
    # reading the ids from the ids text    
    with open('id_s.txt', 'r', encoding='utf-8') as f:
        for file__ in f:
            id_, name = file__.strip().split(':')
            files_ids.append({'id': id_, 'name': name})

    with open('file_names.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        
    file_names = "\n".join(["- " + line for line in lines])
    file_name = get_gemini_response(input_prompt,file_names, prompt)
    file_name = (file_name.replace('- ', ''))

    id = None
    for file in files_ids:
        if file['name'] == f'{file_name}':
            id = file['id']
            break
    if id:
        bot.reply_to(message, f"[+]━━━【✅ تم العثور علي الماده ✅】━━[+]\n\n"
                    f"الاسم: {file_name}\n"
                    f"الرابط: https://drive.google.com/drive/u/0/folders/{id}")
    else:
        bot.reply_to(message, f"[-]━━━【لم يتم العثور علي الماده】━━[-]")

def poll_telebot():
    bot.infinity_polling(allowed_updates=util.update_types)

# Error Handling
def main():
    retries = 3  # Number of retries
    delay = 5  # Delay in seconds between retries

    for attempt in range(retries):
        try:
            poll_telebot()
        except telebot.apihelper.ApiException as e:
            time.sleep(delay)
        else:
            break
    else:
        print("Polling failed after retries.")

if __name__ == "__main__":
    main()

# https://drive.google.com/drive/folders/1qAaKgG7myO29BgEaVqu7aBU84iHmNhgO?usp=sharing
# https://drive.google.com/file/d/1_T3a6l3j5QNyUiN9BkgL2bndfVkxYN-p/view?usp=sharing
# https://drive.google.com/drive/u/0/folders/1-cuECSpS-NLG41kpEyhdgc9Cxf6rnK9Q