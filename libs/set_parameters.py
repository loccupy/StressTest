from libs.range_of_values import Limiters


def set_limiters(reader):
    try:
        limiters_objects = ["0.0.17.0.0.255",
                            "0.0.17.0.1.255",
                            "0.0.17.0.2.255",
                            "0.0.17.0.3.255",
                            "0.0.17.0.4.255",
                            "0.0.17.0.5.255"]
        meter_type = reader.deviceType

        for obis in limiters_objects:
            res = Limiters(obis, meter_type)
            res.set_normal_threshold(reader)
            res.set_threshold_duration_min_over(reader)
            res.set_threshold_duration_min_under(reader)

        return "Лимитеры установлены"
    except Exception as e:
        print(f"Лимитеры не установлены, ошибка {e.args}.")
        txt = f"Лимитеры не установлены, ошибка {e.args}."
        return txt