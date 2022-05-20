import requests
import json

class obj:
    def __init__(self, dict_: dict):
        self.__dict__.update(dict_)

class TelegramBot:
    URL = 'https://api.telegram.org/bot'

    def __init__(self, token: str):
        self.token = token
        self.message_handler_dict = {'commands':{}}

    def get_updates(self, offset: int=0):
        result = requests.get(f'{self.URL}{self.token}/getUpdates?offset={offset}').json()
        return result['result']

    def send_message(self, chat_id: int, text: str):
        requests.get(f'{self.URL}{self.token}/sendMessage?chat_id={chat_id}&text={text}')

    def message_handler(self, commands: list):
        def wrapper(func):
            for command in commands:
                self.message_handler_dict['commands'][command] = func
        return wrapper

    def dict2obj(self, dict: dict):
        return json.loads(json.dumps(dict), object_hook=obj)

    def run(self):
        update_id = 0
        if (_update:=self.get_updates()):
            update_id = _update[-1]['update_id']
        while True:
            updates = self.get_updates(update_id)
            for update in updates:
                if update_id < update['update_id']:
                    update_id = update['update_id']
                    update_obj = self.dict2obj(update)
                    #command
                    print(self.message_handler_dict)
                    if hasattr(update_obj.message, 'text') and hasattr(update_obj.message, 'entities'):
                        if (func := self.message_handler_dict['commands'].get(update_obj.message.text)):
                            func(update_obj.message)

bot = TelegramBot(token='Token')

@bot.message_handler(commands=['/start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'start')

@bot.message_handler(commands=['/help'])
def send_welcome2(message):
    bot.send_message(message.chat.id, 'help')

bot.run()