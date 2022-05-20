#### Telegramz

Это простая, незавершенная реализация Telegram Bot API на Python, создана исключительно ради интереса 😊. 

```python

import telegramz

bot = telegramz.Bot(token='token')

@bot.message_handler(commands=['/start', '/help'])
def send_start_help(message):
    bot.send_message(message.chat.id, 'Команда')

@bot.message_handler(func=lambda message:\
                    message.text.lower() in ['привет', 'здравствуйте'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Здравствуйте')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)

bot.run()
```