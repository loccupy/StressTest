import datetime
import os

from PyQt5 import uic, QtWidgets

from libs.EmittingStream import EmittingStream
from libs.Worker import Worker

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import QSettings, QRegExp
from PyQt5.QtGui import QTextCursor, QIntValidator, QRegExpValidator


class FileUploader(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('company', 'STRESS')
        self.initUI()
        self.load_settings()  # Загружаем сохраненные настройки при запуске

    def initUI(self):
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.join(current_dir, 'libs', 'maket.ui')

        uic.loadUi(ui_path, self)

        self.applyDarkTheme()

        self.worker = Worker()
        self.worker.signal.connect(self.update_text)

        # Добавляем поля ввода и чек боксы в секцию ввода данных
        self.fields = {}

        # Добавляем поле для ввода названия файла
        self.fileNameField = self.findChild(QtWidgets.QLineEdit, 'file_name')
        self.change_time_for_disconnect_and_connect()
        self.create_log_section()
        self.create_fields_for_config_the_master_meter()
        self.create_meter_rows()

        # Кнопки
        self.start_checking = self.findChild(QtWidgets.QPushButton, 'start_test')
        self.start_checking.clicked.connect(self.start_thread)

        self.text_edit = self.findChild(QtWidgets.QTextEdit, 'textEdit')
        self.text_edit.setReadOnly(True)  # Запрещаем редактирование
        self.redirect_stdout()
        self.stream.textWritten.connect(self.on_text_written)

        self.stop_checking = self.findChild(QtWidgets.QPushButton, 'stop_test')
        self.stop_checking.clicked.connect(self.stop_thread)

    def save_settings(self):
        # Сохраняем все важные настройки
        self.settings.setValue('file_name', self.fileNameField.text())

        # Сохранение настроек ведущего счетчика
        self.settings.setValue('serial', self.serial_field.text())
        self.settings.setValue('password', self.password_field.text())
        self.settings.setValue('main_speed', self.main_speed_field.text())
        self.settings.setValue('main_com_port', self.main_com_port_field.text())
        self.settings.setValue('aux_speed', self.aux_speed_field.text())
        self.settings.setValue('aux_com_port', self.aux_com_port_field.text())

        # Сохранение времени отключения/подключения
        self.settings.setValue('check_disconnect', self.disconnect_checkbox_1.isChecked())
        self.settings.setValue('disconnect_time', self.disconnect_field_1.text())
        self.settings.setValue('check_connect', self.disconnect_checkbox_2.isChecked())
        self.settings.setValue('connect_time', self.disconnect_field_2.text())

        # Сохранение состояния чекбоксов журналов
        for label, checkbox in self.log_checkboxes.items():
            self.settings.setValue(f'log_{label}', checkbox.isChecked())

        # Сохранение настроек счетчиков
        for i in range(6):
            self.settings.setValue(f'com_{i}', self.fields[f'com_{i}'].text())
            self.settings.setValue(f'type_{i}', self.fields[f'type_{i}'].currentText())
            self.settings.setValue(f'check_{i}', self.fields[f'check_{i}'].isChecked())

    def load_settings(self):
        # Загружаем сохраненные настройки
        self.fileNameField.setText(self.settings.value('file_name', ''))

        # Загружаем настройки ведущего счетчика
        self.serial_field.setText(self.settings.value('serial', ''))
        self.password_field.setText(self.settings.value('password', ''))
        self.main_speed_field.setText(self.settings.value('main_speed', ''))
        self.main_com_port_field.setText(self.settings.value('main_com_port', ''))
        self.aux_speed_field.setText(self.settings.value('aux_speed', ''))
        self.aux_com_port_field.setText(self.settings.value('aux_com_port', ''))

        # Загружаем время отключения/подключения
        check_value = self.settings.value('check_disconnect', False)
        if isinstance(check_value, str):
            self.disconnect_checkbox_1.setChecked(check_value.lower() == 'true')
        else:
            self.disconnect_checkbox_1.setChecked(check_value)
        self.disconnect_field_1.setText(self.settings.value('disconnect_time', ''))
        check_value = self.settings.value('check_connect', False)
        if isinstance(check_value, str):
            self.disconnect_checkbox_2.setChecked(check_value.lower() == 'true')
        else:
            self.disconnect_checkbox_2.setChecked(check_value)
        self.disconnect_field_2.setText(self.settings.value('connect_time', ''))

        # Загружаем состояние чекбоксов журналов
        for label, checkbox in self.log_checkboxes.items():
            # Преобразуем значение в булево
            checked_value = self.settings.value(f'log_{label}', False)
            if isinstance(checked_value, str):
                # Если значение пришло как строка, преобразуем его
                checkbox.setChecked(checked_value.lower() == 'true')
            else:
                checkbox.setChecked(checked_value)

        # Загружаем настройки счетчиков
        for i in range(6):
            self.fields[f'com_{i}'].setText(self.settings.value(f'com_{i}', ''))

            type_value = self.settings.value(f'type_{i}', '')
            index = self.fields[f'type_{i}'].findText(type_value)
            if index != -1:
                self.fields[f'type_{i}'].setCurrentIndex(index)

            # Аналогично преобразуем значение для чекбоксов счетчиков
            check_value = self.settings.value(f'check_{i}', False)
            if isinstance(check_value, str):
                self.fields[f'check_{i}'].setChecked(check_value.lower() == 'true')
            else:
                self.fields[f'check_{i}'].setChecked(check_value)


    def get_all_data(self):
        # Инициализируем словарь для хранения всех данных
        all_data = {
            'meter_data': {},
            'log_data': {},
            'config_data': {},
            'time_data': {},
            'file_name': ''
        }

        # Собираем данные из полей счетчиков
        try:
            labels = ["Включить 1-ый ведомый счетчик", "Включить 2-ый ведомый счетчик", "Включить 3-ый ведомый счетчик",
                      "Включить 4-ый ведомый счетчик", "Включить 5-ый ведомый счетчик", "Включить 6-ый ведомый счетчик"]
            for i in range(6):  # Для 6 счетчиков
                meter_name = labels[i]

                # Получаем данные с проверкой существования
                com_port = "COM" + self.fields.get(f'com_{i}', QLineEdit()).text()
                meter_type = self.fields.get(f'type_{i}', QtWidgets.QComboBox()).currentText()

                # Добавляем данные в структуру
                all_data['meter_data'][meter_name] = {
                    # 'enabled': enabled,
                    'com_port': com_port,
                    'type': meter_type
                }

        except Exception as e:
            print(f"Ошибка при получении данных счетчиков: {e}")
            return None

        # Собираем данные из секции журналов
        try:
            log_data = {
                label: checkbox.isChecked()
                for label, checkbox in self.log_checkboxes.items()
            }
            all_data['log_data'] = log_data
        except Exception as e:
            print(f"Ошибка при получении данных журналов: {e}")
            return None

        # Собираем данные конфигурации ведущего счетчика
        try:
            config_data = {
                'id': {
                    'serial': self.serial_field.text(),
                    'password': self.password_field.text()
                },
                'main_connection': {
                    'speed': self.main_speed_field.text(),
                    'com_port': "COM" + self.main_com_port_field.text()
                },
                'auxiliary_connection': {
                    'speed': self.aux_speed_field.text(),
                    'com_port': "COM" + self.aux_com_port_field.text()
                }
            }

            all_data['config_data'] = config_data
        except Exception as e:
            print(f"Ошибка при получении данных конфигурации: {e}")
            return None

        # Собираем данные времени отключения/подключения
        try:
            time_data = {
                'disconnect_time': self.disconnect_field_1.text(),
                'connect_time': self.disconnect_field_2.text()
            }
            all_data['time_data'] = time_data
        except Exception as e:
            print(f"Ошибка при получении данных времени: {e}")
            return None

        time_for_file_name = datetime.datetime.now().replace(microsecond=0).strftime("_%d.%m.%y_%H.%M.%S")
        # Получаем имя файла
        all_data['file_name'] = (self.fileNameField.text() + time_for_file_name + ".txt")

        # Проверяем, что все секции данных успешно собраны
        if not all(key in all_data for key in ['meter_data', 'log_data', 'config_data', 'time_data', 'file_name']):
            print("Не все данные были успешно собраны")
            return None

        return all_data

    def change_time_for_disconnect_and_connect(self):
        self.disconnect_checkbox_1 = self.findChild(QtWidgets.QCheckBox, 'check_disconnect')
        self.disconnect_field_1 = self.findChild(QtWidgets.QLineEdit, 'disconnect_time')
        regex = QRegExp(r'^[\d]{1,3}[-]{1}[\d]{1,3}$')
        self.disconnect_field_1.setValidator(QRegExpValidator(regex))
        self.disconnect_field_1.setEnabled(False)
        self.disconnect_checkbox_1.stateChanged.connect(
            lambda checked: self.toggle_input_field(self.disconnect_checkbox_1, self.disconnect_field_1)
        )

        self.disconnect_checkbox_2 = self.findChild(QtWidgets.QCheckBox, 'check_reconnect')
        self.disconnect_field_2 = self.findChild(QtWidgets.QLineEdit, 'reconnect_time')
        regex = QRegExp(r'^[\d]{1,3}[-]{1}[\d]{1,3}$')
        self.disconnect_field_2.setValidator(QRegExpValidator(regex))
        self.disconnect_field_2.setEnabled(False)
        self.disconnect_checkbox_2.stateChanged.connect(
            lambda checked: self.toggle_input_field(self.disconnect_checkbox_2, self.disconnect_field_2)
        )

    def create_log_section(self):
        self.log_checkboxes = {
            "Журнал диагностики": self.findChild(QtWidgets.QCheckBox, 'self_diagnosis_log'),
            "Журнал вкл/выкл": self.findChild(QtWidgets.QCheckBox, 'on_off_log'),
            "Журнал коррекции времени": self.findChild(QtWidgets.QCheckBox, 'time_log'),
            "Журнал напряжения": self.findChild(QtWidgets.QCheckBox, 'voltage_log')
        }

    def create_fields_for_config_the_master_meter(self):
        self.serial_field = self.findChild(QtWidgets.QLineEdit, 'serial')
        self.serial_field.setValidator(QIntValidator())

        self.password_field = self.findChild(QtWidgets.QLineEdit, 'password')
        regex = QRegExp(r'^[A-Za-z\d!#$@&,()*+\'-./:;<=>?**\[\]^_"{}|~]{6,16}$')
        self.password_field.setValidator(QRegExpValidator(regex))

        self.main_speed_field = self.findChild(QtWidgets.QLineEdit, 'speed_main')
        self.main_speed_field.setValidator(QIntValidator())

        self.main_com_port_field = self.findChild(QtWidgets.QLineEdit, 'com_main')
        self.main_com_port_field.setValidator(QIntValidator())

        self.aux_speed_field = self.findChild(QtWidgets.QLineEdit, 'speed_reserve')
        self.aux_speed_field.setValidator(QIntValidator())

        self.aux_com_port_field = self.findChild(QtWidgets.QLineEdit, 'com_reserve')
        self.aux_com_port_field.setValidator(QIntValidator())

    def create_meter_rows(self):
        checkbox_1 = self.findChild(QtWidgets.QCheckBox, 'first_check')
        com_port_field_1 = self.findChild(QtWidgets.QLineEdit, 'first_com')
        com_port_field_1.setEnabled(False)

        checkbox_1.stateChanged.connect(
            lambda checked, cb=checkbox_1, fd=com_port_field_1: self.toggle_input_field(cb, fd)
        )

        meter_type_field_1 = self.findChild(QtWidgets.QComboBox, 'first_type')
        meter_type_field_1.setEditable(False)


        self.fields['check_0'] = checkbox_1
        self.fields['com_0'] = com_port_field_1
        self.fields['type_0'] = meter_type_field_1

        checkbox_2 = self.findChild(QtWidgets.QCheckBox, 'second_check')
        com_port_field_2 = self.findChild(QtWidgets.QLineEdit, 'second_com')
        com_port_field_2.setEnabled(False)

        checkbox_2.stateChanged.connect(
            lambda checked, cb=checkbox_2, fd=com_port_field_2: self.toggle_input_field(cb, fd)
        )

        meter_type_field_2 = self.findChild(QtWidgets.QComboBox, 'second_type')
        meter_type_field_2.setEditable(False)

        self.fields['check_1'] = checkbox_2
        self.fields['com_1'] = com_port_field_2
        self.fields['type_1'] = meter_type_field_2

        checkbox_3 = self.findChild(QtWidgets.QCheckBox, 'third_check')
        com_port_field_3 = self.findChild(QtWidgets.QLineEdit, 'third_com')
        com_port_field_3.setEnabled(False)

        checkbox_3.stateChanged.connect(
            lambda checked, cb=checkbox_3, fd=com_port_field_3: self.toggle_input_field(cb, fd)
        )

        meter_type_field_3 = self.findChild(QtWidgets.QComboBox, 'third_type')
        meter_type_field_3.setEditable(False)

        self.fields['check_2'] = checkbox_3
        self.fields['com_2'] = com_port_field_3
        self.fields['type_2'] = meter_type_field_3

        checkbox_4 = self.findChild(QtWidgets.QCheckBox, 'forth_check')
        com_port_field_4 = self.findChild(QtWidgets.QLineEdit, 'forth_com')
        com_port_field_4.setEnabled(False)

        checkbox_4.stateChanged.connect(
            lambda checked, cb=checkbox_4, fd=com_port_field_4: self.toggle_input_field(cb, fd)
        )

        meter_type_field_4 = self.findChild(QtWidgets.QComboBox, 'forth_type')
        meter_type_field_4.setEditable(False)

        self.fields['check_3'] = checkbox_4
        self.fields['com_3'] = com_port_field_4
        self.fields['type_3'] = meter_type_field_4

        checkbox_5 = self.findChild(QtWidgets.QCheckBox, 'fifth_check')
        com_port_field_5 = self.findChild(QtWidgets.QLineEdit, 'fifth_com')
        com_port_field_5.setEnabled(False)

        checkbox_5.stateChanged.connect(
            lambda checked, cb=checkbox_5, fd=com_port_field_5: self.toggle_input_field(cb, fd)
        )

        meter_type_field_5 = self.findChild(QtWidgets.QComboBox, 'fifth_type')
        meter_type_field_5.setEditable(False)

        self.fields['check_4'] = checkbox_5
        self.fields['com_4'] = com_port_field_5
        self.fields['type_4'] = meter_type_field_5

        checkbox_6 = self.findChild(QtWidgets.QCheckBox, 'sixth_check')
        com_port_field_6 = self.findChild(QtWidgets.QLineEdit, 'sixth_com')
        com_port_field_6.setEnabled(False)

        checkbox_6.stateChanged.connect(
            lambda checked, cb=checkbox_6, fd=com_port_field_6: self.toggle_input_field(cb, fd)
        )

        meter_type_field_6 = self.findChild(QtWidgets.QComboBox, 'sixth_type')
        meter_type_field_6.setEditable(False)

        self.fields[f'check_5'] = checkbox_6
        self.fields[f'com_5'] = com_port_field_6
        self.fields[f'type_5'] = meter_type_field_6

    # Создаем метод для управления состоянием поля ввода
    def toggle_input_field(self, checkbox, field):
        if checkbox.isChecked():
            field.setEnabled(True)  # Разрешаем ввод данных
        else:
            field.setEnabled(False)  # Запрещаем ввод данных
            field.clear()  # Очищаем поле при отключении

    def check_fields(self):
        if not self.main_com_port_field.text().strip():
            # Показываем предупреждение
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Введите COM основного соединения!",
                QMessageBox.Ok
            )
            return False
        elif not self.main_speed_field.text().strip():
            # Показываем предупреждение
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Введите скорость основного соединения!",
                QMessageBox.Ok
            )
            return False
        if self.fields.get('check_0', QtWidgets.QCheckBox).isChecked():
                if not self.fields.get(f'com_0', QLineEdit()).text():
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Введите COM для ПЕРВОГО ведущего счетчика!",
                        QMessageBox.Ok
                    )
                    return False
        if self.fields.get('check_1', QtWidgets.QCheckBox).isChecked():
                if not self.fields.get(f'com_1', QLineEdit()).text():
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Введите COM для ВТОРОГО ведущего счетчика!",
                        QMessageBox.Ok
                    )
                    return False
        if self.fields.get('check_2', QtWidgets.QCheckBox).isChecked():
                if not self.fields.get(f'com_2', QLineEdit()).text():
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Введите COM для ТРЕТЬЕГО ведущего счетчика!",
                        QMessageBox.Ok
                    )
                    return False
        if self.fields.get('check_3', QtWidgets.QCheckBox).isChecked():
                if not self.fields.get(f'com_3', QLineEdit()).text():
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Введите COM для ЧЕТВЕРТОГО ведущего счетчика!",
                        QMessageBox.Ok
                    )
                    return False
        if self.fields.get('check_4', QtWidgets.QCheckBox).isChecked():
                if not self.fields.get(f'com_4', QLineEdit()).text():
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Введите COM для ПЯТОГО ведущего счетчика!",
                        QMessageBox.Ok
                    )
                    return False
        if self.fields.get('check_5', QtWidgets.QCheckBox).isChecked():
                if not self.fields.get(f'com_5', QLineEdit()).text():
                    QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Введите COM для ШЕСТОГО ведущего счетчика!",
                        QMessageBox.Ok
                    )
                    return False
        return True

    def start_thread(self):
        try:
            if not self.check_fields():
                return

            # Получаем все данные перед запуском
            all_data = self.get_all_data()

            # Отправляем данные в рабочий поток
            self.worker.set_input_data(all_data)
            self.worker.start()
        except Exception as e:
            print(e)

    def stop_thread(self):
        self.worker.running = False
        print("Тест скоро остановится...")

    def update_text(self, text):
        self.text_edit.append(text)

    def redirect_stdout(self):
        self.stream = EmittingStream()
        sys.stdout = self.stream
        sys.stderr = self.stream

    def on_text_written(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        QApplication.processEvents()

    def applyDarkTheme(self):
        # Определяем стили для темной темы
        dark_stylesheet = """
        QWidget {
            background-color: #2c313c;
            color: #ffffff;
        }

        QLineEdit {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px;
        }

        QLineEdit:focus {
            border: 1px solid #61dafb;
        }

        QPushButton {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px 10px;
        }

        QPushButton:hover {
            background-color: #444950;
        }

        QPushButton:pressed {
            background-color: #2c313c;
        }
        """

        # Применяем стиль к приложению
        self.setStyleSheet(dark_stylesheet)

    def closeEvent(self, event):
        # Сохраняем настройки при закрытии приложения
        self.save_settings()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    ex = FileUploader()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
