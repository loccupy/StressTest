from datetime import datetime

from libs.test_settings import initialization


class Configuration:
    filename = "default_name" + str(datetime.now().time().replace(microsecond=0)) + ".txt"  # название файла для записи логов

    serial_number = 0
    password = '1234567898765432'

    base_connect = ["COM3", 9600]  # координаты для оптопорта ведущего счетчика
    emergency_connect = ["COM1", 9600]  # координаты для rs ведущего счетчика

    flag_for_on_off_log = False  # True если нужно считывать журнал, на момент включения должно быть минимум 5 записей
    flag_for_time_correction_log = False  # True если нужно считывать журнал, на момент включения должно быть минимум 4 записей
    flag_for_self_diagnostic_log = False  # True если нужно считывать журнал, на момент включения должно быть минимум 20 записей
    flag_for_read_voltage_for_ozz = False  # True если нужно считывать вольтаж при тестировании ОЗЗ

    sleep_after_disconnect = 0  # Время обязательного ожидания после выключения реле, если 0, то значение будет случайно выбрано из диапазона 5-20 секунд
    sleep_after_reconnect = 0  # Время обязательного ожидания после включения реле, если 0, то значение будет случайно выбрано из диапазона 13-20 секунд

    com_for_1_meter = "COM"
    device_type_for_1_meter = "3PH"

    com_for_2_meter = "COM"
    device_type_for_2_meter = "3PH"

    com_for_3_meter = "COM"
    device_type_for_3_meter = "3PH"

    com_for_4_meter = "COM"
    device_type_for_4_meter = "3PH"

    com_for_5_meter = "COM"
    device_type_for_5_meter = "3PH"

    com_for_6_meter = "COM"
    device_type_for_6_meter = "3PH"

    com_for_7_meter = "COM"
    device_type_for_7_meter = "3PH"


# Подключение к ведущему ведомому счетчику
# @pytest.fixture
def connection_for_leading_meter(com, baud, address, password):
    reader, settings = initialization(com=com, address=16 + address, baud=baud, password=password, ip=None)
    res = [reader, settings]
    return res
    # try:
    #     reader.close()
    # except Exception as e:
    #     print(e)
    #     pass


# Подключение к первому ведомому счетчику
# @pytest.fixture
def connection_for_1_wingman_meter():
    try:
        if Configuration.com_for_1_meter:
            reader, settings = initialization(com=Configuration.com_for_1_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)


# Подключение ко второму ведомому счетчику
# @pytest.fixture
def connection_for_2_wingman_meter():
    try:
        if Configuration.com_for_2_meter:
            reader, settings = initialization(com=Configuration.com_for_2_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)


# Подключение к третьему ведомому счетчику
# @pytest.fixture
def connection_for_3_wingman_meter():
    try:
        if Configuration.com_for_3_meter:
            reader, settings = initialization(com=Configuration.com_for_3_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)


# Подключение к четвертому ведомому счетчику
# @pytest.fixture
def connection_for_4_wingman_meter():
    try:
        if Configuration.com_for_4_meter:
            reader, settings = initialization(com=Configuration.com_for_4_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)


# Подключение ко пятому ведомому счетчику
# @pytest.fixture
def connection_for_5_wingman_meter():
    try:
        if Configuration.com_for_5_meter:
            reader, settings = initialization(com=Configuration.com_for_5_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)


# Подключение к шестому ведомому счетчику
# @pytest.fixture
def connection_for_6_wingman_meter():
    try:
        if Configuration.com_for_6_meter:
            reader, settings = initialization(com=Configuration.com_for_6_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)


# Подключение к седьмому ведомому счетчику
# @pytest.fixture
def connection_for_7_wingman_meter():
    try:
        if Configuration.com_for_7_meter:
            reader, settings = initialization(com=Configuration.com_for_7_meter, address=16, baud=9600,
                                              password='1234567898765432', ip=None)
            res = [reader, settings]
            return res
            # try:
            #     reader.close()
            # except Exception as e:
            #     print(e)
            #     pass
        else:
            return 1
    except Exception as e:
        print(e.args)
