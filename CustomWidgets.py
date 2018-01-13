import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randint

app = QApplication(sys.argv)

#---------------------------------------------------------------------------
# Motor Movement Task
#---------------------------------------------------------------------------

class DragSymbol(QLabel):
    #
    # Definition of Class-properties
    #
    startWithTimer      = False
    #
    # Getter for the member-properties to make the properties available to the environment
    #
    def getStartWithTimer(self):
        return self.startWithTimer
    #
    # Setter for setting the member-properties from environment
    #
    def setStartWithTimer(self, startWithTimer):
        self.startWithTimer = startWithTimer
    #
    # Overwrite the contructor, first call the super constructor and after that do the individual settings
    #
    def __init__(self, parent):
        super(DragSymbol, self).__init__(parent)             # call the constructor of the super class in this case QLabel
        #
        # init the local properties, in our case redundant because they are set in the definition area
        #
        self.imageRand           = 0
        self.startWithTimer      = False
        #QPixmap is an off-screen image representation that can be used as a paint device
        #http://doc.qt.io/qt-5/qpixmap.html#details
        self.setPixmap(QPixmap("ExpCircle.jpg"))
        self.setScaledContents(True)
    #
    # Overwrite the method to handle the mouse move events
    #
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:              # when the event is not!! the left mouse-Button, return without any action
            return                                    # leaves method without doing anything

        #  write the information of which pixmap/image was dragged into MimeData
        mimeData = QMimeData()
        mimeData.setText("{0:d}".format(self.imageRand))

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the Widget (In this case the image of the symbol) and save it as pixmap
        pixmap = QPixmap.grabWidget(self)

        # make pixmap half transparent
        painter = QPainter(pixmap)
        # QPainter performs painting on widgets and other paint devices
        # painter.CompositionMod = Sets how the pixel of the image (the source) are merged with the pixel in another image (the destination)
        # painter.CompositionMode_DestinationIn = The output is the destination, where the alpha is reduced by that of the source
        # painter.fillRect = Fills a rectangle with the brush specified
        # pixmap.rect() = Returns the pixmap's rectangle
        # Q Color = Sets the "ghostish look"
        # Source: http://doc.qt.io/qt-4.8/qpainter.html#CompositionMode-enum
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
        painter.end()
        drag = QDrag(self)                                # make a QDrag, that supports MIME-based drag and drop data transfer: http://doc.qt.io/qt-4.8/qdrag.html#details
        drag.setMimeData(mimeData)                        # put our MimeData
        drag.setPixmap(pixmap)                            # set its Pixmap
        drag.setHotSpot(e.pos())                          # shift the Pixmap so that it coincides with the cursor position

        # start the drag operation
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:

            return

    # Method to start a timer to change the images
    def initChangeImageTimer(self):
        if self.startWithTimer == True:
            self.imageRand = randint(0, 2)
            self.imageTimer = QTimer()
            self.imageTimer.timeout.connect(self.changeImage)
            self.imageTimer.start(600)

    # Method to change the image the method is called by the timer above
    def changeImage(self):

        # In timer option get a new random value as long as the new random is equals to the actual
        if self.startWithTimer == True:

            saveImageRand = self.imageRand
            while self.imageRand == saveImageRand:
                self.imageRand = randint(0, 2)

        if self.imageRand == 0:
            self.setPixmap(QPixmap("ExpCircle.jpg"))
        elif self.imageRand == 1:
            self.setPixmap(QPixmap("ExpTriangle.jpg"))
        else:
            self.setPixmap(QPixmap("ExpQuadrat.jpg"))
#
# Create class to handle the drop (the box)
#

class DropArea(QLabel):
    #
    # Definition of class-properties
    #
    outputLabel         = QLabel()
    successCounter      = 0
    #
    # Getter for the member-properties to make the properties available to the environment
    #
    def getOutputLabel(self):
        return self.outputLabel

    def getSuccessCounter(self):
        return self.successCounter
    #
    # Setter for setting the member-properties from environment
    #
    def setOutputLabel(self, outputLabel):
        self.outputLabel = outputLabel

    def setSuccessCounter(self, successCounter):
        self.successCounter = successCounter

    # method the reset the counter for next round of experiment
    def resetSuccessCounter(self):
        self.successCounter = 0

    #
    # Overwrite the contructor, first call the super constructor and after that do the individual settings
    #
    def __init__(self,parent):
        super(DropArea, self).__init__(parent)  # parent constructor that is needed!
        self.setAcceptDrops(True)               # This will accept drops!
        self.setPixmap(QPixmap("ExpBox.jpg"))   # changes picture of dropEvent!
        self.setScaledContents(True)

        self.outputLabel.setText("")
        self.successCounter      = 0

    def dragEnterEvent(self, e): # Here I specify what happens when event gets dragged!

        if e.mimeData().hasFormat('text/plain'):    # Here I specify the format of the Data that can be dragged in! My Mime Data carries text
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):                                     # What happens when event gets dropped
        result = e.mimeData().text()                            # saves the content of MimeData
        if result == str(0):                                    # 0 = circle symbol
            self.successCounter = self.successCounter + 1       # gain a point
            self.outputLabel.setText(str(self.successCounter))  # refresh the display

#---------------------------------------------------------------------------
# Sentence Comprehension Task
#---------------------------------------------------------------------------

class KeyboardWidget(QWidget):
    keyPressed = pyqtSignal(str)

    def keyPressEvent(self, keyEvent):
        if keyEvent.isAutoRepeat():   # Hinder  people to just keep pressing the button
            return
        #
        # Restrict to the allowed keys
        #
        if (keyEvent.text().upper() == "K" or keyEvent.text().upper() == "L"):
            self.keyPressed.emit(keyEvent.text())


#---------------------------------------------------------------------------
# Distance estimation task
#---------------------------------------------------------------------------

class Ball(QLabel):

    # Overwrite the contructor, first call the super constructor and after that do the individual settings
    #
    def __init__(self, parent):
        super(Ball, self).__init__(parent)             # call the constructor of the super class in this case QLabel
        #
        # init the local properties
        #
        self.setPixmap(QPixmap("ExpCircle.jpg"))
        self.setScaledContents(True)
    #
    # Overwrite the method to handle the mouse move events
    #
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:                         # when the event is not!! the left mouse-Button, return without any action
            return                                               # leaves method without doing anything
        #
        #  write some information into MimeData
        #
        mimeData = QMimeData()
        mimeData.setText('%d,%d' % (e.x(), e.y()))               # write in information about position of the mimeData

        pixmap = QPixmap.grabWidget(self)
        #
        # below makes the pixmap half transparent
        #
        painter = QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
        painter.end()
        drag = QDrag(self)                                                                          # make a QDrag
        drag.setMimeData(mimeData)                                                                  # put our MimeData
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())
        # exec_ will return the accepted action from dropEvent
        # IMPORTANT don't delete this, it returns the Drag Action
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            return


# Create class to handle the drop

class DropFrame(QFrame):

    def __init__(self,parent):
        super(DropFrame, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e): # Here I specify what is accepted as a to be dropped in
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):   # What happens when event gets dropped

        # get the clicked mouse position inside of the object as a text
        mime = e.mimeData().text()
        # now convert the values from a text to x and y coordinates
        # map() = Return an iterator that applies function to every item of iterable, yielding the results
        # https://docs.python.org/3/library/functions.html#map
        x, y = map(int, mime.split(','))  # split the text, convert the single values to integer and map the values to the variables
        # move the object to the new position by taking into account the clicked mouse position
        e.source().move(e.pos() - QPoint(x, y))
        # set the drop action as Move
        e.setDropAction(Qt.MoveAction)
        # tell the QDrag we accepted it
        e.accept()

