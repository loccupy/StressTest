class TestDataStore:
    """Хранит записанные и прочитанные значения лимитеров, сравнивает их."""

    def __init__(self):
        self.recorded = {}   # obis -> {"normal_threshold": ..., ...}
        self.read_values = {}  # obis -> {"normal_threshold": ..., ...}

    def record(self, obis, values):
        """Сохраняет записанные значения по OBIS-коду."""
        self.recorded[obis] = dict(values)

    def read(self, obis, values):
        """Сохраняет прочитанные значения по OBIS-коду."""
        self.read_values[obis] = dict(values)

    def compare(self, obis):
        """Сравнивает записанные и прочитанные значения для одного OBIS.
        Возвращает (True, []) если совпадают, (False, [список несовпадений])."""
        if obis not in self.recorded:
            return False, [f"Нет записанных данных для {obis}"]
        if obis not in self.read_values:
            return False, [f"Нет прочитанных данных для {obis}"]

        mismatches = []
        for key in self.recorded[obis]:
            rec = self.recorded[obis][key]
            rd = self.read_values[obis][key]
            if rec != rd:
                mismatches.append(
                    f"{key}: записано={rec}, прочитано={rd}"
                )
        return len(mismatches) == 0, mismatches

    def compare_all(self):
        """Сравнивает все сохранённые OBIS-коды.
        Возвращает (True, []) если все совпали, (False, список проблем)."""
        all_ok = True
        all_issues = []

        for obis in self.recorded:
            ok, issues = self.compare(obis)
            if not ok:
                all_ok = False
                for issue in issues:
                    all_issues.append(f"{obis}: {issue}")

        return all_ok, all_issues
