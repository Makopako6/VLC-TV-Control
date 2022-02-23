from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import (
    Qt,
    QPropertyAnimation,
    QVariantAnimation,
    QPoint,
    QEasingCurve,
    QSize,
    pyqtSignal
)
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
from util import get_screen_size, get_local_file


class Window(QWidget):
    onMove = pyqtSignal(QPoint)

    def __init__(self, p=None, width: int = 640, height: int = 480):
        super(Window, self).__init__(p)
        self.setWindowTitle("Window")
        self.resize(width, height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.opacity = 255

    def mousePressEvent(self, event) -> None:
        self.window().windowHandle().startSystemMove()

        QtWidgets.QWidget.mousePressEvent(self, event)

    def raiseBaseWidget(self):
        self.titlebar.raise_()

    def moveEvent(self, a0) -> None:
        self.onMove.emit(self.pos())
        QWidget.moveEvent(self, a0)

    def setOpacity(self, opacity: int):
        self.opacity = opacity

    def paintEvent(self, event) -> None:
        window_border_radius = 64
        s = self.size()
        qp = QPainter(self)

        grad = QLinearGradient(0, 0, 250, 500)
        grad.setColorAt(0.0, QColor(75, 75, 75))
        grad.setColorAt(1.0, QColor(40, 40, 40))

        qp.setBrush(grad)
        qp.setPen(QColor("transparent"))
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           window_border_radius, window_border_radius)
        qp.end()
        QWidget.paintEvent(self, event)


class Grip(QtWidgets.QSizeGrip):
    isResizing = pyqtSignal(bool)

    def __init__(self, p):
        super(Grip, self).__init__(p)

    def mousePressEvent(self, a0) -> None:
        self.isResizing.emit(True)
        QtWidgets.QSizeGrip.mousePressEvent(self, a0)

    def mouseReleaseEvent(self, mouseEvent) -> None:
        self.isResizing.emit(False)
        QtWidgets.QSizeGrip.mouseReleaseEvent(self, mouseEvent)


class WindowContainer(QWidget):
    def __init__(self, window):
        super(WindowContainer, self).__init__()
        self.resize(250, 642)
        self.windowObject = window(self)
        self.windowObject.move(20, 20)
        self.dropShadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.dropShadow.setBlurRadius(32)
        self.dropShadow.setColor(QColor(0, 0, 0, 128))
        self.dropShadow.setOffset(0, 0)
        self.windowObject.setGraphicsEffect(self.dropShadow)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setFocusPolicy(Qt.StrongFocus)

        self.sizeGrip = Grip(self)

        self.showAnimation = QPropertyAnimation(self, b"pos")
        self.showAnimation.setDuration(500)

        self.hideAnimation = QPropertyAnimation(self, b"pos")
        self.hideAnimation.setDuration(500)

        self.oldPos = self.get_center()

        with(open(get_local_file("style.qss"))) as styleFile:
            self.setStyleSheet(styleFile.read())

    # def focusOutEvent(self, a0) -> None:
    #     anim = QVariantAnimation(self)
    #     anim.setDuration(150)
    #     anim.setStartValue(32)
    #     anim.setEndValue(8)
    #     anim.valueChanged.connect(self.dropShadow.setBlurRadius)
    #     anim.start()
    #     QWidget.focusOutEvent(self, a0)

    # def focusInEvent(self, a0) -> None:
    #     if not self.dropShadow.blurRadius() == 32:
    #         anim = QVariantAnimation(self)
    #         anim.setDuration(150)
    #         anim.setStartValue(8)
    #         anim.setEndValue(32)
    #         anim.valueChanged.connect(self.dropShadow.setBlurRadius)
    #         anim.start()
    #         QWidget.focusInEvent(self, a0)

    def get_center(self):
        geometry = self.frameGeometry()
        geometry.moveCenter(get_screen_size().center())
        return geometry.topLeft()

    def sizeEvent(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def windowCloseEvent(self) -> None:
        self.oldPos = self.pos()
        self.hideAnimation.setStartValue(self.oldPos)
        self.hideAnimation.setEndValue(QPoint(self.x(), get_screen_size().height()))
        self.hideAnimation.setEasingCurve(QEasingCurve.InCubic)
        self.hideAnimation.start()
        self.hideAnimation.finished.connect(self.close)

    def showEvent(self, event) -> None:
        self.showAnimation.setStartValue(QPoint(self.x(), get_screen_size().height()))
        self.showAnimation.setEndValue(self.oldPos)
        self.showAnimation.setEasingCurve(QEasingCurve.OutCubic)
        self.showAnimation.start()
        QWidget.showEvent(self, event)

    def minimizeEvent(self):
        self.oldPos = self.pos()
        self.hideAnimation.setStartValue(self.oldPos)
        self.hideAnimation.setEndValue(QPoint(self.x(), get_screen_size().height()))
        self.hideAnimation.setEasingCurve(QEasingCurve.InCubic)
        self.hideAnimation.start()
        self.hideAnimation.finished.connect(self.showMinimized)

    def resizeEvent(self, a0) -> None:
        self.windowObject.resize(self.width() - 40, self.height() - 40)
        self.sizeGrip.move(self.windowObject.width() + 10, self.windowObject.height() + 10)
        QWidget.resizeEvent(self, a0)
