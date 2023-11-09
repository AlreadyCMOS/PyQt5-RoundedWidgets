"""
（MyWidgets）：自定义控件类库
=============================================
=============================================

class列表：
----------
RoundedWidget（圆角窗体）

RoundedButton（圆角按钮）

ShadowFrame（阴影边框）
"""


###########################
###-------加载模块-------###
###########################
from PyQt5 import QtWidgets, QtCore, QtGui
import typing





#########################
###-------定义类-------###
#########################

### -----圆角窗体----- ###
class RoundedWidget(QtWidgets.QWidget):

    ### 定义信号 ###
    clicked:    QtCore.pyqtSignal = QtCore.pyqtSignal()
    entered:    QtCore.pyqtSignal = QtCore.pyqtSignal()
    pressed:    QtCore.pyqtSignal = QtCore.pyqtSignal()
    left:       QtCore.pyqtSignal = QtCore.pyqtSignal()



    ### 函数重载 ###
    @typing.overload
    def __init__(self) -> None: pass
    @typing.overload
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None: pass

    @typing.overload
    def setBackgroundColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setBackgroundColor(self, color: QtGui.QColor) -> None: pass

    @typing.overload
    def setBottomColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setBottomColor(self, color: QtGui.QColor) -> None: pass



    ### 构造函数 ###
    def __init__(self, a0: QtWidgets.QWidget | None = None) -> None:
        if a0 is None:
            super().__init__()
        elif isinstance(a0, QtWidgets.QWidget):
            super().__init__(a0)
        else:
            raise TypeError("Parameter passed error!")

        ### private属性 ###
        self.__radius:                  int | float = 10
        self.__bottom_width:            int | float = 0 
        self.__background_gradient:     QtGui.QGradient = None
        self.__draw_bottom:             bool = True
        self.__bottom_offset:           list = [0, 0, 0, 0]
        self.__background_offset:       list = [0, 0, 0, 0]

        self.__color_dict: dict[str, QtGui.QColor] = {
            "background": QtGui.QColor(240, 240, 240, 255),
            "bottom": QtGui.QColor(50, 50, 50, 255)
        }

    
    
    ### private类函数 ###
    def __setColorDict(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None, 
        a2: int | None, 
        a3: int | None, 
        key: str
    ) -> None:

        if (
            isinstance(a0, int) and 
            isinstance(a1, int) and 
            isinstance(a2, int) and 
            (isinstance(a3, int) or a3 is None)
        ):
            if a3 is not None:
                self.__color_dict[key].setRgb(a0, a1, a2, a3)
            else:
                self.__color_dict[key].setRgb(a0, a1, a2)

        elif isinstance(a0, QtGui.QColor) and a1 is None and a2 is None and a3 is None:
            self.__color_dict[key].setRgb(a0.red(), a0.green(), a0.blue(), a0.alpha())

        else:
            raise TypeError("Parameter passed error!")



    ### 重写类函数 ###
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)      ### 抗锯齿 ###
        painter.setPen(QtGui.QColor(QtCore.Qt.transparent))

        rect = QtCore.QRectF(
            0 + self.__bottom_offset[0],
            0 + self.__bottom_offset[1],
            self.rect().width() + self.__bottom_offset[2], 
            self.rect().height() + self.__bottom_offset[3]
        )

        if self.__draw_bottom:
            painter.setBrush(self.__color_dict.get("bottom"))
            painter.drawRoundedRect(rect, self.__radius, self.__radius)
        
        rect = QtCore.QRectF(
            self.__bottom_width + self.__background_offset[0],
            self.__bottom_width + self.__background_offset[1],
            self.rect().width() - 2 * self.__bottom_width + self.__background_offset[2], 
            self.rect().height() - 2 * self.__bottom_width + self.__background_offset[3]
        )
        
        if self.__background_gradient is not None:
            painter.setBrush(self.__background_gradient)
        else:
            painter.setBrush(self.__color_dict.get("background"))
        painter.drawRoundedRect(rect, self.__radius - self.__bottom_width , self.__radius - self.__bottom_width)
        return super().paintEvent(a0)
    


    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.MouseButton.LeftButton:
            self.pressed.emit()
        return super().mousePressEvent(a0)
    


    def enterEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.entered.emit()
        return super().enterEvent(a0)
    


    def leaveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.left.emit()
        return super().leaveEvent(a0)
    


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if (
            0 < a0.x() < self.width() and 
            0 < a0.y() < self.height() and 
            a0.button() == QtCore.Qt.MouseButton.LeftButton
        ):
            self.clicked.emit()
        return super().mouseReleaseEvent(a0)



    ### 定义类函数 ###
    def setRadius(self, r: int | float) -> None:
        if not isinstance(r, (int, float)):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        if r < 0:
            self.__radius = 0
        else:
            self.__radius = r
        self.update()
         
    

    def radius(self) -> int | float:
        return self.__radius



    def setBottomVisible(self, judge: bool) -> None:
        if not isinstance(judge, bool):
            raise TypeError("Parameter passed error! The parameter type must be 'bool'.")
        self.__draw_bottom = judge
        self.update()



    def setBackgroundColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__setColorDict(a0, a1, a2, a3, "background")
        self.update()



    def setBottomWidth(self, width: int | float) -> None:
        if not isinstance(width, (int, float)):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        if width < 0:
            self.__bottom_width = 0
        else:
            self.__bottom_width = width
        self.update()
            
    
    
    def setBottomColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__setColorDict(a0, a1, a2, a3, "bottom")
        self.update()



    def backgroundColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("background"))



    def setDarkStyle(self) -> None:
        self.setBottomVisible(True)
        self.setBottomColor(200, 200, 200)
        self.setBackgroundColor(20, 20, 45)
        


    def setLightStyle(self) -> None:
        self.setBottomVisible(True)
        self.setBottomColor(50, 50, 50)
        self.setBackgroundColor(240, 240, 240)
        


    def setBackgroundGradient(self, gradient: QtGui.QGradient) -> None:
        if not isinstance(gradient, QtGui.QGradient):
            raise TypeError("Parameter passed error! The parameter type must be 'QGradient'.")
        self.__background_gradient = None
        match type(gradient):
            case QtGui.QLinearGradient:
                self.__background_gradient = QtGui.QLinearGradient(gradient)
            case QtGui.QRadialGradient:
                self.__background_gradient = QtGui.QRadialGradient(gradient)
            case QtGui.QConicalGradient:
                self.__background_gradient = QtGui.QConicalGradient(gradient)
            case QtGui.QGradient:
                self.__background_gradient = QtGui.QGradient(gradient)
        self.update()
    


    def removeGradients(self) -> None:
        self.__background_gradient = None
        self.update()
    


    def bottomWidth(self) -> int | float:
        return self.__bottom_width
    


    def bottomColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("bottom"))
    


    def setBottomOffset(
        self, 
        x: int | float, 
        y: int | float, 
        w: int | float, 
        h: int | float
    ) -> None:

        if not (
            isinstance(x, (int, float)) and 
            isinstance(y, (int, float)) and 
            isinstance(w, (int, float)) and 
            isinstance(h, (int, float))
        ):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        self.__bottom_offset[0] = x
        self.__bottom_offset[1] = y
        self.__bottom_offset[2] = w
        self.__bottom_offset[3] = h
        self.update()
    


    def setBackgroundOffset(
        self, 
        x: int | float, 
        y: int | float, 
        w: int | float, 
        h: int | float
    ) -> None:
        
        if not (
            isinstance(x, (int, float)) and 
            isinstance(y, (int, float)) and 
            isinstance(w, (int, float)) and 
            isinstance(h, (int, float))
        ):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        self.__background_offset[0] = x
        self.__background_offset[1] = y
        self.__background_offset[2] = w
        self.__background_offset[3] = h
        self.update()



    def bottomOffset(self) -> tuple:
        return tuple(self.__bottom_offset)
    


    def backgroundOffset(self) -> tuple:
        return tuple(self.__background_offset)





### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###





### -----圆角按钮----- ###
class RoundedButton(RoundedWidget):

    ### 函数重载 ###
    @typing.overload
    def __init__(self) -> None: pass
    @typing.overload
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None: pass
    @typing.overload
    def __init__(self, parent: QtWidgets.QWidget | None = ..., text: str = ...) -> None: pass
    @typing.overload
    def __init__(self, text: str = ...) -> None: pass

    @typing.overload
    def setBackgroundColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setBackgroundColor(self, color: QtGui.QColor) -> None: pass

    @typing.overload
    def setEnteredColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setEnteredColor(self, color: QtGui.QColor) -> None: pass

    @typing.overload
    def setPressedColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setPressedColor(self, color: QtGui.QColor) -> None: pass

    @typing.overload
    def setTextColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setTextColor(self, color: QtGui.QColor) -> None: pass



    ### 构造函数 ###
    def __init__(
        self, 
        a0: QtWidgets.QWidget | str | None = None, 
        a1: str | None = None
    ) -> None:
        
        if (a0 is not None and a1 is not None) and not isinstance(a0, QtWidgets.QWidget):
            raise TypeError("Parameter passed error!")
        elif isinstance(a0, QtWidgets.QWidget):
            super().__init__(a0)
        else:
            super().__init__()

        ### private属性 ###
        self.__text_lable:      QtWidgets.QLabel = QtWidgets.QLabel(self)
        self.__h_layout:        QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)
        self.__label_palette:   QtGui.QPalette = QtGui.QPalette()
        self.__text_font:       QtGui.QFont = QtGui.QFont()

        self.__color_dict: dict[str, QtGui.QColor] = {
            "standard": QtGui.QColor(250, 250, 250, 255),
            "entered": QtGui.QColor(240, 240, 240, 255),
            "pressed": QtGui.QColor(220, 220, 220, 255),
            "text": QtGui.QColor(50, 50, 50, 255),
        }
        self.__gradient_dict: dict[str, QtGui.QGradient] = {
            "standard": None,
            "entered": None,
            "pressed": None
        }

        ### 初始化 ###
        if isinstance(a1, str):
            self.__text_lable.setText(a1)
        elif isinstance(a0, str):
            self.__text_lable.setText(a0)
        self.__text_font.setFamily("微软雅黑")
        self.__text_font.setPointSize(11)
        self.__text_lable.setAlignment(QtCore.Qt.AlignCenter)   ### 字体居中 ###
        self.__label_palette.setColor(QtGui.QPalette.WindowText, self.__color_dict.get("text"))
        self.__text_lable.setPalette(self.__label_palette)
        self.__h_layout.addWidget(self.__text_lable)
        self.setBottomColor(50, 50, 50)
        self.setBottomWidth(1.5)
        super().setFont(self.__text_font)
        super().setBackgroundColor(self.__color_dict.get("standard"))



    ### private类函数 ###
    def __setColorDict(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None, 
        a2: int | None, 
        a3: int | None, 
        key: str
    ) -> None:
        
        if (
            isinstance(a0, int) and 
            isinstance(a1, int) and 
            isinstance(a2, int) and 
            (isinstance(a3, int) or a3 is None)
        ):
            if a3 is not None:
                self.__color_dict[key].setRgb(a0, a1, a2, a3)
            else:
                self.__color_dict[key].setRgb(a0, a1, a2)

        elif isinstance(a0, QtGui.QColor) and a1 is None and a2 is None and a3 is None:
            self.__color_dict[key].setRgb(a0.red(), a0.green(), a0.blue(), a0.alpha())

        else:
            raise TypeError("Parameter passed error!")



    def __setGradientDict(self, gradient: QtGui.QGradient, key: str) -> None:
        if not isinstance(gradient, (QtGui.QGradient)):
            raise TypeError("Parameter passed error! The parameter type must be 'QGradient'.")
        self.__gradient_dict[key] = None
        match type(gradient):
            case QtGui.QLinearGradient:
                self.__gradient_dict[key] = QtGui.QLinearGradient(gradient)
            case QtGui.QRadialGradient:
                self.__gradient_dict[key] = QtGui.QRadialGradient(gradient)
            case QtGui.QConicalGradient:
                self.__gradient_dict[key] = QtGui.QConicalGradient(gradient)
            case QtGui.QGradient:
                self.__gradient_dict[key] = QtGui.QGradient(gradient)
    


    ### 重写类函数 ###
    def setBackgroundColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__setColorDict(a0, a1, a2, a3, "standard")
        super().setBackgroundColor(self.__color_dict.get("standard"))



    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.__gradient_dict.get("pressed") is not None:
                super().setBackgroundGradient(self.__gradient_dict.get("pressed"))
            else:
                super().removeGradients()
                super().setBackgroundColor(self.__color_dict.get("pressed"))
        return super().mousePressEvent(a0)



    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.__gradient_dict.get("entered") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("entered"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("entered"))
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        return super().enterEvent(a0)
    


    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.__gradient_dict.get("standard") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("standard"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("standard"))
        return super().leaveEvent(a0)
    


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.__gradient_dict.get("entered") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("entered"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("entered"))
        return super().mouseReleaseEvent(a0)
    


    def setDarkStyle(self) -> None:
        self.setBottomVisible(True)
        self.setTextColor(200, 200, 200)
        self.setBottomColor(200, 200, 200)
        self.setEnteredColor(65, 65, 85)
        self.setPressedColor(50, 50, 70)
        self.setBackgroundColor(40, 40, 60)
        


    def setLightStyle(self) -> None:
        self.setBottomVisible(True)
        self.setTextColor(50, 50, 50)
        self.setBottomColor(50, 50, 50)
        self.setEnteredColor(240, 240, 240)
        self.setPressedColor(220, 220, 220)
        self.setBackgroundColor(250, 250, 250)
    


    def setBackgroundGradient(self, gradient: QtGui.QGradient) -> None:
        self.__setGradientDict(gradient, "standard")
        super().setBackgroundGradient(self.__gradient_dict.get("standard"))
    


    def removeGradients(self) -> None:
        for key in self.__gradient_dict:
            self.__gradient_dict[key] = None
        super().removeGradients()
    


    def backgroundColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("standard"))
    


    def setFont(self, a0: QtGui.QFont) -> None:
        if not isinstance(a0, QtGui.QFont):
            raise TypeError("Parameter passed error! The parameter type must be 'QFont'.")
        self.__text_font = QtGui.QFont(a0)
        return super().setFont(self.__text_font)
    
    

    ### 定义类函数 ###
    def setTextSize(self, size: int | float) -> None:
        if not isinstance(size, (int, float)):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        self.__text_font.setPointSizeF(float(size))
        super().setFont(self.__text_font)



    def setText(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError("Parameter passed error! The parameter type must be 'str'.")
        self.__text_lable.setText(text)
            
    

    def setEnteredColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__setColorDict(a0, a1, a2, a3, "entered")



    def setPressedColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__setColorDict(a0, a1, a2, a3, "pressed")



    def setTextColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__setColorDict(a0, a1, a2, a3, "text")
        self.__label_palette.setColor(QtGui.QPalette.WindowText, self.__color_dict.get("text"))
        self.__text_lable.setPalette(self.__label_palette)
    


    def pressedColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("pressed"))

    

    def enteredColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("entered"))



    def textColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("text"))
    


    def setEnteredGradient(self, gradient: QtGui.QGradient) -> None:
        self.__setGradientDict(gradient, "entered")



    def setPressedGradient(self, gradient: QtGui.QGradient) -> None:
        self.__setGradientDict(gradient, "pressed")



    def text(self) -> str:
        return self.__text_lable.text()
    


    def textSize(self) -> float:
        return self.__text_font.pointSizeF()
    

    
    def font(self) -> QtGui.QFont:
        return QtGui.QFont(self.__text_font)
    


    def setTextBold(self) -> None:
        self.__text_font.setBold(True)
        super().setFont(self.__text_font)
    


    def removeTextBold(self) -> None:
        self.__text_font.setBold(False)
        super().setFont(self.__text_font)

    

    def textBold(self) -> bool:
        return self.__text_font.bold()
    




### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###





### -----阴影边框----- ###
class ShadowFrame(object):

    ### -----绘制阴影（私有类）----- ###
    class __ShadowPainter(QtWidgets.QWidget):
        
        ### 构造函数（ __ShadowPainter） ###
        def __init__(
            self, 
            parent: QtWidgets.QWidget | None = None, 
            bind_obj: RoundedWidget | None = None,
            shadow_width: int | float = None
        ) -> None:
            super().__init__(parent)
            
            ### private属性 ###
            self.__bind_obj:        RoundedWidget = bind_obj
            self.__shadow_width:    int | float = shadow_width
            self.__shadow_radiu:    int | float = self.__bind_obj.radius() + self.__shadow_width
            self.__centers_dict:    dict[str, QtCore.QPointF] = None
            self.__pie_gradient:    QtGui.QRadialGradient = QtGui.QRadialGradient()
            self.__rect_gradient:   QtGui.QLinearGradient = QtGui.QLinearGradient()

            ### 初始化 ###
            self.setGeometry(
                self.__bind_obj.x() - self.__shadow_width,
                self.__bind_obj.y() - self.__shadow_width,
                self.__bind_obj.width() + 2 * self.__shadow_width,
                self.__bind_obj.height() + 2 * self.__shadow_width
            )
            self.__setCenterDict()
            self.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
            self.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
            self.__bind_obj.raise_()
            self.lower()



        ### private类函数 ###
        def __setCenterDict(self):
            if self.__centers_dict is not None:
                del self.__centers_dict

            above = self.__shadow_radiu
            below = self.height() - self.__shadow_radiu
            left = self.__shadow_radiu
            right = self.width() - self.__shadow_radiu
            self.__centers_dict: dict[str, QtCore.QPointF] = {
                "upperL": QtCore.QPointF(left, above),
                "upperR": QtCore.QPointF(right, above),
                "lowerL": QtCore.QPointF(left, below),
                "lowerR": QtCore.QPointF(right, below)
            }



        ### 重写类函数 ###
        def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QColor(QtCore.Qt.transparent))
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            pie_rect_width = 2 * self.__shadow_radiu
            self.__pie_gradient.setCenterRadius(self.__shadow_radiu)

            self.__pie_gradient.setCenter(self.__centers_dict.get("upperL"))
            self.__pie_gradient.setFocalPoint(self.__centers_dict.get("upperL"))
            painter.setBrush(self.__pie_gradient)
            painter.drawPie(
                QtCore.QRectF(
                    self.__centers_dict.get("upperL").x() - self.__shadow_radiu,
                    self.__centers_dict.get("upperL").y() - self.__shadow_radiu,
                    pie_rect_width, 
                    pie_rect_width
                ),
                90 * 16,
                90 * 16
            )

            self.__pie_gradient.setCenter(self.__centers_dict.get("upperR"))
            self.__pie_gradient.setFocalPoint(self.__centers_dict.get("upperR"))
            painter.setBrush(self.__pie_gradient)
            painter.drawPie(
                QtCore.QRectF(
                    self.__centers_dict.get("upperR").x() - self.__shadow_radiu,
                    self.__centers_dict.get("upperR").y() - self.__shadow_radiu,
                    pie_rect_width, 
                    pie_rect_width
                ),
                0 * 16,
                90 * 16
            )

            self.__pie_gradient.setCenter(self.__centers_dict.get("lowerL"))
            self.__pie_gradient.setFocalPoint(self.__centers_dict.get("lowerL"))
            painter.setBrush(self.__pie_gradient)
            painter.drawPie(
                QtCore.QRectF(
                    self.__centers_dict.get("lowerL").x() - self.__shadow_radiu,
                    self.__centers_dict.get("lowerL").y() - self.__shadow_radiu,
                    pie_rect_width, 
                    pie_rect_width
                ),
                180 * 16,
                90 * 16
            )

            self.__pie_gradient.setCenter(self.__centers_dict.get("lowerR"))
            self.__pie_gradient.setFocalPoint(self.__centers_dict.get("lowerR"))
            painter.setBrush(self.__pie_gradient)
            painter.drawPie(
                QtCore.QRectF(
                    self.__centers_dict.get("lowerR").x() - self.__shadow_radiu,
                    self.__centers_dict.get("lowerR").y() - self.__shadow_radiu,
                    pie_rect_width, 
                    pie_rect_width
                ),
                270 * 16,
                90 * 16
            )

            self.__rect_gradient.setStart(self.__shadow_width, 0)
            self.__rect_gradient.setFinalStop(0, 0)
            painter.setBrush(self.__rect_gradient)
            painter.drawRect(
                QtCore.QRectF(
                    0, 
                    self.__centers_dict.get("upperL").y(), 
                    self.__shadow_width, 
                    self.__bind_obj.height() - 2 * self.__bind_obj.radius()
                )
            )

            self.__rect_gradient.setStart(0, self.__shadow_width)
            self.__rect_gradient.setFinalStop(0, 0)
            painter.setBrush(self.__rect_gradient)
            painter.drawRect(
                QtCore.QRectF(
                    self.__centers_dict.get("upperL").x(),
                    0,
                    self.__bind_obj.width() - 2 * self.__bind_obj.radius(),
                    self.__shadow_width
                )
            )

            self.__rect_gradient.setStart(self.width() - self.__shadow_width, 0)
            self.__rect_gradient.setFinalStop(self.width(), 0)
            painter.setBrush(self.__rect_gradient)
            painter.drawRect(
                QtCore.QRectF(
                    self.width() - self.__shadow_width,
                    self.__centers_dict.get("upperR").y(),
                    self.__shadow_width, 
                    self.__bind_obj.height() - 2 * self.__bind_obj.radius()
                )
            )
            
            self.__rect_gradient.setStart(0, self.height() - self.__shadow_width)
            self.__rect_gradient.setFinalStop(0, self.height())
            painter.setBrush(self.__rect_gradient)
            painter.drawRect(
                QtCore.QRectF(
                    self.__centers_dict.get("lowerL").x(),
                    self.height() - self.__shadow_width,
                    self.__bind_obj.width() - 2 * self.__bind_obj.radius(),
                    self.__shadow_width
                )
            )

            return super().paintEvent(a0)
            


        ### 定义类函数 ###
        def setColorAt(self, pos, color) -> None:
            a = self.__bind_obj.radius() / self.__shadow_radiu
            b = self.__shadow_width / self.__shadow_radiu
            self.__rect_gradient.setColorAt(pos, color)
            self.__pie_gradient.setColorAt(a + b * pos, color)
            self.update()
        


        def clearGradient(self) -> None:
            del self.__pie_gradient, self.__rect_gradient
            self.__pie_gradient = QtGui.QRadialGradient()
            self.__rect_gradient = QtGui.QLinearGradient()



        def setShadowWidth(self, width: int | float) -> None:
            self.__shadow_width = width
            self.__shadow_radiu = self.__bind_obj.radius() + self.__shadow_width
            self.setGeometry(
                self.__bind_obj.x() - self.__shadow_width,
                self.__bind_obj.y() - self.__shadow_width,
                self.__bind_obj.width() + 2 * self.__shadow_width,
                self.__bind_obj.height() + 2 * self.__shadow_width
            )
            self.__setCenterDict()
            self.update()



    ### ========================================================================================================= ###



    ### 函数重载 ###
    @typing.overload
    def __init__(self) -> None: pass
    @typing.overload
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None: pass
    @typing.overload
    def __init__(self, parent: QtWidgets.QWidget | None = ..., bind_obj: RoundedWidget | None = ...) -> None: pass



    ### 构造函数（ShadowFrame） ###
    def __init__(
        self, 
        parent: QtWidgets.QWidget | None = None, 
        bind_obj: RoundedWidget | None = None
    ) -> None:

        if  (parent is not None and not isinstance(parent, QtWidgets.QWidget)) or \
            (bind_obj is not None and not isinstance(bind_obj, RoundedWidget)) or \
            (parent is None and bind_obj is not None):
            raise TypeError("Parameter passed error!")
        elif isinstance(parent, QtWidgets.QWidget) and isinstance(bind_obj, RoundedWidget):
            if parent is not bind_obj.parent():
                raise TypeError("Parameter passed error!, the parent of 'bind_obj' is not the parameter 'parent'")

        ### private属性 ###
        self.__parent:          QtWidgets.QWidget = parent
        self.__shadow:          self.__ShadowPainter = None
        self.__shadow_width:    int | float = 15

        self.__gradient_color_list: list = [
            [0, QtGui.QColor(0, 0, 0, 0)],
            [1, QtGui.QColor(0, 0, 0, 0)]
        ]
        
        ### 初始化 ###
        if bind_obj is not None and parent is not None:
            self.__shadow = self.__ShadowPainter(parent, bind_obj, self.__shadow_width)



    ### private类函数 ###
    def __flash(self) -> None:
        self.__shadow.clearGradient()
        for i in range(len(self.__gradient_color_list)):
            self.__shadow.setColorAt(self.__gradient_color_list[i][0], self.__gradient_color_list[i][1])



    ### 定义类函数 ###
    def setBindObject(self, bind_obj: RoundedWidget) -> None:
        if not isinstance(bind_obj, RoundedWidget):
            raise TypeError("Parameter passed error! The parameter type must be 'RoundedWidget'.")
        elif self.__parent is None:
            raise AttributeError("The 'parent' of the frame is None")
        
        if self.__shadow is not None:
            self.__shadow.deleteLater()
            del self.__shadow
        self.__shadow = self.__ShadowPainter(self.__parent, bind_obj, self.__shadow_width)
        self.__flash()
    


    def setParent(self, parent: QtWidgets.QWidget) -> None:
        if not isinstance(parent, QtWidgets.QWidget):
            raise TypeError("Parameter passed error! The parameter type must be 'QWidget'.")
        elif self.__parent is not None:
            del self.__parent
        self.__parent = parent
    


    def setColorAt(self, pos: int | float, color: QtGui.QColor) -> None:
        if not (isinstance(pos, (int, float)) and isinstance(color, QtGui.QColor)):
            raise TypeError("Parameter passed error!")
        elif self.__parent is None:
            raise AttributeError("The 'parent' of the frame is None")
        elif self.__shadow is None:
            raise AttributeError("The 'bind_obj' of the frame is None")
        
        judge = True
        position = pos

        if pos < 0: 
            position = 0
        elif pos > 1: 
            position = 1

        for i in range(len(self.__gradient_color_list)):
            if position == self.__gradient_color_list[i][0]:
                self.__gradient_color_list[i][1] = QtGui.QColor(color)
                judge = False
                break
        if judge:
            self.__gradient_color_list.append(list([position, QtGui.QColor(color)]))

        self.__flash()



    def setShadowWidth(self, width: int | float) -> None:
        if not isinstance(width, (int, float)):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        elif self.__parent is None:
            raise AttributeError("The 'parent' of the frame is None")
        elif self.__shadow is None:
            raise AttributeError("The 'bind_obj' of the frame is None")
        
        if width < 0:
            self.__shadow_width = 0
        else:
            self.__shadow_width = width
        self.__shadow.setShadowWidth(self.__shadow_width)
        self.__flash()
    


    def shadowWidth(self) -> int | float:
        return self.__shadow_width
    


    def resetColor(self) -> None:
        if self.__parent is None:
            raise AttributeError("The 'parent' of the frame is None")
        elif self.__shadow is None:
            raise AttributeError("The 'bind_obj' of the frame is None")
        
        del self.__gradient_color_list
        self.__gradient_color_list = [
            [0, QtGui.QColor(0, 0, 0, 0)],
            [1, QtGui.QColor(0, 0, 0, 0)]
        ]
        self.__flash()



    def deleteLater(self) -> None:
        if self.__shadow is not None:
            self.resetColor()
            self.__shadow.deleteLater()
            self.__shadow = None
                




### ============================================================================================================= ###
### ============================================================================================================= ###
### ============================================================================================================= ###





### -----圆角窗口----- ###
class RoundedWindow(RoundedWidget):

    LIGHT_STYLE:    int = 0x00
    DARK_STYLE:     int = 0x01
    resized:        QtCore.pyqtSignal = QtCore.pyqtSignal()



    ### -----窗体框架（私有类）----- ###
    class __Frame(RoundedWidget):
        
        resized:        QtCore.pyqtSignal = QtCore.pyqtSignal()



        ### -----窗口按钮（私有类）----- ###
        class __WindowButton(QtWidgets.QWidget):

            clicked:    QtCore.pyqtSignal = QtCore.pyqtSignal()
            entered:    QtCore.pyqtSignal = QtCore.pyqtSignal()
            left:       QtCore.pyqtSignal = QtCore.pyqtSignal()

            def __init__(self, parent: QtWidgets.QWidget) -> None:
                super().__init__(parent)
                self.button_state: int = 0        # 0: normal, 1: entered, 2: pressed
                self.color_list: list = None
                

            def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
                if (
                    0 < a0.x() < self.width() and 
                    0 < a0.y() < self.height() and 
                    a0.button() == QtCore.Qt.MouseButton.LeftButton
                ):
                    self.clicked.emit()
                self.update()
                return super().mouseReleaseEvent(a0)
            

            def enterEvent(self, a0: QtCore.QEvent) -> None:
                self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
                self.entered.emit()
                self.button_state = 1
                self.update()
                return super().enterEvent(a0)


            def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
                self.button_state = 2
                self.update()
                return super().mousePressEvent(a0)
            

            def leaveEvent(self, a0: QtCore.QEvent) -> None:
                self.left.emit()
                self.button_state = 0
                self.update()
                return super().leaveEvent(a0)



        ### ========================================================================================================= ###



        ### -----关闭按钮（私有类）----- ###
        class __CloseButton(__WindowButton):

            def __init__(self, parent: QtWidgets.QWidget) -> None:
                super().__init__(parent)
            

            def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
                painter = QtGui.QPainter(self)
                pen = QtGui.QPen()
                rect_center = self.width() / 2

                painter.setBrush(QtGui.QColor(QtCore.Qt.transparent))
                pen.setWidthF(1.5)
                pen.setColor(self.color_list[self.button_state])
                painter.setPen(pen)
                
                painter.drawLine(
                    QtCore.QPointF(rect_center - 5, rect_center - 5),
                    QtCore.QPointF(rect_center + 5, rect_center + 5)
                )
                painter.drawLine(
                    QtCore.QPointF(rect_center + 5, rect_center - 5), 
                    QtCore.QPointF(rect_center - 5, rect_center + 5)
                )

                return super().paintEvent(a0)
        


        ### ========================================================================================================= ###



        ### -----最小化按钮（私有类）----- ###
        class __MinimizeButton(__WindowButton):

            def __init__(self, parent: QtWidgets.QWidget) -> None:
                super().__init__(parent)
                self.timer:       QtCore.QTimer = QtCore.QTimer(self)
                self.offset:      int = 0
                self.count:       int = 0

                self.timer.setInterval(20)
                self.entered.connect(self.timer.start)
                self.left.connect(self.timer.start)
                self.timer.timeout.connect(self.__flush)


            def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
                painter = QtGui.QPainter(self)
                pen = QtGui.QPen()
                rect_center = self.width() / 2

                painter.setBrush(QtGui.QColor(QtCore.Qt.transparent))
                pen.setWidthF(1.5)
                pen.setColor(self.color_list[self.button_state])
                painter.setPen(pen)

                painter.drawLine(
                    QtCore.QPointF(rect_center + 6.5, self.height() / 2 + self.offset),
                    QtCore.QPointF(rect_center - 6.5, self.height() / 2 + self.offset)
                )

                return super().paintEvent(a0)
            

            def __flush(self) -> None:
                if self.count == 6:
                    self.timer.stop()
                    self.count = 0
                    
                    if self.button_state == 1:
                        self.offset = 6
                    else:
                        self.offset = 0
                    self.update()
                    return
                
                if self.button_state == 1:
                    self.offset += 1
                elif self.offset > 0:
                    self.offset -= 1

                self.count += 1
                self.update()
        


        ### ========================================================================================================= ###



        ### -----最大化按钮（私有类）----- ###
        class __MaximizeButton(__WindowButton):
            
            def __init__(self, parent: QtWidgets.QWidget) -> None:
                super().__init__(parent)
                self.__change_icon = False


            def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
                painter = QtGui.QPainter(self)
                pen = QtGui.QPen()
                rect_center = self.width() / 2

                painter.setBrush(QtGui.QColor(QtCore.Qt.transparent))
                pen.setWidthF(1.5)
                pen.setColor(self.color_list[self.button_state])
                painter.setPen(pen)

                if not self.__change_icon:
                    painter.drawRect(
                        QtCore.QRectF(
                            QtCore.QPointF(rect_center - 7, rect_center - 6),
                            QtCore.QPointF(rect_center + 7, rect_center + 6)
                        )
                    )
                    
                else:
                    painter.drawRect(
                        QtCore.QRectF(
                            QtCore.QPointF(rect_center - 7, rect_center - 3),
                            QtCore.QPointF(rect_center + 4, rect_center + 6)
                        )
                    )
                    painter.drawLine(
                        QtCore.QPointF(rect_center - 3, rect_center - 6),
                        QtCore.QPointF(rect_center + 7, rect_center - 6)
                    )
                    painter.drawLine(
                        QtCore.QPointF(rect_center + 7, rect_center - 6),
                        QtCore.QPointF(rect_center + 7, rect_center + 1)
                    )
                
                return super().paintEvent(a0)
            

            def changeIcon(self) -> None:
                self.__change_icon = not self.__change_icon
                self.update()



        ### ========================================================================================================= ###



        ### 构造函数（__Frame） ###
        def __init__(self, window_style: int = None) -> None:
            super().__init__()

            ### private属性 ###
            self.__mouse_pos:               QtCore.QPoint = None
            self.__mouse_global_pos:        QtCore.QPoint = None
            self.__mouse_pressed:           bool = False
            self.__geometry_disabled:       bool = False
            self.__pressed_area:            int = 0      # 0: None, 1: above, 2: below, 3: left, 4: right, 5: move area
            self.__original_size:           QtCore.QSize = None
            self.__close_button:            self.__CloseButton = self.__CloseButton(self)
            self.__max_button:              self.__MaximizeButton = self.__MaximizeButton(self)
            self.__min_button:              self.__MinimizeButton = self.__MinimizeButton(self)

            
            ### public属性 ###
            self.move_area_width:           int = 24
            self.resize_area_width:         int = 5
            self.win_button_offset:         int = 10
            self.enable_resize:             bool = True
            self.frame_radius:              int | float = 25


            ### 初始化 ###
            self.setWindowStyle(window_style)
            self.setRadius(self.frame_radius)
            self.setBottomVisible(False)
            self.setBottomWidth(0)
            self.setMouseTracking(True)
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.setMinimumSize(0, 0)

            self.__close_button.entered.connect(self.__geometryDisabled)
            self.__close_button.left.connect(self.__geometryEnabled)
            self.__close_button.clicked.connect(self.close)
            self.__max_button.entered.connect(self.__geometryDisabled)
            self.__max_button.left.connect(self.__geometryEnabled)
            self.__max_button.clicked.connect(self.__maxButtonClicked)
            self.__min_button.entered.connect(self.__geometryDisabled)
            self.__min_button.left.connect(self.__geometryEnabled)
            self.__min_button.clicked.connect(self.showMinimized)
            


        ### private类函数 ###
        def __setCursor(self, a0: QtGui.QMouseEvent) -> None:
            if not self.isMaximized():
                if (a0.y() <= self.resize_area_width or a0.y() >= self.height() - self.resize_area_width) and self.enable_resize:
                    self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)
                elif (a0.x() <= self.resize_area_width or a0.x() >= self.width() - self.resize_area_width) and self.enable_resize:
                    self.setCursor(QtCore.Qt.CursorShape.SizeHorCursor)
                elif self.resize_area_width < a0.y() <= self.move_area_width + self.resize_area_width:
                    self.unsetCursor()
                else:
                    self.unsetCursor()
                    self.__geometryDisabled()
                    return
                self.__geometryEnabled()



        def __geometryDisabled(self) -> None:
            self.__geometry_disabled = True



        def __geometryEnabled(self) -> None:
            self.__geometry_disabled = False
        


        def __maxButtonClicked(self) -> None:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
            
        

        ### 重写类函数 ###
        def showMaximized(self) -> None:
            if not self.isMaximized():
                self.__max_button.changeIcon()
            super().showMaximized()
            self.setRadius(0)
            self.unsetCursor()
            self.setButtonPosition()
            self.resized.emit()

        

        def showMinimized(self) -> None:
            super().showMinimized()
            self.setButtonPosition()
            self.resized.emit()
        


        def showNormal(self) -> None:
            if self.isMaximized():
                self.__max_button.changeIcon()
            super().showNormal()
            self.setRadius(self.frame_radius)
            self.setButtonPosition()
            self.resized.emit()


   
        def resize(self, w: int, h: int) -> None:
            super().resize(w, h)
            self.setButtonPosition()
            self.resized.emit()
        


        def setGeometry(self, ax: int, ay: int, aw: int, ah: int) -> None:
            self.move(ax, ay)
            self.resize(aw, ah)
        


        def setMinimumWidth(self, minw: int) -> None:
            if minw < self.move_area_width * 3 + 80:
                return super().setMinimumWidth(self.move_area_width * 3 + 80)
            return super().setMinimumWidth(minw)



        def setMinimumHeight(self, minh: int) -> None:
            if minh < self.move_area_width + 2 * (self.resize_area_width + 3) + 3:
                return super().setMinimumHeight(self.move_area_width + 2 * (self.resize_area_width + 3) + 3)
            return super().setMinimumHeight(minh)



        def setMaximumWidth(self, maxw: int) -> None:
            if maxw < self.move_area_width * 3 + 80:
                return super().setMinimumWidth(self.move_area_width * 3 + 80)
            return super().setMaximumWidth(maxw)
        


        def setMaximumHeight(self, maxh: int) -> None:
            if maxh < self.move_area_width + 2 * (self.resize_area_width + 3) + 3:
                return super().setMinimumHeight(self.move_area_width + 2 * (self.resize_area_width + 3) + 3)
            return super().setMaximumHeight(maxh)



        def setMinimumSize(self, minw: int, minh: int) -> None:
            self.setMinimumWidth(minw)
            self.setMinimumHeight(minh)



        def setMaximumSize(self, maxw: int, maxh: int) -> None:
            self.setMaximumWidth(maxw)
            self.setMaximumHeight(maxh)



        def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
            if self.__geometry_disabled or self.isMaximized():
                return super().mousePressEvent(a0)
            
            self.__mouse_pressed = True
            self.__mouse_pos = QtCore.QPoint(a0.pos())
            self.__mouse_global_pos = QtCore.QPoint(a0.globalPos())
            self.__original_size = QtCore.QSize(self.size())
            
            if (
                self.resize_area_width < a0.y() <= self.move_area_width + self.resize_area_width and
                self.resize_area_width < a0.x() < self.width() - self.resize_area_width and
                a0.button() == QtCore.Qt.MouseButton.LeftButton
            ):
                self.__pressed_area = 5

            elif self.enable_resize:
                if a0.y() <= self.resize_area_width:
                    self.__pressed_area = 1
                elif a0.y() >= self.height() - self.resize_area_width:
                    self.__pressed_area = 2
                elif a0.x() <= self.resize_area_width:
                    self.__pressed_area = 3
                elif a0.x() >= self.width() - self.resize_area_width:
                    self.__pressed_area = 4

            return super().mousePressEvent(a0)



        def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
            self.__mouse_pressed = False
            self.__mouse_pos = None
            self.__pressed_area = 0
            self.__original_size = None
            self.__setCursor(a0)
            return super().mouseReleaseEvent(a0)
        


        def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
            if not self.__mouse_pressed:
                self.__setCursor(a0)
                return super().mouseMoveEvent(a0)

            match self.__pressed_area:
                case 5:     # move
                    self.move(
                        a0.globalX() - self.__mouse_pos.x(),
                        a0.globalY() - self.__mouse_pos.y()
                    )

                case 1:     # above resize
                    if self.height() != self.minimumHeight() and self.height() != self.maximumHeight():
                        self.move(
                            self.x(),
                            a0.globalY() - self.__mouse_pos.y()
                        )
                    self.resize(
                        self.__original_size.width(),
                        self.__original_size.height() - (a0.globalY() - self.__mouse_global_pos.y())
                    )

                case 2:     # below resize
                    self.resize(
                        self.__original_size.width(),
                        self.__original_size.height() + (a0.globalY() - self.__mouse_global_pos.y())
                    )

                case 3:     # left resize
                    if self.width() != self.minimumWidth() and self.width() != self.maximumWidth():
                        self.move(
                            a0.globalX() - self.__mouse_pos.x(),
                            self.y()
                        )
                    self.resize(
                        self.__original_size.width() - (a0.globalX() - self.__mouse_global_pos.x()),
                        self.__original_size.height()
                    )

                case 4:     # right resize
                    self.resize(
                        self.__original_size.width() + (a0.globalX() - self.__mouse_global_pos.x()),
                        self.__original_size.height()
                    )

            return super().mouseMoveEvent(a0)
        


        ### 定义类函数 ###
        def setButtonPosition(self) -> None:
            self.__close_button.setGeometry(
                self.width() - (self.win_button_offset + self.move_area_width), 
                self.resize_area_width, 
                self.move_area_width,
                self.move_area_width
            )
            self.__max_button.setGeometry(
                self.width() - (self.win_button_offset + self.move_area_width + self.move_area_width + 10), 
                self.resize_area_width, 
                self.move_area_width, 
                self.move_area_width
            )
            self.__min_button.setGeometry(
                self.width() - (self.win_button_offset + self.move_area_width + 2 * self.move_area_width + 20), 
                self.resize_area_width, 
                self.move_area_width, 
                self.move_area_width
            )
        


        def setWindowStyle(self, window_style: int) -> None:
            match window_style:
                case None | 0x00:
                    self.setBackgroundColor(240, 240, 240)
                    self.__close_button.color_list = [
                        QtGui.QColor(50, 50, 50),
                        QtGui.QColor(220, 0, 0),
                        QtGui.QColor(135, 0, 0)
                    ]
                    self.__max_button.color_list = [
                        QtGui.QColor(50, 50, 50),
                        QtGui.QColor(100, 100, 100),
                        QtGui.QColor(40, 40, 40)
                    ]
                    self.__min_button.color_list = [
                        QtGui.QColor(50, 50, 50),
                        QtGui.QColor(100, 100, 100),
                        QtGui.QColor(40, 40, 40)
                    ]

                case 0x01:
                    self.setBackgroundColor(20, 20, 45)
                    self.__close_button.color_list = [
                        QtGui.QColor(200, 200, 200),
                        QtGui.QColor(220, 0, 0),
                        QtGui.QColor(135, 0, 0)
                    ]
                    self.__max_button.color_list = [
                        QtGui.QColor(200, 200, 200),
                        QtGui.QColor(255, 255, 255),
                        QtGui.QColor(150, 150, 150)
                    ]
                    self.__min_button.color_list = [
                        QtGui.QColor(200, 200, 200),
                        QtGui.QColor(255, 255, 255),
                        QtGui.QColor(150, 150, 150)
                    ]



    ### ========================================================================================================= ###



    ### 函数重载 ###
    @typing.overload
    def __init__(self) -> None: pass
    @typing.overload
    def __init__(self, window_style: int | None = ...) -> None: pass

    @typing.overload
    def frameResize(self, a0: QtCore.QSize) -> None: pass
    @typing.overload
    def frameResize(self, w: int, h: int) -> None: pass

    @typing.overload
    def resize(self, a0: QtCore.QSize) -> None: pass
    @typing.overload
    def resize(self, w: int, h: int) -> None: pass

    @typing.overload
    def setGeometry(self, a0: QtCore.QRect) -> None: pass
    @typing.overload
    def setGeometry(self, ax: int, ay: int, aw: int, ah: int) -> None: pass

    @typing.overload
    def setMaximumSize(self, maxw: int, maxh: int) -> None: pass
    @typing.overload
    def setMaximumSize(self, s: QtCore.QSize) -> None: pass

    @typing.overload
    def setMinimumSize(self, minw: int, minh: int) -> None: pass
    @typing.overload
    def setMinimumSize(self, s: QtCore.QSize) -> None: pass

    @typing.overload
    def move(self, a0: QtCore.QPoint) -> None: pass
    @typing.overload
    def move(self, ax: int, ay: int) -> None: pass

    @typing.overload
    def setBackgroundColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setBackgroundColor(self, color: QtGui.QColor) -> None: pass

    @typing.overload
    def setBottomColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setBottomColor(self, color: QtGui.QColor) -> None: pass


    
    ### 构造函数（RoundedWindow） ###
    def __init__(self, a0 = None) -> None:
        super().__init__()
        
        ### private属性 ###
        self.__frame:           self.__Frame = self.__Frame(a0)
        self.__offset_w:        int = None
        self.__offset_h:        int = None
        

        ### 初始化 ###
        self.setParent(self.__frame)
        super().setRadius(0)
        super().setBottomWidth(0)
        super().setBottomVisible(False)
        super().setBackgroundColor(0, 0, 0, 0)
        self.__frame.resized.connect(self.__setPosition)
        self.__frame.resize(500, 400)
        self.__offset_w = self.__frame.width() - self.width()
        self.__offset_h = self.__frame.height() - self.height()
        


    ### private类函数 ###
    def __setPosition(self) -> None:
        y = self.__frame.resize_area_width + self.__frame.move_area_width + 3
        height = (
            self.__frame.height() - 
            self.__frame.move_area_width - 
            self.__frame.resize_area_width - 
            self.__frame.radius()
        )

        if self.__frame.radius() < self.__frame.resize_area_width + 3:
            height = (
                self.__frame.height() - 
                self.__frame.move_area_width - 
                2 * (self.__frame.resize_area_width + 3)
            )

        if self.__frame.radius() > self.__frame.resize_area_width + self.__frame.move_area_width + 3:
            y = self.__frame.radius()

        super().setGeometry(
            self.__frame.resize_area_width + 3,
            y,
            self.__frame.width() - 2 * (self.__frame.resize_area_width + 3),
            height
        )
        self.resized.emit()



    ### 重写类函数 ###
    def show(self) -> None:
        self.__frame.show()
    


    def close(self) -> None:
        self.__frame.close()
    


    def resize(self, a0: int | QtCore.QSize, a1: int = None) -> None:
        if isinstance(a0, int) and isinstance(a1, int):
            self.__frame.resize(a0 + self.__offset_w, a1 + self.__offset_h)
        elif isinstance(a0, QtCore.QSize) and a1 is None:
            self.__frame.resize(a0.width() + self.__offset_w, a0.height() + self.__offset_h)
        else:
            raise TypeError("Parameter passed error!")
    


    def setGeometry(
            self, a0: int | QtCore.QRect, 
            a1: int | None = None, 
            a2: int | None = None, 
            a3: int | None = None
    ) -> None:
        
        if isinstance(a0, QtCore.QRect) and a1 is None and a2 is None and a3 is None:
            self.__frame.setGeometry(a0.x(), a0.y(), a0.width(), a0.height())
        elif isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and isinstance(a3, int):
            self.__frame.setGeometry(a0, a1, a2, a3)
        else:
            raise TypeError("Parameter passed error!")
    


    def setMaximumWidth(self, maxw: int) -> None:
        if isinstance(maxw, int):
            self.__frame.setMaximumWidth(maxw + self.__offset_w)
            self.__setPosition()
            self.__frame.setButtonPosition()
        else:
            raise TypeError("Parameter passed error!")
    


    def setMaximumHeight(self, maxh: int) -> None:
        if isinstance(maxh, int):
            self.__frame.setMaximumHeight(maxh + self.__offset_h)
            self.__setPosition()
            self.__frame.setButtonPosition()
        else:
            raise TypeError("Parameter passed error!")
        self.setMinimumHeight()


    
    def setMaximumSize(self, a0: int | QtCore.QSize, a1: int | None = None) -> None:
        if isinstance(a0, QtCore.QSize) and a1 is None:
            self.__frame.setMaximumSize(a0.width() + self.__offset_w, a0.height() + self.__offset_h)
        elif isinstance(a0, int) and isinstance(a1, int):
            self.__frame.setMaximumSize(a0 + self.__offset_w, a1 + self.__offset_h)
        else:
            raise TypeError("Parameter passed error!")
        
        self.__setPosition()
        self.__frame.setButtonPosition()
    


    def setMinimumWidth(self, minw: int) -> None:
        if isinstance(minw, int):
            self.__frame.setMinimumWidth(minw + self.__offset_w)
            self.__setPosition()
            self.__frame.setButtonPosition()
        else:
            raise TypeError("Parameter passed error!")



    def setMinimumHeight(self, minh: int) -> None:
        if isinstance(minh, int):
            self.__frame.setMinimumHeight(minh + self.__offset_h)
            self.__setPosition()
            self.__frame.setButtonPosition()
        else:
            raise TypeError("Parameter passed error!")
    


    def setMinimumSize(self, a0: int | QtCore.QSize, a1: int | None = None) -> None:
        if isinstance(a0, QtCore.QSize) and a1 is None:
            self.__frame.setMinimumSize(a0.width() + self.__offset_w, a0.height() + self.__offset_h)
        elif isinstance(a0, int) and isinstance(a1, int):
            self.__frame.setMinimumSize(a0 + self.__offset_w, a1 + self.__offset_h)
        else:
            raise TypeError("Parameter passed error!")
        
        self.__setPosition()
        self.__frame.setButtonPosition()
    


    def isWindow(self) -> bool:
        return self.__frame.isWindow()



    def move(self, a0: int | QtCore.QPoint, a1: int | None = None) -> None:
        self.__frame.move(a0, a1)
    

    
    def showMaximized(self) -> None:
        self.__frame.showMaximized()



    def showNormal(self) -> None:
        self.__frame.showNormal()



    def showMinimized(self) -> None:
        self.__frame.showMinimized()
    


    def isMaximized(self) -> bool:
        return self.__frame.isMaximized()



    def isMinimized(self) -> bool:
        return self.__frame.isMinimized()
    


    def frameSize(self) -> QtCore.QSize:
        return QtCore.QSize(self.__frame.size())
    


    def pos(self) -> QtCore.QPoint:
        return QtCore.QPoint(self.__frame.pos())
    


    def frameGeometry(self) -> QtCore.QRect:
        return QtCore.QRect(self.__frame.geometry())
    


    def setBackgroundColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__frame.setBackgroundColor(a0, a1, a2, a3)
    


    def setBottomVisible(self, judge: bool) -> None:
        self.__frame.setBottomVisible(judge)
    


    def setBottomColor(
        self, 
        a0: int | QtGui.QColor, 
        a1: int | None = None, 
        a2: int | None = None, 
        a3: int | None = None
    ) -> None:
        self.__frame.setBottomColor(a0, a1, a2, a3)
    


    def setBottomWidth(self, width: int | float) -> None:
        self.__frame.setBottomWidth(width)
    


    def backgroundColor(self) -> QtGui.QColor:
        return self.__frame.backgroundColor()
    


    def bottomColor(self) -> QtGui.QColor:
        return self.__frame.bottomColor()
    


    def backgroundOffset(self) -> tuple:
        return self.__frame.backgroundOffset()



    def bottomOffset(self) -> tuple:
        return self.__frame.bottomOffset()
    


    def bottomWidth(self) -> int | float:
        return self.__frame.bottomWidth()
    


    def setBackgroundOffset(
        self, 
        x: int | float, 
        y: int | float, 
        w: int | float, 
        h: int | float
    ) -> None:
        self.__frame.setBackgroundOffset(x, y, w, h)
    


    def setBottomOffset(
        self, 
        x: int | float, 
        y: int | float, 
        w: int | float, 
        h: int | float
    ) -> None:
        self.__frame.setBottomOffset(x, y, w, h)



    def setRadius(self, r: int | float) -> None:
        self.__frame.setRadius(r)
        self.__frame.frame_radius = self.__frame.radius()
    


    def radius(self) -> int | float:
        return self.__frame.radius()
    


    def setBackgroundGradient(self, gradient: QtGui.QGradient) -> None:
        self.__frame.setBackgroundGradient(gradient)



    ### 定义类函数 ###
    def frameResize(self, a0: int | QtCore.QSize, a1: int = None) -> None:
        if isinstance(a0, int) and isinstance(a1, int):
            self.__frame.resize(a0, a1)
        elif isinstance(a0, QtCore.QSize) and a1 is None:
            self.__frame.resize(a0.width(), a0.height())
        else:
            raise TypeError("Parameter passed error!")
    


    def resizeAreaWidth(self) -> int:
        return self.__frame.resize_area_width
    


    def setWinButtonOffset(self, offset: int) -> None:
        if not isinstance(offset, int):
            raise TypeError("Parameter passed error!")
        
        if offset >= 0:
            self.__frame.win_button_offset = offset
        else:
            self.__frame.win_button_offset = 0

        self.__frame.setButtonPosition()

    

    def enableResize(self) -> None:
        self.__frame.enable_resize = True
    


    def disableResize(self) -> None:
        self.__frame.enable_resize = False
    


    def setResizeAreaWidth(self, width: int) -> None:
        if not isinstance(width, int):
            raise TypeError("Parameter passed error!")
        if width >= 0:
            self.__frame.resize_area_width = width
        else:
            self.__frame.resize_area_width = 0
    


    def winButtonOffset(self) -> int:
        return self.__frame.win_button_offset
    


    def resizeEnabled(self) -> bool:
        return self.__frame.enable_resize
    


    def setWindowStyle(self, window_style: int) -> None:
        if not isinstance(window_style, int):
            raise TypeError("Parameter passed error!")
        self.__frame.setWindowStyle(window_style)

    

    def removeGradients(self) -> None:
        self.__frame.removeGradients()