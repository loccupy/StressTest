import datetime
from time import sleep

from gurux_dlms.objects import GXDLMSDisconnectControl
from libs.write_file import write_file


def relay_reconnect_connect(base_connect, emergency_connect, count, sleep_time_after_disconnect,
                            sleep_time_after_reconnect):
    try:
        relay = GXDLMSDisconnectControl("0.0.96.3.10.255")
        x = 1
        while x <= 3:
            connect = base_connect
            setting = connect[1]
            reader = connect[0]
            try:
                if not setting.media.isOpen():
                    setting.media.open()

                reader.initializeConnection()

                if reader.read(relay, 4) != 2:
                    relay.controlMode = 4
                    reader.write(relay, 4)
                    print('Установлен режим реле 2')

                reader.relay_disconnect()  # вылетает если реле уже разомкнуто ??
                reader.disconnect()
                sleep(sleep_time_after_disconnect)
                reader.initializeConnection()
                reader.relay_reconnect()
                reader.disconnect()
                setting.media.close()
                break
            except Exception as e:
                time = str(datetime.datetime.now())
                write_file(f'>> Неудачное соединения во время дисконнекта-реконнекта реле №{x}!!! \n'
                           f' Ошибка {e.args}\n'
                           f' Реальное время: {time} >> Итерация выкл/вкл №{count}\n\n')
                if x == 3:
                    base_connect, emergency_connect = emergency_connect, base_connect
                    x = 1
                    continue
                x += 1
                sleep(3)
                continue

        sleep(sleep_time_after_reconnect)
    except Exception as e:
        print(f'Ошибка при установке реле {e}')
        raise e
