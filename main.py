from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from window import Window, WindowContainer
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
import os
import glob
import subprocess
import ffmpeg
import sys
import time
from PyQt5 import QtTest

#Keep track of the channel number
chan = 0
channum = chan + 1
#Keep track of it something is currently playing
onoffz = 0
#get every channel file in the folder

mylist = [f for f in glob.glob( "*.channel")]
print(mylist)

#get total number of channels
max = len(mylist)

class RemoteButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(RemoteButton, self).__init__(*args, **kwargs)
        self.original_icon_size = None

    def mousePressEvent(self, e) -> None:
        self.original_icon_size = self.iconSize()
        size = self.iconSize().width() - 1
        self.setIconSize(QSize(size, size))
        QtWidgets.QPushButton.mousePressEvent(self, e)

    def mouseReleaseEvent(self, e) -> None:
        self.setIconSize(self.original_icon_size)
        QtWidgets.QPushButton.mouseReleaseEvent(self, e)


class GoToChannelDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(GoToChannelDialog, self).__init__(*args, **kwargs)
        self.pixmap = QPixmap(8, 8)
        self.pixmap.fill(Qt.transparent)
        self.setWindowIcon(QIcon(self.pixmap))
        self.setWindowTitle("Go to channel")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(450, 200)

        self.vlay = QtWidgets.QVBoxLayout(self)
        #self.hlay = QtWidgets.QHBoxLayout(self)

        self.channel_num = QtWidgets.QLineEdit(self)
        self.channel_num.setPlaceholderText("Enter channel number (interger)")
        self.channel_num.setFixedHeight(55)
        
        self.go_button = QtWidgets.QPushButton("Go", self)
        self.go_button.setFixedHeight(45)
        
        self.vlay.addWidget(self.channel_num)
        self.vlay.addSpacing(25)
        self.vlay.addWidget(self.go_button)
        self.go_button.clicked.connect(self.on_channum)
        

    def on_channum(self):
        global chan
        global channum
        global onoffz
        onoffz = 1
        plaza = self.channel_num.text()
        if plaza.isdigit() == True :
            channum = int(self.channel_num.text())
            chan = channum - 1
                #self.channel_name
            if channum < 1:
                channum = 1
                chan    = 0
            
            if channum > max:
                channum = max
                chan = max - 1
            #self.current_channel.setText("Channel: " + str(channum))
            os.startfile( mylist[chan] )
        else:
            self.channel_num.setPlaceholderText("Please type an interger value")
           

class CreateChannelDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(CreateChannelDialog, self).__init__(*args, **kwargs)
        self.pixmap = QPixmap(8, 8)
        self.pixmap.fill(Qt.transparent)
        self.setWindowIcon(QIcon(self.pixmap))
        self.setWindowTitle("Create channel")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(455, 155)

        self.vlay = QtWidgets.QVBoxLayout(self)
        self.browse_lay = QtWidgets.QHBoxLayout()

        self.path_display = QtWidgets.QLineEdit(self)
        self.path_display.setReadOnly(True)

        self.browse_button = RemoteButton(self)
        self.browse_button.setIcon(QIcon("res/select_folder.svg"))
        self.browse_button.setFixedSize(35, 35)
        self.browse_button.setToolTip("Browse Folder")
        self.browse_button.clicked.connect(self.on_browse)

        self.channel_name = QtWidgets.QLineEdit(self)
        self.channel_name.setPlaceholderText("Channel name")

        self.create_button = QtWidgets.QPushButton("Create", self)
        self.create_button.setFixedHeight(45)
        self.create_button.clicked.connect(self.on_create)


        self.browse_lay.addWidget(self.path_display)
        self.browse_lay.addWidget(self.browse_button)
        self.vlay.addLayout(self.browse_lay)
        self.vlay.addWidget(self.channel_name)
        self.vlay.addSpacing(35)
        self.vlay.addWidget(self.create_button) 

        self.file_dialog = QtWidgets.QFileDialog(self)
        

    def on_browse(self):
        folder = self.file_dialog.getExistingDirectory(caption="Select a folder to source your media files from")
        self.path_display.setText(folder)

    def on_create(self):
                
        global string
        global entry
        string = str( self.channel_name.text() )

        search_path  = str( self.path_display.text() )

        #default output file for your new channel
        channel_name = string + '.channel'

        # open the new.channel file to output things to
        f  = open(channel_name, 'w')
        df = open('log.txt', 'w')

        # channel is 0 by default
        f.write("0\n")

        time.sleep(0.3)
        self.close()
        

        #function... returns the duration HH:MM:SS of a video file
        def getLength(filename):
          #uses ffprobe to get info about the video file
          result = subprocess.Popen(['ffprobe', '-hide_banner', '-show_entries', 'format=size, duration',\
                           '-i', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

          #finds the info that has the word "Duration"
          y = [x for x in result.stdout.readlines() if "Duration: " in x]

          #get the location of the "Duration: " phrase
          loc = y[0].find("Duration: ")

          #assuming we find the location of that phrase..
          if loc != -1:
          #cut out everything before and everything more than 10 characters later
            print ( y[0][loc+10:loc+18] )
            return y[0][loc+10:loc+18]
          else:
          #if we don't find anything then set it to be 2 seconds of nothing...
            print ( y[0][loc+10:loc+18] )
            return '00:00:02'
            


        #main code... walk through the subfolders looking for movie files
        i = 0
        print ('searching ' + search_path + ' for media files...\n')

        #
        for dirpath, dirnames, files in os.walk(search_path):
          for name in files:
            #debug
        #############################################################################
        # EDIT THE LINE BELOW TO CHANGE THE TYPE OF MEDIA FILES YOU WANT TO FIND
        #############################################################################
            if name.lower().endswith(".avi") or name.lower().endswith(".mpg") or name.lower().endswith(".mpeg") or name.lower().endswith(".asf") or name.lower().endswith(".wmv") or name.lower().endswith(".wma") or name.lower().endswith(".mp4") or name.lower().endswith(".mov") or name.lower().endswith(".3gp") or name.lower().endswith(".ogg") or name.lower().endswith(".ogm") or name.lower().endswith(".mkv") or name.lower().endswith(".mp3") or name.lower().endswith(".flv") or name.lower().endswith(".mov") or name.lower().endswith(".wav") or name.lower().endswith(".flac") :
              fn = os.path.join(dirpath, name)
              #print fn
              try:
                #figure out the full name, output it, then save it
                #fn_full = os.environ["PWD"] + fn[1:]
                fn_full = fn
                print (fn_full)


                
                #figure out the length, output it, then save it
                fn_len  = getLength(fn_full)
                print (fn_len)

                #write the file name and the output
                f.write("%s\n" % fn_full)
                f.write("%s\n" % fn_len)
                print ('added!\n')
                i = i + 1

              except:
                print ('error (with getLength()?)\n')
                pass # ignore errors

            else:
              df.write('<SKIPPING> ' + os.path.join(dirpath, name) + '\n')
        ''' 
              i = i + 1
              if(i > 10):break
          if(i > 10):break
        '''

        #user output
        print ('' + str(i) + ' files found\n')
        #update internal channel list
        mylist = [f for f in glob.glob( "*.channel")]
        #close the file
        f.close()
        df.close()


class MainWindow(Window):
    def __init__(self, p):
        super(MainWindow, self).__init__(p)
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(25, 0, 25, 0)
        self.channel_ctrl_lay = QtWidgets.QHBoxLayout()

        px = QPixmap("res/emma-trans.png")
        px = px.scaled(80, 80)

        self.logo = QtWidgets.QLabel(self)
        self.logo.setPixmap(px)
        self.logo.setFixedSize(90 , 90)
        self.logo.setObjectName("logo")
        #self.logo.move(60, 100)
    
        #self.clogo = QtWidgets.QVBoxLayout(self)
        #self.clogo.addWidget(self.logo , alignment=Qt.AlignHCenter)
        
        self.goto_channel_dialog = GoToChannelDialog(self)
        self.create_channel_dialog = CreateChannelDialog(self)

        self.current_channel = QtWidgets.QLabel("Current channel: n/a", self)
        self.current_channel.setObjectName("current-channel")
        self.current_channel.setFixedHeight(35)

        self.off_button = RemoteButton(self)
        self.off_button.setObjectName("off-button")
        self.off_button.setFixedSize(96, 96)
        self.off_button.setIcon(QIcon("res/turn_off.svg"))
        self.off_button.setIconSize(QSize(80, 80))
        self.off_button.clicked.connect(self.onoff)
        #self.off_button.clicked.connect(self.parent().windowCloseEvent)
        #self.off_button.setToolTip("Exit")

        self.goto_channel = RemoteButton(self)
        self.goto_channel.setObjectName("round-button")
        self.goto_channel.setFixedSize(70, 70)
        self.goto_channel.setIcon(QIcon("res/goto_channel.svg"))
        self.goto_channel.setIconSize(QSize(60, 60))
        self.goto_channel.setToolTip("Go to channel")
        self.goto_channel.clicked.connect(self.on_goto_channel)

        self.channel_min = RemoteButton(self)
        self.channel_min.setFixedSize(35, 50)
        self.channel_min.setIcon(QIcon("res/channel_min.svg"))
        self.channel_min.setIconSize(QSize(25, 25))
        self.channel_min.setToolTip("Switch to previous channel")
        self.channel_min.clicked.connect(self.on_channel_min)  

        self.create_channel = RemoteButton(self)
        self.create_channel.setFixedHeight(50)
        self.create_channel.setIcon(QIcon("res/add_channel.svg"))
        self.create_channel.setIconSize(QSize(25, 25))
        self.create_channel.setToolTip("Create new channel")
        self.create_channel.clicked.connect(self.on_create_channel)

        self.channel_plus = RemoteButton(self)
        self.channel_plus.setFixedSize(35, 50)
        self.channel_plus.setIcon(QIcon("res/channel_plus.svg"))
        self.channel_plus.setIconSize(QSize(25, 25))
        self.channel_plus.setToolTip("Switch to next channel")
        self.channel_plus.clicked.connect(self.on_channel_plus)

        self.channel_ctrl_lay.addWidget(self.channel_min)
        self.channel_ctrl_lay.addWidget(self.create_channel)
        self.channel_ctrl_lay.addWidget(self.channel_plus)

       
        self.vlay.addWidget(self.logo, alignment=Qt.AlignHCenter)
        self.vlay.addSpacing(-60)
        self.vlay.addWidget(self.off_button, alignment=Qt.AlignHCenter)
        self.vlay.addWidget(self.goto_channel, alignment=Qt.AlignHCenter)
        #self.vlay.addWidget(self.logo)
        self.vlay.addLayout(self.channel_ctrl_lay)
        self.vlay.addSpacing(-50)
        self.vlay.addWidget(self.current_channel, alignment=Qt.AlignHCenter)
        self.vlay.addSpacing(-25)

    def onoff(self):
        global onoffz
        if onoffz == 0:
            global mylist
            mylist = [f for f in glob.glob( "*.channel")]
            if mylist :
                onoffz = 1
                os.startfile( mylist[chan] )
                self.current_channel.setText("Channel: " + str(channum))
        else:
               
            fileDir = os.path.dirname(os.path.realpath('off.channel'))
            filename = os.path.join(fileDir, 'res/off.channel')  
            os.startfile( filename )
            #QtTest.QTest.qWait(500)
            self.off_button.clicked.connect(self.parent().windowCloseEvent)
            self.off_button.setToolTip("Exit")
            QtTest.QTest.qWait(500)
            sys. exit()
            #self.close()
            
            
            
    def on_channel_min(self):
        global mylist
        mylist = [f for f in glob.glob( "*.channel")]
        if mylist :
            global onoffz
            onoffz = 1
            global chan
            global channum
            chan    = chan - 1
            channum = channum - 1
            print('sex')
            if channum < 1:
                channum = 1
                chan    = 0
            os.startfile( mylist[chan] )
            self.current_channel.setText("Channel: " + str(channum) )

    def on_channel_plus(self):
        global mylist
        mylist = [f for f in glob.glob( "*.channel")]
        if mylist :
            global onoffz
            onoffz = 1
            global chan
            global channum
            chan    = chan + 1
            channum = channum + 1
            
            if channum > max:
                channum = 1
                chan    = 0
            os.startfile( mylist[chan] )
            self.current_channel.setText("Channel: " + str(channum) )
       

    def on_goto_channel(self):
        self.goto_channel_dialog.exec_()
        self.current_channel.setText("Channel: " + str(channum))


    def on_create_channel(self):
        self.create_channel_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wcon = WindowContainer(MainWindow)
    wcon.show()
    sys.exit(app.exec_())
