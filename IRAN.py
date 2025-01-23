import json
import urllib.parse
import urllib.request

# اطلاعات ربات (توکن و آیدی‌ها)
BOT_TOKEN = "7763504661:AAGFCsiffOqRRQPdWrGsM0gA-SinzKsOW3c"  # توکن ربات
API_URL = f"https://api.telegram.org/bot{7763504661:AAGFCsiffOqRRQPdWrGsM0gA-SinzKsOW3c}"
DESTINATION_CHAT_ID = "https://t.me/f6rsi"  # آیدی چت مقصد (مثلاً گروهی که اطلاعات به آن ارسال شود)

# ارسال درخواست به API تلگرام
def send_request(method, data):
    url = f"{API_URL}/{method}"
    encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url, data=encoded_data)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))

# ارسال پیام با دکمه‌ها
def send_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📊 ضرایب و مسابقات", "url": "https://example.com"},  # لینک خود را جایگزین کنید
            ],
            [
                {"text": "🎲 گذاشتن شرط", "callback_data": "place_bet"}
            ]
        ]
    }
    data = {
        "chat_id": chat_id,
        "text": "لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        "reply_markup": json.dumps(keyboard)
    }
    send_request("sendMessage", data)

# پردازش پاسخ‌های کاربر
def process_update(update):
    if "callback_query" in update:  # وقتی کاربر روی دکمه کلیک می‌کند
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        callback_data = query["data"]

        if callback_data == "place_bet":
            send_request("sendMessage", {"chat_id": chat_id, "text": "لطفاً مبلغ را به تومان وارد کنید:"})
        return

    if "message" in update:  # وقتی کاربر پیامی می‌فرستد
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # ذخیره اطلاعات شرط‌بندی
        if text.isdigit():
            send_request("sendMessage", {"chat_id": chat_id, "text": "مبلغ دریافت شد! حالا نام تیم‌ها را وارد کنید."})
        elif "و" in text:  # فرض می‌کنیم کاربر نام تیم‌ها را با "و" جدا کند
            send_request("sendMessage", {"chat_id": chat_id, "text": "برد یا مساوی؟ لطفاً مشخص کنید."})
        elif text.lower() in ["برد", "مساوی"]:
            send_request("sendMessage", {"chat_id": chat_id, "text": "لطفاً نام و شماره تماس خود را وارد کنید."})
        elif len(text.split()) >= 2:  # فرض می‌کنیم کاربر نام و شماره تماس را ارسال کرده است
            # ارسال اطلاعات به چت مقصد
            send_request("sendMessage", {
                "chat_id": DESTINATION_CHAT_ID,
                "text": f"اطلاعات شرط‌بندی جدید:\n{text}"
            })
            send_request("sendMessage", {"chat_id": chat_id, "text": "اطلاعات شما با موفقیت ثبت شد. ممنون!"})

# حلقه برای بررسی پیام‌های جدید
def main():
    offset = 0
    while True:
        data = {"offset": offset, "timeout": 10}
        response = send_request("getUpdates", data)

        for update in response.get("result", []):
            process_update(update)
            offset = update["update_id"] + 1

if __name__ == "__main__":
    main()
