import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

# Environment variables
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@YourChannelName")  # Fallback if not set
FORCE_JOIN_LINK = os.getenv("FORCE_JOIN_LINK", "https://t.me/+JlERJvczl-k2OWJl")
SHARE_LINK = os.getenv("SHARE_LINK", "https://t.me/share/url?url=%20JOIN%20THIS%20AMAZING%20GROUP%20%F0%9F%A5%B5%20-%20https%3A%2F%2Ft.me/DESIGNBYKINGBOT")

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username if user.username else user.first_name
    user_id = user.id

    # Welcome message
    welcome_message = (
        f"{username}, How are you. Your password is {user_id}.🍑\n"
        "Click on get videos button🔞"
    )

    # Create inline keyboard with three buttons
    keyboard = [
        [InlineKeyboardButton("❤GET VIDEOS FREE❤", callback_data="get_videos")],
        [InlineKeyboardButton("LATEST VIDEOS STOCK", url=FORCE_JOIN_LINK)],
        [InlineKeyboardButton("SHARE AND GET VIP", url=SHARE_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send welcome message with buttons
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Handler for button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    if query.data == "get_videos":
        try:
            # Fetch recent messages (videos) from the channel
            async for message in context.bot.get_chat_history(chat_id=CHANNEL_ID, limit=6):
                if message.video and message.video.file_id:
                    await query.message.reply_video(
                        video=message.video.file_id,
                        caption=message.caption if message.caption else "Enjoy the video! 🎥"
                    )
            else:
                await query.message.reply_text("No videos found in the channel.")
        except TelegramError as e:
            await query.message.reply_text(f"Error fetching videos: {e.message}")
            logger.error(f"Error fetching videos: {e.message}")

# Main function to run the bot
async def main():
    if not TOKEN:
        logger.error("BOT_TOKEN is not set. Exiting.")
        return

    # Build application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start polling
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
