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
        self.__radius: int | float = 10
        self.__bottom_width: int | float = 0 
        self.__background_gradient: QtGui.QGradient = None
        self.__draw_bottom: bool = True
        self.__bottom_offset: list = [0, 0, 0, 0]
        self.__background_offset: list = [0, 0, 0, 0]
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



    ### 定义类函数 ###
    def setRadius(self, r: int | float) -> None:
        if not isinstance(r, (int, float)):
            raise TypeError("Parameter passed error! The parameter type must be 'int' or 'float'.")
        if r < 0:
            self.__radius = 0
        else:
            self.__radius = r
        self.update()
         
    

    def raduis(self) -> int | float:
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
            case _: pass
    


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
        
        ### 构造函数 ###
        def __init__(
            self, 
            parent: QtWidgets.QWidget | None = None, 
            bind_obj: RoundedWidget | None = None,
            shadow_width: int | float = None
        ) -> None:
            super().__init__(parent)

            self.__bind_obj = bind_obj
            self.__shadow_width = shadow_width
            self.__shadow_radiu = self.__bind_obj.raduis() + self.__shadow_width
            self.__centers_dict: dict[str, QtCore.QPointF] = None
            self.__pie_gradient = QtGui.QRadialGradient()
            self.__rect_gradient = QtGui.QLinearGradient()

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
                    self.__bind_obj.height() - 2 * self.__bind_obj.raduis()
                )
            )

            self.__rect_gradient.setStart(0, self.__shadow_width)
            self.__rect_gradient.setFinalStop(0, 0)
            painter.setBrush(self.__rect_gradient)
            painter.drawRect(
                QtCore.QRectF(
                    self.__centers_dict.get("upperL").x(),
                    0,
                    self.__bind_obj.width() - 2 * self.__bind_obj.raduis(),
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
                    self.__bind_obj.height() - 2 * self.__bind_obj.raduis()
                )
            )
            
            self.__rect_gradient.setStart(0, self.height() - self.__shadow_width)
            self.__rect_gradient.setFinalStop(0, self.height())
            painter.setBrush(self.__rect_gradient)
            painter.drawRect(
                QtCore.QRectF(
                    self.__centers_dict.get("lowerL").x(),
                    self.height() - self.__shadow_width,
                    self.__bind_obj.width() - 2 * self.__bind_obj.raduis(),
                    self.__shadow_width
                )
            )

            return super().paintEvent(a0)
            


        ### 定义类函数 ###
        def shadowWidth(self) -> int | float:
            return self.__shadow_width



        def setColorAt(self, pos, color) -> None:
            a = self.__bind_obj.raduis() / self.__shadow_radiu
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
            self.__shadow_radiu = self.__bind_obj.raduis() + self.__shadow_width
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



    ### 构造函数 ###
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

        self.__parent: QtWidgets.QWidget = parent
        self.__shadow: self.__ShadowPainter = None
        self.__shadow_width = 15
        self.__gradient_color_list: list = [
            [0, QtGui.QColor(0, 0, 0, 0)],
            [1, QtGui.QColor(0, 0, 0, 0)]
        ]
        
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
        
        judge: bool = True
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