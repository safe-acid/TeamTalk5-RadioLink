from config import Config as conf

messages = {
    "help_top": {
        "en": "Radio Selection:\n",
        "ru": "Выбор Радио:\n"
    },
    
    "help": {
        "en": "X: number of station for playing\nadd: add own station URL\nexmple: add RadioFM https://radio.playlist.m3u8\nv25: set volume\nv: about\nq: exit",
        "ru": "X: укажите число, для выбора номера станции\nadd: Добавить свою радиостанцию\nПример: add RadioFM https://radio.playlist.m3u8\nv25: громкость\nv: версия\nq: выход"  
    },
    
    "about": {
        "en": f"RadioLink version: {conf.version}, {conf.sdk} - Котяра 🐾",
        "ru": f"RadioLink version: {conf.version}, {conf.sdk} - Котяра 🐾"
    },  
     
    "info": {
        "en": "\"h\" help",
        "ru": "\"h\" справка"
    },
      
    "vol_set_to": {
        "en": "Volume set to",
        "ru": "Громкость установлена на "
    },
    
     "wrong_volume": {
        "en": f"Invalid volume level. Please use a number from 0 to {conf.max_volume}",
        "ru": f"Неверный уровень громкости. Пожалуйста, используйте число от 0 до {conf.max_volume}"
    },
     
      "wrong_volume_format": {
        "en": f"Invalid volume command format. Use 'v' followed by a number from 0 to {conf.max_volume}",
        "ru": f"Неверный формат команды громкости. Используйте 'v' с числом от 0 до {conf.max_volume}"
    },
      
    "wrong_volume_format": {
        "en": f"Invalid volume command format. Use 'v' followed by a number from 0 to {conf.max_volume}",
        "ru": f"Неверный формат команды громкости. Используйте 'v' с числом от 0 до {conf.max_volume}"
    },
    
    "bot_sleeping": {
        "en": "bot has fallen asleep",
        "ru": "бот уснул"
    },
    
    "requested": {
        "en": "requested",
        "ru": "запросил"
    },
    
    "station":{
        "en": "Station",
        "ru": "Станция"
    },
    
    "error_only_admin":{
        "en": "Error - only administrators can operate this bot",
        "ru": "Ошибка - управлять ботом могут только администраторы"
    },
    "add_url":{
        "en": "Station has been added'",
        "ru": "Радиостанция добавлена'"
    },
     "wrong_url":{
        "en": "Wrong URL",
        "ru": "Неправильная ссылка"
    },
     "wrong_url_command":{
        "en": "Invalid command format. Use: add <name> <url>",
        "ru": "Неправильная команда, используйте: add ИмяСтацнии https://ссылка_на_поток"
    }

}