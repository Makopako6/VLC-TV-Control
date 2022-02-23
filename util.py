from PyQt5.QtGui import QGuiApplication, QIcon, QWindow, QImage, QPixmap, QPainter, QBrush
from PyQt5.QtCore import QSize, QRect, Qt
import os


def get_screen_size():
    return QGuiApplication.primaryScreen().geometry()


def get_local_file(file):
    return os.path.join(os.path.split(__file__)[0], file)


def mask_image_circ(imgdata, imgtype='jpg', size=64, angle=0):
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)
    brush = QBrush(image)
    painter = QPainter(out_img)
    painter.translate(rect.center())
    painter.rotate(angle)
    painter.translate(-rect.center())
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio,
                   Qt.SmoothTransformation)

    return pm


def path_to_icon(icon_path, icon_color=None, icon_size: QSize = QSize(25, 25)):
    if icon_color is not None:
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(icon_size)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.setBrush(icon_color)
        painter.setPen(icon_color)
        painter.drawRect(pixmap.rect())
        painter.end()
        return QIcon(pixmap)
    else:
        icon = QIcon(icon_path)
        return icon
