from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from appUi import MainWindow, help
import time, os
import datetime
import sys
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler
from configparser import ConfigParser



class MainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        """
        Initializing the MainWindow
        """

        ## Setting up the MainWindow
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TABFYE!")
        self.setWindowIcon(QIcon('appUi/icons8-eye-64.png'))

        ## Creating objects for classes imported from modules
        # ConfigParser for saving configuration
        self.config = ConfigParser()
        # BackgroundScheduler does the scheduling job of
        # showing the notification every @self.time_interval seconds/minutes
        self.scheduler = BackgroundScheduler()

        ## Variables
        # These variables determine the time in which
        # the reminder needs to be disabled
        self.disable_reminder_starthour = self.timeEdit.time().hour()
        self.disable_reminder_endhour = self.timeEdit_2.time().hour()
        self.disable_reminder_startmin = self.timeEdit.time().minute()
        self.disable_reminder_endmin = self.timeEdit_2.time().minute()
        # disable_reminder = True, if disable option is checked
        self.disable_reminder = False
        # do_not_start = True, if today's day name (e.g.Monday)
        # is checked
        self.do_not_start = False
        self.time_interval_in_seconds = True
        self.time_interval = 5
        self.s5.setChecked(True)

        ## Connecting the time interval options with a function
        self.s5.toggled.connect(self.select_time_interval)
        self.s10.toggled.connect(self.select_time_interval)
        self.m10.toggled.connect(self.select_time_interval)
        self.m20.toggled.connect(self.select_time_interval)
        self.m30.toggled.connect(self.select_time_interval)
        self.m40.toggled.connect(self.select_time_interval)
        self.h1.toggled.connect(self.select_time_interval)

        if self.time_interval_in_seconds == True:
            self.scheduler.add_job(self.break_remind_notifier, 'interval', seconds=self.time_interval,
                                   id='reminder_job')
        else:
            self.scheduler.add_job(self.break_remind_notifier, 'interval', minutes=self.time_interval,
                                   id='reminder_job')

        ## Open/create config file
        if not os.path.exists('config.ini'):
            print("Config file not found")

            self.config.add_section('day')
            self.config.set('day', 'Monday', 'False')
            self.config.set('day', 'Tuesday', 'False')
            self.config.set('day', 'Wednesday', 'False')
            self.config.set('day', 'Thursday', 'False')
            self.config.set('day', 'Friday', 'False')
            self.config.set('day', 'Saturday', 'False')
            self.config.set('day', 'Sunday', 'False')

            with open('config.ini', 'w') as file:
                self.config.write(file)

        else:
            print("Config file found")
            self.config.read('config.ini')

        # Determine today's day name
        now = datetime.datetime.now()
        self.today = now.strftime("%A")
        # print(self.today)

        # Restore the previous checkstates from the config file
        if self.config.get('day', 'Monday') == 'True':
            self.checkMonday.setChecked(True)
            if self.today == 'Monday':
                do_not_start = True
        if self.config.get('day', 'Tuesday') == 'True':
            self.checkTuesday.setChecked(True)
            if self.today == 'Tuesday':
                do_not_start = True
        if self.config.get('day', 'Wednesday') == 'True':
            self.checkWednesday.setChecked(True)
            if self.today == 'Wednesday':
                do_not_start = True
        if self.config.get('day', 'Thursday') == 'True':
            self.checkThursday.setChecked(True)
            if self.today == 'Thursday':
                do_not_start = True
        if self.config.get('day', 'Friday') == 'True':
            self.checkFriday.setChecked(True)
            if self.today == 'Friday':
                do_not_start = True
        if self.config.get('day', 'Saturday') == 'True':
            self.checkSaturday.setChecked(True)
            if self.today == 'Saturday':
                do_not_start = True
        if self.config.get('day', 'Sunday') == 'True':
            self.checkSunday.setChecked(True)
            if self.today == 'Sunday':
                do_not_start = True

        # Start the reminders only if today was not checked
        if self.do_not_start == False:
            self.scheduler.start()
        else:
            print("Disabled for today")

        ## Connecting the GUI objects with their functions
        self.enableReminder.setChecked(True)
        self.enableReminder.stateChanged.connect(self.reminder_function)
        self.disableReminder.stateChanged.connect(self.reminder_function)
        self.checkMonday.stateChanged.connect(self.check_day_of_the_week)
        self.checkTuesday.stateChanged.connect(self.check_day_of_the_week)
        self.checkWednesday.stateChanged.connect(self.check_day_of_the_week)
        self.checkThursday.stateChanged.connect(self.check_day_of_the_week)
        self.checkFriday.stateChanged.connect(self.check_day_of_the_week)
        self.checkSaturday.stateChanged.connect(self.check_day_of_the_week)
        self.checkSunday.stateChanged.connect(self.check_day_of_the_week)

        self.helpButton.clicked.connect(self.help_dialog)

        time = self.timeEdit.time()
        self.timeEdit.dateTimeChanged.connect(self.displayDT)
        self.timeEdit_2.dateTimeChanged.connect(self.displayDT)
        


    def select_time_interval(self):
        """
        Change the time interval in which the reminders are displayed
        :return: Nothing
        """
        if self.s5.isChecked():
            self.time_interval_in_seconds = True
            self.time_interval = 5
        elif self.s10.isChecked():
            self.time_interval_in_seconds = True
            self.time_interval = 10
        elif self.m10.isChecked():
            self.time_interval_in_seconds = False
            self.time_interval = 10
        elif self.m20.isChecked():
            self.time_interval_in_seconds = False
            self.time_interval = 20
        elif self.m30.isChecked():
            self.time_interval_in_seconds = False
            self.time_interval = 30
        elif self.m40.isChecked():
            self.time_interval_in_seconds = False
            self.time_interval = 40
        elif self.h1.isChecked():
            self.time_interval_in_seconds = False
            self.time_interval = 60

        if self.time_interval_in_seconds == True:
            print("Time interval : " + str(self.time_interval) + " seconds")
            # self.scheduler.shutdown()
            self.scheduler.remove_all_jobs()
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(self.break_remind_notifier, 'interval', seconds=self.time_interval)
        else:
            print("Time interval : " + str(self.time_interval) + " minutes")
            # self.scheduler.shutdown()
            self.scheduler.remove_all_jobs()
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(self.break_remind_notifier, 'interval', minutes=self.time_interval)

        self.enableReminder.setChecked(True)
        self.disableReminder.setChecked(False)
        if self.do_not_start == False:
            self.scheduler.start()



    def help_dialog(self):
        """
        Open the GUI help dialog
        :return: Nothing
        """
        self.window = QtWidgets.QMainWindow()
        self.ui = help.Ui_Dialog()
        self.ui.setupUi(self.window)
        self.ui.closeButton.clicked.connect(self.window.close)
        # self.window.resize(500, 440)
        self.window.setWindowIcon(QIcon('appUi/question.png'))
        self.window.show()



    def disable_reminder_in_timerange(self):
        """
        Set @self.disable_reminder = True, when @self.disableReminder is checked
        :return: 
        """
        self.disable_reminder = True
        # self.scheduler.pause()



    def reminder_function(self):
        """
        When the states of @self.enableReminder or @self.disableReminder are changed,
        turn on/off the reminding schedule to reflect the change
        :return: Nothing
        """
        
        # Get current time to compare with disalbe timings
        currentHour = QTime.currentTime().hour()
        currentMin = QTime.currentTime().minute()
        print("CurrentHour " + str(currentHour) + " CurrentMin " + str(currentMin))
        
        # Start/Resume/Pause reminding schedule according to
        # whether it is enabled and if the current time falls
        # into the disable time range
        if self.enableReminder.isChecked() == True:
            print("EnableReminder " + str(self.enableReminder.isChecked()))
            if self.disableReminder.isChecked() == True:
                print("DisableReminder " + str(self.disableReminder.isChecked()))
                if not (currentHour >= self.disable_reminder_starthour and currentMin >= self.disable_reminder_startmin
                        and ((currentHour < self.disable_reminder_endhour)
                             or (currentHour == self.disable_reminder_endhour and currentMin < self.disable_reminder_endmin))):
                    self.scheduler.resume()
                else:
                    print("DisableReminder " + str(self.disableReminder.isChecked()))
                    print("Pausing...")
                    self.scheduler.pause()
            else:
                self.scheduler.resume()
        else:
            print("EnableReminder " + str(self.enableReminder.isChecked()))
            self.scheduler.pause()



    def break_remind_notifier(self):
        """
        Show notification when the job is called for
        :return: Nothing
        """

        print("Look away for a while!")
        self.reminder_label.setText('Take a break!')

        # Windows 10 notifications need .ico files
        # but Linux needs .png
        # So check the OS for appropriate icons
        if os.name == 'nt':
            app_icon = 'appUi/icons8-eye-64.ico'
        elif os.name == 'posix':
            app_icon = 'appUi/icons8-eye-64.png'

        # Show the notification
        notification.notify(
            title='Take a break for your eyes!',
            message='Look at an object 20ft away for 20s',
            app_icon=app_icon,  # e.g. 'C:\\icon_32x32.ico'
            timeout=10,  # seconds
        )

        time.sleep(1)
        self.reminder_label.clear()
        print("Break over!")



    def displayDT(self):
        """
        Get the disable timings input when it is changed
        :return: Nothing
        """
        self.disable_reminder_starthour = self.timeEdit.time().hour()
        self.disable_reminder_endhour = self.timeEdit_2.time().hour()
        self.disable_reminder_startmin = self.timeEdit.time().minute()
        self.disable_reminder_endmin = self.timeEdit_2.time().minute()

        print("disable_reminder_starthour " + str(self.disable_reminder_starthour) + " disable_reminder_startmin " + str(self.disable_reminder_startmin))
        print("disable_reminder_endhour " + str(self.disable_reminder_endhour) + " disable_reminder_endmin " + str(self.disable_reminder_endmin))

        time = self.timeEdit.time().hour()
        time2 = self.timeEdit_2.time()
        currentTime = QTime.currentTime().hour()
        # if currentTime == time:
        #     print("Yeah, they are equal indeed")



    def check_day_of_the_week(self):
        """
        If today is checked, then disable the reminder for today,
        Resume otherwise
        :return: Nothing
        """
        if (self.checkMonday.isChecked() == True and self.today == 'Monday' or
                self.checkTuesday.isChecked() == True and self.today == 'Tuesday'
                or self.checkWednesday.isChecked() == True and self.today == 'Wednesdasy'
                or self.checkThursday.isChecked() == True and self.today == 'Thursday'
                or self.checkFriday.isChecked() == True and self.today == 'Friday'
                or self.checkSaturday.isChecked() == True and self.today == 'Saturday'
                or self.checkSunday.isChecked() == True and self.today == 'Sunday'):
            print("Today is checked")
            self.scheduler.pause()
        else:
            self.scheduler.resume()



    def __del__(self):
        """
        Destructor function
        :return: Nothing
        """
        print("Exiting app...")
        self.scheduler.shutdown()
        config = ConfigParser()
        config.read('config.ini')
        config.set('day', 'Monday', str(self.checkMonday.isChecked()))
        config.set('day', 'Tuesday', str(self.checkTuesday.isChecked()))
        config.set('day', 'Wednesday', str(self.checkWednesday.isChecked()))
        config.set('day', 'Thursday', str(self.checkThursday.isChecked()))
        config.set('day', 'Friday', str(self.checkFriday.isChecked()))
        config.set('day', 'Saturday', str(self.checkSaturday.isChecked()))
        config.set('day', 'Sunday', str(self.checkSunday.isChecked()))

        with open('config.ini', 'w') as file:
            config.write(file)




## Initializing the main app
app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')

## Creating the window object
window = MainWindow()
window.show()

## Execute the app
app.exec()


## Save the configurations
config = ConfigParser()
config.read('config.ini')
config.set('day', 'Monday', str(window.checkMonday.isChecked()))
config.set('day', 'Tuesday', str(window.checkTuesday.isChecked()))
config.set('day', 'Wednesday', str(window.checkWednesday.isChecked()))
config.set('day', 'Thursday', str(window.checkThursday.isChecked()))
config.set('day', 'Friday', str(window.checkFriday.isChecked()))
config.set('day', 'Saturday', str(window.checkSaturday.isChecked()))
config.set('day', 'Sunday', str(window.checkSunday.isChecked()))

with open('config.ini', 'w') as file:
    config.write(file)

print("Exiting...")
