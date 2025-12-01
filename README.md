## PyFlyff (Deprecated)

> **Project Retired:**  
> PyFlyff had a great run with over **2,000 downloads**, but it’s now retired.  
> Check out its modern successor: [**Mini PyFlyff**](https://github.com/ils94/Mini_PyFlyff).

## Overview

**PyFlyff** is a **QtWebEngine-based** desktop client for playing [Flyff Universe](https://universe.flyff.com/play), with additional features like simple automation (Mini Ftool) and multi-client controls.

## Client Hotkeys

-   **Ctrl + Shift + F5** → Reloads the client back to `https://universe.flyff.com/play`.
    
-   **Ctrl + Shift + F11** → Toggle fullscreen mode for the main window.
    
-   **Ctrl + Shift + PgUp** → Open a new client window.
    
-   To stop the **Mini Ftool loop**, press the configured **Activation Key** again.

## Features

### Mini Ftool

Lets you automate up to **5 hotkeys** to repeatedly use skills/items (ideal for heal spamming or mage/psy/elementor 1x1 grinding).

-   Press the **Activation Key** again to stop the loop.
    
-   Separate in-game keys with commas `,`.
    

Example configuration:

```
Activation Key: f1
In-Game Hotkey(s): 1,2,3,4,5
Repeat: 10
Interval(s): 1,5,10,15,20
Min Interval: 0
Fix Loop: YES
Profile Name: RM
```

 **How it works:**

-   **Activation Key:** the key you press to start/stop the loop.
    
-   **In-Game Hotkey(s):** keys pressed in the Alt Client in sequential order.
    
-   **Repeat:** number of times the loop runs (higher values simulate “endless” loops).
    
-   **Interval(s):** delay in seconds for each key.
    
    -   e.g. with `1,5,10,15,20`, key `1` is pressed every 1 second, `2` every 5 seconds, and so on.
        
-   **Fix Loop:** prevents overlapping actions when intervals align, ensuring a clean 1→2→3→4→5 rotation.
    
-   **Profile Name:** name of the client window so Win32 API can target it.

### Alt Control

Lets you map keys from the **Main Client** to send commands to an **Alt Client**, avoiding frequent Alt-Tab switching.

Example:

```
Main Client Hotkey: 1,2,3,4,5,6,7,8,9
Alt Client Hotkey: f1,f2,f3,f4,f5,f6,f7,f8,f9
```

Pressing `1` in the Main Client sends `f1` to the Alt Client, and so on.

### Reset Hotkeys

Clears all Mini Ftool and Alt Control settings as well as the stored Main/Alt Client window identifiers — useful if you want to reconfigure without restarting the PyFlyff client.

### User Agent

Lets you spoof your playing environment or fix login/recaptcha issues:

-   If Google marks the client as unsafe, set **User Agent → None**, save, and restart.
    
-   If recaptcha complains about an outdated browser, set **User Agent → any value** to bypass it.

### Community Links

Access helpful Flyff Universe resources directly within the client:

-   Flyffipedia
    
-   Madrigal Inside
    
-   Flyffulator
    
-   Madrigal Maps
    
-   Flyff Model Viewer
    
-   Skillulator


## Disclaimer

PyFlyff includes light automation tools that can ease grinding.  
However, **using automation is against the game’s Terms of Service** and may result in a ban.

The Mini Ftool adds slight randomness to actions, but it does **not** guarantee safety against detection.  
Use responsibly — you’ve been warned.

## Known Issues

-   If Google login is blocked, set a new **User Agent** and restart.

## Build Instructions

Install dependencies:

```bash
pip install pyinstaller pywin32 PyQt6 PyQt6-WebEngine
```

Create a `.BAT` file:

If Python is available in your PATH:

```bash
pyinstaller PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole
xcopy icons dist\PyFlyff\icons\
```

If Python is not in PATH, use full paths:

PyFlyff.py

```bash
Path\to\python.exe Path\to\pyinstaller.py PyFlyff.py --icon=icons/PyFlyff.ico --onedir --noconsole

xcopy icons dist\PyFlyff\icons\
```

-   `pyinstaller.py` is located in `<Python Installation>\Scripts`.
    
-   Place the `.BAT` file in the project folder and run it.
    
-   After building, ensure the `icons` folder is inside `dist\PyFlyff` to prevent startup errors.

## Android Client

For easier dual-clienting on mobile, try the Android version:  
[**FlyffUAndroid**](https://github.com/ils94/FlyffUAndroid)
