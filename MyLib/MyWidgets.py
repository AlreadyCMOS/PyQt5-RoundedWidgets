"""
（MyWidgets）：自定义控件类库
=============================================
=============================================

class列表：
----------
RoundedWidget（圆角窗体）

RoundedButton（圆角按钮）
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
    def setStrokeColor(self, r: int, g: int, b: int, alpha: int = ...) -> None: pass
    @typing.overload
    def setStrokeColor(self, color: QtGui.QColor) -> None: pass



    ### 构造函数 ###
    def __init__(self, a0: QtWidgets.QWidget | None = None) -> None:
        if a0 is None:
            super().__init__()
        elif isinstance(a0, QtWidgets.QWidget):
            super().__init__(a0)
        else:
            raise TypeError("Parameter passed error!")

        ### private属性 ###
        self.__radius: int | float = 10
        self.__stroke_width: int | float = 0 
        self.__stroke_color: QtGui.QColor = QtGui.QColor(50, 50, 50)
        self.__background_color: QtGui.QColor = QtGui.QColor(240, 240, 240)
        self.__background_gradient: QtGui.QGradient = None



    ### 重写类函数 ###
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)      ### 抗锯齿 ###
        painter.setPen(QtGui.QColor(QtCore.Qt.transparent))

        if self.__stroke_width > 0:
            painter.setBrush(self.__stroke_color)
            painter.drawRoundedRect(self.rect(), self.__radius, self.__radius)

        rect = QtCore.QRectF(
            self.__stroke_width,
            self.__stroke_width,
            self.rect().width() - 2 * self.__stroke_width, 
            self.rect().height() - 2 * self.__stroke_width
        )
        if self.__background_gradient is not None:
            painter.setBrush(self.__background_gradient)
        else:
            painter.setBrush(self.__background_color)
        painter.drawRoundedRect(rect, self.__radius - self.__stroke_width , self.__radius - self.__stroke_width)
        return super().paintEvent(a0)

    

    ### 定义类函数 ###
    def setRadius(self, r: int | float) -> None:
        if isinstance(r, (int, float)):
            self.__radius = r
            self.update()
        else:
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float.")
        
    

    def radius(self) -> int | float:
        return self.__radius
        


    def setBackgroundColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        if isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and (isinstance(a3, int) or a3 is None):
            if a3 is not None: 
                self.__background_color.setRgb(a0, a1, a2, a3)
            else: 
                self.__background_color.setRgb(a0, a1, a2)
        elif isinstance(a0, QtGui.QColor) and a1 is None and a2 is None and a3 is None:
            self.__background_color = QtGui.QColor(a0)
        else:
            raise TypeError("Parameter passed error!")
        self.update()



    def setStrokeWidth(self, width: int | float) -> None:
        if isinstance(width, (int, float)):
            self.__stroke_width = width
            self.update()
        else:
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float.")
    

    
    def setStrokeColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        if isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and (isinstance(a3, int) or a3 is None):
            if a3 is not None:
                self.__stroke_color.setRgb(a0, a1, a2, a3)
            else:
                self.__stroke_color.setRgb(a0, a1, a2)
        elif isinstance(a0, QtGui.QColor) and a1 is None and a2 is None and a3 is None:
            self.__stroke_color = QtGui.QColor(a0)
        else:
            raise TypeError("Parameter passed error!")
        self.update()



    def backgroundColor(self) -> QtGui.QColor:
        color = QtGui.QColor(self.__background_color)
        return color



    def setDarkStyle(self) -> None:
        self.setStrokeColor(200, 200, 200)
        self.setBackgroundColor(20, 20, 45)
        


    def setLightStyle(self) -> None:
        self.setStrokeColor(50, 50, 50)
        self.setBackgroundColor(240, 240, 240)
        


    def setBackgroundGradient(self, gradient: QtGui.QGradient) -> None:
        if not isinstance(gradient, QtGui.QGradient):
            raise TypeError("Parameter passed error! The parameter type must be 'QGradient'.")
        if self.__background_gradient is not None:
            self.__background_gradient = None
        self.__background_gradient = QtGui.QGradient(gradient)
        self.update()
    


    def removeGradients(self) -> None:
        self.__background_gradient = None
        self.update()
    


    def strokeWidth(self) -> int | float:
        return self.__stroke_width
    


    def strokeColor(self) -> QtGui.QColor:
        color = QtGui.QColor(self.__stroke_color)
        return color





### -----圆角按钮----- ###
class RoundedButton(RoundedWidget):

    ### 定义信号 ###
    clicked = QtCore.pyqtSignal()
    entered = QtCore.pyqtSignal()
    pressed = QtCore.pyqtSignal()
    left = QtCore.pyqtSignal()



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
    def __init__(self, a0: QtWidgets.QWidget | str | None = None, a1: str | None = None) -> None:
        if (a0 is not None and a1 is not None) and not isinstance(a0, QtWidgets.QWidget):
            raise TypeError("Parameter passed error!")
        elif isinstance(a0, QtWidgets.QWidget):
            super().__init__(a0)
        else:
            super().__init__()

        ### private属性 ###
        self.__standard_color: dict = {"r": 250, "g": 250, "b": 250, "a": 255}
        self.__pressed_color: dict = {"r": 220, "g": 220, "b": 220, "a": 255}
        self.__entered_color: dict = {"r": 240, "g": 240, "b": 240, "a": 255}
        self.__text_color: QtGui.QColor = QtGui.QColor(50, 50, 50)
        self.__text_lable: QtWidgets.QLabel = QtWidgets.QLabel(self)
        self.__h_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)
        self.__label_palette: QtGui.QPalette = QtGui.QPalette()
        self.__text_font: QtGui.QFont = QtGui.QFont()
        self.__standard_gradient: QtGui.QGradient = None
        self.__entered_gradient: QtGui.QGradient = None
        self.__pressed_gradient: QtGui.QGradient = None

        ### 初始化 ###
        if isinstance(a1, str):
            self.__text_lable.setText(a1)
        elif isinstance(a0, str):
            self.__text_lable.setText(a0)
        self.__text_font.setFamily("微软雅黑")
        self.__text_font.setPointSize(11)
        self.setStrokeColor(50, 50, 50)
        self.setStrokeWidth(1.5)
        self.__text_lable.setAlignment(QtCore.Qt.AlignCenter)   ### 字体居中 ###
        self.__label_palette.setColor(QtGui.QPalette.WindowText, self.__text_color)
        self.__text_lable.setPalette(self.__label_palette)
        self.__h_layout.addWidget(self.__text_lable)
        super().setFont(self.__text_font)
        super().setBackgroundColor(250, 250, 250)



    ### private类函数 ###
    def __changeColorDict(self, a0: int | QtGui.QColor | None, a1: int | None, a2: int | None, a3: int | None, target: dict) -> None:
        if isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and (isinstance(a3, int) or a3 is None):
            if a3 is not None:
                target["a"] = a3
            else:
                target["a"] = 255
            target["r"] = a0
            target["g"] = a1
            target["b"] = a2
        elif isinstance(a0, QtGui.QColor) and a1 is None and a2 is None and a3 is None:
            target["r"] = a0.red()
            target["g"] = a0.green()
            target["b"] = a0.blue()
            target["a"] = a0.alpha()
        else:
            raise TypeError("Parameter passed error!")
    


    ### 重写类函数 ###
    def setBackgroundColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__changeColorDict(a0, a1, a2, a3, self.__standard_color)
        super().setBackgroundColor(
            self.__standard_color.get("r"),
            self.__standard_color.get("g"),
            self.__standard_color.get("b"),
            self.__standard_color.get("a"),
        )



    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.__pressed_gradient is not None:
            super().setBackgroundGradient(self.__pressed_gradient)
        else:
            super().removeGradients()
            super().setBackgroundColor(
                self.__pressed_color.get("r"),
                self.__pressed_color.get("g"),
                self.__pressed_color.get("b"),
                self.__pressed_color.get("a"),
            )
        self.pressed.emit()
        return super().mousePressEvent(a0)



    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.__entered_gradient is not None:
            super().setBackgroundGradient(self.__entered_gradient)
        else:
            super().removeGradients()
            super().setBackgroundColor(
                self.__entered_color.get("r"),
                self.__entered_color.get("g"),
                self.__entered_color.get("b"),
                self.__entered_color.get("a")
            )
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.entered.emit()
        return super().enterEvent(a0)
    


    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.__standard_gradient is not None:
            super().setBackgroundGradient(self.__standard_gradient)
        else:
            super().removeGradients()
            super().setBackgroundColor(
                self.__standard_color.get("r"),
                self.__standard_color.get("g"),
                self.__standard_color.get("b"),
                self.__standard_color.get("a")
            )
        self.left.emit()
        return super().leaveEvent(a0)
    


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.__entered_gradient is not None:
            super().setBackgroundGradient(self.__entered_gradient)
        else:
            super().removeGradients()
            super().setBackgroundColor(
                self.__entered_color.get("r"),
                self.__entered_color.get("g"),
                self.__entered_color.get("b"),
                self.__entered_color.get("a")
            )
        self.clicked.emit()
        return super().mouseReleaseEvent(a0)
    


    def setDarkStyle(self) -> None:
        self.setTextColor(200, 200, 200)
        self.setStrokeColor(200, 200, 200)
        self.setEnteredColor(65, 65, 85)
        self.setPressedColor(50, 50, 70)
        self.setBackgroundColor(40, 40, 60)
        


    def setLightStyle(self) -> None:
        self.setTextColor(50, 50, 50)
        self.setStrokeColor(50, 50, 50)
        self.setEnteredColor(240, 240, 240)
        self.setPressedColor(220, 220, 220)
        self.setBackgroundColor(250, 250, 250)
    


    def setBackgroundGradient(self, gradient: QtGui.QGradient | None) -> None:
        if not isinstance(gradient, QtGui.QGradient):
            raise TypeError("Parameter passed error! The parameter type must be 'QGradient'.")
        if self.__standard_gradient is not None:
            self.__standard_gradient = None
        self.__standard_gradient = QtGui.QGradient(gradient)
        super().setBackgroundGradient(self.__standard_gradient)
    


    def removeGradients(self) -> None:
        self.__standard_gradient = None
        self.__pressed_gradient = None
        self.__entered_gradient = None
        super().removeGradients()
    


    def backgroundColor(self) -> QtGui.QColor:
        color = QtGui.QColor(
            self.__standard_color.get("r"),
            self.__standard_color.get("g"),
            self.__standard_color.get("b"),
            self.__standard_color.get("a"),
        )
        return color
    


    def setFont(self, a0: QtGui.QFont) -> None:
        if isinstance(a0, QtGui.QFont):
            self.__text_font = QtGui.QFont(a0)
            return super().setFont(self.__text_font)
        else:
            raise TypeError("Parameter passed error! The parameter type must be 'QFont'.")
    


    ### 定义类函数 ###
    def setTextSize(self, size: int | float) -> None:
        if isinstance(size, (int, float)):
            self.__text_font.setPointSizeF(float(size))
        else:
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        super().setFont(self.__text_font)



    def setText(self, text: str) -> None:
        if isinstance(text, str):
            self.__text_lable.setText(text)
        else:
            raise TypeError("Parameter passed error! The parameter type must be 'str'.")

    

    def setEnteredColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__changeColorDict(a0, a1, a2, a3, self.__entered_color)



    def setPressedColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__changeColorDict(a0, a1, a2, a3, self.__pressed_color)



    def setTextColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        if isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and (isinstance(a3, int) or a3 is None):
            if a3 is not None:
                self.__text_color.setRgb(a0, a1, a2, a3)
            else:
                self.__text_color.setRgb(a0, a1, a2)
        elif isinstance(a0, QtGui.QColor) and a1 is None and a2 is None and a3 is None:
            self.__text_color = QtGui.QColor(a0)
        else:
            raise TypeError("Parameter passed error!")
        self.__label_palette.setColor(QtGui.QPalette.WindowText, self.__text_color)
        self.__text_lable.setPalette(self.__label_palette)
    


    def pressedColor(self) -> QtGui.QColor:
        color = QtGui.QColor(
            self.__pressed_color.get("r"),
            self.__pressed_color.get("g"),
            self.__pressed_color.get("b"),
            self.__pressed_color.get("a")
        )
        return color

    

    def enteredColor(self) -> QtGui.QColor:
        color = QtGui.QColor(
            self.__entered_color.get("r"),
            self.__entered_color.get("g"),
            self.__entered_color.get("b"),
            self.__entered_color.get("a")
        )
        return color



    def textColor(self) -> QtGui.QColor:
        color = QtGui.QColor(
            self.__text_color.red(),
            self.__text_color.green(),
            self.__text_color.blue(),
            self.__text_color.alpha()
        )
        return color
    


    def setEnteredGradient(self, gradient: QtGui.QGradient) -> None:
        if not isinstance(gradient, QtGui.QGradient):
            raise TypeError("Parameter passed error! The parameter type must be 'QGradient'.")
        if self.__entered_gradient is not None:
            self.__entered_gradient = None
        self.__entered_gradient = QtGui.QGradient(gradient)



    def setPressedGradient(self, gradient: QtGui.QGradient) -> None:
        if not isinstance(gradient, QtGui.QGradient):
            raise TypeError("Parameter passed error! The parameter type must be 'QGradient'.")
        if self.__pressed_gradient is not None:
            self.__pressed_gradient = None
        self.__pressed_gradient = QtGui.QGradient(gradient)



    def text(self) -> str:
        return self.__text_lable.text()
    


    def textSize(self) -> float:
        return self.__text_font.pointSizeF()
    

    
    def font(self) -> QtGui.QFont:
        font = QtGui.QFont(self.__text_font)
        return font
    


    def setTextBold(self) -> None:
        self.__text_font.setBold(True)
        super().setFont(self.__text_font)
    


    def removeTextBold(self) -> None:
        self.__text_font.setBold(False)
        super().setFont(self.__text_font)

    

    def textBold(self) -> bool:
        return self.__text_font.bold()
    


