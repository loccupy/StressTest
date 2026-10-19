from libs.objects_for_testing_the_file_system.limiters import Limiters
from libs.objects_for_testing_the_file_system.test_data_store import TestDataStore

# Общее (singleton) хранилище запланированных и фактических значений по OBIS.
_store = TestDataStore()

LIMITER_OBIS = [
    "0.0.17.0.0.255",
    "0.0.17.0.1.255",
    "0.0.17.0.2.255",
    "0.0.17.0.3.255",
    "0.0.17.0.4.255",
    "0.0.17.0.5.255",
]


def set_limiters(reader):
    """Записывает лимитеры и сохраняет записанные значения в общее хранилище.

    Значения в хранилище — то, что реально подтверждено записаться при
    read-back внутри методов set_*. Это «план» для последующей сверки.
    """
    try:
        meter_type = reader.deviceType

        for obis in LIMITER_OBIS:
            res = Limiters(obis, meter_type)
            res.set_normal_threshold(reader)
            res.set_threshold_duration_min_over(reader)
            res.set_threshold_duration_min_under(reader)
            _store.record(obis, res.recorded_values)

        return "Лимитеры установлены"
    except Exception as e:
        print(f"Лимитеры не установлены, ошибка {e.args}.")
        txt = f"Лимитеры не установлены, ошибка {e.args}."
        return txt


def read_limiters(reader):
    """Независимо считывает лимитеры и сохраняет фактические значения в хранилище."""
    try:
        meter_type = reader.deviceType

        for obis in LIMITER_OBIS:
            res = Limiters(obis, meter_type)
            res.read_normal_threshold(reader)
            res.read_threshold_duration_min_over(reader)
            res.read_threshold_duration_min_under(reader)
            _store.read(obis, res.read_values)

        return "Лимитеры считаны"
    except Exception as e:
        print(f"Лимитеры не прочитаны, ошибка {e.args}.")
        txt = f"Лимитеры не прочитаны, ошибка {e.args}."
        return txt


def verify_limiters(reader):
    """Сверка записанного: заново считывает лимитеры и сравнивает с тем, что записывали.

    Возвращает строку-вердикт и печатает её. Сравнение идёт по каждому OBIS и
    каждому атрибуту (normal_threshold / min_over / min_under).
    """
    read_status = read_limiters(reader)
    if read_status != "Лимитеры считаны":
        # Прочитать не удалось — вердикт вынести нельзя, возвращаем причину.
        return read_status

    ok, issues = _store.compare_all()
    if ok:
        txt = (f"Проверка лимитеров: все значения записались корректно "
               f"({len(_store.recorded)} OBIS).")
    else:
        detail = "\n".join(f"  - {issue}" for issue in issues)
        txt = f"Проверка лимитеров: найдены расхождения:\n{detail}"
    print(txt)
    return txt
