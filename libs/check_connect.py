from gurux_dlms.objects import GXDLMSDisconnectControl


def check_connect_for_lead_meter(connect, text):
    print(text)
    reader = connect[0]
    settings = connect[1]
    try:
        if not settings.media.isOpen():
            settings.media.open()
        reader.initializeConnection()

        relay = GXDLMSDisconnectControl("0.0.96.3.10.255")
        if reader.read(relay, 4) != 2:
            relay.controlMode = 2
            reader.write(relay, 4)
            print('Установлен режим реле 2')
        reader.relay_disconnect()
        reader.relay_reconnect()

        reader.close()
        print("Соединение корректное")
    except Exception as e:
        settings.media.close()
        if text == "Проверка основного соединения с ведущим счетчиком":
            raise Exception(f'{text} >> Не удается установить соединение с ошибкой {e}. Остановка программы.')
        else:
            print(f'{text} >> Не удается установить соединение с ошибкой {e}. Выполнение программы продолжится.')


def check_connect_for_wingman_meter(connect, com, text):
    if com == "COM":
        print(text, ">> Счетчик не подключен")
        return
    print(text)
    reader = connect[0]
    settings = connect[1]
    try:
        if not settings.media.isOpen():
            settings.media.open()
        reader.initializeConnection()

        relay = GXDLMSDisconnectControl("0.0.96.3.10.255")
        if reader.read(relay, 4) != 2:
            relay.controlMode = 2
            reader.write(relay, 4)
            print('Установлен режим реле 2')
        reader.relay_disconnect()
        reader.relay_reconnect()

        reader.close()
        print(f'{text} >> Соединение корректное')
    except Exception as e:
        settings.media.close()
        raise Exception(f'{text} >> Не удается установить соединение с ошибкой {e}. Остановка программы.')
