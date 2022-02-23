-----------------------------------------------------------------------------------------------
VLC TV Control 1.0 by Ken, 2022 ( Twi: @MandatoryTopic , www.ghostfight.net)
-----------------------------------------------------------------------------------------------

This is modidication of VLC Custom TV Channel Maker v0.02 by Jason Ozubko, 
2018 (jdozubko@gmail.com) ( https://addons.videolan.org/p/1154052 )

This program adds an .exe with a gui to VLC Custom TV Channel Maker v0.0 that allows users to click through 
their channels and eliminates the need to open and compile code to create channels. 
Channels can be generated from any local media the user has by simply pointing the program
at the directory it is stored in. To steal Jason's description (repeated later), the program

"randomly arranges a unique programming schedule for your media, each day, and then allows 
you to "tune in" to your channel or channels. For example, if you create a sci-fi channel
 out of all your sci fi videos, when you load that channel in to VLC, depending on the 
time of day, it will be somewhere in the middle of playing a video.  If you then close the 
channel but return 2 minutes later, you will find that the video that was on before is still 
on but now 2 minutes ahead in time!"


----------------------------------SET UP---------------------------------------------------------


-This program operates by generating .channel files to be read by a VLC .lua script to create randomized playlist
from. In order for this to work three minor things must be done:


1) Place the channelwatch.lua file in this folder in the VLC playlist folder, Generally:

Windows:
    C:\Program Files\VideoLAN\VLC\lua\playlist\
                       or
    C:\Program Files (x86)\VideoLAN\VLC\lua\playlist\
Mac OS X:
    VLC.app/Contents/MacOS/share/lua/playlist/
Linux:
    /usr/share/vlc/lua/playlist/


2) After generating a channel file, immediately make VLC the default program for
all channel files. This can also be done before creating your own channel file by using the 
off.channel file in the res folder in this directory



3) Set VLC to only allow one isntance of itself to be open at once, so that as you switch channels
you are not opening multiple instances of vlc


Note: It is possible, but not likely, that a copy of FFprobe might need to be in the folder (or installed on the computer)
in order for the program to scan media files. If you have already done steps 1 through 3 and it is still not working, 
this may be the issuer. FFprobe can be downloaded here:
https://ffmpeg.org/download.html


------------------------------------USE-----------------------------------------------------------

Please look at the SEEME.PNG in this folder.


The .channel files will be generated in the same folder as the .exe and should stay there. 
.channel files must remain in the same folder as the .exe in order for the program to open them.
Likewise files in the res folder should not be moved. The scrolling buttons will at the bottom of
the controller will move through the channels. The arrow button in the middle will allow you to input
what channel (number) you would like to view. Channel numbers correspond to their alphanumeric order. 

The Power button will terminate the program if a channel has been started with the program. If not channel
has been started with the program, then the power button will turn on the first channel. The scroll buttons
will also turn on channels.

The plus button at the bottom will allow you to generate channels by providing a directory with media files
and a desired channel name.


-----------------------------------ISSUES AND CONSIDERATIONS------------------------------------------

The Channel files are lists of media file locations and their durations. The program cannot handle many
special characters and so files that use certain special characters (including most non 
roman alphabets and scripts) will typically be ignored. If you notice a file causes an error when playing
or does not get a dureation in the .channel file, then that is likely why. 

When generating a .channel file it may take ~0.25 seconds to add each media file, so folders with hundreds of entries 
may take a few minutes to process in their entirety. 

The .py files for the program are included in the Py-files folder for users interested in modification
or use on non-windows machines. However, my code is extremely bad and so main.py is illegible. 

Outside of that the detailed operation is the same as in VLC Custom TV Channel Maker v0.02
As such I will paste the README for that program below for users interested in that level of detail.


Note: The channelwatch.lua file with the program has been slightly changed from that 
in VLC Custom TV Channel Maker v0.02, primarily to allow for the creation of channels using
less than 30 hours of media each. Should this, for whatever reason, be objectionable, users 
can swap it out with the original. 

GUI design by negated_kevin
https://www.fiverr.com/negated_kevin?source=inbox

VLC Custom TV Channel Maker readme:

---------------------------------------------------------------------------
VLC Custom TV Channel Maker v0.02 by Jason Ozubko, 2018 (jdozubko@gmail.com)
---------------------------------------------------------------------------

DESCRIPTION:

Have you ever wanted to make your own custom TV station from your home
media library?  Well now you can!  Up until now, if you wanted to
create a pseudo-TV station out of your personal media collection, the
best you could do is load all your media into a playlist and hit shuffle.
With the VLC Channel Maker add-on however, you can truly simulate an
ongoing TV station.  

The VLC Channel Maker randomly arranges a unique programming schedule for
your media, each day, and then allows you to "tune in" to your channel or
channels.  For example, if you create a sci-fi channel out of all your
sci fi videos, when you load that channel in to VLC, depending on the 
time of day, it will be somewhere in the middle of playing a video.  If 
you then close the channel but return 2 minutes later, you will find that 
the video that was on before is still on but now 2 minutes ahead in time!

---------------------------------------------------------------------------

THE FILES AND HOW TO USE THEM:

Two scripts should have come with this package: channelwatch.lua and 
makechannel.py. 

OTHER REQUIRED PROGRAMS
To use these scripts you will need to install python 2.7 and ffprobe (see 
instructions below). If you do not install these extra programs then the 
channel maker scripts will not work.

---------------------------------------------------------------------------


CHANNELWATCH.LUA
This file is a lua playlist script. It basically tells VLC how to load the
.channel files that you're going to make.  You need to put this lua script 
file in one of the following folders, based on your operating system:

Windows:

    C:\Program Files\VideoLAN\VLC\lua\playlist\

                       or

    C:\Program Files (x86)\VideoLAN\VLC\lua\playlist\


Mac OS X:

    VLC.app/Contents/MacOS/share/lua/playlist/


Linux:

    /usr/share/vlc/lua/playlist/


---------------------------------------------------------------------------


MAKECHANNEL.PY
This file is going to actually make your .channel files.  makechannel.py 
is a python script file that will search your computer for all valid video 
files, and save them to a .channel file, such as shows.channel or 
new.channel.  

To use this script you will need to have both python and ffprobe installed
(see instructions below).

Before using this script, edit it in any text editor (such as Notepad). 
There are two lines you will want to edit.

search_path  = 'c:\\media\\videos\\'
channel_name = 'new.channel'

search_path tells the script where you have your video files saved. Edit 
this line to reflect where you have your media files saved.

channel_name is the default file name that the script will output to. You 
can change this now or leave this as is and just rename the channel file 
after you run the script.


---------------------------------------------------------------------------


BUILDING A CHANNEL FILE
After editing makechannel.py so that it knows where your media files are 
stored, simply run the file and it will do the rest. The simplest way to 
run this file is from the command prompt or terminal. 

In Windows press Windows Key+R then type in cmd. On a mac open up the 
terminal which is found in the utilities section of applications. In Linux 
CTRL-ALT-T usually opens the terminal.

Once the command prompt/terminal opens navigate to where makechannel.py is 
saved and type: python makechannel.py

The script will start searching for media files. Each time it finds a file 
you will see the file name, the length of the video, and the phrase 
"added!", this will mean the video has been added to the .channel file. So 
you'll see something like:

Movie 1.avi
1:42:36
added!

Movie 2.avi
2:02:10
added!

etc.

If you do not see this kind of output then the script is not finding any 
media files. Check that you've specified the correct search_path and that
you have both python and ffprobe installed correctly and then try again.


---------------------------------------------------------------------------


RUNNING A CHANNEL FILE
Once you have a .channel file you can drag it into VLC and it should load. 
If it does not, you may not have put channelwatch.lua in the correct place.

You can also set VLC to be the default application to open .channel files. 
This will allow you to simply double click a .channel file to open and play 
the channel. To do this just try to open a .channel file and your computer 
should ask you what program to use, select VLC as the application to use to 
open .channel files and set it as the default application to use from now
on.


---------------------------------------------------------------------------


CREATING MULTIPLE CHANNELS FROM THE SAME LIBRARY
One cool feature of the channel maker is that you can have multiple 
channels made from the same media library. That is, you can have different 
viewing schedules for the exact same list of videos.

To activate this feature, take a channel file that you've created then make
a copy of it. Open the copy in a text editor and you should see the first 
line contains a 0. Edit this 0 to be another number like 1 or 2 or 381 (any 
3 digit number will work).

Now, open this copied .channel file and you'll see that although it's using 
all the same media files as the original channel, it has a different 
broadcast schedule and is showing videos in a different order.

So you could have a movies1.channel, movies2.channel, and movies3.channel 
file and each could have the same listing of videos but as long as each has 
a unique number on the first line of the file, they will all play their 
files on a different schedule.

You can use this technique to create hundreds of channels off of the same 
media.


---------------------------------------------------------------------------


MANUALLY EDITING .CHANNEL FILES
If you open up a .channel file in a text editor, you will see that, 
starting on the second line of the file, .channel files are a big list of 
video files and video lengths. For example:

C:\Media\Videos\MyShow.Season 1\MyShow.S01E01.Pilot.avi
00:21:21
C:\Media\Videos\MyShow.Season 1\MyShow.S01E02.The.Friend.avi
00:20:42
C:\Media\Videos\MyShow.Season 1\MyShow.S01E03.Blind.Dates.avi
00:20:57

The first line always represents the location of the video file and the 
line directly BELOW that always represents to total run time of that 
video.

To remove a video file from a channel, simply delete BOTH the file 
location line and the run time line directly BELOW that.  

If you  want to include other video files from another channel, simply 
copy over the location line AND the run time line and place it in the 
.channel file.  Hence, you can customize the content on a channel to be
anything that you like.


---------------------------------------------------------------------------


REQUIRED THIRD-PARTY PROGRAMS: PYTHON AND FFPROBE
Finally, do not forget to install both python and ffprobe before running 
these scripts. Again, they will not work without these extra programs.

For Python make sure to get version 2.7. For ffprobe you simple need 
ffprobe.exe (or equivalent on Mac or Linux). 

You will need to make sure you have both python and ffprobe setup in 
your system path, so that when you type either python or ffprobe into 
the command prompt/terminal your computer runs the program.

If you're having trouble getting makechannel.py running try typing in 
ffprobe into the command prompt/terminal and see if it runs. If it says 
unknown program then you don't have the paths setup correctly. If you're 
having a lot of trouble just copy ffprobe.exe into the folder where you 
have makechannel.py

Python 2.7
https://www.python.org/download/releases/2.7/

ffprobe
https://www.ffmpeg.org/download.html 
(NOTE don't click the big download button)
(     instead get the package for your OS)


---------------------------------------------------------------------------


OTHER NOTES, HINTS, AND TIPS
A few other helpful facts. When the channelwatch.lua script runs it tries 
to setup a playlist of 30 hours of video content for the day from your 
.channel file. If you have less than 30 hours worth of video in a .channel 
file it is possible the .channel won't load.

DO NOT have the RANDOM setting turned on in VLC. In normal playlists this 
feature will randomize the order of files played back but because the 
channel maker creates a specific schedule for the day, having this feature 
on will randomize playback and thus elminate the real-time viewing feature 
of this script.

VLC is also known to hang in rare circumstances when trying to load a 
.channel file. If this happens use the windows task manager (CTRL-ALT-DEL) 
to find vlc.exe in the running processes on your system and end it. This 
will force close VLC. If you try to open the same .channel file that just 
cause VLC problems the file will almost always work now. That is, the file 
is fine and will work, but sometimes VLC just needs a force close.

The .channel files can be moved anywhere on your computer and they should 
work fine so feel free to move them somewhere convenient.


---------------------------------------------------------------------------


THANKS! If you like VLC Channel Maker, make sure to tell your friends!
