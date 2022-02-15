# -*- coding: utf-8 BOM-*-

"""
PiLogger Program

Author: Olin Ruppert-Bousquet
Email: olinrb@live.com
Website: https://github.com/OlinRB


This GUI written in Pygame utilizes the Python-OBD Library to send
real-time ECU data to screen.

Available modes:
    Home
    DTC (engine code) reader:
    Virtual Dash
        -with data logging capability to csv file


    Program works in conjunction with ELM 327 adapter and has
    been designed to fit the Raspberry Pi 800x480 7-inch
    touchscreen display


    Application WILL run without ECU connection
    Initial debug mode set on to view connection
    process - turned off once GUI is launched


    Python-OBD: https://python-obd.readthedocs.io/en/latest/
        elm327.py file modified to support ELM327v1.5 (slow adapter)
    Button Class: https://github.com/russs123/pygame_button
    Pygame doc.: https://www.pygame.org/docs/ref/pygame.html

"""

import obd
import csv
from datetime import date
from constants import *

obd.logger.setLevel(obd.logging.DEBUG)

if raspberry_pi:
    connection = obd.Async()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    connection = obd.Async("\\.\\COM3")  # PC -> connected port may vary between devices
    screen = pygame.display.set_mode((800, 480))

pygame.display.set_caption('PiLogger')

# Text size for flash messages
textPopUp = 100


# GUI buttons
virtualDash = button(20, 20, "Virtual Dash", screen)
dtc = button(350, 20, "Read Codes", screen)
quit = button(670, 20, "Quit", screen)
go_home = button(20, 20, "Home", screen)
data_log_off = button(350, 20, "Data Log", screen)
data_log_on = button(350, 20, "Logging", screen)


#############################
#      Global Values        #
#                           #
#############################


rpm = 0
load = 0
maf = 0.0
o2_trim = 0.0
timing_advance = 0.0
coolant_temp = 160
fuel_rail_press = 0.0
intake_temp = 0
afr = 0.0
codes = []


#############################
#    RPM GAUGE FUNCTIONS    #
#                           #
#############################

def rpm_gauge():
    rpm_gauge = pygame.transform.scale(gauge_image, (210,210))
    return rpm_gauge
def gauge_needle():
    needle = pygame.transform.scale(needle_image, (190, 2))
    return needle
def rotate_needle(needle, angle):
    rotated_needle = pygame.transform.rotozoom(needle, angle, 1)
    return rotated_needle



#############################
#      VIRTUAL DASH         #
#       FUNCTIONS           #
#############################


def virtualDashIntro():
    text = small_font.render("WELCOME TO VIRTUAL DASH", True, green)
    text_box = text.get_rect()
    text_box.center = (405, 80)
    screen.blit(text, text_box)

def virtDash():
    gauge = rpm_gauge()
    angle = 36 * (rpm * -.001) + 90
    needle_copy = gauge_needle()
    needle_rotated = rotate_needle(needle_copy, angle)
    screen.blit(gauge, (screen.get_width() / 2 - 105, 200))
    # Centering equation courtesy of DaFluffyPotato on Youtube: https://www.youtube.com/channel/UCYNrBrBOgTfHswcz2DdZQFA
    screen.blit(needle_rotated, (screen.get_width() / 2 - int(needle_rotated.get_width() / 2),
                                 305 - int(needle_rotated.get_height() / 2)))
    if rpm < 3500:
        display_rpm = rpm_font.render(str(rpm), True, green)
    else:
        display_rpm = rpm_font.render(str(rpm), True, red)
    screen.blit(display_rpm, (365, 430))
    screen.blit(rpm_text, (440, 450))

    screen.blit(coolant_temp_text, (500, 160))
    coolant_temp_display = font.render(str(coolant_temp), True, silver)
    screen.blit(coolant_temp_display, (500, 190))
    screen.blit(deg_F, (560, 210))

    screen.blit(o2_trim_text, (375, 100))
    o2_display = font.render(str("{:.1f}".format(o2_trim)), True, silver)
    screen.blit(o2_display, (380, 130))
    screen.blit(percent, (440, 148))

    screen.blit(intake_temp_text, (230, 160))
    intake_temp_display = font.render(str(intake_temp), True, silver)
    screen.blit(intake_temp_display, (230, 190))
    screen.blit(deg_F, (290, 210))

    screen.blit(maf_text, (205, 300))
    maf_display = font.render(str("{:.1f}".format(maf)), True, silver)
    screen.blit(maf_display, (205, 340))
    screen.blit(gs_text, (260, 360))

    screen.blit(timing_text, (535, 300))
    timing_adv_display = font.render(str("{:.1f}".format(timing_advance)), True, silver)
    screen.blit(timing_adv_display, (535, 340))
    deg = small_font.render(degree_sign, True, orange)
    screen.blit(deg, (595, 346))

    screen.blit(fuel_rail_text, (670, 100))
    screen.blit(fuel_rail_text2, (670, 140))
    fuel_rail_display = big_font.render(str("{:.1f}".format(fuel_rail_press)), True, white)
    screen.blit(fuel_rail_display, (655, 180))
    screen.blit(psi_text, (670, 270))

    screen.blit(engine_load_e, (20, 100))
    screen.blit(engine_load_l, (20, 140))
    engine_l_display = big_font.render(str(int(load)), True, white)
    screen.blit(engine_l_display, (20, 180))
    screen.blit(percent, (100, 228))

    screen.blit(afr_text, (700, 335))
    afr_display = big_font.render(str("{:.1f}".format(afr)), True, white)
    screen.blit(afr_display, (690, 370))

#############################
#   DATA LOGGING FUNCTIONS  #
#############################

logging_active = small_font.render("Logging Active", True, red)

filename = "data_logging_" + str(date.today()) + ".csv"
header = ['RPM', 'Intake Temp.', 'MAF (g/s)', 'Engine Load', 'Fuel Rail Press.', 'AFR', 'Long B2 Trim', 'Timing Adv.']
with open(filename, "w", newline="") as dl:
    writer = csv.writer(dl)
    writer.writerow(header)

def log_to_file(file_name):
    screen.blit(logging_active, (510, 20))
    row = [str(rpm), str(intake_temp), str(maf), str(load), str(fuel_rail_press), str(afr), str(o2_trim), str(timing_advance)]
    with open(filename, "a", newline="") as dl:
        writer = csv.writer(dl)
        writer.writerow(row)


#############################
#   CODE READER FUNCTIONS   #
#############################


def dtcIntro():
    text_box = text.get_rect()
    text_box.center = (400, 30)
    screen.blit(text, text_box)

def display_dtc(code_list):
    screen.blit(dtc_text, (50, 100))
    y_loc = 200
    # Display DTC codes
    if len(code_list) != 0:
        for code in code_list:
            code = small_font.render(str(code), True, white)
            screen.blit(code, (60, y_loc))
            y_loc += 50
    else:
        screen.blit(no_codes, (60, 200))


#############################
#       GET FPS             #
#############################

# Fps function derived from pythonprogramming.com
# https://pythonprogramming.altervista.org/pygame-how-to-display-the-frame-rate-fps-on-the-screen/

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = small_font.render(fps + " fps", 1, pygame.Color("coral"))
    return fps_text


#########################################
#   Functions to retrieve ECU data      #
#########################################

# Functions written as so defined by Python-OBD authors
# https://python-obd.readthedocs.io/en/latest/Async%20Connections/
def get_speed(s):
    global speed
    if not s.is_null():
        # speed = int(s.value.magnitude) #for kph
        speed = int(s.value.magnitude * .060934)  # for mph


def get_fuel_rail_press(fp):
    global fuel_rail_press
    if not fp.is_null():
        fuel_rail_press = float(fp.value.magnitude) * .145038  # kp to psi


def get_intake_temp(it):
    global intake_temp
    if not it.is_null():
        intake_temp = int(int(it.value.magnitude) * 1.8 + 32)  # C to F


def get_afr(af):
    global afr
    if not af.is_null():
        afr = float(af.value.magnitude) * 14.64 # Convert to AFR for normal gasoline engines


def get_rpm(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)


def get_load(l):
    global load
    if not l.is_null():
        load = int(l.value.magnitude)


def get_coolant_temp(ct):
    global coolant_temp
    if not ct.is_null():
        coolant_temp = int(int(ct.value.magnitude) * 1.8 + 32) # convert to F


def get_intake_press(ip):
    global intake_pressure
    if not ip.is_null():
        intake_pressure = float(ip.value.magnitude)


def get_baro_press(bp):
    global baro_pressure
    if not bp.is_null():
        baro_pressure = float(bp.value.magnitude)


def get_dtc(c):
    global codes
    if not c.is_null():
        codes = c.value


def get_timing_a(ta):
    global timing_advance
    if not ta.is_null():
        timing_advance = str(ta.value).replace("degree", "") # in degrees / remove text from val
        timing_advance = float(timing_advance)


def get_maf(m):
    global maf
    if not m.is_null():
        maf = str(m.value).replace("gps", "")  # grams / second / remove text from val
        maf = float(maf)


def get_o2(o):
    global o2_trim
    if not o.is_null():
        o2_trim = str(o.value).replace("percent", "")  # +/- 3 percent normal range - negative = rich, positive = lean
        o2_trim = float(o2_trim)

def ecu_connections():
    connection.watch(obd.commands.SPEED, callback=get_speed)
    connection.watch(obd.commands.RPM, callback=get_rpm)
    connection.watch(obd.commands.ENGINE_LOAD, callback=get_load)
    connection.watch(obd.commands.GET_DTC, callback=get_dtc)
    connection.watch(obd.commands.COOLANT_TEMP, callback=get_coolant_temp)
    connection.watch(obd.commands.INTAKE_TEMP, callback=get_intake_temp)
    connection.watch(obd.commands.FUEL_RAIL_PRESSURE_DIRECT, callback=get_fuel_rail_press)
    connection.watch(obd.commands.COMMANDED_EQUIV_RATIO, callback=get_afr)
    connection.watch(obd.commands.MAF, callback=get_maf)
    connection.watch(obd.commands.TIMING_ADVANCE, callback=get_timing_a)
    connection.watch(obd.commands.LONG_O2_TRIM_B1, callback=get_o2)

    connection.start()


# Turn off debug mode
obd.logger.removeHandler(obd.console_handler)


# Game loop variables
run = True
home = True
vDash = False
dtcMode = False
logging = False
cnt = 0  # For flash messages
clock = pygame.time.Clock()  # Initiate clock for fps

# Call watch() for ecu connections
ecu_connections()


#################################
#          Game Loop            #
#################################
while run:

    screen.fill(black)
    screen.blit(update_fps(), (0, 456))

    if home:
        screen.blit(quattro_image, (155, 200))
        vDash = False
        dtcMode = False
        cnt = 0
        if virtualDash.draw_button():
            counter = 0
            home = False
            vDash = True

        if dtc.draw_button():
            home = False
            dtcMode = True
    if quit.draw_button():
        run = False
    if not home:
        if go_home.draw_button():
            home = True

    if vDash and cnt < textPopUp:
        virtualDashIntro()
        cnt += 1
    if dtcMode and cnt < textPopUp:
        dtcIntro()
        cnt += 1
    if vDash:
        virtDash()
        if not logging:
            if data_log_off.draw_button():
                logging = True

        if logging:
            log_to_file(filename)

            if data_log_on.draw_button():
                logging = False

    if dtcMode:
        display_dtc(codes)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
