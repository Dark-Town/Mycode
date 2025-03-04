
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your OpenAI API key and Telegram token
OPENAI_API_KEY = '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'
TELEGRAM_TOKEN = '7117516548:AAHK93XIFjv-cdajI0MXIBGck-QhpScBTMs'

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! I am your GPT bot. Type something to get started.')

def gpt_response(prompt: str) -> str:
    """Get a response from the OpenAI GPT model."""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # or 'gpt-4' if you have access
        'messages': [{'role': 'user', 'content': prompt}],
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    # Check for errors in the response
    if response.status_code != 200:
        return "Sorry, I couldn't process your request."
    
    return response.json()['choices'][0]['message']['content']

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages and respond with GPT output."""
    user_message = update.message.text
    bot_reply = gpt_response(user_message)
    update.message.reply_text(bot_reply)

def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
