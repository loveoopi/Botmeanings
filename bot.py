import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError
import asyncio

# Replace with your bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with the token from BotFather
# Replace with your channel ID (e.g., "@YourChannelName" or chat ID for private channels)
CHANNEL_ID = "https://t.me/share/url?url=%20JOIN%20THIS%20AMAZING%20GROUP%20%F0%9F%A5%B5%20-%20https%3A%2F%2Ft.me/DESIGNBYKINGBOT"  # Replace with your channel's username or ID
# Replace with the force-join channel link
FORCE_JOIN_LINK = "https://t.me/+JlERJvczl-k2OWJl"
# Replace with the share link
SHARE_LINK = "https://t.me/share/url?url=%20JOIN%20THIS%20AMAZING%20GROUP%20%F0%9F%A5%B5%20-%20https%3A%2F%2Ft.me/DESIGNBYKINGBOT"

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
            messages = await context.bot.get_chat_history(chat_id=CHANNEL_ID, limit=6)  # Adjust limit to 5-6 videos
            video_count = 0
            for message in messages:
                if message.video and video_count < 6:  # Check for video and limit to 6
                    await query.message.reply_video(
                        video=message.video.file_id,
                        caption=message.caption if message.caption else "Enjoy the video! 🎥"
                    )
                    video_count += 1
            if video_count == 0:
                await query.message.reply_text("No videos found in the channel.")
        except TelegramError as e:
            await query.message.reply_text(f"Error fetching videos: {e.message}")
            logger.error(f"Error fetching videos: {e.message}")

# Main function to run the bot
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
