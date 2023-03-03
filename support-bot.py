import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

# set the username or ID of the channel you want to get the ID for
target_chat_id = int('YOUR INTERNAL SUPPORT CHAT ID')

# replace the token with your bot's token
bot = telebot.TeleBot('YOUR_TOKEN')

# define the custom keyboard
keyboard_main = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
faq_button = KeyboardButton('FAQ')
support_button = KeyboardButton('Support')
keyboard_main.add(faq_button, support_button)

keyboard_faq = ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
faq1_button = KeyboardButton('Question 1?')
faq2_button = KeyboardButton('Question 2?')
faq3_button = KeyboardButton('Question 3?')
main_menu_button = KeyboardButton('Main Menu')
keyboard_faq.add(faq1_button, faq2_button, faq3_button, main_menu_button)

keyboard_back = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
back_button = KeyboardButton('Back')
keyboard_back.add(back_button, main_menu_button)

# define a handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text='Hello, welcome to the Support chat bot of the Market Maker Tools! Please select one of the options below or type directly your message.', reply_markup=keyboard_main)

# define the message handler for the restart command
@bot.message_handler(commands=['restart'])
def handle_restart(message):    
    # set the welcome message adn the main menu keyboard
    bot.send_message(chat_id=message.chat.id, text='Hello, welcome to the Support chat bot of the Market Maker Tools! Please select one of the options below or type directly your message.', reply_markup=keyboard_main)

# define the message handler for the "FAQ" message
@bot.message_handler(func=lambda message: message.text == 'FAQ')
def handle_faq_option(message):
    bot.send_message(chat_id=message.chat.id, text="Select one of the FAQs below to learn more.", reply_markup=keyboard_faq)

# define the message handler for the "FAQ#1" command
@bot.message_handler(func=lambda message: message.text == 'How to login the Market Maker Tools?')
def faq_message(message):
    bot.reply_to(message, "Answer 1.", reply_markup=keyboard_back)

# define the message handler for the "FAQ#2" command
@bot.message_handler(func=lambda message: message.text == 'How to create a new strategy?')
def faq_message(message):
    bot.reply_to(message, "Answer 2.", reply_markup=keyboard_back)    

# define the message handler for the "FAQ#3" command
@bot.message_handler(func=lambda message: message.text == 'How to create a new order?')
def faq_message(message):
    bot.reply_to(message, "Answer 3.", reply_markup=keyboard_back)

@bot.message_handler(func=lambda message: message.text == 'Back')
def handle_back_option(message):
    bot.send_message(chat_id=message.chat.id, text="Select one of the FAQs below to learn more.", reply_markup=keyboard_faq)

@bot.message_handler(func=lambda message: message.text == 'Main Menu')
def handle_main_menu_option(message):
    bot.send_message(chat_id=message.chat.id, text='Hello, welcome to the Support chat bot of the Market Maker Tools! Please select one of the options below or type directly your message.', reply_markup=keyboard_main)

# define the message handler for the "Support" message
@bot.message_handler(func=lambda message: message.text == 'Support')
def handle_support_option(message):
    bot.send_message(chat_id=message.chat.id, text='Type your message directly in the chat.', reply_markup=keyboard_back)

@bot.message_handler(chat_types=["private"])
def forward_message(message: Message):
    # forward the message to the channel
    bot.forward_message(target_chat_id, message.chat.id, message.message_id)

# create a handler function to receive responses from the channel
@bot.message_handler(chat_types=["group"], func=lambda message: message.chat.id == target_chat_id)
def forward_response(message: Message):
    # check if the message was a reply to a message forwarded by the bot
    if message.reply_to_message and message.reply_to_message.forward_from:
        # get the ID of the user who sent the original message
        user_id = message.reply_to_message.forward_from.id
        # send the response back to the user
        bot.send_message(user_id, message.text)

# start the bot
bot.polling()
