# 06.03.2017
# In the real experiment the Motor Movement Task will lasts for 15 minutes, and there will be more Stimuli in the
# Sentence Comprehension Task and Distance Estimation Task, I cut it down so it is faster to go through.

import sys
import time   # This allows to get the system time
import math   # This allows to import math function
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ass3V9 import *
from random import randint
from os import listdir
from CustomWidgets import *
import random

# pyuic4 -o Ass3V9.py Ass3V9.ui   CONVERSION! TODO Delete this

app = QApplication(sys.argv)
window = QMainWindow()


ui = Ui_MainWindow()
ui.setupUi(window)

# My own code start here!
#
#---------------------------------------------------------------------------
# Main variables
#---------------------------------------------------------------------------
#
# Page Independent Variables
#
window.CondAwayTowards                      = 0                 # 0 = Away and 1 = Towards
window.CondCognitiveNeutral                 = 0                 # 0 = Cogntive Load and 1 = Neutral
window.destinationFile                      = "SPSSfile.csv"    # Resultfile
window.generalTimer                         = QTimer()          # define a general application timer
window.generalTimerCounter                  = 0                 # general counter for timer themes
window.page                                 = 0                 # can be used to set a page
window.widthWidget                          = 1351              # Width of StackedWidget
window.heightWidget                         = 881               # Height of StackedWidget
#
# Page 1 (Consent form)
# at the moment no variables necessary
#
# Page 2 (Demographics)
#
window.page2Age                             = 0
window.page2Gender                          = ""
window.page2Education                       = ""
window.page2Nationality                     = ""
#
# Page 3 (Introduction to Motor movement manipulation)
#
window.page3textDragLabel                   = ""
window.page3textDropLabel                   = ""
window.page3CogntiveLoad                    = ""                    # Stays empty when there is no cognitive load!
#
# Page 4 (Animation movement manipulation)
#
window.RoundPage4 = 0                                               # Which step of the explanation
#
# Page 5 (Motor movement manipulation)
#
window.page5TestTrial                       = True                  # At the beginning we want to start with a test trial!
window.page5seconds                         = 15                    # This is the default time, we assume people start with a test trial
window.page5minutes                         = 0
window.page5TotalCount                      = 0                     # The Number the (correct) symbol was dropped into the container, use for EmailList
#
# Page 6 (Introduction to Language Comprehension Test)
# no variables necessary
#
# Page 7 (Step-by-step explanation Language Comprehension Task)
#
window.RoundPage7                           = 0                         # Beginning of explanation round is 0
#
# Page 8 (Language Comprehension Task)
#
window.page8KKey                            = "K"                      # definition for key k
window.page8LKey                            = "L"                      # definition for key k
window.page8StimuliListFileName             = "Stimuli.csv"            # name of the file that contents the stimuli-informations
window.page8StimuliList                     = []                       # contailer for holding the different read stimuli
window.page8ActiveStimuli                   = 0                        # counter that represents the actual stimuli
window.page8StimuliDetails                  = []                       # list that represents the actual stimuli
window.page8CorrectSensibleAway             = 0                        # All the correct guesses for each type of sentence!
window.page8CorrectSensibleTowards          = 0
window.page8CorrectNonsensibleAway          = 0
window.page8CorrectNonsensibleTowards       = 0
window.page8TrialStart                      = False                    # NEVER touch this value!
window.page8NumberSensibleTowards           = 0                        # counter that represents the number of sensible Towards stimuli
window.page8NumberSensibleAway              = 0                        # counter that represents the number of sensible Away stimuli
window.page8NumberNonsensibleTowards        = 0                        # counter that represents the number of nonsensible Towards stimuli
window.page8NumberNonsensibleAway           = 0                        # counter that represents the number of nonsensible Away stimuli
window.page8StimuliStartTime                = 0
window.page8TestList                        = []                        # List of Test Stimuli
window.page8RealTrialList                   = []                        # List of Real Stimuli
window.page8palette                         = QtGui.QPalette()          # The color of the feedback message
window.page8TestTrial                       = True                      # We begin with a test trial!!
window.page8CorrectDecisionText             = ""                        # Message whether nonsensible/sensible decision was correct
window.page8InTimeText                      = ""                        # Message about whether decision was made in time
# The dependent variables!
window.page8PercentageCorrectSensibleTowards     = 0                         # Percentages of Correct decision for each sentence type
window.page8PercentageCorrectSensibleAway        = 0
window.page8PercentageCorrectNonsensibleTowards  = 0
window.page8PercentageCorrectNonsensibleAway     = 0
window.page8TimeSensibleTowards                  = 0                         # the summary of the descision time sensible Towards
window.page8TimeSensibleAway                     = 0                         # the summary of the descision time sensible Away
window.page8TimeNonsensibleTowards               = 0                         # the summary of the descision time nonsensible Towards
window.page8TimeNonsensibleAway                  = 0                         # the summary of the descision time nonsensible Away
#
# Page 9 Explanation Estimation Task
# no variables necessary
#
# Page 10 Step-by-step explanation Estimation Task
#
window.RoundPage10                           = 0                              # The beginning of the rounds of step-by-step explanation page
#
# Page 11 (Distance estimation task)
#
window.page11minutes                            = 0
window.page11seconds                            = 8                                     # Time you have to make decision
window.page11StartTrial                         = False                                 # DON'T CHANGE THIS !!! This start test trial
window.page11DistanceList                       = [0, 0, 0, 0]                          # !! Keep the Conditions with the same number!!
window.page11DirectionList                      = ["up", "up", "up", "up"]              # Ball place up/below
window.page11RealConditionList                  = ["10 cm","3 cm","12 cm", "7 cm"]    # Real Condition
window.page11TestCondition                      = ["8 cm","5 cm"]              # Test Condition
window.page11activeExperimentRound              = 0                                     # Active ExperimentRound
window.page11TestTrial                          = True                                  # Test Trial default == True
window.page11XValue1                            = 540                                   # Ball always start from QFrame center, thus the default X value is 540
window.page11YValue1                            = 410                                   # Ball always start from QFrame center, thus the default Y value is 410
window.page11XValue2                            = 0                                     # Get this values later from moved object
window.page11YValue2                            = 0                                     # Get this values later from moved object
# use this value to converse the distance from pixel to cm! ASSUMING 96 dpi!
window.page11PixelIntoCentimeter                = 37.795275590551               # 1 cm = 37.795276 pixel (http://www.endmemo.com/sconvert/centimeterpixel.php)
# Dependent Variables
window.page11AverageDistance                    = 0                                      # How far was the ball positioned from center
window.page11PercentageUp                       = 0                                      # How often was the ball positioned in upper screen
window.page11PercentageDown                     = 0                                      # How often was the ball positioned in lower screen
#
# Page 12 Email Page
#
window.EmailListFile                            = "EmailList.csv"
#
# Page 13 (Debrief) No variables necessary
#

# Function Library
#---------------------------------------------------------------------------
# General functions:
#---------------------------------------------------------------------------
#
# General Timer
#
# General Timer function
def GeneralTimer (timerValue, functionName):
    window.generalTimer = QTimer()
    window.generalTimerCounter = 0  # Reset to 0
    window.generalTimer.stop()      # In case I forgto to stop it
    window.generalTimer.timeout.connect(functionName)
    window.generalTimer.start(timerValue)
#
# Setting a Page
#
def setPage(page):
    window.nextPage = page
    ui.stackedWidget.setCurrentIndex(window.nextPage)
#
# Open Fullscreen
#
def windowfullscreen():
    window.showFullScreen()
    windowCentreH = window.width()/2
    windowCentreV = window.height()/2
    ui.stackedWidget.setGeometry(windowCentreH - window.widthWidget/2, windowCentreV - window.heightWidget/2,
                         window.widthWidget, window.heightWidget)
#
# Initialize the SPSS-File and decide in which conditions the participant is going to be
#
def InitFileAndExperiment():
    combinedConditionCounterList   = [0,0,0,0]                      # create a list to hold the number of existing combined conditions
                                                                    # the index of the list represents the combined condition and the
                                                                    # value represetnts the number of existing combined condition


    try :
        if window.destinationFile in listdir():                         # Look for result file and create a new one, if it does not exist
            file = open(window.destinationFile, 'r')
            lines = file.readlines()

            for line in lines[1:]:
                help = line.split(',')
                combinedCondition = (int(help[4]) * (2**1) ) + int(help[5] * (2**0) )  # create a bitwiese value with help 4 = 2^1 (2) plus help 5 = 2^0 (1)
                combinedConditionCounterList[combinedCondition] +=1

                dataList = []
                dataList.append(line.split(','))


            # Get the first index of the cell with the min number of  combinedCondition. That is the condition combination for this try
            combinedCondition = combinedConditionCounterList.index(min(combinedConditionCounterList))

            # now I mask bitwise to extract the single condition value
            # & = bitwise calculation 1 & 1 is 1, everything else is 0
            # like the following table:
            # Bit A     Bit B       Result A&B
            # -----     -------     -----------
            #   0           0           0
            #   0           1           0
            #   1           0           0
            #   1           1           1
            #
            #  A number is a combination of bits here we need 4 different values and thus need 2 bits 2^0 (=1) and 2^1 (=2)
            #  so whe can represent our 4 values with
            #    2      1
            #   2^1    2^0      = bit 2 + bit 1
            #   ---    ---        --------------
            #    0      0       =       0
            #    0      1       =       1
            #    1      0       =       2
            #    1      1       =       3
            #
            # We can seperate the single bits from a value my masking them using the & operator
            # To look for bit 2^1 whe have to mask the value with the value 2 and use the & operator
            # When the result: (x & (2^1))  > 0 the bit 1 ist set!!
            # another example (if more than 2 bits):
            # if ( x & (2^7)) > 0   then bit 7 ist set and so on.
            # Here we only neet bit 0 and 1
            ## Sources:
            # https: // www.youtube.com / watch?v = hXUUbWKT3x0
            # https: // wiki.python.org / moin / BitwiseOperators
            if ((combinedCondition & 2 ) > 0 ):
                window.CondAwayTowards  = 1

            if ((combinedCondition & 1 ) > 0 ):
                window.CondCognitiveNeutral  = 1

        else:
            file = open(window.destinationFile, 'w')
            header = "Age,Gender,Education,Nationality,CondAwayTowads,CondCognitiveNeutral,CorrectSensibleTo,RTSensibleTo," \
                 "CorrectSensibleAway,RTSensibleAway,CorrectNonsensibleTo,RTNonsensibleTo,CorrectNonsensibleAway,TimeNonsensibleAway," \
                 "AverageDistance,PercentageUp,PercentageDown"
            file.write(header)

    except:
        print ("exception found but has not to be handled")
#
# Save the experiment
#
def saveExperiment():
    if window.destinationFile in listdir():
        file = open(window.destinationFile, 'a')

        detail = "\n {0:d},{1:s},{2:s},{3:s},{4:d},{5:d},{6:f},{7:d},{8:f},{9:d},{10:f},{11:d},{12:f},{13:d},{14:f},{15:f},{16:f}".format(
            window.page2Age
            , window.page2Gender
            , window.page2Education
            , window.page2Nationality
            , window.CondAwayTowards
            , window.CondCognitiveNeutral
            , window.page8PercentageCorrectSensibleTowards
            , window.page8TimeSensibleTowards
            , window.page8PercentageCorrectSensibleAway
            , window.page8TimeSensibleAway
            , window.page8PercentageCorrectNonsensibleTowards
            , window.page8TimeNonsensibleTowards  # bis hierher OK
            , window.page8PercentageCorrectNonsensibleAway
            , window.page8TimeNonsensibleAway
            , window.page11AverageDistance
            , window.page11PercentageUp
            , window.page11PercentageDown)

        file.write(detail)
        file.close()
# Save Email
# I write this in a separate file, because in a real experiment we should not be able to trace back the contact details
# to the experiment data!
def EmailList():
    if window.EmailListFile in listdir():
        file = open(window.EmailListFile, 'a')
    else:
        file = open(window.EmailListFile, 'w')
        header = "TotalCount,CondCognitiveNeutral,EmailAddress"
        file.write(header)
    # Write in the total number of correct hits and e-mail address, also save  which condition it was, so it is fair competition
    file.write("\n{0:d},{1:d},{2:s}".format(window.page5TotalCount, window.CondCognitiveNeutral, window.EmailAddress))
    file.close()

#---------------------------------------------------------------------------
# Page specific functions
#---------------------------------------------------------------------------
#
# Page 1 Consent form
#

# Function to enable the Entry-fields of Page 1 after the defined time ia reached
def handlePage1Timer():
    window.generalTimerCounter += 1
    if window.generalTimerCounter == 5:  # In real experiment I will set it higher so people read the consent form!
        window.generalTimer.stop()
        ui.Info.setEnabled(True)
        ui.CheckYes.setEnabled(True)
        ui.CheckNo.setEnabled(True)
        ui.Continue.setEnabled(True)

# General Action handler for available actions of page 1 (Consent form)
def ActionHandlerPage1():
    if ui.CheckYes.isChecked():
        setPage(1)
    else:
        ui.DontParticipate.show()  # show Widget with error message and leave button

# Function to init and handle the tasks for Page 1 (Consent form)
def InitAndHandlePage1():
    ui.DontParticipate.hide()  # hides Leave message and button
    setPage(2)

    # Timer after 10 Second you can continue! To make sure people don't skip the consent form!
    GeneralTimer(1000,handlePage1Timer)

    # Connect the Continue-Button with the action handler for page 1
    ui.Continue.clicked.connect(ActionHandlerPage1)
    # Connect the Leave-BUtton with last action hander for page 14 (end of experiment)
    ui.LeaveExp.clicked.connect(ActionHandlerPage14)
#
# Page 2 Demographics
#

# General Action handler for available actions of page 2 (Demographics)
def ActionHandlerPage2():
    errorDetected = False

    if ui.Age.value() == 0 or ui.Age.value() < 10:  # Restrict age to a realistic age of a student participant
        ui.ErrorAge.show()
        errorDetected = True
    else:
        window.page2Age = ui.Age.value()
        ui.ErrorAge.hide()

    if ui.Male.isChecked():
        window.page2Gender = "male"
        ui.ErrorGender.hide()
    elif ui.Female.isChecked():
        window.page2Gender = "female"
        ui.ErrorGender.hide()

    if not ui.Male.isChecked() and not ui.Female.isChecked():
        ui.ErrorGender.show()
        errorDetected = True
    if ui.Degree.currentText() == "Please indicate":
        ui.ErrorDegree.show()
        errorDetected = True
    else:
        window.page2Education = ui.Degree.currentText()
        ui.ErrorDegree.hide()

    if ui.Nationality.currentText()== "Please indicate":
         ui.ErrorNationality.show()
         errorDetected = True
    else:
        window.page2Nationality = ui.Nationality.currentText()
        ui.ErrorNationality.hide()

    if errorDetected == False:
        setPage(2)

# Function to init and handle the tasks for Page 2 (Demographics)
def InitAndHandlePage2():
    # hide the error messages
    ui.ErrorAge.hide()
    ui.ErrorDegree.hide()
    ui.ErrorGender.hide()
    ui.ErrorNationality.hide()

    ui.Continue2.clicked.connect(ActionHandlerPage2)

#
# Page 3 Introduction to motor movement manipulation
#

# General Action handler for available actions of page 3 (Intro Motor Task)
def ActionHandlerPage3():
    #Next page
    setPage(3)

# Function to init and handle the tasks for page 3 (Intro Motor Task)
def InitAndHandlePage3():

    # Set the correct text!
    if window.CondAwayTowards == 0:   # 0 = Away, that means the drag label is down, and the drop label is up
        window.page3textDragLabel = "lower"
        window.page3textDropLabel = "upper"

    else: #window.CondAwayTowards == 1, 1= Towards, that means the drag label is up, and the drop label is down
        window.page3textDragLabel = "upper"
        window.page3textDropLabel = "lower"

    if window.CondCognitiveNeutral == 0: # 0 = Cognitive Load
        window.page3CogntiveLoad = " The symbols will constantly change, you need to drag the CIRCLE symbol in order to get points. "

    # In the real experiment participants will have to do that task for 15 minutes, so illustrate thh experiment I cut down the time to 30 seconds,
    # so you can go through it in less time
    page3Explanation = ("This task will test your ability to persist motor movement. You goal is to move the symbol from the {0:s} part of the screen"
                 " into the container of the {1:s} part of the screen. Every time you drop the circle into the box, you will gain a point. "
                "{2:s}Just click the symbol with your left mouse, hold the left mouse button and release it, when you moved the symbol over the container. "
                "Importantly, there is a time limit of 15 minutes and the person with the highest score will win £50! Try to get as many points as possible!".format(
        window.page3textDragLabel,
        window.page3textDropLabel,
        window.page3CogntiveLoad))

    ui.page3Expl.setText(page3Explanation)
    ui.StartAnimation.clicked.connect(ActionHandlerPage3)

#
# Page 4 Explanation Motor movement manipulation
#

# Animate the explanation to make them more engaging
def AnimationPage4():

    if window.RoundPage4 == 1: # Changing image
        if window.CondCognitiveNeutral == 0: # 0= Cogntive load
            if window.AnimationRound == 0:
                ui.Symbol.setPixmap(QPixmap("ExpTriangle.jpg"))
            if window.AnimationRound == 1:
                ui.Symbol.setPixmap(QPixmap("ExpQuadrat.jpg"))
            if window.AnimationRound == 2:
                ui.Symbol.setPixmap(QPixmap("ExpCircle.jpg"))
                window.generalTimer.stop()
                ui.NextStepPage4.setEnabled(True)

            window.AnimationRound = window.AnimationRound + 1

    elif window.RoundPage4 == 2:

        currentYMouse = ui.Mouse.y()

        if window.CondAwayTowards == 0: # 0 = Away, default is Towards

            if ui.Mouse.y() < 720:
                ui.Mouse.setGeometry(640, currentYMouse + 10, 20, 31)
            else:
                window.generalTimer.stop()
                ui.NextStepPage4.setEnabled(True)
                ui.Symbol_2.show()


        else:

            if ui.Mouse.y() > 70:
                ui.Mouse.setGeometry(640, currentYMouse - 10, 20, 31)
            else:
                window.generalTimer.stop()
                ui.Symbol_2.show()
                ui.NextStepPage4.setEnabled(True)

    elif window.RoundPage4 == 3:  # Move the symbol and the mouse up

        if window.CondAwayTowards == 0: # TODO Make Sure that is is the correct option!! This case it is wrong
                currentYMouse = ui.Mouse.y()
                currentYSymbol = ui.Symbol_2.y()
                if ui.Mouse.y() > 90: # TODO make it better
                    ui.Mouse.setGeometry(640, currentYMouse - 10,20,31)
                if ui.Symbol_2.y() > 30:
                    ui.Symbol_2.setGeometry(540,currentYSymbol - 10,191,141)
                else:
                    window.generalTimer.stop()
                    ui.NextStepPage4.setEnabled(True)

        else: # Towards Condition
                currentYMouse = ui.Mouse.y()
                currentYSymbol = ui.Symbol_2.y()
                if ui.Mouse.y() < 760:
                    ui.Mouse.setGeometry(640, currentYMouse + 10,20,31)
                if ui.Symbol_2.y() < 700:
                    ui.Symbol_2.setGeometry(540,currentYSymbol + 10,191,141)
                else:
                    window.generalTimer.stop()
                    ui.NextStepPage4.setEnabled(True)

def ActionHandlerPage4():

    if window.RoundPage4 == 0:                           # Maybe here you can decide which text should be presented
        ui.Step1.setText("1. You will see a symbol in the {0:s} part of the screen. {1:s}". format(window.page3textDragLabel,window.page3CogntiveLoad))
        ui.Step1.show()
        ui.Intro.hide()
        ui.NextStepPage4.setText("Next Step")
        if window.CondAwayTowards == 0:                 # 0= Away, default is Towards
            ui.Symbol.setGeometry(540,660,191,141)      # down
            ui.Symbol_2.setGeometry(540,660,191,141)    # down
            ui.Box.setGeometry(540,10,231,221)          # up

        ui.Symbol.show()
        ui.Box.show()
        window.AnimationRound = 0                       # Sets animation round
        if window.CondCognitiveNeutral == 0:
            GeneralTimer(600, AnimationPage4) # TODO adjust the timer!
            ui.NextStepPage4.setEnabled(False)

    elif window.RoundPage4 == 1:
        ui.Mouse.show()
        GeneralTimer(30, AnimationPage4)
        ui.NextStepPage4.setEnabled(False)              # So people can only go on when animation is over
        ui.Step2.show()


    elif window.RoundPage4 == 2:
        ui.LeftButton.show()
        ui.Step3.setText("3. Hold the left mouse button and drag the symbol over the container in the {0:s} part of the screen "
                         "and release the left mouse button".format(window.page3textDropLabel))
        ui.Step3.show()
        GeneralTimer(30, AnimationPage4)
        ui.NextStepPage4.setEnabled(False)

    elif window.RoundPage4 ==3:
        ui.Symbol_2.hide()
        ui.LeftButton.hide()
        ui.Step4.show()
        ui.PointsAndTime.show()
        ui.NextStepPage4.setText("Start Test Trial")

    elif window.RoundPage4 == 4:
        setPage(4)
        TimerforDragAndDropPage5() # !Important! Starts Timer for next page

    window.RoundPage4 = window.RoundPage4 + 1

def InitAndHandlePage4():
    # Hide all the stuff you don't need at the beginning
    ui.PointsAndTime.hide()
    ui.Symbol.hide()
    ui.Symbol_2.hide()
    ui.Box.hide()
    ui.Mouse.hide()
    ui.Step1.hide()
    ui.Step2.hide()
    ui.Step3.hide()
    ui.Step4.hide()
    ui.LeftButton.hide()

    ui.NextStepPage4.clicked.connect(ActionHandlerPage4)
#
# Page 5 Motor movement task
#
# This iS a stopwatch running down in time for Page 5!
def ClockFunction():

    if window.page5seconds > 0:
        window.page5seconds -= 1

    else:

        if window.page5minutes > 0:                                         # next step
            window.page5minutes -= 1
            window.page5seconds = 59

        elif window.page5minutes == 0 and window.page5seconds == 0:

            window.generalTimer.stop()                                      # This stops the general timer
            ui.dragImage.setStartWithTimer(False)                           # Stops the changing of Pictures AND the Timer!
            #
            # Only save the values when participants is in real condition
            #
            if window.page5TestTrial == False:
                window.page5TotalCount = ui.dropArea.getSuccessCounter()    # Save the TotalCount in order to do the lottery later!
                setPage(7)                                                  # Go directly to Language Comprehension Task (Page8)

            else: # window.page4 == True
                # Reset the counter
                ui.dropArea.resetSuccessCounter()
                ui.counterLabel.setText("0")
                # Get to the next page!
                setPage(5)

    window.time = "{0:d},:,{1:d}".format(window.page5minutes, window.page5seconds) # output

    # Present the output in LCD Clock
    ui.LCDClock.setDigitCount(len(window.time))
    ui.LCDClock.display(window.time)

# This adjust the time-limit and starts the clock for page 5
def TimerforDragAndDropPage5():
    #
    # Decide whether object should change
    #
    if window.CondCognitiveNeutral == 0:        # 0 = Cognitive Load COndition, with changing images!
        ui.dragImage.setStartWithTimer(True)    # Sets Random Picture True, Cogntive Load Condition
        ui.dragImage.initChangeImageTimer()     # Set if needed!

    else:
        ui.dragImage.setStartWithTimer(False)
    # set a different time for the real experiment
    if window.page5TestTrial == False:
        window.page5seconds = 20
        window.page5minutes = 0         # In real experiment this would be set to 15 minutes
    #
    # Initalize the general time
    #
    GeneralTimer(1000, ClockFunction)

# InitandHandle Page 5 (Motor Movement Manipulation)
def InitAndHandlePage5():
    window.successFullEvent = 0

    # Create a Label to display the number of hits
    ui.counterLabel = QLabel(ui.page_5)
    ui.counterLabel.setGeometry(970, 280, 281, 91)
    ui.counterLabel.setText("0")
    ui.counterLabel.setFrameStyle(QFrame.Box)
    ui.counterLabel.setFrameShadow(QFrame.Raised)

    # Create the drag Label
    ui.dragImage = DragSymbol(ui.page_5)

    # Create the drop Label
    ui.dropArea = DropArea(ui.page_5)
    # This shows points
    ui.dropArea.setOutputLabel(ui.counterLabel)

    if window.CondAwayTowards == 0:     # This means the mouse should be physically moved away from the person, that means that
                                        # the drag image is below and the drop image is above!
        ui.dragImage.setGeometry(540,660,191,141)  # below ball
        ui.dropArea.setGeometry(540, 10, 231, 221) # upp box

    else:   # This means the mouse should be physically moved towards  the person, that means that the drag image is above and the drop image is below!
        ui.dragImage.setGeometry(540, 10, 191, 141)    # upp ball
        ui.dropArea.setGeometry(540, 660, 231, 221)    # below box

#
# Page 6 Explanation of Language Comprehension Task
#
# Next page
def ActionHandlerPage6():
    setPage(6)

# Function to init and handle the tasks for page 6 (Intro Language Comprehension Taks
def InitAndHandlePage6():
    ui.StartAnimation_page6.clicked.connect(ActionHandlerPage6)
#
# Page 7 Step-by-step explanation to Language Comprehension Task
#
def AnimationPage7():
    currentYFinger = ui.Finger.y()
    if ui.Finger.y() > 640:
        ui.Finger.setGeometry(430, currentYFinger  - 10,251,221)
    else:
        window.generalTimer.stop()
        ui.NextStep_Page7.setEnabled(True)

def ActionHandlerPage7():

    if window.RoundPage7 == 0:
        ui.Step1_Page7.show()
        ui.KButton.show()
        ui.RedX.show()
        ui.NextStep_Page7.setText("Next Step")

    if window.RoundPage7 == 1:
        ui.Step2_Page7.show()
        ui.RedX.hide()
        ui.ExampleSentence.show()
        ui.LButton.show()

    if window.RoundPage7 == 2:
        ui.Step3_Page7.show()
        ui.Finger.show()
        GeneralTimer(50,AnimationPage7)
        ui.NextStep_Page7.setEnabled(False)  # So people can only go on when animation is over

    if window.RoundPage7 == 3:
        ui.Step4_Page7.show()
        ui.NextStep_Page7.setText("Start Test Trial")

    if window.RoundPage7 == 4:
        ui.KeyBoardWidget.setFocus()        # Set focus to keyboard
        if window.page8TestTrial == True:
            page8GetStimuliList()           # THis only has to be done once, as the beginning
        # Next Page
        setPage(7)

    window.RoundPage7 = window.RoundPage7 + 1  # Explanation Rounds

def InitAndHandlePage7():

    # hide everything
    ui.Step1_Page7.hide()
    ui.Step2_Page7.hide()
    ui.Step3_Page7.hide()
    ui.Step4_Page7.hide()
    ui.RedX.hide()
    ui.Finger.hide()
    ui.ExampleSentence.hide()
    ui.KButton.hide()
    ui.LButton.hide()

    ui.NextStep_Page7.clicked.connect(ActionHandlerPage7)

#
# Page 8 Language Comprehension task
#
# Method to read the list of defined stimuli from Stimuli.csv and shuffle the list
# First get the file-entries an fill them into the liste, row 0 contains the header and has to be ignored!!
def page8GetStimuliList():

    file = open(window.page8StimuliListFileName, 'r')
    content = file.readlines()
    file.close()

    for i in content[1:]:                                           # if test round just show the first ones
        window.page8StimuliList.append(i.strip('\n').split(","))    # Strip the \n at the end of From Split to create seperate items


    # Save two different Lists, one for the test trial and one for the real trial!
    for j in window.page8StimuliList[0:5]:                      # This stores a TestList, THE FIRST FOUR STIMULI!
        window.page8TestList.append(j)

    for k in window.page8StimuliList[5:]:                       # This stores The Real List, the rest of the stimuli
        window.page8RealTrialList.append(k)

        # Calculate the nessessary main values for the statistics, only for the real list
        if ((k[1] == "True") and (k[2] == "Towards")):
            window.page8NumberSensibleTowards += 1
        if ((k[1] == "True") and (k[2] == "Away")):
            window.page8NumberSensibleAway += 1
        if ((k[1] == "False") and (k[2] == "Towards")):
            window.page8NumberNonsensibleTowards += 1
        if ((k[1] == "False") and (k[2] == "Away")):
            window.page8NumberNonsensibleAway += 1
    #
    # and now shuffle the list to get a randomized list
    #
    random.shuffle(window.page8RealTrialList)  # We only need to randomize the stimuli of the real test, the control test does not need to be randomized!

def ActionHandlerPage8(keyEvent): # Umbennen! window.page6TestTrial = True
    #
    # Definition of locale variables
    #
    descisionTime   = 0                            # to hold the descision time of the actual stimuli
    #
    # The first task ist to enable the tries when the start is requested
    #
    if window.page8TrialStart == False: # This is the Introduction, so participant has time to focus on red cross in the middle of the screen!
        #
        # This decides which list has to be used!
        #
        if window.page8TestTrial == True:
            window.page8StimuliList = window.page8TestList
        else:  # window.page8TestTrial == False
            window.page8StimuliList = window.page8RealTrialList

        if keyEvent.upper() == window.page8KKey: # In case somebody pressed shift, its the upper key, so program still works!
            window.page8TrialStart = True
            ui.x.hide()
            ui.Explanation.hide()
            #
            # get the details of the active stimuli
            #
            window.page8StimuliDetails = window.page8StimuliList[window.page8ActiveStimuli]
            ui.Stimuli.setText(window.page8StimuliDetails[0])
            ui.Stimuli.show()
            #
            # Remember the time when the stimulus changes!
            #
            window.page8StimuliStartTime = int(round(time.time() * 1000))                   # get the actual time in milliseconed
    #
    # react to the keys only when the trial starts and the list is not completely finished
    #
    elif ((window.page8TrialStart   == True                         ) and
          (window.page8ActiveStimuli < len(window.page8StimuliList) )       ):   # Only react to keys when not all stimuli have been shown

        #
        # calculate the needed time for the descision
        #
        #if window.page8TestTrial == False: # Try to give feedback of decision time! When it took too long!
        descisionTime = int(round(time.time() * 1000)) - window.page8StimuliStartTime   # calculate the needed time (actual time minus saved timestamp)
        #
        # Set the next stimuli active
        #
        window.page8ActiveStimuli = window.page8ActiveStimuli + 1
        #
        # Handle k pressed
        #
        if keyEvent.upper() == window.page8KKey: # User decides its a sensible sentence!
            if (window.page8StimuliDetails[1] == "True"):
                #
                # In test trial give feedback!
                #
                if window.page8TestTrial == True:

                    window.page8CorrectDecisionText = "Good Job, the sentence is indeed sensible!"# Give positive feedback!!
                    if descisionTime > 2300: # This give Feedback of decision time, when it took too long!
                        window.page8InTimeText = " But try to be faster next time"  # give feedback about timing
                    ui.Feedback.setText(window.page8CorrectDecisionText+window.page8InTimeText)
                    window.page8palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green) # TODO make this default later!!
                    ui.Feedback.setPalette(window.page8palette)
                    # ToDo include Smiley?
                #
                # actualize the values for statistics, only during the real trial!
                #
                else: # window.page8TestTrial == False, This is the real trial!

                    if (window.page8StimuliDetails[2] == "Away"):

                            window.page8CorrectSensibleAway += 1
                            window.page8TimeSensibleAway    += descisionTime

                    else :

                            window.page8CorrectSensibleTowards   += 1
                            window.page8TimeSensibleTowards      += descisionTime


            else: # (window.page8StimuliDetails[1] == "False") # Non correct answer because sentence is nonsensible!
                #
                # In test trial give feedback!
                #
                if window.page8TestTrial == True:
                    window.page8CorrectDecisionText = "Too bad, the sentence is nonsensible!"  # Give negative feedback
                    if descisionTime > 2300:                                            # This give Feedback of decision time, when it took too long!
                        window.page8InTimeText = " Please try to be faster next time"   # give feedback about timing
                    ui.Feedback.setText(window.page8CorrectDecisionText + window.page8InTimeText)
                    window.page8palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
                    ui.Feedback.setPalette(window.page8palette)

                else: # window.page8TestTrial == False, This is the real trial!
                    if (window.page8StimuliDetails[2] == "Away"):

                        window.page8TimeNonsensibleAway += descisionTime

                    else:
                        window.page8TimeNonsensibleTowards += descisionTime

        #
        # Handle L pressed
        #
        if keyEvent.upper() == window.page8LKey:# User decides its a nonsensible sentence! In case somebody pressed shift, its the upper key so program still works!

            if (window.page8StimuliDetails[1] == "False"):

                if window.page8TestTrial == True:
                    window.page8CorrectDecisionText = "Good Job, the sentence is indeed nonsensible!"   # Give positive feedback!!
                    if descisionTime > 2300:  # This give Feedback of decision time, when it took too long!
                        window.page8InTimeText = " But try to be faster next time"                      # give feedback about timing
                    ui.Feedback.setText(window.page8CorrectDecisionText + window.page8InTimeText)
                    window.page8palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
                    ui.Feedback.setPalette(window.page8palette)

                #
                # actualize the values for statistics, only during the real trial!
                #
                else:  # window.page8TestTrial == False, This is the real trial!
                    if (window.page8StimuliDetails[2] == "Away"):
                        #
                        # actualize the values for statistics
                        #
                        window.page8CorrectNonsensibleAway += 1
                        window.page8TimeNonsensibleAway    += descisionTime

                    else :
                        #
                        # actualize the values for statistics
                        #
                        window.page8CorrectNonsensibleTowards    += 1
                        window.page8TimeNonsensibleTowards       += descisionTime

            else : # window.page8StimuliDetails[1] == "True", sentences was sensible!
                if window.page8TestTrial == True:
                    window.page8CorrectDecisionText = "Too bad, the sentence is sensible!"  # Give negative feedback
                    if descisionTime > 2300:  # This give Feedback of decision time, when it took too long!
                        window.page8InTimeText = " Please try to be faster next time"  # give feedback about timing
                    ui.Feedback.setText(window.page8CorrectDecisionText + window.page8InTimeText)
                    window.page8palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)  # TODO make this default later!!
                    ui.Feedback.setPalette(window.page8palette)
                #
                # actualize the values for statistics, only during the real trial!
                #
                else:  # window.page8TestTrial == False, This is the real trial!
                    if (window.page8StimuliDetails[2] == "Away"):
                        window.page8TimeSensibleAway += descisionTime

                    else:
                        window.page8TimeSensibleTowards += descisionTime
        #
        # while the end of the list is not reached, refresh the display else start the next page
        #
        if (window.page8ActiveStimuli < len(window.page8StimuliList)):
            #
            # get the details of the active stimuli
            #
            window.page8StimuliDetails = window.page8StimuliList[window.page8ActiveStimuli] # get the details of the actual stimuli
            ui.Stimuli.setText(window.page8StimuliDetails[0])  # display the actual stimuli test for the user
            window.page8StimuliStartTime = int(round(time.time() * 1000))                   # get the actual time in milliseconed
        else:
            #
            # End of rounds
            #
            if window.page8TestTrial == False:  # The real round
                window.page = 10
                window.page8PercentageCorrectSensibleTowards        = window.page8CorrectSensibleTowards / window.page8NumberSensibleTowards
                window.page8PercentageCorrectSensibleAway           = window.page8CorrectSensibleAway / window.page8NumberSensibleAway
                window.page8PercentageCorrectNonsensibleTowards     = window.page8CorrectNonsensibleTowards / window.page8NumberNonsensibleTowards
                window.page8PercentageCorrectNonsensibleAway        = window.page8CorrectNonsensibleAway / window.page8NumberNonsensibleAway

            else:
                # Get to the next page!
                window.page = 8
                # Reset Trial List and show/hide the messages
                window.page8TrialStart = False
                ui.x.show()
                ui.Explanation.show()
                ui.Feedback.hide() # Hide The fedback messsage
                ui.Stimuli.hide() # Hide the last Stimuli


            window.page8ActiveStimuli = 0 # Reset the active stimuli for next round
            setPage(window.page)

def InitAndHandlePage8():
    ui.KeyBoardWidget = KeyboardWidget(ui.page_8)
    ui.KeyBoardWidget.setGeometry(200, 40, 500, 500)
    ui.KeyBoardWidget.keyPressed.connect(ActionHandlerPage8)
    ui.Stimuli.hide() # Hide Simuli here

#
# Page 9 Explanation Estimation Distance Task
#
def ActionHandlerPage9():
    #Next page
    setPage(9)

# Show video/animation?
def InitAndHandlePage9():
    ui.StartExplanation_page9.clicked.connect(ActionHandlerPage9)

#
# Page 10 Step-by-step explanation Estimation Distance Task
#
def AnimationPage10():

    if window.RoundPage10 == 3: # Next step
        currentYMousePage10 = ui.mouse_page10.y()
        if ui.mouse_page10.y() > 330:
            ui.mouse_page10.setGeometry(570, currentYMousePage10 - 10, 21, 21)
        else:
            window.generalTimer.stop()
            ui.NextStep_Page10.setEnabled(True)

    if window.RoundPage10 == 4:
        currentXMousePage10 = ui.mouse_page10.x()
        currentXBallPage10  = ui.Ball_Page10.x()

        if ui.mouse_page10.x() < 800: # Move mouse to the side, so you don't suggest participant to move it up or down
            ui.mouse_page10.setGeometry(currentXMousePage10 + 10, 330, 21, 21)
            ui.Ball_Page10.setGeometry(currentXBallPage10 + 10, 320, 31, 31)
        else:
            window.generalTimer.stop()
            ui.NextStep_Page10.setEnabled(True)

def ActionHandlerPage10():

    if window.RoundPage10 == 0:
        ui.NextStep_Page10.setText("Next Step")
        ui.Step1_Page10.show()
        ui.IntroFramePage10.show()
        ui.Cross_Page10.show()
        ui.Ball_Page10.show()
        ui.Frame.show()

    if window.RoundPage10 == 1:
        ui.Step2_Page10.show()

    if window.RoundPage10 == 2:
        ui.Step3_Page10.show()
        ui.mouse_page10.show()
        GeneralTimer(50,AnimationPage10)
        ui.NextStep_Page10.setEnabled(False)

    if window.RoundPage10 == 3:
        ui.Step4_Page10.show()
        ui.LeftMousebutton_Page10.show()
        GeneralTimer(50, AnimationPage10)
        ui.NextStep_Page10.setEnabled(False)

    if window.RoundPage10 == 4:
        ui.Step5_Page10.show()

    if window.RoundPage10 == 5:
        ui.Step6_Page10.show()
        ui.NextStep_Page10.setText("Start Test Trial")

    if window.RoundPage10 == 6:
        setPage(10)

    window.RoundPage10 = window.RoundPage10 + 1



# Show video/animation?
def InitAndHandlePage10():
    # Hide all the stuff you don't need
    ui.IntroFramePage10.hide()
    ui.LeftMousebutton_Page10.hide()
    ui.Ball_Page10.hide()
    ui.mouse_page10.hide()
    ui.Frame.hide()
    ui.Step1_Page10.hide()
    ui.Step2_Page10.hide()
    ui.Step3_Page10.hide()
    ui.Step4_Page10.hide()
    ui.Step5_Page10.hide()
    ui.Step6_Page10.hide()
    ui.Cross_Page10 .hide()

    ui.NextStep_Page10.clicked.connect(ActionHandlerPage10)

#
# Page 11 Distance Estimation Task
#
def ActionHandlerPage11():

    #Trial Start
    if window.page11StartTrial == False:

        # Decide which Statements should be shown:
        if window.page11TestTrial == True:
            window.page11TextList = window.page11TestCondition

        else:  # window.page11TestTrial == False:
            window.page11TextList = window.page11RealConditionList

        ui.StartPage11.hide()           # Hide the Button to start task, so subject can't press it again
        window.page11StartTrial = True  # This STARTS the trial
        # Set the text!
        window.page11InstructionText = "Position the ball {0:s} away from the center of the screen".format(
            window.page11TextList[window.page11activeExperimentRound])

        ui.InstructionDistanceTask.setText(window.page11InstructionText)
        # After you set the text, put next round
        GeneralTimer(1000, ClockFunction2)

    elif window.page11StartTrial == True: # Now the Task STARTS

        if window.page11TestTrial == False:  # only save variables in REAL trial
            # Save the Distance of the object!
            # Get the necessary values!
            window.page11XValue2 = ui.EstimationTaskBall.x()
            window.page11YValue2 = ui.EstimationTaskBall.y()

            # Get the distance via the Pythagorean theorem (a^2 + b^2 = c^2) and convert it into cm
            window.page11PixelDistance = math.sqrt(((window.page11XValue2 - window.page11XValue1) ** 2) + (
                (window.page11YValue2 - window.page11YValue1) ** 2))
            window.page11DistanceList[window.page11activeExperimentRound] = window.page11PixelDistance / window.page11PixelIntoCentimeter

            # write in the outcome of direction, "up" is default
            if ((window.page11YValue1 - window.page11YValue2) < 0):
                window.page11DirectionList[window.page11activeExperimentRound] = "down"

        # Display next round
        window.page11activeExperimentRound = window.page11activeExperimentRound + 1  # Order to command very important!!

        if window.page11activeExperimentRound < len(window.page11TextList):
            window.page11InstructionText = "Position the ball {0:s} away from the center of the screen".format(
                window.page11TextList[window.page11activeExperimentRound])

            ui.InstructionDistanceTask.setText(window.page11InstructionText)


        #
        else: # When limit of test round has been found

            window.generalTimer.stop()        # Stop Timer

            window.page11StartTrial = False  # Reset, so that trial starts from beginning, !Different from window.page11TestTrial!

            if window.page11TestTrial == False:         # This is the real trial!

                # Get values out of lists and calculate averages!
                for i in window.page11DistanceList:
                    window.page11AverageDistance = window.page11AverageDistance + i   # Average estimated distance

                for i in window.page11DirectionList:
                    if i == "up":
                        window.page11PercentageUp = window.page11PercentageUp + 1           # Percentage of how often object was palced in upper screen
                    else:
                        window.page11PercentageDown = window.page11PercentageDown + 1       # Percentage of how often object was placed in lower screen

                window.page11AverageDistance = window.page11AverageDistance/len(window.page11DistanceList)
                window.page11PercentageUp = window.page11PercentageUp/len(window.page11DirectionList)
                window.page11PercentageDown = window.page11PercentageDown/len(window.page11DirectionList)

                # I have all the data I need, now I save the whole experiment!
                saveExperiment()

                window.page = 12  # Get to email page
            else:  # window.TestTrialPage11 == True
                # Just go to the next page! Where the real trials start
                window.page = 11

            window.page11activeExperimentRound = 0          # Reset the active stimuli
            ui.StartPage11.show()                           # Show the button for real trial
            ui.InstructionDistanceTask.setText("Task description will appear here")  # Reset text for real trial
            setPage(window.page)


    window.page11seconds = 8                                # 8 seconds for the decisions
    ui.EstimationTaskBall.setGeometry(540, 410, 30, 30)     # Reset Object in QFrame center

def InitAndHandlePage11():

    ui.EstimationTaskFrame = DropFrame(ui.page_11)
    ui.EstimationTaskFrame.setGeometry(0, 0, 1080, 820)
    ui.EstimationTaskFrame.setFrameStyle(QFrame.Box | QFrame.Plain)  # Set framestyle
    ui.EstimationTaskFrame.setLineWidth(2)
    # Set the clock
    window.time = "{0:d},:,{1:d}".format(window.page11minutes, window.page11seconds)  # output
    ui.LCDClock2.setDigitCount(len(window.time))
    ui.LCDClock2.display(window.time)

    ui.EstimationTaskBall = Ball(ui.page_11)
    ui.EstimationTaskBall.setGeometry(540, 410, 30, 30)

    ui.StartPage11.clicked.connect(ActionHandlerPage11)


def ClockFunction2(): # Clock function for Estimation Task

    if window.page11seconds > 0:
        window.page11seconds -= 1


    else:
        ActionHandlerPage11()
    window.time = "{0:d},:,{1:d}".format(window.page11minutes, window.page11seconds)  # output
    # Present the output in LCD Clock
    ui.LCDClock2.setDigitCount(len(window.time))
    ui.LCDClock2.display(window.time)

#
# Page 12 Start of real trials
#
def ActionHandlerPage12():

    # Set the conditions on non-test for the three tasks
    window.page5TestTrial   = False
    window.page8TestTrial   = False
    window.page11TestTrial  = False

    #Start first task (Motor Movement Task)
    setPage(4)
    TimerforDragAndDropPage5()   # IMPORTANT! Start the Timer for the task!

def InitAndHandlePage12():
    ui.StartExp.clicked.connect(ActionHandlerPage12)

#
# Page 13 (E-mail List)
#
def ActionHandlerPage13():
    errorDetected   = False

    ui.ErrorClick.hide()
    ui.ErrorEmail.hide()

    if not ui.YesParticipate.isChecked() and not ui.NoParticipate.isChecked():
        ui.ErrorClick.show()
        errorDetected = True
    elif ui.YesParticipate.isChecked():
        if ui.Email.text().find("@") == -1 or ui.Email.text().find(".") == -1: # Check whether people typed in a valid e-mail!
            ui.ErrorEmail.show()
            errorDetected = True
        else:
            window.EmailAddress = ui.Email.text()
            EmailList()

    # everything ist ok, so let us leave the Page
    if errorDetected == False:
        setPage(13)

# Initialize Page 13 (E-mail Page)
def InitAndHandlePage13():

    ui.ErrorClick.hide()
    ui.ErrorEmail.hide()

    ui.ContinueEmail.clicked.connect(ActionHandlerPage13)

#
# Page 14 Debrief
#
# Exit the experiment!
def ActionHandlerPage14():
    QApplication.quit()

# Initialize Page 14 (Debrief):
def InitAndHandlePage14():
    ui.terminateExp.clicked.connect(ActionHandlerPage14)

#---------------------------------------------------------------------------
# Initialzation of the whole eperiment
#---------------------------------------------------------------------------
# Start Fullscreen
windowfullscreen()
# Initiliazation of the experiment file
InitFileAndExperiment()
# Init and handle page 1 (Consent form)
InitAndHandlePage1()
# Init and handle page 2 (Demographics)
InitAndHandlePage2()
# Init ad handle page 3 (Explanation Motor Movements Manipulation)
InitAndHandlePage3()
# Init and handle page 4 (Step-by-step Explanation Motor Movements Manipulation)
InitAndHandlePage4()
# #Init and handle page 5 (Motor Movement Task)
InitAndHandlePage5()
# # Init and handle page 6 (Explanation Language Comprehension)
InitAndHandlePage6()
# #Init and handle page 7 (Step-by-step Explanation Language Comprehension)
InitAndHandlePage7()
# #Init and handle page 8 (Language Comprehension Task)
InitAndHandlePage8()
#Init and handle page 9 (Explanation Estimation Task)
InitAndHandlePage9()
#Init and handle page 10 (Step-by-Step Explanation Estimation Task)
InitAndHandlePage10()
# Init and handle page 11 (Estimation Task)
InitAndHandlePage11()
# Init and handle page 12 (Start Real Tasks)
InitAndHandlePage12()
# Init and handle page 13 (E-mail Page)
InitAndHandlePage13()
# Init and handle page 14 (Debrief)
InitAndHandlePage14()
#---------------------------------------------------------------------------
# My own code ends here!
#
window.show()
sys.exit(app.exec_())