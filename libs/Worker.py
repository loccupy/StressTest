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

            i_1 = 0
            i_2 = 0
            i_3 = 0
            i_4 = 0
            i_5 = 0
            i_6 = 0
            i_7 = 0

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

            connection_for_1_meter = connection_for_1_wingman_meter()
            check_connect_for_wingman_meter(connection_for_1_meter, Configuration.com_for_1_meter,
                                            "Проверка соединения с первым счетчиком")
            connection_for_2_meter = connection_for_2_wingman_meter()
            check_connect_for_wingman_meter(connection_for_2_meter, Configuration.com_for_2_meter,
                                            "Проверка соединения со вторым счетчиком")
            connection_for_3_meter = connection_for_3_wingman_meter()
            check_connect_for_wingman_meter(connection_for_3_meter, Configuration.com_for_3_meter,
                                            "Проверка соединения с третьим счетчиком")
            connection_for_4_meter = connection_for_4_wingman_meter()
            check_connect_for_wingman_meter(connection_for_4_meter, Configuration.com_for_4_meter,
                                            "Проверка соединения с четвертым счетчиком")
            connection_for_5_meter = connection_for_5_wingman_meter()
            check_connect_for_wingman_meter(connection_for_5_meter, Configuration.com_for_5_meter,
                                            "Проверка соединения с пятым счетчиком")
            connection_for_6_meter = connection_for_6_wingman_meter()
            check_connect_for_wingman_meter(connection_for_6_meter, Configuration.com_for_6_meter,
                                            "Проверка соединения с шестым счетчиком")
            # connection_for_7_meter = connection_for_7_wingman_meter()

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

                if Configuration.com_for_1_meter != "COM":
                    # подключение к первому счетчику

                    i_1 = main_loop(connection_for_1_meter, i_1, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "ПЕРВЫЙ", Configuration.device_type_for_1_meter)

                if self.running is False:
                    print("Тест остановлен.")
                    break

                if Configuration.com_for_2_meter != "COM":
                    # отсчитываем время после реконнекта для второго счетчика
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # подключение ко второму счетчику
                    i_2 = main_loop(connection_for_2_meter, i_2, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "ВТОРОЙ", Configuration.device_type_for_2_meter)

                if self.running is False:
                    print("Тест остановлен.")
                    break

                if Configuration.com_for_3_meter != "COM":
                    # отсчитываем время после реконнекта для третьего счетчика
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # подключение к третьему счетчику
                    i_3 = main_loop(connection_for_3_meter, i_3, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "ТРЕТИЙ", Configuration.device_type_for_3_meter)

                if self.running is False:
                    print("Тест остановлен.")
                    break

                if Configuration.com_for_4_meter != "COM":
                    # отсчитываем время после реконнекта для четвертого счетчика
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # подключение к четвертому счетчику
                    i_4 = main_loop(connection_for_4_meter, i_4, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "ЧЕТВЕРТЫЙ", Configuration.device_type_for_4_meter)

                if self.running is False:
                    print("Тест остановлен.")
                    break

                if Configuration.com_for_5_meter != "COM":
                    # отсчитываем время после реконнекта для ПЯТОГО счетчика
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # подключение ко пятому счетчику
                    i_5 = main_loop(connection_for_5_meter, i_5, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "ПЯТЫЙ", Configuration.device_type_for_5_meter)

                if self.running is False:
                    print("Тест остановлен.")
                    break

                if Configuration.com_for_6_meter != "COM":
                    # отсчитываем время после реконнекта для ШЕСТОГО счетчика
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # подключение к шестому счетчику
                    i_6 = main_loop(connection_for_6_meter, i_6, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "ШЕСТОЙ", Configuration.device_type_for_6_meter)

                if self.running is False:
                    print("Тест остановлен.")
                    break

                if Configuration.com_for_7_meter != "COM":
                    # отсчитываем время после реконнекта для СЕДЬМОГО счетчика
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    sleep_time_after_reconnect = original_time_after_reconnect + int(elapsed_time)

                    # подключение к седьмому счетчику
                    i_7 = main_loop(connection_for_7_wingman_meter, i_7, count, sleep_time_after_disconnect,
                                    sleep_time_after_reconnect, "СЕДЬМОЙ", Configuration.device_type_for_7_meter)

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
