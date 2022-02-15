from buttonClass import *
import os

raspberry_pi = False

#############################
#     Fonts                 #
#                           #
#############################

font = pygame.font.SysFont('agencyfb', 40)
small_font = pygame.font.SysFont('agencyfb', 20)
big_font = pygame.font.SysFont('agencyfb', 70)
rpm_font = pygame.font.SysFont('agencyfb', 40)

#############################
#    Images                 #
#                           #
#############################

if raspberry_pi:
    quattro_image = pygame.image.load("/home/pi/Desktop/OBD_Delay/images/sportquattro.jpg")  # for RPI 4
    gauge_image = pygame.image.load("/home/pi/Desktop/OBD_Delay/images/gaugecrop.jpg")
    needle_image = pygame.image.load("/home/pi/Desktop/OBD_Delay/images/needtransp.png")
else:
    path = os.path.dirname(os.path.abspath(__file__)) + "\\images"
    quattro_image = pygame.image.load(path + "\\sportquattro.jpg")
    gauge_image = pygame.image.load(path + "\\gaugecrop.jpg")
    needle_image = pygame.image.load(path + "\\needtransp.png")

#############################
#      DTC TEXT             #
#                           #
#############################

text = small_font.render("WELCOME TO THE CODE READER", True, silver)
dtc_text = font.render("OBDII CODES:", True, white)
no_codes = 'There are no codes at this time'
no_codes = small_font.render(no_codes, True, white)

#############################
#      Virtual Dash         #
#          Text             #
#                           #
#############################

rpm_text = small_font.render("RPM", True, orange)
degree_sign = u"\N{DEGREE SIGN}"
deg_F = small_font.render(degree_sign + "F", True, orange)
coolant_temp_text = small_font.render("Coolant Temp", True, silver)
o2_trim_text = small_font.render("O2 Trim", True, silver)
percent = small_font.render("%", True, orange)
intake_temp_text = small_font.render("Intake Temp", True, silver)
maf_text = small_font.render("MAF", True, silver)
gs_text = small_font.render("G/S", True, orange)
timing_text = small_font.render("Timing Adv.", True, silver)
psi_text = small_font.render("PSI", True, orange)
fuel_rail_text = font.render("Fuel Rail", True, silver)
fuel_rail_text2 = font.render("Pressure", True, silver)
engine_load_e = font.render("Engine", True, silver)
engine_load_l = font.render("Load", True, silver)
afr_text = font.render("AFR", True, silver)
speed_text = font.render("Speed", True, silver)
mph = small_font.render("MPH", True, orange)

