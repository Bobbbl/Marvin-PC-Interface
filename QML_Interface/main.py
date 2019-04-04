# This Python file uses the following encoding: utf-8
import os
import sys
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QAbstractListModel, Qt, QUrl, QStringListModel
from PySide2.QtGui import QGuiApplication


def upbutton_handler():
    print("Up")


def downbutton_handler():
    print("Down")


def leftbutton_handler():
    print("Left")


def rightbutton_handler():
    print("Right")


def stopbutton_handler():
    print("Stop")


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    rootobject = view.rootObject()

    rootobject.upbutton_pressed.connect(upbutton_handler)
    rootobject.downbutton_pressed.connect(downbutton_handler)
    rootobject.leftbutton_pressed.connect(leftbutton_handler)
    rootobject.rightbutton_pressed.connect(rightbutton_handler)
    rootobject.stopbutton_pressed.connect(stopbutton_handler)

    if view.status() == QQuickView.Error:
        sys.exit(-1)

    view.show()

    app.exec_()
    del view


