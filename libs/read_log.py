from datetime import datetime
from time import sleep

import pandas as pd

from gurux_dlms.objects import GXDLMSProfileGeneric, GXDLMSRegister

from libs.connecting import Configuration


def read_voltage_of_any_phase_for_ozz(reader):
    try:
        if Configuration.flag_for_read_voltage_for_ozz:
            data = GXDLMSRegister('1.0.72.7.0.255')
            array_for_check = []
            result_array = []
            for i in range(5):
                value = reader.read(data, 2)
                array_for_check.append(value)
                result_array.append([datetime.now().time().replace(microsecond=0), value])
                sleep(3)

            headings = ["Время считывания", "Значение напряжения"]
            index = ["1", "2", "3", "4", "5"]
            df = pd.DataFrame(result_array, columns=headings, index=index)

            res = set(i for i in array_for_check)
            if len(res) == 5:
                return f"   Метрологический чип функционирует!\n\n{df}"
            elif (array_for_check[0] == array_for_check[1] == array_for_check[2] == array_for_check[3] or
                  array_for_check[0] == array_for_check[1] == array_for_check[2] == array_for_check[3]
                  == array_for_check[4]):
                return f"   Обнаружено возможное зависание метрологического чипа!\n\n{df}"
            else:
                return f"   Обнаружены повторения значений, возможно зависание метрологического чипа!\n\n{df}"
        else:
            return "Считывание напряжения выключено"
    except Exception as e:
        print(f"Невозможно считать журнал напряжения, ошибка {e.args}")


def read_self_diagnostic_logs(reader_for_tt):
    try:
        if Configuration.flag_for_self_diagnostic_log:
            pg = GXDLMSProfileGeneric("0.0.99.98.7.255")
            reader_for_tt.read(pg, 3)
            entries_in_use = reader_for_tt.read(pg, 7)
            logs = reader_for_tt.readRowsByEntry(pg, entries_in_use - 19, 20)
            res = []
            for i in range(len(logs)):
                res.append([logs[i][0].toFormatString(), logs[i][1], logs[i][2]])
            headings = ["Время фиксации записи", "Событие самодиагностики", " Время работы ПУ"]
            index = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
                     "12", "13", "14", "15", "16", "17", "18", "19", "20"]
            df = pd.DataFrame(res, columns=headings, index=index)
            return df
        else:
            return "Считывание журнала выключено"
    except Exception as e:
        print(f"Невозможно считать журнал самодиагностики, ошибка {e.args}")


def reset_on_off_log(reader):
    try:
        reader.reset_profile("0.0.99.98.2.255")
    except Exception as e:
        print(f"Невозможно очистить журнал вкл/выкл, ошибка {e.args}")


def read_on_off_log(reader_for_tt):
    try:
        if Configuration.flag_for_on_off_log:
            pg = GXDLMSProfileGeneric("0.0.99.98.2.255")
            reader_for_tt.read(pg, 3)
            entries_in_use = reader_for_tt.read(pg, 7)
            logs = reader_for_tt.readRowsByEntry(pg, entries_in_use - 4, 5)
            res = []
            for i in range(len(logs)):
                res.append([logs[i][0].toFormatString(), logs[i][1], logs[i][2]])
            headings = ["Время фиксации записи", "Событие", "Время работы ПУ"]
            index = ["1", "2", "3", "4", "5"]
            df = pd.DataFrame(res, columns=headings, index=index)
            # reset_on_off_log(reader_for_tt) # при включении резет надо переделать на считывание 2-х записей
            return df
        else:
            return "Считывание журнала выключено"
    except Exception as e:
        print(f"Невозможно считать журнал вкл/выкл, ошибка {e.args}")


def read_time_correction_log(reader):
    try:
        if Configuration.flag_for_time_correction_log:
            pg = GXDLMSProfileGeneric("0.0.99.98.13.255")
            reader.read(pg, 3)
            entries_in_use = reader.read(pg, 7)
            logs = reader.readRowsByEntry(pg, entries_in_use - 3, 4)
            res = []
            for i in range(len(logs)):
                res.append([logs[i][0].toFormatString(), logs[i][1], logs[i][2]])
            headings = ["Текущие дата и время", "Старое время", "Время работы ПУ"]
            index = ["1", "2", "3", "4"]
            df = pd.DataFrame(res, columns=headings, index=index)
            return df
        else:
            return "Считывание журнала выключено"
    except Exception as e:
        print(f"Невозможно считать журнал коррекции времени, ошибка {e.args}")
