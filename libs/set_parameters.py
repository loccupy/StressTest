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


# Тексты вердиктов сверки лимитеров по фазе проверки.
# Сравнение (read_limiters + compare_all) общее; различаются только формулировки
# и наличие ветки «пропущено» для первой фазы.
#   readback    — сверка только что записанного (после set_limiters);
#   after_cycle — сверка сохранности после выкл/вкл (до set_limiters).
LIMITER_VERDICTS = {
    "readback": {
        "ok": "Проверка лимитеров: все значения записались корректно ({n} OBIS).",
        "mismatch": "Проверка лимитеров: найдены расхождения:\n{detail}",
    },
    "after_cycle": {
        "skip": ("Проверка сохранности лимитеров после выкл/вкл: пропущена — "
                 "нет записанных значений прошлого цикла (первый цикл теста)."),
        "ok": ("Проверка сохранности лимитеров после выкл/вкл: все значения "
               "сохранились корректно ({n} OBIS)."),
        "mismatch": ("Проверка сохранности лимитеров после выкл/вкл: найдены "
                     "расхождения (часть значений не пережила выкл/вкл):\n{detail}"),
    },
}


def verify_limiters(reader, phase="readback"):
    """Сверка лимитеров: заново считывает их и сравнивает с записанным в `_store.recorded`.

    Одна реализация для двух фаз; меняется только смысл сравнения (что лежит
    в `_store.recorded` на момент вызова) и тексты вердиктов:
      - phase="readback"    — сверка только что записанного. Вызывать ПОСЛЕ
        `set_limiters`, когда `recorded` уже наполнен значениями этого цикла.
      - phase="after_cycle" — сверка сохранности после выкл/вкл реле. Вызывать
        ДО `set_limiters`, чтобы сравнить со снимком ПРОШЛОГО цикла; на первом
        цикле (`recorded` пуст) возвращает «пропущено» и не трогает прибор.

    Возвращает строку-вердикт. Вердикты ok/mismatch печатает; «пропущено»
    и сбой чтения возвращает без печати — как было в исходных функциях.
    """
    texts = LIMITER_VERDICTS[phase]

    if phase == "after_cycle" and not _store.recorded:
        # Сравнить не с чем: записей прошлого цикла ещё нет.
        return texts["skip"]

    read_status = read_limiters(reader)
    if read_status != "Лимитеры считаны":
        # Прочитать не удалось — вердикт вынести нельзя, возвращаем причину.
        return read_status

    ok, issues = _store.compare_all()
    if ok:
        txt = texts["ok"].format(n=len(_store.recorded))
    else:
        detail = "\n".join(f"  - {issue}" for issue in issues)
        txt = texts["mismatch"].format(detail=detail)
    print(txt)
    return txt
