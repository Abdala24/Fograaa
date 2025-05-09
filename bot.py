
import telebot
import os

TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('إضافة شحنة', 'حالة الشحنات')
    if message.from_user.id == ADMIN_ID:
        markup.row('لوحة تحكم الأدمن')
    bot.send_message(
        message.chat.id,
        "مرحباً بك في نظام ShahenX للشحن! اختر من الأزرار:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "لوحة تحكم الأدمن")
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "أهلاً بك في لوحة تحكم الأدمن!\n- عرض الشحنات\n- إدارة المستخدمين")
    else:
        bot.send_message(message.chat.id, "هذه الميزة مخصصة للأدمن فقط.")

@bot.message_handler(func=lambda message: message.text == "حالة الشحنة")
def check_shipment_status(message):
    # هنا يتحقق من وجود الشحنة
    if message.chat.id in user_data and 'tracking' in user_data[message.chat.id]:
        bot.send_message(
            message.chat.id,
            f"حالة الشحنة:\nرقم التتبع: {user_data[message.chat.id]['tracking']}"
        )
    else:
        bot.send_message(message.chat.id, "لا توجد شحنة مسجلة لهذا الحساب.")

@bot.message_handler(func=lambda m: m.text == 'إضافة شحنة')
def add_shipment(message):
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "ادخل اسم العميل:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    user_data[message.chat.id]['name'] = message.text
    msg = bot.send_message(message.chat.id, "ادخل رقم الهاتف:")
    bot.register_next_step_handler(msg, get_phone)

def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    msg = bot.send_message(message.chat.id, "ادخل العنوان:")
    bot.register_next_step_handler(msg, get_address)

def get_address(message):
    user_data[message.chat.id]['address'] = message.text
    msg = bot.send_message(message.chat.id, "ادخل رقم التتبع:")
    bot.register_next_step_handler(msg, save_shipment)

def save_shipment(message):
    user_data[message.chat.id]['tracking'] = message.text
    bot.send_message(
        message.chat.id,
        f"تم حفظ الشحنة:\n"
        f"اسم: {user_data[message.chat.id]['name']}\n"
        f"هاتف: {user_data[message.chat.id]['phone']}\n"
        f"عنوان: {user_data[message.chat.id]['address']}\n"
        f"تتبع: {user_data[message.chat.id]['tracking']}"
    )

bot.polling(non_stop=True)
