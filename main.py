from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = '7714617822:AAHqmCs9fsRGO0Jdvj_aXWUU-1L1M4aBOSw'  # توکن ربات
ADMIN_ID = 784488848 # آیدی ادمین

user_messages = {}  # ذخیره پیام‌های کاربران برای ارسال پاسخ

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("به ربات پیام ناشناس خوش آمدید! پیام خود را ارسال کنید.")

async def anonymous_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    message_text = update.message.text
    
    # ذخیره پیام فرستنده
    user_messages[user_id] = update.message
    
    # ارسال پیام به ادمین
    await context.bot.send_message(ADMIN_ID, f"""📩 پیام ناشناس جدید:

{message_text}

🆔 از کاربر: {user_id}

برای پاسخ دادن از دستور /reply <user_id> <message> استفاده کنید.""")
    
    # ارسال تأییدیه به فرستنده
    await update.message.reply_text("✅ پیام شما ناشناس ارسال شد!")

async def reply(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != ADMIN_ID:
        await update.message.reply_text("⛔ شما اجازه استفاده از این دستور را ندارید.")
        return
    
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ استفاده صحیح: /reply <user_id> <message>")
        return
    
    user_id = int(args[0])
    reply_text = " ".join(args[1:])
    
    if user_id in user_messages:
        await context.bot.send_message(user_id, f"""📩 پاسخ از ادمین:

{reply_text}""")
        await update.message.reply_text("✅ پاسخ ارسال شد!")
    else:
        await update.message.reply_text("❌ کاربر یافت نشد یا پیام قبلی موجود نیست.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anonymous_message))
    app.run_polling()

if __name__ == "__main__":
    main()