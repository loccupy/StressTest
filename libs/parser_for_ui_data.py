from libs.connecting import Configuration


def parser_for_ui_data(all_data):
    # Сброс всех ведомых счетчиков к значениям по умолчанию перед загрузкой новых.
    # Без этого при снятии галочки N-го счетчика Configuration.com_for_N_meter
    # сохраняло бы старое значение, и Worker.run() считал бы его включённым
    # (bug: неочищенное состояние).
    for n in range(1, 7):
        setattr(Configuration, f"com_for_{n}_meter", "COM")
        setattr(Configuration, f"device_type_for_{n}_meter", "3PH")

    # Получение данных ведомых счетчиков (1–6)
    labels = ["Включить 1-ый ведомый счетчик", "Включить 2-ый ведомый счетчик", "Включить 3-ый ведомый счетчик",
              "Включить 4-ый ведомый счетчик", "Включить 5-ый ведомый счетчик", "Включить 6-ый ведомый счетчик"]

    meter_data = all_data['meter_data']
    meter_com_ports = [meter_data[label]['com_port'] for label in labels]
    meter_types = [meter_data[label]['type'] for label in labels]

    # Получение данных журналов
    log_checkboxes = ["Журнал диагностики", "Журнал вкл/выкл", "Журнал коррекции времени", "Журнал напряжения"]

    diagnostic_log_enabled = all_data['log_data'][log_checkboxes[0]]
    on_off_log_enabled = all_data['log_data'][log_checkboxes[1]]
    time_log_enabled = all_data['log_data'][log_checkboxes[2]]
    voltage_log_enabled = all_data['log_data'][log_checkboxes[3]]

    # Получение конфигурации соединений
    serial_number = all_data['config_data']['id']['serial']
    password = all_data['config_data']['id']['password']
    speed_main_connection = all_data['config_data']['main_connection']['speed']
    com_main_connection = all_data['config_data']['main_connection']['com_port']
    speed_aux_connection = all_data['config_data']['auxiliary_connection']['speed']
    com_aux_connection = all_data['config_data']['auxiliary_connection']['com_port']

    # Получение времени отключения/подключения
    if "-" in all_data['time_data']['disconnect_time']:
        res_1 = all_data['time_data']['disconnect_time'].split("-")[0]
        res_2 = all_data['time_data']['disconnect_time'].split("-")[1]
        disconnect_time_data = [res_1, res_2]
    elif all_data['time_data']['disconnect_time'] == '':
        disconnect_time_data = ''
    else:
        disconnect_time_data = int(all_data['time_data']['disconnect_time'])

    if "-" in all_data['time_data']['connect_time']:
        res_1 = all_data['time_data']['connect_time'].split("-")[0]
        res_2 = all_data['time_data']['connect_time'].split("-")[1]
        connect_time_data = [res_1, res_2]
    elif all_data['time_data']['connect_time'] == '':
        connect_time_data = ''
    else:
        connect_time_data = int(all_data['time_data']['connect_time'])

    # connect_time_data = all_data['time_data']['connect_time']

    # Получение имени файла
    file_name = all_data['file_name']

    # Переписываем данные в классе
    if file_name != '':
        Configuration.filename = file_name

    if disconnect_time_data != '':
        Configuration.sleep_after_disconnect = disconnect_time_data
    if connect_time_data != '':
        Configuration.sleep_after_reconnect = connect_time_data

    if serial_number != '':
        Configuration.serial_number = int(serial_number)
    if password != '':
        Configuration.password = password
    if com_main_connection != 'COM':
        Configuration.base_connect[0] = com_main_connection
    if speed_main_connection != '':
        Configuration.base_connect[1] = int(speed_main_connection)
    if com_aux_connection != 'COM':
        Configuration.emergency_connect[0] = com_aux_connection
    if speed_aux_connection != '':
        Configuration.emergency_connect[1] = int(speed_aux_connection)

    Configuration.flag_for_on_off_log = on_off_log_enabled
    Configuration.flag_for_time_correction_log = time_log_enabled
    Configuration.flag_for_self_diagnostic_log = diagnostic_log_enabled
    Configuration.flag_for_read_voltage_for_ozz = voltage_log_enabled

    # Ведомые счетчики 1–6 — цикл вместо шести повторяющихся блоков
    for idx in range(6):
        n = idx + 1
        com_port = meter_com_ports[idx]
        meter_type = meter_types[idx]
        if com_port != 'COM':
            setattr(Configuration, f"com_for_{n}_meter", com_port)
        if meter_type != '':
            setattr(Configuration, f"device_type_for_{n}_meter", meter_type)

    # return conf
