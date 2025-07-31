from libs.connecting import Configuration


def parser_for_ui_data(all_data):
    # Получение данных счетчиков
    labels = ["Включить 1-ый ведомый счетчик", "Включить 2-ый ведомый счетчик", "Включить 3-ый ведомый счетчик",
              "Включить 4-ый ведомый счетчик", "Включить 5-ый ведомый счетчик", "Включить 6-ый ведомый счетчик"]

    # meter1_enabled = all_data['meter_data'][labels[0]]['enabled']
    meter1_com_port = all_data['meter_data'][labels[0]]['com_port']
    meter1_type = all_data['meter_data'][labels[0]]['type']

    # meter2_enabled = all_data['meter_data'][labels[1]]['enabled']
    meter2_com_port = all_data['meter_data'][labels[1]]['com_port']
    meter2_type = all_data['meter_data'][labels[1]]['type']

    # meter3_enabled = all_data['meter_data'][labels[2]]['enabled']
    meter3_com_port = all_data['meter_data'][labels[2]]['com_port']
    meter3_type = all_data['meter_data'][labels[2]]['type']

    # meter4_enabled = all_data['meter_data'][labels[3]]['enabled']
    meter4_com_port = all_data['meter_data'][labels[3]]['com_port']
    meter4_type = all_data['meter_data'][labels[3]]['type']

    # meter5_enabled = all_data['meter_data'][labels[4]]['enabled']
    meter5_com_port = all_data['meter_data'][labels[4]]['com_port']
    meter5_type = all_data['meter_data'][labels[4]]['type']

    # meter6_enabled = all_data['meter_data'][labels[5]]['enabled']
    meter6_com_port = all_data['meter_data'][labels[5]]['com_port']
    meter6_type = all_data['meter_data'][labels[5]]['type']

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

    if meter1_com_port != 'COM':
        Configuration.com_for_1_meter = meter1_com_port
    if meter1_type != '':
        Configuration.device_type_for_1_meter = meter1_type

    if meter2_com_port != 'COM':
        Configuration.com_for_2_meter = meter2_com_port
    if meter2_type != '':
        Configuration.device_type_for_2_meter = meter2_type

    if meter3_com_port != 'COM':
        Configuration.com_for_3_meter = meter3_com_port
    if meter3_type != '':
        Configuration.device_type_for_3_meter = meter3_type

    if meter4_com_port != 'COM':
        Configuration.com_for_4_meter = meter4_com_port
    if meter4_type != '':
        Configuration.device_type_for_4_meter = meter4_type

    if meter5_com_port != 'COM':
        Configuration.com_for_5_meter = meter5_com_port
    if meter5_type != '':
        Configuration.device_type_for_5_meter = meter5_type

    if meter6_com_port != 'COM':
        Configuration.com_for_6_meter = meter6_com_port
    if meter6_type != '':
        Configuration.device_type_for_6_meter = meter6_type

    # return conf
