from PyQt5 import QtGui
from PyQt5.QtWidgets import QComboBox, QCheckBox, QLineEdit,\
    QRadioButton, QSpinBox, QSlider, QListWidget, QTabWidget
from PyQt5.QtCore import QSettings
from distutils.util import strtobool
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QLabel, QMainWindow, QPushButton, QWidget

import inspect


class QMainWindow(QMainWindow):
    companie_name = 'CompanieName'
    software_name = 'SoftwareName'
    settings_ui_name = 'defaultUiwidget'
    settings_ui_user_name = 'user'
    _names_to_avoid = {}

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.settings = QSettings(self.companie_name, self.software_name)

    def closeEvent(self, e):
        self._gui_save()

    @classmethod
    def _get_handled_types(cls):
        return QComboBox, QLineEdit, QCheckBox, QRadioButton, QSpinBox, QSlider, QListWidget, QTabWidget

    @classmethod
    def _is_handled_type(cls, widget):
        return any(isinstance(widget, t) for t in cls._get_handled_types())

    def _gui_save(self):
        """
        save "ui" controls and values to registry "setting"
        :return:
        """
        name_prefix = f"{self.settings_ui_name}/"
        self.settings.setValue(name_prefix + "geometry", self.saveGeometry())

        for name, obj in inspect.getmembers(self):
            if not self._is_handled_type(obj):
                continue

            name = obj.objectName()
            value = None
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current index from combobox
                value = obj.itemText(index)  # get the text for current index

            elif isinstance(obj, QTabWidget):
                value = obj.currentIndex()

            elif isinstance(obj, QLineEdit):
                value = obj.text()

            elif isinstance(obj, QCheckBox):
                value = obj.isChecked()

            elif isinstance(obj, QRadioButton):
                value = obj.isChecked()

            elif isinstance(obj, QSpinBox):
                value = obj.value()

            elif isinstance(obj, QSlider):
                value = obj.value()

            elif isinstance(obj, QListWidget):
                self.settings.beginWriteArray(name)
                for i in range(obj.count()):
                    self.settings.setArrayIndex(i)
                    self.settings.setValue(name_prefix + name, obj.item(i).text())
                self.settings.endArray()

            if value is not None:
                self.settings.setValue(name_prefix + name, value)

    def _gui_restore(self):
        """
        restore "ui" controls with values stored in registry "settings"
        :return:
        """

        name_prefix = f"{self.settings_ui_name}/"
        geometry_value = self.settings.value(name_prefix + "geometry")
        if geometry_value:
            self.restoreGeometry(geometry_value)

        for name, obj in inspect.getmembers(self):
            if not self._is_handled_type(obj):
                continue
            if name in self._names_to_avoid:
                continue

            name = obj.objectName()
            value = None
            if not isinstance(obj, QListWidget):
                value = self.settings.value(name_prefix + name)
                if value is None:
                    continue

            if isinstance(obj, QComboBox):
                index = obj.findText(value)  # get the corresponding index for specified string in combobox

                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index

            elif isinstance(obj, QTabWidget):
                try:
                    value = int(value)
                except ValueError:
                    value = 0
                obj.setCurrentIndex(value)

            elif isinstance(obj, QLineEdit):
                obj.setText(value)

            elif isinstance(obj, QCheckBox):
                obj.setChecked(strtobool(value))

            elif isinstance(obj, QRadioButton):
                obj.setChecked(strtobool(value))

            elif isinstance(obj, QSlider):
                obj.setValue(int(value))

            elif isinstance(obj, QSpinBox):
                obj.setValue(int(value))

            elif isinstance(obj, QListWidget):
                size = self.settings.beginReadArray(name_prefix + name)
                for i in range(size):
                    self.settings.setArrayIndex(i)
                    value = self.settings.value(name_prefix + name)
                    if value is not None:
                        obj.addItem(value)
                self.settings.endArray()

    def _add_setting(self, name, value):
        name_prefix = f"{self.settings_ui_user_name}/"
        self.settings.setValue(name_prefix + name, value)

    def _get_setting(self, name):
        name_prefix = f"{self.settings_ui_user_name}/"
        return self.settings.value(name_prefix + name)
