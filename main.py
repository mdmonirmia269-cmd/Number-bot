import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

API_TOKEN = '9239200994:AAF1CfmE-CA0fHi6rT0CAxam_3vnOo25Yx0'
bot = telebot.TeleBot(API_TOKEN)

API_BASE_URL = 'https://www.npnetworkbd.com/api/user'
API_KEY = 'YOUR_NP_API_KEY'  # আপনার আসল কি এখানে দেবেন

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📞 Get Number", callback_data='get_number'),
        InlineKeyboardButton("💰 Balance", callback_data='balance'),
        InlineKeyboardButton("👥 Refer & Earn", callback_data='refer'),
        InlineKeyboardButton("💬 Support", callback_data='support')
    )
    
    welcome_text = (
        "🤖 *Prime Number | Bot*\n"
        "💀 Hello, and I am a Number Auto Bot!\n\n"
        "🛍️ Select a service from the buttons below:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'get_number')
def process_get_number(call):
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📘 Facebook", callback_data='srv_facebook'),
        InlineKeyboardButton("📱 WhatsApp", callback_data='srv_whatsapp'),
        InlineKeyboardButton("📸 Instagram", callback_data='srv_instagram'),
        InlineKeyboardButton("✈️ Telegram", callback_data='srv_telegram'),
        InlineKeyboardButton("❌ Close", callback_data='back_home')
    )
    bot.edit_message_text("🦉 *Choose a service:*", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('srv_'))
def process_service_selection(call):
    bot.answer_callback_query(call.id)
    service_name = call.data.split('_')[1].upper()
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🇲🇦 Morocco (0.20tk)", callback_data=f'getnum_{service_name}_Morocco'),
        InlineKeyboardButton("🔄 Refresh", callback_data=call.data),
        InlineKeyboardButton("⬅️ Back", callback_data='get_number')
    )
    text = f"🌐 *{service_name}*🌐\n🛍️ *Live stock list:*\n\nনিচে উপলব্ধ কান্ট্রি ও প্রাইস দেওয়া হলো:"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('getnum_'))
def process_get_number_request(call):
    bot.answer_callback_query(call.id)
    parts = call.data.split('_')
    service_name = parts[1]
    country = parts[2]
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔄 Change Number", callback_data=f'srv_{service_name.lower()}'),
        InlineKeyboardButton("🌐 Change Country", callback_data='get_number'),
        InlineKeyboardButton("🏠 Home", callback_data='back_home'),
        InlineKeyboardButton("📢 OTP Group", url='https://t.me/YourOTPGroup')
    )
    text = (
        f"🔴 *Country : {country.upper()}-{service_name}-UNKNOWN-NEW-2*\n\n"
        f"🔄 *Waiting for OTP*\n\n"
        f"📱 *Number:* `+212768826110`"
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'back_home')
def back_to_home(call):
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📞 Get Number", callback_data='get_number'),
        InlineKeyboardButton("💰 Balance", callback_data='balance'),
        InlineKeyboardButton("👥 Refer & Earn", callback_data='refer'),
        InlineKeyboardButton("💬 Support", callback_data='support')
    )
    welcome_text = (
        "🤖 *Prime Number | Bot*\n"
        "💀 Hello, and I am a Number Auto Bot!\n\n"
        "🛍️ Select a service from the buttons below:"
    )
    bot.edit_message_text(welcome_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['balance', 'refer', 'support'])
def other_sections(call):
    bot.answer_callback_query(call.id)
    data = call.data
    if data == 'balance':
        text = "💰 *Account Balance:*\nআপনার বর্তমান ব্যালেন্স: `0.00 TK`"
    elif data == 'refer':
        text = "👥 *Refer & Earn:*\nআপনার রেফারেল লিংক শেয়ার করে আয় করুন!"
    else:
        text = "💬 *Support:*\nযেকোনো সমস্যায় আমাদের সাপোর্টে যোগাযোগ করুন।"
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Back", callback_data='back_home'))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

if __name__ == '__main__':
    print("Bot is running with TeleBot...")
    bot.infinity_polling()
