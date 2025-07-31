from notifiers import get_notifier

from libs.connecting import Configuration


def message_in_out(string):
    try:
        telegram = get_notifier('telegram')
        telegram.notify(message=string,
                        token='7938367301:AAFXCHUuNB3VCuB1Xl7BAISUY7kLpMXAp7o',
                        chat_id=218940403)
    except Exception as e:
        print(f"Невозможно отправить сообщение в телегу, ошибка {e.args}")


def write_file(string):
    try:
        print(string)
        with open(Configuration.filename, "a", errors="ignore", encoding='utf-8') as file:
            file.write(string)
    except Exception as e:
        print(f"Не получилось вывести сообщение в терминал или записать в excel_file, ошибка {e.args}")
