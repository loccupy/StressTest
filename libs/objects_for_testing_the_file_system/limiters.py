from libs.objects_for_testing_the_file_system.range_of_values import RangeOfValues

from gurux_dlms.objects import GXDLMSRegister, GXDLMSLimiter
from gurux_dlms import GXUInt8
from random import randint


class Limiters:

    def __init__(self, obis, meter_type):
        self.obis = obis
        self.recorded_values = {
            "normal_threshold": None,
            "threshold_duration_min_over": None,
            "threshold_duration_min_under": None,
        }
        self.read_values = {
            "normal_threshold": None,
            "threshold_duration_min_over": None,
            "threshold_duration_min_under": None,
        }
        self.data = GXDLMSLimiter(obis)
        self.threshold_duration_min_over = RangeOfValues.THRESHOLD_DURATION_MIN_OVER.value
        self.threshold_duration_min_under = RangeOfValues.THRESHOLD_DURATION_MIN_UNDER.value
        if obis == "0.0.17.0.0.255":
            self.name = "Ограничитель мощности"
            self.data_type = RangeOfValues.POWER_DATA_TYPE.value
            if meter_type == "1PH":
                self.normal_threshold = RangeOfValues.POWER_NORMAL_THRESHOLD_1PH.value
            else:
                self.normal_threshold = RangeOfValues.POWER_NORMAL_THRESHOLD_3PH.value
        elif obis == "0.0.17.0.1.255":
            self.name = "Ограничитель тока"
            self.data_type = RangeOfValues.CURRENT_DATA_TYPE.value
            self.normal_threshold = RangeOfValues.CURRENT_NORMAL_THRESHOLD.value
        elif obis == "0.0.17.0.2.255":
            self.name = "Ограничитель напряжения"
            self.data_type = RangeOfValues.VOLTAGE_DATA_TYPE.value
            self.normal_threshold = RangeOfValues.VOLTAGE_NORMAL_THRESHOLD.value
        elif obis == "0.0.17.0.3.255":
            self.name = "Ограничитель по магнитному полю"
            self.data_type = RangeOfValues.MAGNETIC_DATA_TYPE.value
            self.normal_threshold = RangeOfValues.MAGNETIC_NORMAL_THRESHOLD.value
        elif obis == "0.0.17.0.4.255":
            self.name = "Ограничитель по не балансу токов"
            self.data_type = RangeOfValues.IMBALANCE_DATA_TYPE.value
            self.normal_threshold = RangeOfValues.IMBALANCE_NORMAL_THRESHOLD.value
        else: # obis == "0.0.17.0.5.255":
            self.name = "Ограничитель по температуре"
            self.data_type = RangeOfValues.TEMPERATURE_DATA_TYPE.value
            self.normal_threshold = RangeOfValues.TEMPERATURE_NORMAL_THRESHOLD.value

    def read_normal_threshold(self, reader):
        data = self.data
        result = reader.read(data, 4)
        self.read_values["normal_threshold"] = result

    def read_threshold_duration_min_over(self, reader):
        data = self.data
        result = reader.read(data, 6)
        self.read_values["threshold_duration_min_over"] = result

    def read_threshold_duration_min_under(self, reader):
        data = self.data
        result = reader.read(data, 7)
        self.read_values["threshold_duration_min_under"] = result

    def set_normal_threshold(self, reader):
        data = self.data
        data_type = self.data_type

        value = self._get_random_value(4)

        if self.obis == "0.0.17.0.1.255":
            data_register = GXDLMSRegister("1.0.11.134.0.255")
            reader.read(data_register, 2)
            data_register.value = GXUInt8(value)
            reader.write(data_register, 2)
            actual_result = reader.read(data_register, 2)

            if actual_result == value:
                print(f"Уровень лимита по току установлено на {value}%.\n")

            actual_normal_threshold = reader.read(data, 4)
            self.recorded_values["normal_threshold"] = actual_normal_threshold
            maximum_current = reader.read(GXDLMSRegister("1.0.0.6.3.255"), 2)
            expected = maximum_current * value / 100

            if actual_normal_threshold == expected:
                print(f"Normal_Threshold для {self.name} установлено на {actual_normal_threshold}")
            else:
                print(f"Normal_Threshold для {self.name} = {actual_normal_threshold} не совпало с ожидаемым {expected} (процент={value}% от макс. тока {maximum_current})")

        elif self.obis == "0.0.17.0.2.255":
            data_register = GXDLMSRegister("1.0.12.134.0.255")
            reader.read(data_register, 2)
            data_register.value = GXUInt8(value)
            reader.write(data_register, 2)
            actual_result = reader.read(data_register, 2)

            if actual_result == value:
                print(f"Уровень лимита по напряжению установлено на {value}%.\n")

            actual_normal_threshold = reader.read(data, 4)
            self.recorded_values["normal_threshold"] = actual_normal_threshold
            nominal_voltage = reader.read(GXDLMSRegister("1.0.0.6.0.255"), 2)
            expected = nominal_voltage * value / 100

            if actual_normal_threshold == expected:
                print(f"Normal_Threshold для {self.name} установлено на {actual_normal_threshold}")
            else:
                print(f"Normal_Threshold для {self.name} = {actual_normal_threshold} не совпало с ожидаемым {expected} (процент={value}% от ном. напряжения {nominal_voltage})")

        else:
            data.thresholdNormal = value
            data.setDataType(4, data_type)

            reader.write(data, 4)
            result = reader.read(data, 4)
            if result == value:
                print(f"Normal_Threshold для {self.name} установлено на {value}")
                self.recorded_values["normal_threshold"] = value

    def set_threshold_duration_min_over(self, reader):
        data = self.data
        value = self._get_random_value(6)
        data.minOverThresholdDuration = value
        reader.write(data, 6)
        actual_threshold_duration_min_over = reader.read(data, 6)
        if actual_threshold_duration_min_over == value:
            print(f"MinOverThresholdDuration для {self.name} установлено на {value}")
            self.recorded_values["threshold_duration_min_over"] = value


    def set_threshold_duration_min_under(self, reader):
        data = self.data
        value = self._get_random_value(7)
        data.minUnderThresholdDuration = value
        reader.write(data, 7)
        actual_threshold_duration_min_under = reader.read(data, 7)
        if actual_threshold_duration_min_under == value:
            print(f"MinUnderThresholdDuration для {self.name} установлено на {value}")
            self.recorded_values["threshold_duration_min_under"] = value

    def _get_random_value(self, attribute):
        if attribute == 4:
            number_start = self.normal_threshold[0]
            number_stop = self.normal_threshold[1]
        elif attribute == 6:
            number_start = self.threshold_duration_min_over[0]
            number_stop = self.threshold_duration_min_over[1]
        else:
            number_start = self.threshold_duration_min_under[0]
            number_stop = self.threshold_duration_min_under[1]
        return randint(number_start, number_stop)