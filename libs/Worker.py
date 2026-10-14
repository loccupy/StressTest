import datetime
import time

from PyQt5.QtCore import QThread, pyqtSignal

from libs.all_loops import main_loop
from libs.check_connect import check_connect_for_lead_meter, check_connect_for_wingman_meter
from libs.connecting import *
from libs.parser_for_ui_data import parser_for_ui_data
from libs.relay_reconnect_connect import relay_reconnect_connect
from libs.time_for_connect_relay import *
from libs.write_file import write_file, message_in_out


class Worker(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.input_data = None
        self.running = True

    def set_input_data(self, data):
        self.input_data = data

    def run(self):
        self.running = True

        count = 1
        try:
            parser_for_ui_data(self.input_data)

            # Список состояний i для ведомых счётчиков (1–6)
            i_values = [0] * 7  # i_values[n] — состояние i для n-го счётчика

            base_connection_for_lead_meter = connection_for_leading_meter(Configuration.base_connect[0],
                                                                          Configuration.base_connect[1],
                                                                          Configuration.serial_number,
                                                                          Configuration.password)
            check_connect_for_lead_meter(base_connection_for_lead_meter,
                                         "Проверка основного соединения с ведущим счетчиком")

            emergency_connection_for_lead_meter = connection_for_leading_meter(Configuration.emergency_connect[0],
                                                                               Configuration.emergency_connect[1],
                                                                               Configuration.serial_number,
                                                                               Configuration.password)
            check_connect_for_lead_meter(emergency_connection_for_lead_meter,
                                         "Проверка запасного соединения с ведущим счетчиком")

            # Подключение и проверка ведомых счётчиков
            wingman_connections = []  # [(connect_result, com_attr, device_type), ...]
            ordinal_names = ["", "ПЕРВЫЙ", "ВТОРОЙ", "ТРЕТИЙ", "ЧЕТВЕРТЫЙ", "ПЯТЫЙ", "ШЕСТОЙ"]
            # Дательный падеж для текста проверки соединения (как в оригинале)
            check_names = ["", "первым", "вторым", "третьим", "четвертым", "пятым", "шестым"]
            for meter_num in range(1, 7):
                com_attr = f"com_for_{meter_num}_meter"
                device_type_attr = f"device_type_for_{meter_num}_meter"
                if getattr(Configuration, com_attr) == "COM":
                    wingman_connections.append((None, None, None))  # пропуск незаданного
                    continue
                connect_res = connection_for_wingman_meter(getattr(Configuration, com_attr))
                check_connect_for_wingman_meter(connect_res, getattr(Configuration, com_attr),
                                                f"Проверка соединения с {check_names[meter_num]} счетчиком")
                device_type = getattr(Configuration, device_type_attr)
                wingman_connections.append((connect_res, com_attr, device_type))

            with open(Configuration.filename, "a", errors="ignore") as file:
                file.write(
                    f'***************NEW TEST in {str(datetime.now().replace(microsecond=0))}***************\n\n')

            while self.running:
                if self.running is False:
                    print("Тест остановлен.")
                    break

                sleep_time_after_disconnect = time_for_sleep_after_disconnect()
                sleep_time_after_reconnect = time_for_sleep_after_reconnect()

                original_time_after_reconnect = sleep_time_after_reconnect

                # дисконнект-реконнект ведущего счетчика
                relay_reconnect_connect(base_connection_for_lead_meter, emergency_connection_for_lead_meter, count,
                                        sleep_time_after_disconnect, sleep_time_after_reconnect)

                start_time = time.time()

                if self.running is False:
                    print("Тест остановлен.")
                    break

                # Цикл по ведомым счётчикам (1–6)
                for meter_num in range(1, 7):
                    conn_res, com_attr, device_type = wingman_connections[meter_num - 1]
                    if conn_res is None:
                        # счётчик не задан — пропускаем
                        continue

                    # отсчитываем время после реконнекта
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # цикл main_loop для счётчика
                    i_values[meter_num] = main_loop(conn_res, i_values[meter_num], count,
                                                    sleep_time_after_disconnect,
                                                    sleep_time_after_reconnect,
                                                    ordinal_names[meter_num], device_type)

                    if self.running is False:
                        print("Тест остановлен.")
                        break

                if self.running is False:
                    print("Тест остановлен.")
                    break

                count += 1
                # self.signal.emit("Тест выполняется...\n")
                if self.running is False:
                    print("Тест остановлен.")
                    break
                self.msleep(1000)  # Задержка в 1 секунду
                continue
        except Exception as x:
            time_end = str(datetime.now().replace(microsecond=0))
            error_end = x.args
            write_file(f' Неуважительная ошибка >> {error_end}\n'
                       f' Реальное время: {time_end} >> Итерация вкл/выкл №{count}\n')
            message_in_out(f'Неуважительная ошибка {error_end} в {time_end}')

    def stop(self):
        self.running = False
        print("Тест скоро остановится...")
