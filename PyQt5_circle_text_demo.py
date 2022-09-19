from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
import sys


# Creating CircularText class
class CircularText(QWidget):
    def __init__(self, parent = None):
        super(CircularText, self).__init__(parent)

        # Setting window position and size
        self.screen_width = 700
        self.screen_height = 700
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

    # function for drawing circle on background of circular text
    def draw_circle_around_txt(self, txt_rect, circle_colour, qpoint, radius):
        # creating painter and setting rendering hints
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # setting pen size to text size and drawing circle
        height = txt_rect.height()
        painter.setPen(QPen(circle_colour, height))
        painter.drawEllipse(qpoint, radius, radius)

        # closing painter
        painter.end()

    # function for rendring circular text on screen
    def render_txt(self, qpoint, radius, circle_colour, txt, qfont, txt_colour, txt_position, char_space = 0, draw_txt_path = False, draw_rect = False):
        # getting circumference of circle and font matrix
        circumference = int(2 * math.pi * radius)
        fm = QFontMetrics(qfont)

        # creating painter path and setting circlular path to painter path
        painter_path = QPainterPath()
        painter_path.addEllipse(qpoint, radius, radius)

        # getting font bounding rectangle and calling draw circle function
        text_rect = fm.boundingRect(txt)
        self.draw_circle_around_txt(text_rect, circle_colour, qpoint, radius)

        # drawing circular path if set to true
        if draw_txt_path:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.drawPath(painter_path)
            painter.end()

        # getting circular path all point and angle at that point
        # appending geted points and angle in pts and ang list
        pts = []
        ang = []
        cir_per = 0
        cir_per_inc = 1/circumference
        for i in range(0, circumference):
            if cir_per + cir_per_inc < 1:
                cir_per += cir_per_inc
            pts.append(painter_path.pointAtPercent(cir_per))
            ang.append(painter_path.angleAtPercent(cir_per))
        pts.append(painter_path.pointAtPercent(0.999999))
        ang.append(painter_path.angleAtPercent(0.999999))

        # rendering text char one by one in circular path
        set_char_pos = txt_position
        for i in range(len(txt)):
            text_rect = fm.boundingRect(txt[i])  # getting char bounding rectangle
            if txt[i] == ' ': # for space there is no bounding rect 
                text_rect = fm.boundingRect("s") # so I change it to 's' because space and 's' has almost same bounding rect
            set_char_pos += (text_rect.width()+char_space) # seperating char from colliding
            
            # getting point and angle at point 
            point = pts[set_char_pos]
            text_angle = ang[set_char_pos]

            # creating painter and setting render hint
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            
            # setting font and pen
            painter.setFont(qfont)
            painter.setPen(QPen(txt_colour))

            # setting translate position at geted circular path point x, y and rotating text char
            painter.translate(point.x(), point.y())
            painter.rotate(-text_angle)
            
            # setting text char rendering at path point center and drawing text char
            txt_rect = QRectF(-text_rect.width()/2, -text_rect.height()/2, text_rect.width(), text_rect.height())
            painter.drawText(txt_rect, 0, txt[i])

            # drawing bounding box around char if set to true
            if draw_rect:
                painter.drawRect(txt_rect)

            painter.end() # closing painter

    # handle painting event
    def paintEvent(self, event):
        # calling txt render function
        self.render_txt(QPointF(*([self.width()/2]*2)), 200, QColor(0, 67, 0), "I am Prasanna", QFont("Times New Roman", 20, 1, True), Qt.white, 600)
        self.render_txt(QPointF(*([self.width()/2]*2)), 150, QColor(191, 100, 255), "Hello guys", QFont("Consolas", 15, 1, True), Qt.yellow, 200, 20)
        self.render_txt(QPointF(*([self.width()/2]*2)), 100, Qt.red, "Circular text", QFont("Consolas", 13, 1, True), Qt.blue, 0, 1)



# creating QApplication
def load():
    app = QApplication(sys.argv)
    circularText = CircularText()
    circularText.show() 
    app.exec()

# program flow starting point
if __name__ == '__main__':
    load()