import requests
import json

class ConvertDict:
    def __init__(self, dict_: dict):
        self.__dict__.update(dict_)

class Bot:
    URL = 'https://api.telegram.org/bot'

    def __init__(self, token: str):
        self.token = token
        self.message_handler_dict = {'commands': {}, 'func': []}

    def get_updates(self, offset: int=0):
        result = requests.get(f'{self.URL}{self.token}/getUpdates?offset={offset}').json()
        return result['result']

    def send_message(self, chat_id: int, text: str):
        requests.get(f'{self.URL}{self.token}/sendMessage?chat_id={chat_id}&text={text}')

    def message_handler(self, commands: list=[], func=None):
        def wrapper(obj):
            for command in commands:
                self.message_handler_dict['commands'][command] = obj
            if func:
                self.message_handler_dict['func'].append({func: obj})
        return wrapper

    def dict_to_object(self, dict: dict):
        return json.loads(json.dumps(dict), object_hook=ConvertDict)

    def check(self, update):
        if hasattr(update.message, 'text') and hasattr(update.message, 'entities'):
            if (obj := self.message_handler_dict['commands'].get(update.message.text)):
                obj(update.message)
        elif hasattr(update.message, 'text'):
            for func in self.message_handler_dict['func']:
                obj = tuple(func.items())[0]
                if obj[0](update.message):
                    obj[1](update.message)
                    break
                    
    def run(self):
        update_id = 0
        if (_update:=self.get_updates()):
            update_id = _update[-1]['update_id']
        while True:
            updates = self.get_updates(update_id)
            for update in updates:
                if update_id < update['update_id']:
                    update_id = update['update_id']
                    update_obj = self.dict_to_object(update)
                    self.check(update_obj)
