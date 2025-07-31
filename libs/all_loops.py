import datetime
from time import sleep

# from eventlet import Timeout

from libs.read_log import (read_time_correction_log, read_self_diagnostic_logs,
                           read_on_off_log, read_voltage_of_any_phase_for_ozz)
from libs.write_file import write_file, message_in_out


def loop_after_exception(count, connect, counter_number, device_type):
    number = counter_number
    i = 1
    res = connect
    setting = res[1]
    reader = res[0]
    while i < 12:
        # timeout_2 = Timeout(5, Exception)
        try:
            if not setting.media.isOpen():
                setting.media.open()
            reader.initializeConnection()
            assert reader.deviceType == device_type
            sleep(10)
            time_correction_log = read_time_correction_log(reader)
            self_diagnostic_logs = read_self_diagnostic_logs(reader)
            check_phase_for_ozz = read_voltage_of_any_phase_for_ozz(reader)
            on_off_logs = read_on_off_log(reader)
            time_for_success = str(datetime.datetime.now().replace(microsecond=0))

            write_file(f'>> Удачное соединение после {i}-го неудачного c № {number} \n'
                       f' Реальное время: {time_for_success} >> Итерация выкл/вкл №{count}\n'
                       f' Считываем логи журнала самодиагностики после ожидания в 10 сек\n'
                       f' _________________SELF_DIAGNOSTIC_LOGS_________________________________\n '
                       f'{self_diagnostic_logs}\n\n'
                       f' _________________CHECK VOLTAGE PHASE C_________________________________\n '
                       f'{check_phase_for_ozz}\n\n'
                       f' ____________________ON/OFF_ACTIVITIES_________________________________\n '
                       f'{on_off_logs}\n\n'
                       f' ____________________TIME CORRECTION LOG_________________________________\n '
                       f'{time_correction_log}\n'
                       f'_______________________________________________________________________\n\n\n\n'
                       )

            message_in_out(
                f'>> Удачное соединение после {i}-го неудачного. Реальное время: {time_for_success}')

            try:
                reader.close()
            except Exception as e:
                print(e.args)
                return i
            break
        except Exception as e:
            i += 1
            if i == 5:
                time_5 = str(datetime.datetime.now().replace(microsecond=0))
                error_5 = e.args

                write_file(f'>> Долгий старт ИПУ!\n Неудачное соединение №{i} со счетчиком № {counter_number}\n'
                           f' С ошибкой {error_5} \n'
                           f' Реальное время: {time_5} >> Итерация выкл/вкл №{count}\n\n')

                message_in_out(
                    f'Долгий старт ИПУ\n Ошибка >> {error_5} в {time_5}\n Итерация выкл/вкл №{count}')

            elif i == 10:
                time_10 = str(datetime.datetime.now().replace(microsecond=0))
                error_10 = e.args

                write_file(f'>> Зависание ИПУ\n Неудачное соединение №{i} со счетчиком № {counter_number}\n'
                           f' C ошибкой >> {error_10}\n'
                           f' Реальное время: {time_10} >> Итерация вкл/выкл №{count}\n'
                           f' Будет произведена еще одна попытка подключения, в случае неудачи - переход на цикл '
                           f'выкл/вкл \n\n')

                message_in_out(
                    f'Зависание ИПУ\n Ошибка >> {error_10} в {time_10}\n Итерация выкл/вкл №{count}')
            continue
        # finally:
        #     timeout_2.cancel()
    return i


def slave_counter_loop(connect, i, count, sleep_time_after_disconnect,
                       sleep_time_after_reconnect, counter_number, device_type):
    res = connect
    setting = res[1]
    reader = res[0]
    if i == 12:
        sleep(10)
        if not setting.media.isOpen():
            setting.media.open()
        reader.initializeConnection()
        assert reader.deviceType == device_type
        time_correction_log = read_time_correction_log(reader)
        self_diagnostic_logs = read_self_diagnostic_logs(reader)
        check_phase_for_ozz = read_voltage_of_any_phase_for_ozz(reader)
        on_off_logs = read_on_off_log(reader)
        time_for_success = str(datetime.datetime.now().replace(microsecond=0))

        write_file(f'>> Соединение с ведомым счетчиком № {counter_number} установлено!!! \n'
                   f' Реальное время: {time_for_success} >> Итерация выкл/вкл №{count}\n'
                   f' Время ожидания после дисконнекта >> {sleep_time_after_disconnect}\n'
                   f' Время ожидания после реконнекта >> {sleep_time_after_reconnect}\n'
                   f' Считываем логи журнала самодиагностики после ожидания в 10 сек (после цикла в 11 '
                   f'неудачных подключений)\n'
                   f'_________________SELF_DIAGNOSTIC_LOGS_________________________________\n '
                   f'{self_diagnostic_logs}\n\n'
                   f' _________________CHECK VOLTAGE PHASE C_________________________________\n '
                   f'{check_phase_for_ozz}\n\n'
                   f' ____________________ON/OFF_ACTIVITIES_________________________________\n '
                   f'{on_off_logs}\n\n'
                   f' ____________________TIME CORRECTION LOG_________________________________\n '
                   f'{time_correction_log}\n'
                   f'_______________________________________________________________________\n\n\n\n'
                   )
        i = 0
        reader.disconnect()
        setting.media.close()
    else:
        if not setting.media.isOpen():
            setting.media.open()
        reader.initializeConnection()
        if reader.deviceType != device_type:
            write_file(f'>> ТИП СЧЕТЧИКА НЕ СООТВЕТСТВУЕТ\n'
                       f'___________________________________________________________\n\n')
            reader.close()
            raise Exception("ТИП СЧЕТЧИКА НЕ СООТВЕТСТВУЕТ")

        time_correction_log = read_time_correction_log(reader)
        on_off_logs = read_on_off_log(reader)
        self_diagnostic_logs = read_self_diagnostic_logs(reader)
        check_phase_for_ozz = read_voltage_of_any_phase_for_ozz(reader)
        time_for_success = str(datetime.datetime.now().replace(microsecond=0))

        write_file(f'>> Соединение с ведомым счетчиком № {counter_number} установлено!!! \n'
                   f' Реальное время: {time_for_success} >> Итерация выкл/вкл №{count}\n'
                   f' Время ожидания после дисконнекта >> {sleep_time_after_disconnect}\n'
                   f' Время ожидания после реконнекта >> {sleep_time_after_reconnect}\n'
                   f' _________________SELF_DIAGNOSTIC_LOGS_________________________________\n '
                   f'{self_diagnostic_logs}\n\n'
                   f' _________________CHECK VOLTAGE PHASE C_________________________________\n '
                   f'{check_phase_for_ozz}\n\n'
                   f' ____________________ON/OFF_ACTIVITIES_________________________________\n '
                   f'{on_off_logs}\n\n'
                   f' ____________________TIME CORRECTION LOG_________________________________\n '
                   f'{time_correction_log}\n'
                   f'_______________________________________________________________________\n\n\n\n'
                   )

        reader.close()
        return i


def main_loop(connect, i, count, sleep_time_after_disconnect, sleep_time_after_reconnect, counter_number, device_type):
    try:
        i = slave_counter_loop(connect, i, count, sleep_time_after_disconnect, sleep_time_after_reconnect,
                               counter_number,
                               device_type)
    except Exception as e:
        error_1 = e.args

        time_1 = str(datetime.datetime.now().replace(microsecond=0))
        write_file(f'ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM!'
                   f' ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM!'
                   f' ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! ALARM! \n'
                   f'>> Соединение с ведомым счетчиком № {counter_number} не установлено!!!\n'
                   f' Ошибка >> {error_1}. Попытка подключения № 1  \n'
                   f' Реальное время: {time_1} >> Итерация выкл/вкл №{count}\n'
                   f' Время ожидания после дисконнекта >> {sleep_time_after_disconnect}\n'
                   f' Время ожидания после реконнекта >> {sleep_time_after_reconnect}\n\n')

        if error_1 == ('ТИП СЧЕТЧИКА НЕ СООТВЕТСТВУЕТ',):
            raise Exception(f'ТИП СЧЕТЧИКА <<{counter_number}>> НЕ СООТВЕТСТВУЕТ. ОСТАНОВКА ТЕСТА!')

        message_in_out(
            f'Соединение не установлено!Ошибка >> {error_1}\n Реальное время: {time_1}\n Итерация выкл/вкл №{count}')

        i = loop_after_exception(count, connect, counter_number, device_type)
    return i
