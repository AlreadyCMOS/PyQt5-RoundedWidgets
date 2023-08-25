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
        self.__background_gradient: QtGui.QGradient = None
        self.__draw_stroke: bool = True
        self.__stroke_offset: list = [0, 0, 0, 0]
        self.__background_offset: list = [0, 0, 0, 0]
        self.__color_dict: dict[str, QtGui.QColor] = {
            "background": QtGui.QColor(240, 240, 240, 255),
            "stroke": QtGui.QColor(50, 50, 50, 255)
        }

    
    
    ### private类函数 ###
    def __setColorDict(self, a0: int | QtGui.QColor, a1: int | None, a2: int | None, a3: int | None, key: str) -> None:
        if isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and (isinstance(a3, int) or a3 is None):
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
            0 + self.__stroke_offset[0],
            0 + self.__stroke_offset[1],
            self.rect().width() + self.__stroke_offset[2], 
            self.rect().height() + self.__stroke_offset[3]
        )

        if self.__draw_stroke:
            painter.setBrush(self.__color_dict.get("stroke"))
            painter.drawRoundedRect(rect, self.__radius, self.__radius)
        
        rect = QtCore.QRectF(
            self.__stroke_width + self.__background_offset[0],
            self.__stroke_width + self.__background_offset[1],
            self.rect().width() - 2 * self.__stroke_width + self.__background_offset[2], 
            self.rect().height() - 2 * self.__stroke_width + self.__background_offset[3]
        )

        if self.__background_gradient is not None:
            painter.setBrush(self.__background_gradient)
        else:
            painter.setBrush(self.__color_dict.get("background"))
        painter.drawRoundedRect(rect, self.__radius - self.__stroke_width , self.__radius - self.__stroke_width)
        return super().paintEvent(a0)



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



    def drawStroke(self, judge: bool) -> None:
        if not isinstance(judge, bool):
            raise TypeError("Parameter passed error! The parameter type must be 'bool'.")
        self.__draw_stroke = judge



    def setBackgroundColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__setColorDict(a0, a1, a2, a3, "background")
        self.update()



    def setStrokeWidth(self, width: int | float) -> None:
        if not isinstance(width, (int, float)):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        self.__stroke_width = width
        self.update()
            
    
    
    def setStrokeColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__setColorDict(a0, a1, a2, a3, "stroke")
        self.update()



    def backgroundColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("background"))



    def setDarkStyle(self) -> None:
        self.setStrokeColor(200, 200, 200)
        self.setBackgroundColor(20, 20, 45)
        


    def setLightStyle(self) -> None:
        self.setStrokeColor(50, 50, 50)
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
    


    def strokeWidth(self) -> int | float:
        return self.__stroke_width
    


    def strokeColor(self) -> QtGui.QColor:
        return QtGui.QColor(self.__color_dict.get("stroke"))
    


    def setStrokeOffset(self, x: int | float, y: int | float, w: int | float, h: int | float) -> None:
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(w, (int, float)) and isinstance(h, (int, float))):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        self.__stroke_offset[0] = x
        self.__stroke_offset[1] = y
        self.__stroke_offset[2] = w
        self.__stroke_offset[3] = h
    


    def setBackgroundOffset(self, x: int | float, y: int | float, w: int | float, h: int | float) -> None:
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(w, (int, float)) and isinstance(h, (int, float))):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        self.__background_offset[0] = x
        self.__background_offset[1] = y
        self.__background_offset[2] = w
        self.__background_offset[3] = h



    def strokeOffset(self) -> tuple:
        return tuple(self.__stroke_offset)
    


    def backgroundOffset(self) -> tuple:
        return tuple(self.__background_offset)





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
        self.__text_lable: QtWidgets.QLabel = QtWidgets.QLabel(self)
        self.__h_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)
        self.__label_palette: QtGui.QPalette = QtGui.QPalette()
        self.__text_font: QtGui.QFont = QtGui.QFont()
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
        self.setStrokeColor(50, 50, 50)
        self.setStrokeWidth(1.5)
        self.__text_lable.setAlignment(QtCore.Qt.AlignCenter)   ### 字体居中 ###
        self.__label_palette.setColor(QtGui.QPalette.WindowText, self.__color_dict.get("text"))
        self.__text_lable.setPalette(self.__label_palette)
        self.__h_layout.addWidget(self.__text_lable)
        super().setFont(self.__text_font)
        super().setBackgroundColor(self.__color_dict.get("standard"))



    ### private类函数 ###
    def __setColorDict(self, a0: int | QtGui.QColor, a1: int | None, a2: int | None, a3: int | None, key: str) -> None:
        if isinstance(a0, int) and isinstance(a1, int) and isinstance(a2, int) and (isinstance(a3, int) or a3 is None):
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
            case _: pass
    


    ### 重写类函数 ###
    def setBackgroundColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__setColorDict(a0, a1, a2, a3, "standard")
        super().setBackgroundColor(self.__color_dict.get("standard"))



    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.__gradient_dict.get("pressed") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("pressed"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("pressed"))
        self.pressed.emit()
        return super().mousePressEvent(a0)



    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.__gradient_dict.get("entered") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("entered"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("entered"))
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.entered.emit()
        return super().enterEvent(a0)
    


    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.__gradient_dict.get("standard") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("standard"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("standard"))
        self.left.emit()
        return super().leaveEvent(a0)
    


    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.__gradient_dict.get("entered") is not None:
            super().setBackgroundGradient(self.__gradient_dict.get("entered"))
        else:
            super().removeGradients()
            super().setBackgroundColor(self.__color_dict.get("entered"))
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
            
    

    def setEnteredColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__setColorDict(a0, a1, a2, a3, "entered")



    def setPressedColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
        self.__setColorDict(a0, a1, a2, a3, "pressed")



    def setTextColor(self, a0: int | QtGui.QColor, a1: int | None = None, a2: int | None = None, a3: int | None = None) -> None:
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
    


