# PyFlyff
QtWebEngine to play Flyff Universe

# If you wish to support me :)

Bitcoin: 
1JDWqkVGeAw9a6ikUkk8q9n6vwA7pft6Ke

Ethereum: 
0x0fd9b73f25572b54de686c28e1050e25eed552e9

Dash: 
XyTGmhWzeQjNKnTeTD1UpFC3zubqurjtwt

Solana:
41hkroUbrDfYGh8Pmfd7gVAyXMTvFC8eacCyLyD1VHn7

Dogecoin: 
D6nnCqVUyUtL7FLtrmhjh9yLCcN54QjSuZ

# Client Hotkeys

Ctrl+Shift+F5 = reload client back to https://universe.flyff.com/play

Ctrl+Shift+F11 = enter/exit main window fullscreen

Ctrl+Shift+PgUp (PageUp) open a new client window

To stop the Mini Ftool loop, press the Activation Key again.

# Features

Mini Ftool: You can setup up to 5 hotkeys to automatically use a skill/item for you (good for heal spam or mage/psy/elementor 1x1). To stop it, press the same key you used to start the loop.

Separate each key with a comma ","

Example: 

Activation Key: f1

In-Game Hotkey(s): 1,2,3,4,5

Repeat: 10

Interval(s): 1,5,10,15,20

Min Interval: 0

Fix Loop: YES

Profile Name: RM

"Activation Key", is the key you will press to start the mini ftool loop. Pressing it again will stop it.

"In-Game Hotkey(s)" are the Alt Client keys that will be pressed in a sequencial order.

"Repeat" is the number of times the loop will repeat itself, and then stop. If you make it 10, it will repeat 10 times. Longer repeat times will make the loop seems "endless", like setting Repeat: 9999999999.

"Interval" is the amount in seconds for each key, follow along:

1,2,3,4,5

1,5,10,15,20

This means that "1" will be pressed every 1 second.

"2" will be pressed every 5 seconds.

"3" every 10 seconds, "4" every 15 seconds and "5" every 20 seconds.

"Fix Loop", will fix the loop, because mathematically, all keys will be pressed at the same time, due their Intervals reaching the same threshold. So pick "YES" if you wish to always make the Mini Ftool press 1 and 2 and 3 and 4 and 5 and repeat from 1 to 5 without pressing "1 and 2" at the same time.

"Profile Name" is basically the name of your Client Window, so the Win32api can look for it and send API messages to it.

Alt Control: You can set hotkeys for the Main Client to send a direct command to the Alt Client. Good if you don't want to use the Mini Ftool, but still want to command your FS/RM without having to alt+tab. To set multiple keys (up to 104 keys!) add commas between each one.

Example:

Main Client Hotkey: 1,2,3,4,5,6,7,8,9...

Alt Client Hotkey: f1,f2,f3,f4,f5,f6,f7,f8,f9...

This means that when you hit "1" in the Main Client, you will instead hit "f1" in the Alt Client, and so on.

Reset Hotkeys: Clear the variables values from Mini Ftool and Alt Control keys as well as the variable containing the value that is used to identify which window is the Main Client and which window is the Alt Client. Good in case you want to switch keys on both Mini Ftool and Alt Control without the need of completly restarting the PyFlyff Client.

User Agent: You can use this to spoof from where you are playing Flyff Universe, or, you can use it in case you are having trouble with your Google Account login / recaptcha challenge (see the "Known Issues so far" section of this README)

Community: You can access community links within the client, like Flyffipedia, Madrigal Inside, Flyffulator, Madrigal Maps, Flyff Model Viewer, Skillulator

# Disclaimer

As you can see, I added bot like features to my Client. They are simple, yet, very convenient tools to make the grind a bit more bearable, but keep in mind that using automation is against the rules and you might get banned for it. The Mini Ftool generate a random wait time for every repeatable action, but this does not prevent from a GM to identify that you are in fact botting, so try to not abuse it, you have been very much warned.

# Known Issues so far

If when you try to login wih your Google Account, and Google mark my Client as unsafe, set your User Agent by pressing the button "Set User Agent" in the toolbar and type in the input box: None

Hit save and restart the Client, it should let you login with no problem now.

Sometimes you won't be able to resolve the recaptcha challenge since it will report that PyFlyff is an outdated browser, to fix it, set your User Agent to anything really and it will bypass this check.

# How to compile it yourself

You i'll need to pip install those modules to your Python installation:

pip install pyinstaller pywin32 PyQt5 PyQtWebEngine

Then create a .BAT file with this:

IF your Python installation is ACCESSIBLE from Windows Env variables:

pyinstaller PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole
xcopy icons dist\PyFlyff\icons\

IF your Python installation is NOT accessible from Windows Env variables, then you will have to fully tell both python.exe and pyinstaller script locations in the command line:

Path/to/your/python.exe path/to/your/pyinstaller.py PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole
xcopy icons dist\PyFlyff\icons\

pyinstaller.py script is located in your Python installation folder - Scripts

Save both .BAT and put it inside the project folder and run it, wait for the compilation to finish and the resulted folder named "PyFlyff" will appear inside the dist folder created by pyinstaller inside the project folder.

After the compilation is finished, make sure the folder "icons" is inside the generated PyFlyff folder inside the dist folder, else it will give an error when opening the client.

# Android Client

I also made an Android Client that makes it easier for your to Dual Client using your Android Device.

Here is the link: https://github.com/ils94/FlyffUAndroid
