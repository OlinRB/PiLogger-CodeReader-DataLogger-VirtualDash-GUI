PiLogger Application

Author: Olin Ruppert-Bousquet
Email: olinrb@live.com
Website: https://github.com/OlinRB

The PiLogger is a GUI application designed to interface with the
Python-OBD library

*This program was developed for OBD commands supported for a 2007 VW GTI (MK5/FSI)
	- Accepted commands for virtual dash may vary between makes/models

Set Up:
    Install Pygame
    Install Pyserial
    Download Windows fonts (If not Windows device)
    Configure directory for images in constants.py
    Connect to ELM327 device via Bluetooth (Password usually 1234)
    Run program run.py

    If connection issues:
        Determine serial port of Bluetooth connection and modify
        path within connection = obd.Async("...") in run.py

    If PIDS not supported by vehicle:
        run app.py to determine supported commands
        - modify application to fit needs


Code Utilized for Project:
    Python-OBD: https://python-obd.readthedocs.io/en/latest/
    Button Class: https://github.com/russs123/pygame_button
    Pygame doc.: https://www.pygame.org/docs/ref/pygame.html
    app.py written by Mike Szumlinski // https://github.com/szumlins


Layout:


Available modes:
    Home Screen
    DTC (engine code) reader
    Virtual Dash
        -with data logging capability to csv file


    Program works in conjunction with ELM 327 adapter and has
    been designed to fit the Raspberry Pi 800x480 7-inch
    touchscreen display


    Application WILL run without ECU connection
    Initial debug mode set on to view connection
    process - turned off once GUI is launched



Full list of sources for Project found in sources.docx

