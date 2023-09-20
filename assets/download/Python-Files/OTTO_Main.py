from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import pickle
import time
from tkcolorpicker import askcolor
import serial
import numpy as np
from sklearn import linear_model
import datetime
from natsort import natsorted
import webbrowser
import os
from ttkthemes import ThemedTk, THEMES

TITLE_FONT = ("Helvetica", 80)
LARGE_FONT = ("Helvetica", 50)
NORM_FONT_BOLD = ("Helvetica bold", 18)
NORM_FONT = ("Helvetica", 18)
SMALLNORM_FONT = ("Helvetica", 15)
SMALLNORM_FONT_BOLD = ("Helvetica bold", 15)
SMALL_FONT = ("Helvetica", 9)
SMALL_FONT_BOLD = ("Helvetica bold", 10)
BUTTON_FONT = ("Helvetica bold", 10)

colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
          '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#000075', '#808080', '#ffffff',
          '#ffd8b1']

time.sleep(1)
ser = serial.Serial()
pipette_box_array = []
primer_plate_array = []
cdna_plate_array = []
primer_array = []
cdna_array = []
unicode_symbols = ['\u2021', '\u00A7', '\u00A5', '\u00A4', '\u00B6', '\u00D0', '\u2020', '\u2021', '\u2022', '\u00D8',
                   '\u00B1', '\u00A2', '\u00DE', '\u00B5', '\u2013']
cdna_locations = []
primer_locations = []
standard_curve_locations = []
active_wells = []
startMarker = 60
endMarker = 62
end_serial_count = 0
Well_Spacing = 9
tip_count = -1


class OTTO(ThemedTk):

    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)
        self.set_theme("smog")
        self.shared_data = {
            "username": StringVar(),
            "password": StringVar(),
            "replicates": StringVar(),
            "standardcurve": StringVar(),
            "Laser_Module": StringVar(),
            "logarithm_number": StringVar(),
            "dilution_factor_number": StringVar(),
            "row_number": StringVar(),
            "barcode": StringVar(),
            "error_message": StringVar(),
            "cursor_position": StringVar(),
            "cdna_volume": StringVar(),
            "total_cdna_volume": StringVar(),
            "primer_volume": StringVar(),
            "occupied_wells": StringVar(),
            "cdna_number": StringVar(),
            "primer_number": StringVar(),
            "Upper_Right_Tip_Box_coord": StringVar(),
            "Upper_Left_Tip_Box_coord": StringVar(),
            "Bottom_Right_Tip_Box_coord": StringVar(),
            "Bottom_Left_Tip_Box_coord": StringVar(),
            "Tip_Spacing": DoubleVar(),
            "Well_Spacing": DoubleVar(),
            "96_Well_coord": StringVar(),
            "96well2_coord": StringVar(),
            "Primer_coord": StringVar(),
            "primer2_coord": StringVar(),
            "primer3_coord": StringVar(),
            "cDNA_coord": StringVar(),
            "cDNA2_coord": StringVar(),
            "cDNA3_coord": StringVar(),
            "cDNA4_coord": StringVar(),
            "Water_coord": StringVar(),
            "Mastermix_coord": StringVar(),
            "Laser_Module_coord": StringVar(),
            "Remover_coord": StringVar(),
            "pallet_coord": StringVar(),
            "Remover2_coord": StringVar(),
            "Remover3_coord": StringVar(),
            "current_position": StringVar(),
            "primer_row_spacing": StringVar(),
            "primer_column_spacing": StringVar(),
            "cdna_row_spacing": StringVar(),
            "cdna_column_spacing": StringVar(),
            "cdna_sector_spacing": StringVar(),
            "x_change": StringVar(),
            "y_change": StringVar(),
            "z_change": StringVar(),
            "led_color": StringVar(),
            "l_coord": StringVar(),
            "step_size": StringVar(),
            "legible_current_position": StringVar(),
            "Hover_Height_coord": StringVar(),
            "Tip_Box_Hover_Height_coord": StringVar(),
            "absolute_coordinate": StringVar(),
            "global_x": StringVar(),
            "global_y": StringVar(),
            "global_z": StringVar(),
            "welcome": StringVar(),
            "now_date": StringVar(),
            "primer_name": StringVar(),
            "add_tag_item": StringVar(),
            "step_change_x": StringVar(),
            "step_change_y": StringVar(),
            "step_change_z": StringVar(),
            "speed": StringVar(),
            "from_arduino": StringVar(),
            "menuvar": StringVar(),
            "assay_choice": StringVar(),
            "gcode_save": IntVar(),
            "pipettevar": StringVar()
        }
        self.pcal = {
            "pcalstep1": DoubleVar(),
            "pcalvol1": DoubleVar(),
            "pcalstep2": DoubleVar(),
            "pcalvol2": DoubleVar(),
            "pcalstep3": DoubleVar(),
            "pcalvol3": DoubleVar(),
            "pcalstep4": DoubleVar(),
            "pcalvol4": DoubleVar(),
            "pcalstep5": DoubleVar(),
            "pcalvol5": DoubleVar(),
            "linear_coefficient": DoubleVar(),
            "linear_intercept": DoubleVar(),
            "mix_number": DoubleVar()
        }

        with open('coordinates.pickle', 'rb') as handle:
            self.pick = pickle.load(handle)

        # Initial Declarations
        self.shared_data["error_message"].set("error")
        self.shared_data["primer_volume"].set("6")
        self.shared_data["cdna_volume"].set("4")
        self.shared_data["total_cdna_volume"].set("10")
        self.shared_data["current_position"].set("0 0 0 0")
        led_color_instance = "#000000"
        self.shared_data["led_color"].set(led_color_instance)
        self.shared_data["welcome"].set("Welcome back")
        self.shared_data["primer_number"].set("0")
        self.shared_data["cdna_number"].set("0")
        self.shared_data["row_number"].set("3")
        self.pcal["mix_number"].set(3)
        self.shared_data["primer_row_spacing"].set("18.75")
        self.shared_data["primer_column_spacing"].set("30")
        self.shared_data["cdna_row_spacing"].set("9")
        self.shared_data["cdna_column_spacing"].set("30")
        self.shared_data["cdna_sector_spacing"].set("87")
        self.shared_data["assay_choice"].set("PCR")
        legible_current_position2 = self.shared_data["current_position"].get()
        legible_current_position2 = legible_current_position2.split()
        legible_current_position2 = "x = " + legible_current_position2[0] + "   y = " + legible_current_position2[
            1] + "   z = " + legible_current_position2[2] + "   p = " + legible_current_position2[3]
        self.shared_data["legible_current_position"].set(legible_current_position2)
        self.shared_data["gcode_save"].set(0)

        # Pulling coordinates from saved pickle file
        self.shared_data["Upper_Right_Tip_Box_coord"].set(self.pick["main_data"]["Upper_Right_Tip_Box_pick"])
        self.shared_data["Upper_Left_Tip_Box_coord"].set(self.pick["main_data"]["Upper_Left_Tip_Box_pick"])
        self.shared_data["Bottom_Right_Tip_Box_coord"].set(self.pick["main_data"]["Bottom_Right_Tip_Box_pick"])
        self.shared_data["Bottom_Left_Tip_Box_coord"].set(self.pick["main_data"]["Bottom_Left_Tip_Box_pick"])
        self.shared_data["Tip_Spacing"].set(self.pick["main_data"]["Tip_Spacing_pick"])
        self.shared_data["96_Well_coord"].set(self.pick["main_data"]["96_Well_pick"])
        self.shared_data["Well_Spacing"].set(self.pick["main_data"]["Well_Spacing_pick"])
        self.shared_data["Primer_coord"].set(self.pick["main_data"]["Primer_pick"])
        self.shared_data["cDNA_coord"].set(self.pick["main_data"]["cDNA_pick"])
        self.shared_data["Water_coord"].set(self.pick["main_data"]["Water_pick"])
        self.shared_data["Mastermix_coord"].set(self.pick["main_data"]["Mastermix_pick"])
        self.shared_data["Laser_Module_coord"].set(self.pick["main_data"]["Laser_Module_pick"])
        self.shared_data["Remover_coord"].set(self.pick["main_data"]["Remover_pick"])
        self.shared_data["pallet_coord"].set(self.pick["main_data"]["pallet_pick"])
        self.shared_data["Hover_Height_coord"].set(self.pick["main_data"]["Hover_Height_pick"])
        self.shared_data["Tip_Box_Hover_Height_coord"].set(self.pick["main_data"]["Tip_Box_Hover_Height_pick"])
        self.shared_data["pipettevar"].set(self.pick["main_data"]["pipettevar_pick"])

        self.shared_data["now_date"].set(
            str(datetime.datetime.now().day) + " / " + str(datetime.datetime.now().month) + " / " + str(
                datetime.datetime.now().year))

        # tk.Tk.iconbitmap(self, default="clienticon.ico")

        Tk.wm_title(self, "OTTO")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Config1, PCR, MotionControl, GCode):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Start", command=lambda: self.show_frame(Config1))
        filemenu.add_command(label="Motion Control", command=lambda: self.show_frame(MotionControl))
        filemenu.add_command(label="Plate Setup", command=lambda: self.show_frame(PCR))
        filemenu.add_command(label="Gcode", command=lambda: self.show_frame(GCode))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=sys.exit)
        menubar.add_cascade(label="File", menu=filemenu)
        Tk.config(self, menu=menubar)

    def show_frame(self, cont):
        print(cont)
        frame = self.frames[cont]
        frame.tkraise()

    # Changes the color of OTTO title
    def colorPick(self, event):
        user_color_pick = askcolor((255, 255, 255), self)
        self.shared_data["led_color"].set(user_color_pick[1])
        l_coord_string = [str(x) for x in user_color_pick[0]]
        l_coord_string = ' '.join(l_coord_string)
        l_coord_string = "l " + l_coord_string + " 0"
        if l_coord_string == "l 0 0 0 0":
            l_coord_string = "l 0 0 0 255"
        l_coord_string = "<" + l_coord_string + ">"
        l_coord_string = l_coord_string.encode('utf-8')
        strippedmsg = ""
        ser.write(l_coord_string)  # prefix b is required for Python 3.x
        while strippedmsg != 'ok':
            msg = ser.readline()
            decodemsg = msg.decode('utf-8', errors='ignore')
            strippedmsg = decodemsg.rstrip()
            print(strippedmsg)
        self.shared_data["l_coord"].set(user_color_pick[0])
        self.frames[MotionControl].otto_label.config(fg=self.shared_data["led_color"].get())
        self.frames[StartPage].ottoTitle.config(fg=self.shared_data["led_color"].get())
        self.frames[PCR].PCR_otto.config(fg=self.shared_data["led_color"].get())
        self.frames[Config1].ottoTitle.config(fg=self.shared_data["led_color"].get())
        pipetteColor = self.shared_data["led_color"].get()

        print(type(pipetteColor))
        if pipetteColor == "#000000":
            pipetteColor = "#8DC21F"
        print(pipetteColor)
        self.frames[Config1].workarea.itemconfig(self.frames[Config1].pipettebody, fill=pipetteColor)
        self.frames[Config1].workarea.itemconfig(self.frames[Config1].pipettebody2, fill=pipetteColor)

    # Indicates connection status of arduino under OTTO Title
    def serial_status(self):
        starttime = time.time()
        while True:
            while ser.isOpen():
                self.frames[Config1].sercheck.itemconfigure("sercheck", fill="green")
            else:
                self.frames[Config1].sercheck.itemconfigure("sercheck", fill="red")
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    # Controls manual movements of OTTO
    def motioncontroller(self, button):
        current_position = list(self.shared_data["current_position"].get().split())
        current_position = [float(b) for b in current_position]
        if button[0] == 'x':
            if button[1] == '+':
                self.frames[MotionControl].commandList.insert(0, "+" + self.shared_data["step_size"].get() + " to x")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                    str(round((current_position[0] + rel_change), 2)) + " " + str(current_position[1]) + " " + str(
                        current_position[2]) + " " + str(current_position[3]))
                self.absolutepositioning()

            if button[1] == '-':
                self.frames[MotionControl].commandList.insert(0, "-" + self.shared_data["step_size"].get() + " from x")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                    str(round((current_position[0] - rel_change), 2)) + " " + str(current_position[1]) + " " + str(
                        current_position[2]) + " " + str(current_position[3]))
                self.absolutepositioning()

        if button[0] == 'y':
            if button[1] == '+':
                self.frames[MotionControl].commandList.insert(0, "+" + self.shared_data["step_size"].get() + " to y")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                    str(current_position[0]) + " " + str(round((current_position[1] + rel_change), 2)) + " " + str(
                        current_position[2]) + " " + str(current_position[3]))
                self.absolutepositioning()

            if button[1] == '-':
                self.frames[MotionControl].commandList.insert(0, "-" + self.shared_data["step_size"].get() + " from y")
                rel_change = float(self.shared_data["step_size"].get())
                self.shared_data["absolute_coordinate"].set(
                    str(current_position[0]) + " " + str(round((current_position[1] - rel_change), 2)) + " " + str(
                        current_position[2]) + " " + str(current_position[3]))
                self.absolutepositioning()

        if button[0] == 'z':
            if button[1] == '+':
                self.frames[MotionControl].commandList.insert(0, "+" + self.shared_data["step_size"].get() + " to z")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                    str(current_position[0]) + " " + str(current_position[1]) + " " + str(
                        round((current_position[2] + rel_change), 2)) + " " + str(current_position[3]))
                self.absolutepositioning()

            if button[1] == '-':
                self.frames[MotionControl].commandList.insert(0, "-" + self.shared_data["step_size"].get() + " from z")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                    str(current_position[0]) + " " + str(current_position[1]) + " " + str(
                        round((current_position[2] - rel_change), 2)) + " " + str(current_position[3]))
                self.absolutepositioning()

        if button[0] == 'p':
            if button[1] == '+':
                self.frames[MotionControl].commandList.insert(0, "+" + self.shared_data["step_size"].get() + " to p")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                    str(current_position[0]) + " " + str(current_position[1]) + " " + str(
                        current_position[2]) + " " + str(round((current_position[3] + rel_change), 2)))
                self.absolutepositioning()
            if button[1] == '-':
                self.frames[MotionControl].commandList.insert(0, "-" + self.shared_data["step_size"].get() + " from p")
                rel_change = float(self.shared_data["step_size"].get())  # stays positive
                self.shared_data["absolute_coordinate"].set(
                str(current_position[0]) + " " + str(current_position[1]) + " " + str(
                    current_position[2]) + " " + str(round((current_position[3] - rel_change), 2)))
            self.absolutepositioning()

    # Encoding of data sent to Arduino
    def sendToArduino(self, sendStr):
        print(sendStr)
        sendStr = sendStr.encode('utf-8')
        ser.write(sendStr)

    # Reading data sent from Arduino
    def recvFromArduino(self):
        global startMarker, endMarker

        ck = ""
        x = "z"  # any value that is not an end- or startMarker
        byteCount = -1  # to allow for the fact that the last increment will be one too many
        timeout = time.time() + 60
        # wait for the start character
        while ord(x) != startMarker and time.time() < timeout:
            x = ser.read()

        # save data until the end marker is found
        while ord(x) != endMarker and time.time() < timeout:
            if ord(x) != startMarker:
                ck = ck + x
                byteCount += 1
            x = ser.read().decode('utf-8', errors='ignore')

        return (ck)

    # ============================

    def waitForArduino(self):

        # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
        # it also ensures that any bytes left over from a previous message are discarded

        global startMarker, endMarker

        msg = ""
        while msg.find("Arduino is ready") == -1:

            while ser.in_waiting == 0:
                pass

            msg = self.recvFromArduino()

            print(msg)
            print()

    # ======================================

    # Sends data for Arduino to interpret
    def runTest(self, td):
        if self.shared_data["gcode_save"].get():
            text_file = open("GCode.txt", "a")
            text_file.write(td[1:-1])
            text_file.write("\n")
            text_file.close()

        elif not self.shared_data["gcode_save"].get():
            waitingForReply = False

            if waitingForReply == False:
                self.sendToArduino(td)
                print("Sent from PC: " + str(td))
                self.frames[GCode].comlist.insert(0, "Sent from PC: " + str(td))
                self.update()
                waitingForReply = True

            if waitingForReply == True:

                while ser.in_waiting == 0:
                    pass

                dataRecvd = self.recvFromArduino()
                splitmsg = list(dataRecvd.split())
                # self.shared_data["current_position"].set(splitmsg[1] + " " + splitmsg[2] + " " + splitmsg[3] + " " + splitmsg[4])
                # legible_current_position2 = "x = " + splitmsg[1] + "   y = " + splitmsg[2] + "   z = " + splitmsg[3] + "   p = " + splitmsg[4]
                # self.shared_data["legible_current_position"].set(legible_current_position2)

                print("Reply Received: " + dataRecvd)
                self.shared_data["from_arduino"].set(dataRecvd)
                self.frames[GCode].comlist.insert(0, "Reply Received:  " + dataRecvd)
                self.update()
                waitingForReply = False

                print("===========")
                self.frames[GCode].comlist.insert(0, "======================================")
                self.update()
            time.sleep(.01)

    # Sends G-code to Arduino to move to an absolute position
    def absolutepositioning(self):

        global end_serial_count

        end_serial_count = end_serial_count + 1
        print("End_serial_count =" + str(end_serial_count))

        self.shared_data["current_position"].set(self.shared_data["absolute_coordinate"].get())

        splitmsg = list(self.shared_data["current_position"].get().split())
        legible_current_position2 = "x = " + splitmsg[0] + "   y = " + splitmsg[1] + "   z = " + splitmsg[
            2] + "   p = " + splitmsg[3]
        self.shared_data["legible_current_position"].set(legible_current_position2)
        gcode = "X" + splitmsg[0] + " Y" + splitmsg[1] + " Z" + splitmsg[
            2] + " P" + splitmsg[3]

        self.runTest("<G1 " + gcode + ">")

        # gcode = list(self.shared_data["absolute_coordinate"].get().split())
        # hoverheight = [float(b) for b in hoverheight]

        if end_serial_count == 10000000:
            ser.close()
            time.sleep(5)
            ser.open()
            time.sleep(10)
            self.runTest("<g " + self.shared_data["current_position"].get() + ">")
            end_serial_count = 0
            self.shared_data["speed"].set("4000 2500 4000 5000")
            print("RESET the ARDUINO")

    # Offsets all coordinates
    def global_offset(self):
        if self.shared_data["global_x"].get() == "":
            self.shared_data["global_x"].set("0")
        if self.shared_data["global_y"].get() == "":
            self.shared_data["global_y"].set("0")
        if self.shared_data["global_z"].get() == "":
            self.shared_data["global_z"].set("0")

        queposition = list(self.shared_data["Upper_Right_Tip_Box_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Upper_Right_Tip_Box_coord"].set(queposition)

        queposition = list(self.shared_data["Upper_Left_Tip_Box_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Upper_Left_Tip_Box_coord"].set(queposition)

        queposition = list(self.shared_data["Bottom_Right_Tip_Box_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Bottom_Right_Tip_Box_coord"].set(queposition)

        queposition = list(self.shared_data["96_Well_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["96_Well_coord"].set(queposition)

        queposition = list(self.shared_data["96well2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["96well2_coord"].set(queposition)

        queposition = list(self.shared_data["Primer_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Primer_coord"].set(queposition)

        queposition = list(self.shared_data["primer2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["primer2_coord"].set(queposition)

        queposition = list(self.shared_data["primer3_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["primer3_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA2_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA3_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA3_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA4_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA4_coord"].set(queposition)

        queposition = list(self.shared_data["Remover_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Remover_coord"].set(queposition)

        queposition = list(self.shared_data["Remover2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Remover2_coord"].set(queposition)

        queposition = list(self.shared_data["Water_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Water_coord"].set(queposition)

        queposition = list(self.shared_data["Mastermix_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Mastermix_coord"].set(queposition)

        queposition = list(self.shared_data["Remover3_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(queposition[0] + int(self.shared_data["global_x"].get()))
        queposition[1] = str(queposition[1] + int(self.shared_data["global_y"].get()))
        queposition[2] = str(queposition[2] + int(self.shared_data["global_z"].get()))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Remover3_coord"].set(queposition)

        print(queposition)

    def step_change(self):
        if self.shared_data["step_change_x"].get() == "":
            self.shared_data["step_change_x"].set("1")
        if self.shared_data["step_change_y"].get() == "":
            self.shared_data["step_change_y"].set("1")
        if self.shared_data["step_change_z"].get() == "":
            self.shared_data["step_change_z"].set("1")

        queposition = list(self.shared_data["Upper_Right_Tip_Box_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Upper_Right_Tip_Box_coord"].set(queposition)

        queposition = list(self.shared_data["Upper_Left_Tip_Box_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Upper_Left_Tip_Box_coord"].set(queposition)

        queposition = list(self.shared_data["Bottom_Right_Tip_Box_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Bottom_Right_Tip_Box_coord"].set(queposition)

        queposition = list(self.shared_data["96_Well_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["96_Well_coord"].set(queposition)

        queposition = list(self.shared_data["96well2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["96well2_coord"].set(queposition)

        queposition = list(self.shared_data["Primer_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Primer_coord"].set(queposition)

        queposition = list(self.shared_data["primer2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["primer2_coord"].set(queposition)

        queposition = list(self.shared_data["primer3_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["primer3_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA2_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA3_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA3_coord"].set(queposition)

        queposition = list(self.shared_data["cDNA4_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["cDNA4_coord"].set(queposition)

        queposition = list(self.shared_data["Remover_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Remover_coord"].set(queposition)

        queposition = list(self.shared_data["Remover2_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Remover2_coord"].set(queposition)

        queposition = list(self.shared_data["Water_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Water_coord"].set(queposition)

        queposition = list(self.shared_data["Mastermix_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Mastermix_coord"].set(queposition)

        queposition = list(self.shared_data["Remover3_coord"].get().split())
        queposition[0] = int(queposition[0])
        queposition[1] = int(queposition[1])
        queposition[2] = int(queposition[2])
        queposition[0] = str(int(queposition[0] * float(self.shared_data["step_change_x"].get())))
        queposition[1] = str(int(queposition[1] * float(self.shared_data["step_change_y"].get())))
        queposition[2] = str(int(queposition[2] * float(self.shared_data["step_change_z"].get())))
        queposition = queposition[0] + " " + queposition[1] + " " + queposition[2]
        self.shared_data["Remover3_coord"].set(queposition)

    # Prints Primers and cDNAs in the legend area of the GCode Frame
    def prepare_plate(self):
        self.show_frame(GCode)
        global primer_locations
        global cdna_locations
        global unicode_symbols
        global active_wells
        global standard_curve_locations

        primer_locations = natsorted(primer_locations)
        cdna_locations = natsorted(cdna_locations)
        standard_curve_locations = natsorted(standard_curve_locations)

        print(primer_locations)
        print(cdna_locations)
        active_wells = [[[0 for i in range(2)] for j in range(12)] for k in range(8)]
        print(active_wells)
        catch_all_primer = []
        catch_all_cdna = []
        catch_all_standard_curve = []

        for x in range(0, 96):
            self.frames[GCode].workarea.itemconfigure("final_plate" + str(x), fill="white")
            self.frames[GCode].workarea.itemconfigure("text" + str(x), text="")
            self.frames[GCode].workarea.itemconfigure("clearprimers", text="")
            self.frames[GCode].workarea.itemconfigure("clearprimersicon", fill="white", width=0)
            self.frames[GCode].workarea.itemconfigure("clearcdna", text="")
            self.frames[GCode].workarea.itemconfigure("clearcdnaicon", fill="white")
            self.frames[GCode].workarea.itemconfigure("clearstandardcurve", text="")
            self.frames[GCode].workarea.itemconfigure("clearstandardcurveicon", fill="white")

        cdna_number = int(self.shared_data["cdna_number"].get())
        primer_number = int(self.shared_data["primer_number"].get())
        replicates_number = int(self.shared_data["replicates"].get())
        if self.shared_data["logarithm_number"].get() == '':
            standard_curve_number = 0
        if not self.shared_data["logarithm_number"].get() == '':
            standard_curve_number = int(self.shared_data["logarithm_number"].get())

        print(cdna_number)
        print(primer_number)
        print(standard_curve_number)
        space1 = 0
        space2 = 0
        for i in range(0, len(primer_locations)):
            primer_name = primer_locations[i]

            if i == 9:
                space2 = 100
                space1 = 0
            # self.frames[GCode].workarea.create_text(20, 475+20*i, text=(unicode_symbols[int(primer_name[6:])]), font=("Purisa", 15), anchor="nw")
            self.frames[GCode].workarea.create_text(30 + space2, 462 + 20 * space1, text=primer_locations[i],
                                                    font=("DejaVu", 12), anchor="nw", tags="clearprimers")
            self.frames[GCode].workarea.create_oval(10 + space2, 465 + 20 * space1, 25 + space2, 480 + 20 * space1,
                                                    fill=colors[int(primer_name[6:])], width=2, tags="clearprimersicon")
            space1 = space1 + 1

        space1 = 0
        space2 = 0
        for i in range(0, len(cdna_locations)):
            cdna_name = cdna_locations[i]

            if i == 9:
                space2 = 100
                space1 = 0
            # self.frames[GCode].workarea.create_text(20, 475+20*i, text=(unicode_symbols[int(primer_name[6:])]), font=("Purisa", 15), anchor="nw")
            self.frames[GCode].workarea.create_text(350 + space2, 462 + 20 * space1,
                                                    text=(unicode_symbols[int(cdna_name[4:])]),
                                                    font=("Helvetica", 12), anchor="nw", tags="clearcdna")
            self.frames[GCode].workarea.create_text(380 + space2, 462 + 20 * space1, text=cdna_locations[i],
                                                    font=("Helvetica", 12), anchor="nw", tags="clearcdnaicon")

            space1 = space1 + 1

        space1 = 0
        space2 = 0

        sub = [sub.replace('cdna', 'standard curve') for sub in standard_curve_locations]
        for i in range(0, len(standard_curve_locations)):
            standard_curve_name = standard_curve_locations[i]

            if i == 9:
                space2 = 100
                space1 = 0
            # self.frames[GCode].workarea.create_text(20, 475+20*i, text=(unicode_symbols[int(primer_name[6:])]), font=("Purisa", 15), anchor="nw")
            self.frames[GCode].workarea.create_text(130 + space2, 462 + 20 * space1,
                                                    text=(unicode_symbols[int(standard_curve_name[4:])]),
                                                    font=("Helvetica", 12), anchor="nw", tags="clearstandardcurve")
            self.frames[GCode].workarea.create_text(160 + space2, 462 + 20 * space1, text=sub[i],
                                                    font=("Helvetica", 12), anchor="nw", tags="clearstandardcurveicon")

            space1 = space1 + 1

        if primer_number * replicates_number < 13 and (cdna_number + standard_curve_number) < 9:
            for y in range(0, primer_number):
                for x in range(0, standard_curve_number):
                    for i in range(0, replicates_number):
                        active_wells[x][i + y * replicates_number][0] = primer_locations[y]
                        active_wells[x][i + y * replicates_number][1] = standard_curve_locations[x]

            for y in range(0, primer_number):
                for x in range(standard_curve_number, standard_curve_number + cdna_number):
                    for i in range(0, replicates_number):
                        active_wells[x][i + y * replicates_number][0] = primer_locations[y]
                        active_wells[x][i + y * replicates_number][1] = cdna_locations[x - standard_curve_number]

        elif (cdna_number + standard_curve_number) * replicates_number < 13 and primer_number < 9:
            for y in range(0, standard_curve_number):
                for x in range(0, primer_number):
                    for i in range(0, replicates_number):
                        active_wells[x][i + y * replicates_number][0] = primer_locations[x]
                        active_wells[x][i + y * replicates_number][1] = standard_curve_locations[y]

            for y in range(standard_curve_number, standard_curve_number + cdna_number):
                for x in range(0, primer_number):
                    for i in range(0, replicates_number):
                        active_wells[x][i + y * replicates_number][0] = primer_locations[x]
                        active_wells[x][i + y * replicates_number][1] = cdna_locations[y - standard_curve_number]

        else:
            for y in range(0, standard_curve_number):
                for x in range(0, primer_number):
                    for i in range(0, 3):
                        print(primer_locations)
                        print(cdna_locations)
                        catch_all_primer.append(primer_locations[x])
                        if not standard_curve_number == 0:
                            print(standard_curve_locations)
                            catch_all_standard_curve.append(standard_curve_locations[y])

            for a in range(0, cdna_number):
                for b in range(0, primer_number):
                    for j in range(0, replicates_number):
                        print(primer_locations)
                        print(cdna_locations)
                        catch_all_primer.append(primer_locations[b])
                        catch_all_cdna.append(cdna_locations[a])

            print(len(catch_all_primer))
            print(len(catch_all_cdna))
            print(len(catch_all_standard_curve))
        count = -1

        y = 0
        t = 0
        for i in range(0, len(catch_all_standard_curve)):
            active_wells[y][t][0] = catch_all_primer[i]
            if not standard_curve_number == 0:
                active_wells[y][t][1] = catch_all_standard_curve[i]
            t = t + 1
            if t == 12:
                t = 0
                y = y + 1

        for i in range(len(catch_all_standard_curve), len(catch_all_primer)):
            active_wells[y][t][0] = catch_all_primer[i]
            active_wells[y][t][1] = catch_all_cdna[i - len(catch_all_standard_curve)]
            t = t + 1
            if t == 12:
                t = 0
                y = y + 1

        for y in range(0, 8):
            for x in range(0, 12):
                count = count + 1
                if active_wells[y][x][0] != 0:
                    self.frames[GCode].workarea.itemconfigure("final_plate" + str(count),
                                                              fill=self.frames[PCR].plate.itemcget(
                                                                  active_wells[y][x][0], "fill"))
                    self.frames[GCode].workarea.itemconfigure("text" + str(count),
                                                              text=unicode_symbols[int(active_wells[y][x][1][4:])])

        print(active_wells)
        print(len(active_wells))

        # for i in range (0, len())

        self.shared_data["now_date"].set(
            str(datetime.datetime.now().day) + " / " + str(datetime.datetime.now().month) + " / " + str(
                datetime.datetime.now().year))

    def home(self):
        """
        self.shared_data["current_position"].set(self.shared_data["absolute_coordinate"].get())
        splitmsg = list(self.shared_data["current_position"].get().split())
        legible_current_position2 = "x = " + splitmsg[0] + "   y = " + splitmsg[1] + "   z = " + splitmsg[2] + "   p = " + splitmsg[3]
        self.shared_data["legible_current_position"].set(legible_current_position2)
        """
        home_var = "<G28>"
        self.runTest(home_var)
        self.shared_data["current_position"].set("330 360 0 0")
        self.shared_data["legible_current_position"].set("330 360 0 0")
        self.shared_data["absolute_coordinate"].set("330 360 0 0")

        """
        while strippedmsg != 'ok':
            msg = ser.readline()
            decodemsg = msg.decode('utf-8', errors='ignore')
            strippedmsg = decodemsg.rstrip()
            if strippedmsg == "":
                strippedmsg = " "
            if strippedmsg[0] == 'A':
                splitmsg = list(strippedmsg.split())
                self.shared_data["current_position"].set(
                    splitmsg[1] + " " + splitmsg[2] + " " + splitmsg[3] + " " + splitmsg[4])
                legible_current_position2 = "x = " + splitmsg[1] + "   y = " + splitmsg[2] + "   z = " + splitmsg[
                    3] + "   p = " + splitmsg[4]
                self.shared_data["legible_current_position"].set(legible_current_position2)
        """

    # Lasers check to see if tip is on. If it isn't, it will attempt to put on another tip and finally throw an error
    # message if it isn't again.
    def home_tip(self):
        global tip_count
        laser_module = self.shared_data["Laser_Module_coord"].get() + " 0"
        laserhover = list(laser_module.split())
        laserhover = [float(b) for b in laserhover]
        hoverheight = list(self.shared_data["Hover_Height_coord"].get().split())
        hoverheight = [float(b) for b in hoverheight]
        tiphoverheight = list(self.shared_data["Tip_Box_Hover_Height_coord"].get().split())
        tiphoverheight = [float(b) for b in tiphoverheight]
        self.shared_data["absolute_coordinate"].set(
            str(laserhover[0]) + " " + str(laserhover[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()
        self.shared_data["absolute_coordinate"].set(laser_module)
        self.absolutepositioning()

        tip_check = False
        count = 0

        # todo loop is off
        while tip_check == False:
            self.runTest("<M1001>")
            if self.shared_data["from_arduino"].get() == "no" and count == 0:
                tip_count = tip_count + 1
                tip_coord = list(pipette_box_array[tip_count].split())
                tip_coord = [float(b) for b in tip_coord]
                self.shared_data["absolute_coordinate"].set(
                    str(laserhover[0]) + " " + str(laserhover[1]) + " " + str(hoverheight[2]) + " 0")
                self.absolutepositioning()
                self.remove_tip()
                self.shared_data["absolute_coordinate"].set(
                    str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(tiphoverheight[2]) + " 0")
                self.absolutepositioning()
                self.runTest("<G38>")
                self.shared_data["absolute_coordinate"].set(
                    str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(laserhover[0]) + " " + str(laserhover[1]) + " " + str(hoverheight[2]) + " 0")
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(laser_module)
                self.absolutepositioning()
                count = 1
                self.runTest("<M1001>")
            if self.shared_data["from_arduino"].get() == "no" and count == 1:
                self.runTest("<M150 R255 G0 B0>")
                self.win3 = Toplevel()
                self.win3.wm_title("Tip Warning")
                msg = Message(self.win3, text="Failed to detect pipette tip.", font=SMALLNORM_FONT_BOLD)
                msg.pack()
                button = Button(self.win3, text="Recheck", command=self.win3.destroy)
                button.pack()
                self.win3.geometry("%dx%d+%d+%d" % (300, 300, 700, 400))
                self.wait_window(self.win3)

            else:
                tip_check = True
        self.runTest("<M150 R255 G255 B255>")
        self.shared_data["absolute_coordinate"].set(
            str(laserhover[0]) + " " + str(laserhover[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()

    def remove_tip(self):
        global tip_count
        tip_count = tip_count + 1
        tip_coord = list(pipette_box_array[tip_count].split())
        tip_coord = [float(b) for b in tip_coord]
        Remover = list(self.shared_data["Remover_coord"].get().split())
        Remover = [float(b) for b in Remover]
        hoverheight = list(self.shared_data["Hover_Height_coord"].get().split())
        hoverheight = [float(b) for b in hoverheight]
        self.shared_data["absolute_coordinate"].set(
            str(Remover[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()
        self.shared_data["absolute_coordinate"].set(
            str(Remover[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2] + 4) + " 0")
        self.absolutepositioning()
        tip_count = tip_count - 1

    def standard_curve(self):
        global standard_curve_locations
        global cdna_locations
        global Well_Spacing
        global tip_count

        pipette_box_array = []

        # Tip coordinates are receieved as a string so they are split into a list of floats here
        Upper_Right_Tip_Box = list(self.shared_data["Upper_Right_Tip_Box_coord"].get().split())
        Upper_Right_Tip_Box = [float(b) for b in Upper_Right_Tip_Box]
        Upper_Left_Tip_Box = list(self.shared_data["Upper_Left_Tip_Box_coord"].get().split())
        Upper_Left_Tip_Box = [float(b) for b in Upper_Left_Tip_Box]
        Bottom_Right_Tip_Box = list(self.shared_data["Bottom_Right_Tip_Box_coord"].get().split())
        Bottom_Right_Tip_Box = [float(b) for b in Bottom_Right_Tip_Box]
        Bottom_Left_Tip_Box = list(self.shared_data["Bottom_Left_Tip_Box_coord"].get().split())
        Bottom_Left_Tip_Box = [float(b) for b in Bottom_Left_Tip_Box]
        Tip_Spacing = self.shared_data["Tip_Spacing"].get()

        # Arrays are built that contain coordinates for every single position of a tip box based off the initial
        # coordinates set by the user

        # Box 3
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Bottom_Right_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Bottom_Right_Tip_Box[1] - Tip_Spacing * y) + " " + str(Bottom_Right_Tip_Box[2]))
        # Box 4
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Bottom_Left_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Bottom_Left_Tip_Box[1] - Tip_Spacing * y) + " " + str(Bottom_Left_Tip_Box[2]))
        # Box 1
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Upper_Right_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Upper_Right_Tip_Box[1] - Tip_Spacing * y) + " " + str(Upper_Right_Tip_Box[2]))
        # Box 2
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Upper_Left_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Upper_Left_Tip_Box[1] - Tip_Spacing * y) + " " + str(Upper_Left_Tip_Box[2]))

        # cDNA coordinates
        cDNA = list(self.shared_data["cDNA_coord"].get().split())
        cDNA = [float(b) for b in cDNA]
        cdna2 = list(self.shared_data["cDNA2_coord"].get().split())
        cdna2 = [float(b) for b in cdna2]
        cdna3 = list(self.shared_data["cDNA3_coord"].get().split())
        cdna3 = [float(b) for b in cdna3]
        cdna4 = list(self.shared_data["cDNA4_coord"].get().split())
        cdna4 = [float(b) for b in cdna4]
        rowspacing = cDNA[1] - cdna3[1]
        columnspacing = cdna2[0] - cDNA[0]
        sectorspacing = cDNA[1] - cdna4[1]

        for z in range(0, 2):
            for x in range(0, 4):
                for y in range(0, 8):
                    cdna_array.append(str(cDNA[0] + columnspacing * x) + " " + str(
                        cDNA[1] - rowspacing * y - sectorspacing * z) + " " + str(cDNA[2]))

        cdna_count = 1
        cdna_keys = []
        for i in range(0, 64):
            cdna_keys.append("cdna" + str(cdna_count))
            cdna_count = cdna_count + 1

        cdna_keys = tuple(cdna_keys)

        cdna_number_to_position = dict(zip(cdna_keys, cdna_array))

        global active_wells
        print("in standard curve")

        hoverheight = list(self.shared_data["Hover_Height_coord"].get().split())
        hoverheight = [float(b) for b in hoverheight]
        tiphoverheight = list(self.shared_data["Tip_Box_Hover_Height_coord"].get().split())
        tiphoverheight = [float(b) for b in tiphoverheight]

        Water = list(self.shared_data["Water_coord"].get().split())
        Water = [float(b) for b in Water]
        current_position = list(self.shared_data["current_position"].get().split())
        current_position = [float(b) for b in current_position]
        total_concentrate_volume = float(self.shared_data["primer_volume"].get() + self.shared_data["cdna_volume"].get())
        dilution_factor = int(self.shared_data["dilution_factor_number"].get())
        concentrate_volume = total_concentrate_volume * (1 / dilution_factor)
        diluent_volume = total_concentrate_volume - concentrate_volume
        linear_coefficient = self.pcal["linear_coefficient"].get()
        linear_intercept = self.pcal["linear_intercept"].get()
        mix_number = int(self.pcal["mix_number"].get())
        cdna_volume_steps = round((concentrate_volume - linear_intercept) / linear_coefficient, 3)
        Water_volume_steps = round((diluent_volume - linear_intercept) / linear_coefficient, 3)

        mix_volume_steps = round((10 - linear_intercept) / linear_coefficient, 3)

        print(linear_coefficient)
        print(linear_intercept)
        print(cdna_volume_steps)
        print(Water_volume_steps)

        previous_active_wells = "t"

        tip_count = -1

        self.home()
        # self.home_pipette()

        # Put on New Tip
        tip_count = tip_count + 1
        tip_coord = list(pipette_box_array[tip_count].split())
        tip_coord = [float(b) for b in tip_coord]
        self.shared_data["absolute_coordinate"].set(
            str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()
        self.shared_data["absolute_coordinate"].set(
            str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(tiphoverheight[2]) + " 0")
        self.absolutepositioning()
        self.runTest("<G38>")
        self.shared_data["absolute_coordinate"].set(
            str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()

        # Place Water in all standard curve locations other than first well which contains undiluted mixture
        for v in range(0, len(standard_curve_locations) - 1):
            # Go to and pick up Water
            self.shared_data["absolute_coordinate"].set(
                str(Water[0]) + " " + str(current_position[1]) + " " + str(hoverheight[2]) + " 0")
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(Water[0]) + " " + str(current_position[1]) + " " + str(hoverheight[2]) + " " + str(Water_volume_steps))
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(Water[0]) + " " + str(current_position[1]) + " " + str(Water[2]) + " " + str(Water_volume_steps))
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(Water[0]) + " " + str(current_position[1]) + " " + str(Water[2]) + " 0")
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(Water[0]) + " " + str(current_position[1]) + " " + str(hoverheight[2]) + " 0")
            self.absolutepositioning()

            # Go to first Serial Dilution well
            next_cdna_coord = list(cdna_number_to_position.get(standard_curve_locations[v + 1]).split())
            next_cdna_coord = [float(b) for b in next_cdna_coord]
            self.shared_data["absolute_coordinate"].set(
                str(next_cdna_coord[0]) + " " + str(next_cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(next_cdna_coord[0]) + " " + str(next_cdna_coord[1]) + " " + str(next_cdna_coord[2]) + " " + str(
                    0))
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(next_cdna_coord[0]) + " " + str(next_cdna_coord[1]) + " " + str(next_cdna_coord[2]) + " " + str(
                    Water_volume_steps))
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(next_cdna_coord[0]) + " " + str(next_cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                    Water_volume_steps))
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(next_cdna_coord[0]) + " " + str(next_cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
            self.absolutepositioning()

        # Remove Tip
        self.remove_tip()

        tip_count = tip_count + 1
        tip_coord = list(pipette_box_array[tip_count].split())
        tip_coord = [float(b) for b in tip_coord]

        self.shared_data["absolute_coordinate"].set(
            str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()
        self.shared_data["absolute_coordinate"].set(
            str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(tiphoverheight[2]) + " 0")
        self.absolutepositioning()
        self.runTest("<G38>")
        self.shared_data["absolute_coordinate"].set(
            str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
        self.absolutepositioning()

        # Perform Serial Dilution
        for v in range(0, len(standard_curve_locations)):
            if v == 0:
                # Standard Curve
                cdna_coord = list(cdna_number_to_position.get(standard_curve_locations[v]).split())
                cdna_coord = [float(b) for b in cdna_coord]
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                        mix_volume_steps))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(
                        mix_volume_steps))
                self.absolutepositioning()

                # Standard Curve MIX
                for k in range(0, mix_number):
                    # if mix_volume_steps < cdnavol
                    self.shared_data["absolute_coordinate"].set(
                        str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                            cdna_coord[2]) + " " + str(0))
                    self.absolutepositioning()
                    self.shared_data["absolute_coordinate"].set(
                        str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                            cdna_coord[2]) + " " + str(mix_volume_steps))
                    self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                        hoverheight[2]) + " " + str(mix_volume_steps))
                self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                        hoverheight[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                        hoverheight[2]) + " " + str(cdna_volume_steps))
                self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(
                        cdna_volume_steps))
                self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                self.absolutepositioning()

            else:
                # Standard Curve
                cdna_coord = list(cdna_number_to_position.get(standard_curve_locations[v]).split())
                cdna_coord = [float(b) for b in cdna_coord]
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(
                        cdna_volume_steps))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                        cdna_volume_steps))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                        0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                        mix_volume_steps))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(
                        mix_volume_steps))
                self.absolutepositioning()

                # Standard Curve MIX
                for k in range(0, mix_number):
                    self.shared_data["absolute_coordinate"].set(
                        str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                            cdna_coord[2]) + " " + str(0))
                    self.absolutepositioning()
                    self.shared_data["absolute_coordinate"].set(
                        str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                            cdna_coord[2]) + " " + str(mix_volume_steps))
                    self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                        hoverheight[2]) + " " + str(mix_volume_steps))
                self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                        hoverheight[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                        hoverheight[2]) + " " + str(cdna_volume_steps))
                self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(
                        cdna_volume_steps))
                self.absolutepositioning()

                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(0))
                self.absolutepositioning()
                self.shared_data["absolute_coordinate"].set(
                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                self.absolutepositioning()

        # Remove Tip
        self.remove_tip()
        self.shared_data["absolute_coordinate"].set(str(0) + " " + str(0) + " " + str(0) + " " + str(0))
        self.absolutepositioning()

    # 96 well PCR run
    def test_run(self):

        global primer_locations
        global cdna_locations
        global primer_plate_array
        global cdna_plate_array
        global Well_Spacing
        global standard_curve_locations
        global tip_count
        if os.path.exists("GCode.txt"):
            os.remove("GCode.txt")

        cdna_locations = standard_curve_locations + cdna_locations

        # Tip coordinates are receieved as a string so they are split into a list of floats here
        Upper_Right_Tip_Box = list(self.shared_data["Upper_Right_Tip_Box_coord"].get().split())
        Upper_Right_Tip_Box = [float(b) for b in Upper_Right_Tip_Box]
        Upper_Left_Tip_Box = list(self.shared_data["Upper_Left_Tip_Box_coord"].get().split())
        Upper_Left_Tip_Box = [float(b) for b in Upper_Left_Tip_Box]
        Bottom_Right_Tip_Box = list(self.shared_data["Bottom_Right_Tip_Box_coord"].get().split())
        Bottom_Right_Tip_Box = [float(b) for b in Bottom_Right_Tip_Box]
        Bottom_Left_Tip_Box = list(self.shared_data["Bottom_Left_Tip_Box_coord"].get().split())
        Bottom_Left_Tip_Box = [float(b) for b in Bottom_Left_Tip_Box]
        Tip_Spacing = self.shared_data["Tip_Spacing"].get()

        # Arrays are built that contain coordinates for every single position of a tip box based off the initial
        # coordinates set by the user

        # Box 3
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Bottom_Right_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Bottom_Right_Tip_Box[1] - Tip_Spacing * y) + " " + str(Bottom_Right_Tip_Box[2]))
        # Box 4
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Bottom_Left_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Bottom_Left_Tip_Box[1] - Tip_Spacing * y) + " " + str(Bottom_Left_Tip_Box[2]))

        # Box 1
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Upper_Right_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Upper_Right_Tip_Box[1] - Tip_Spacing * y) + " " + str(Upper_Right_Tip_Box[2]))
        # Box 2
        for y in range(0, 12):
            for x in range(0, 8):
                pipette_box_array.append(str(Upper_Left_Tip_Box[0] - Tip_Spacing * x) + " " + str(
                    Upper_Left_Tip_Box[1] - Tip_Spacing * y) + " " + str(Upper_Left_Tip_Box[2]))

        print(pipette_box_array)
        print(cdna_locations)
        print(primer_locations)

        left_well = list(self.shared_data["96_Well_coord"].get().split())
        left_well = [float(b) for b in left_well]
        right_well = list(self.shared_data["96_Well_coord"].get().split())
        right_well = [float(b) for b in right_well]

        # left well (primer)
        for y in range(0, 8):
            for x in range(0, 12):
                primer_plate_array.append(
                    str(left_well[0] + Well_Spacing * x) + " " + str(left_well[1] - Well_Spacing * y) + " " + str(
                        left_well[2]))
        print(primer_plate_array)

        # right well (cDNA)
        for y in range(0, 8):
            for x in range(0, 12):
                cdna_plate_array.append(
                    str(right_well[0] + Well_Spacing * x) + " " + str(right_well[1] - Well_Spacing * y) + " " + str(
                        right_well[2]))
        print(cdna_plate_array)
        primer1 = list(self.shared_data["Primer_coord"].get().split())
        primer1 = [float(b) for b in primer1]
        primer_column_spacing = float(self.shared_data["primer_column_spacing"].get())
        primer_row_spacing = float(self.shared_data["primer_row_spacing"].get())

        for y in range(0, 9):
            for x in range(0, 2):
                primer_array.append(str(primer1[0] + primer_column_spacing * x) + " " + str(
                    primer1[1] + primer_row_spacing * y) + " " + str(primer1[2]))

        print(primer_array)
        cDNA = list(self.shared_data["cDNA_coord"].get().split())
        cDNA = [float(b) for b in cDNA]
        rowspacing = float(self.shared_data["cdna_row_spacing"].get())
        columnspacing = float(self.shared_data["cdna_column_spacing"].get())
        sectorspacing = float(self.shared_data["cdna_sector_spacing"].get())

        for z in range(0, 2):
            for x in range(0, 4):
                for y in range(0, 8):
                    cdna_array.append(str(cDNA[0] - columnspacing * x) + " " + str(
                        cDNA[1] + rowspacing * y + sectorspacing * z) + " " + str(cDNA[2]))

        cdna_count = 1
        cdna_keys = []
        for i in range(0, 64):
            cdna_keys.append("cdna" + str(cdna_count))
            cdna_count = cdna_count + 1

        cdna_keys = tuple(cdna_keys)

        cdna_number_to_position = dict(zip(cdna_keys, cdna_array))

        primer_count = 1
        primer_keys = []
        for i in range(0, 18):
            primer_keys.append("primer" + str(primer_count))
            primer_count = primer_count + 1

        primer_keys = tuple(primer_keys)
        primer_number_to_position = dict(zip(primer_keys, primer_array))

        global active_wells
        print("in test run")

        hoverheight = list(self.shared_data["Hover_Height_coord"].get().split())
        hoverheight = [float(b) for b in hoverheight]
        tiphoverheight = list(self.shared_data["Tip_Box_Hover_Height_coord"].get().split())
        tiphoverheight = [float(b) for b in tiphoverheight]
        cdna_volume = float(self.shared_data["cdna_volume"].get())
        primer_volume = float(self.shared_data["primer_volume"].get())
        linear_coefficient = self.pcal["linear_coefficient"].get()
        linear_intercept = self.pcal["linear_intercept"].get()
        mix_number = int(self.pcal["mix_number"].get())
        cdna_volume_steps = round((cdna_volume - linear_intercept) / linear_coefficient, 3)
        primer_volume_steps = round((primer_volume - linear_intercept) / linear_coefficient, 3)

        mix_volume_steps = round(linear_coefficient * 10 + linear_intercept, 3)

        print(linear_coefficient)
        print(linear_intercept)
        print(primer_volume_steps)
        print(cdna_volume_steps)

        self.home()
        # self.home_pipette()
        print(primer_locations)

        if int(self.shared_data["standardcurve"].get()) == 1:
            self.standard_curve()
        else:
            tip_count = -1

        for v in range(0, len(primer_locations)):
            tip_count = tip_count + 1
            tip_coord = list(pipette_box_array[tip_count].split())
            tip_coord = [float(b) for b in tip_coord]
            self.shared_data["absolute_coordinate"].set(
                str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(tiphoverheight[2]) + " 0")
            self.absolutepositioning()
            self.runTest("<G38>")
            self.shared_data["absolute_coordinate"].set(
                str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
            self.absolutepositioning()
            if int(self.shared_data["Laser_Module"].get()) == 1:
                self.home_tip()

            i = 0
            plate_count = -1

            for y in range(0, 8):
                for x in range(0, 12):
                    plate_count = plate_count + 1
                    if active_wells[y][x][0] == primer_locations[v]:

                        # PRIMER
                        primer_coord = list(primer_number_to_position.get(primer_locations[v]).split())
                        primer_coord = [float(b) for b in primer_coord]
                        self.shared_data["absolute_coordinate"].set(
                            str(primer_coord[0]) + " " + str(primer_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                                primer_volume_steps))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(primer_coord[0]) + " " + str(primer_coord[1]) + " " + str(primer_coord[2]) + " " + str(
                                primer_volume_steps))
                        self.absolutepositioning()

                        # PRIMER MIX
                        if i == 0:
                            i = 1
                            for k in range(0, mix_number):
                                self.shared_data["absolute_coordinate"].set(
                                    str(primer_coord[0]) + " " + str(primer_coord[1]) + " " + str(
                                        primer_coord[2]) + " " + str(0))
                                self.absolutepositioning()
                                self.shared_data["absolute_coordinate"].set(
                                    str(primer_coord[0]) + " " + str(primer_coord[1]) + " " + str(
                                        primer_coord[2]) + " " + str(primer_volume_steps))
                                self.absolutepositioning()

                        self.shared_data["absolute_coordinate"].set(
                            str(primer_coord[0]) + " " + str(primer_coord[1]) + " " + str(primer_coord[2]) + " " + str(
                                0))
                        self.absolutepositioning()

                        self.shared_data["absolute_coordinate"].set(
                            str(primer_coord[0]) + " " + str(primer_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                                0))
                        self.absolutepositioning()

                        # PRIMER to PLATE
                        plate_coord = list(primer_plate_array[plate_count].split())
                        plate_coord = [float(b) for b in plate_coord]
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(plate_coord[2]) + " " + str(0))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(plate_coord[2]) + " " + str(
                                primer_volume_steps))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                                primer_volume_steps))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(str(plate_coord[0]) + " " + str(plate_coord[1])
                                                                    + " " + str(hoverheight[2]) + " " + str(0))
                        self.absolutepositioning()
            # Remove Tip
            self.remove_tip()

        for v in range(0, len(cdna_locations)):

            tip_count = tip_count + 1
            tip_coord = list(pipette_box_array[tip_count].split())
            tip_coord = [float(b) for b in tip_coord]

            self.shared_data["absolute_coordinate"].set(
                str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
            self.absolutepositioning()
            self.shared_data["absolute_coordinate"].set(
                str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(tiphoverheight[2]) + " 0")
            self.absolutepositioning()
            self.runTest("<G38>")
            self.shared_data["absolute_coordinate"].set(
                str(tip_coord[0]) + " " + str(tip_coord[1]) + " " + str(hoverheight[2]) + " 0")
            self.absolutepositioning()
            if int(self.shared_data["Laser_Module"].get()) == 1:
                self.home_tip()
            plate_count = -1
            i = 0

            for y in range(0, 8):
                for x in range(0, 12):
                    plate_count = plate_count + 1

                    if active_wells[y][x][1] == cdna_locations[v]:

                        # CDNA
                        cdna_coord = list(cdna_number_to_position.get(cdna_locations[v]).split())
                        cdna_coord = [float(b) for b in cdna_coord]
                        self.shared_data["absolute_coordinate"].set(
                            str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                                cdna_volume_steps))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(
                                cdna_volume_steps))
                        self.absolutepositioning()

                        # CDNA MIX
                        if i == 0:
                            i = 1
                            for k in range(0, mix_number):
                                self.shared_data["absolute_coordinate"].set(
                                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                                        cdna_coord[2]) + " " + str(0))
                                self.absolutepositioning()
                                self.shared_data["absolute_coordinate"].set(
                                    str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(
                                        cdna_coord[2]) + " " + str(cdna_volume_steps))
                                self.absolutepositioning()

                        self.shared_data["absolute_coordinate"].set(
                            str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(cdna_coord[2]) + " " + str(0))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(cdna_coord[0]) + " " + str(cdna_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                        self.absolutepositioning()

                        # CDNA to PLATE
                        plate_coord = list(cdna_plate_array[plate_count].split())
                        plate_coord = [float(b) for b in plate_coord]
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(plate_coord[2]) + " " + str(0))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(plate_coord[2]) + " " + str(
                                cdna_volume_steps))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(hoverheight[2]) + " " + str(
                                cdna_volume_steps))
                        self.absolutepositioning()
                        self.shared_data["absolute_coordinate"].set(
                            str(plate_coord[0]) + " " + str(plate_coord[1]) + " " + str(hoverheight[2]) + " " + str(0))
                        self.absolutepositioning()
            # Remove Tip
            self.remove_tip()

        self.shared_data["absolute_coordinate"].set(str(0) + " " + str(0) + " " + str(0) + " " + str(0))
        self.absolutepositioning()


class StartPage(Frame):
    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1, uniform="foo")
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=1, uniform="foo")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(10, weight=3)

        self.ottoTitle = Label(self, text="OTTO", font=TITLE_FONT)
        self.ottoTitle.grid(row=1, column=3)
        self.ottoTitle.bind('<Button-1>', self.controller.colorPick)
        print(self.controller.shared_data["led_color"].get())

        photoPipetteTips = PhotoImage(file="pipette_underline.gif")
        title_Underline = Label(self, image=photoPipetteTips)
        title_Underline.photo = photoPipetteTips
        title_Underline.grid(row=2, column=3)

        self.website_link = Canvas(self, width=300, height=125, bg="lemon chiffon")
        self.website_link.create_text(150, 50, width=250,
                                      text="This is an early alpha version intended as a supplement to the "
                                           "publication. For updated versions, see the link below:")
        self.website_link.create_text(150, 100, text="https://openliquidhandler.com/", tag="website", fill="blue")
        self.website_link.tag_bind("website", "<Button-1>",
                                   lambda x: webbrowser.open_new("https://openliquidhandler.com/"))

        self.website_link.grid(row=0, column=6, sticky='ne')

        # userframe = Frame(self)
        # Label(userframe, text="Username:", font=SMALL_FONT).pack(side=LEFT)
        # self.userEntry = Entry(userframe, textvariable=self.controller.shared_data["username"])
        # self.userEntry.pack(side=LEFT)
        # userframe.grid(row=3, column=3)
        #
        # passframe = Frame(self)
        # Label(passframe, text="Password: ", font=SMALL_FONT).pack(side=LEFT)
        # self.passEntry = Entry(passframe, show='*', textvariable=self.controller.shared_data["password"])
        # self.passEntry.pack(side=LEFT)
        # passframe.grid(row=4, column=3)
        #
        # loginframe = Frame(self)
        # Label(loginframe, text="                    ", font=SMALL_FONT).pack(side=LEFT)
        # Label(loginframe, text="New User", font="Helvetica 12 underline").pack(side=LEFT)
        # Label(loginframe, text="           ", font=SMALL_FONT).pack(side=LEFT)
        # Button(loginframe, text="Login", command=self.login_on_button).pack(side=LEFT)
        # loginframe.grid(row=5, column=3)
        self.port = StringVar()
        style = ttk.Style()
        portFrame = Frame(self)
        Label(portFrame, text="Enter Port Name:", font="Helvetica 16").pack(side=LEFT, padx=(0, 10))
        port_entry = Entry(portFrame, textvariable=self.port, width=15)
        port_entry.pack(side=LEFT)
        portFrame.grid(row=5, column=3, pady=40)
        style.configure("welcome.TButton", font=("Helvetica", 16))
        Button(self, text="Connect!", command=lambda: self.connect_port(),
               style="welcome.TButton").grid(row=7, column=3)

        quote = Label(self, text="Fast is fine, but accuracy is everything.", font="Helvetica 16 italic")
        quote.grid(row=8, column=3)

        quote2 = Label(self, text="-Xenophon                    ", font="Helvetica 16 italic")
        quote2.grid(row=9, column=3, sticky="e")

        credit = Label(self, text="By David Florian & Mateusz Odziomek", font=SMALL_FONT)
        credit.grid(row=11, column=6, sticky="E")

    def connect_port(self):
        try:
            ser.baudrate = 9600
            ser.port = "{}".format(self.port.get())
            ser.open()
            if ser.isOpen():
                self.controller.show_frame(Config1)
        except (serial.serialutil.SerialException, UnboundLocalError):
                self.win = Toplevel()
                self.win.geometry("%dx%d+%d+%d" % (300, 300, 600, 300))
                self.win.wm_title("Reminder!")
                self.win.attributes('-topmost', 'true')
                s = ttk.Style()
                self.bg = s.lookup('TFrame', 'background')
                self.win.configure(background=self.bg)
                self.win.grid_columnconfigure(0, weight=1)
                self.win.grid_columnconfigure(2, weight=1)
                textframe = Canvas(self.win, background=self.bg, width=200, height=150)
                Label(self.win, font=("Helvetica", 20), text="Warning:").grid(row=1, column=1, padx=20, pady=10)
                textframe.create_text(100, 20,
                                      text="Port is incorrect. Please check it again.",
                                      font="Helvetica 12", width=150, anchor="n")
                textframe.configure(state="disabled")
                textframe.grid(row=2, column=1)
                Button(self.win, text="Got it!", command=lambda: self.win.destroy()).grid(row=3, column=1)
                Button(self.win, text="Continue without connecting",
                       command=lambda: [self.controller.show_frame(Config1), self.win.destroy()]).grid(row=4, column=1)


    def login_on_button(self):
        for line in open("usernamespasswords", "r").readlines():  # Read the lines
            login_info = line.split()  # Split on the space, and store the results in a list of two strings
            if self.userEntry.get() == login_info[0] and self.passEntry.get() == login_info[1]:
                print("Correct credentials!")
                self.controller.show_frame(Config1)
                print(type(self.controller.shared_data["username"].get()))
                self.controller.shared_data["welcome"].set(
                    "Welcome back " + self.controller.shared_data["username"].get() + "!")
                return True
            else:
                print("Incorrect credentials.")
                credit = Label(self, text="Incorrect Login", fg="red", font=SMALL_FONT)
                credit.grid(row=6, column=3)
                return False


class Config1(Frame):
    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.ottoTitle = Label(self, text="OTTO", font=LARGE_FONT)
        self.ottoTitle.bind('<Button-1>', self.controller.colorPick)
        s = ttk.Style()
        self.bg = s.lookup('TFrame', 'background')
        self.sercheck = Canvas(self, width=150, height=20, background=self.bg)
        self.sercheck.create_text(60, 12.5, text="Serial Connection", font=SMALL_FONT)
        self.sercheck.create_oval(120, 5, 135, 20, tags="sercheck", width=3, fill="red")
        self.sercheck.grid(row=2, column=7, pady=(0, 10))
        # self.controller.serial_status()
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.ottoTitle.grid(row=1, column=7, padx=20, pady=20, sticky="ne", rowspan=2)
        Label(self, textvariable=controller.shared_data["welcome"], font=("Helvetica", 40)).grid(row=1, column=3,
                                                                                                 sticky="n",
                                                                                                 pady=(45, 0))
        self.workarea = Canvas(self, width=200, height=670, background='white')

        p1x = 0
        p1y = 0
        self.pipettebody = self.workarea.create_polygon(100.470 + p1x, 117.290 + p1y, 100.470 + p1x, 92.920 + p1y,
                                                        14.000 + p1x, 77.560 + p1y, 11.660 + p1x, 94.560 + p1y,
                                                        30.660 + p1x, 97.230 + p1y, 45.660 + p1x, 117.230 + p1y,
                                                        51.070 + p1x, 310.900 + p1y, 121.500 + p1x, 310.900 + p1y,
                                                        131.500 + p1x, 120.960 + p1y, fill="red")
        p2x = 51
        p2y = 317
        self.pipettebody2 = self.workarea.create_rectangle(0 + p2x, 0 + p2y, 45.73 + p2x, 29.71 + p2y, width=0,
                                                           fill="red")
        p3x = 0
        p3y = 0
        self.plunger = self.workarea.create_polygon(94.50 + p3x, 28.83 + p3y, 53.70 + p3x, 28.83 + p3y, 46.23 + p3x,
                                                    37.01 + p3y, 53.70 + p3x, 45.19 + p3y, 69.76 + p3x, 45.19 + p3y,
                                                    69.76 + p3x, 87.19 + p3y, 71.30 + p3x, 87.46 + p3y, 78.44 + p3x,
                                                    88.73 + p3y, 78.44 + p3x, 45.18 + p3y, 94.50 + p3x, 45.18 + p3y,
                                                    101.97 + p3x, 37.00 + p3y, 94.50 + p3x, 28.83 + p3y, fill="#C4B898")
        p4x = 0
        p4y = 0
        self.tip = self.workarea.create_polygon(87.15 + p4x, 351.00 + p4y, 61.38 + p4x, 351.00 + p4y, 59.38 + p4x,
                                                353.00 + p4y, 59.38 + p4x, 381.00 + p4y, 61.38 + p4x, 383.00 + p4y,
                                                65.46 + p4x, 383.00 + p4y, 67.46 + p4x, 385.00 + p4y, 67.46 + p4x,
                                                584.66 + p4y, 69.46 + p4x, 586.66 + p4y, 79.21 + p4x, 586.66 + p4y,
                                                81.21 + p4x, 584.66 + p4y, 81.21 + p4x, 385.00 + p4y, 83.21 + p4x,
                                                383.00 + p4y, 87.29 + p4x, 383.00 + p4y, 89.29 + p4x, 381.00 + p4y,
                                                89.29 + p4x, 352.92 + p4y, 87.15 + p4x, 351.00 + p4y, fill="#C4B898")
        p5x = 0
        p5y = 0
        self.tip2 = self.workarea.create_polygon(107.48 + p5x, 315.57 + p5y, 117.48 + p5x, 315.57 + p5y, 117.48 + p5x,
                                                 339.23 + p5y, 117.48 + p5x, 339.43 + p5y, 91.12 + p5x, 393.76 + p5y,
                                                 84.7 + p5x, 564.26 + p5y, 60.08 + p5x, 564.26 + p5y, 60.08 + p5x,
                                                 547.73 + p5y, 74.27 + p5x, 547.73 + p5y, 81.11 + p5x, 393.73 + p5y,
                                                 107.48 + p5x, 339.31 + p5y, fill="#786A56")
        p6x = 0
        p6y = 0
        self.tip3 = self.workarea.create_polygon(119 + p6x, 97 + p6y, 130 + p6x, 97 + p6y, 130 + p6x, 97 + p6y,
                                                 130 + p6x, 93 + p6y, 130 + p6x, 92 + p6y, 106 + p6x, 92 + p6y,
                                                 105 + p6x, 93 + p6y, 105 + p6x, 118 + p6y, 105 + p6x, 118 + p6y,
                                                 118 + p6x, 119 + p6y, 119 + p6x, 119 + p6y, 119 + p6x, 98 + p6y,
                                                 119 + p6x, 97 + p6y, fill="#C4B898")
        self.pipettetext = self.workarea.create_text(88, 160, text="Select\nPipette", font=NORM_FONT_BOLD)
        self.workarea.grid(row=3, column=7, rowspan=4)

        self.textframe = Canvas(self, bg="white", width=300, height=350)
        self.intro_text = self.textframe.create_text(150, 140, text="OTTO is not currently equipped with a pipette. "
                                                                    "Please click the button below to go to the motion "
                                                                    "controller to configure the work space and pipette."
                                                                    " After, please select the assay "
                                             "you wish to run as well as the plate size. Click setup plate when ready. "
                                             .format(self.controller.shared_data["pipettevar"].get()),
                              font="Helvetica 14", width=250)
        self.textframe.configure(state="disabled")
        style = ttk.Style()
        style.configure("configure.TButton", font=("Helvetica", 14), background="white")
        layout = Button(self, text="Layout", command=lambda: self.controller.show_frame(MotionControl),
                        style="configure.TButton")
        self.textframe.create_window(150, 320, window=layout)
        self.textframe.grid(row=3, column=1, padx=(75, 0), pady=(100, 0))

        assayframe = Canvas(self, bg="white", width=300, height=350)
        style = ttk.Style()
        style.configure("big.TRadiobutton", font=("Helvetica", 18), background="white")
        assays = [
            (1, "PCR"),
            (2, "Dilution"),
            (3, "Flow")
        ]

        assayframe.create_text(150, 80, text="Choice of Assay: ", font=NORM_FONT)
        radiobuttons = []
        for val, text in assays:
            radioassay = ttk.Radiobutton(self, text=text, style="big.TRadiobutton",
                                         variable=self.controller.shared_data["assay_choice"], value=val)
            radioassay.grid(sticky="w")
            radiobuttons.append(radioassay)
            assayframe.create_window(100, 120 + 40 * val, window=radioassay, anchor="w")

        # Disables the other options as the features haven't been implemented yet
        for buttons in radiobuttons:
            if buttons == radiobuttons[0]:
                continue
            buttons.config(state=DISABLED)
        assayframe.grid(row=3, column=3, pady=(100, 0))

        self.workarea4 = Canvas(self, bg='white', width=300, height=350)
        self.workarea4.create_text(150, 50, text="Select Type of Plate:", font=('Helvetica', 15))

        self.menuvar = StringVar()
        style.configure("big.TMenubutton", font=("Helvetica", 15))
        dropdown = OptionMenu(self, self.menuvar, '96 Well Plate', '96 Well Plate', '384 Well Plate', 'Flow Tubes',
                              style="big.TMenubutton")
        # Disabled until features are implemented
        dropdown['menu'].entryconfigure('384 Well Plate', state="disabled")
        dropdown['menu'].entryconfigure('Flow Tubes', state="disabled")
        self.menuvar.set("Select")
        self.menuvar.trace("w", self.option_change)
        self.workarea4.create_window(150, 80, window=dropdown)
        for controlY in range(0, 8):
            for controlX in range(0, 12):
                self.workarea4.create_oval(18.0769 + 23.0769 * controlX, 143.8889 + 18.889 * controlY,
                                           28.0769 + 23.0769 * controlX, 153.889 + 18.889 * controlY, width=2)
        self.plate = self.workarea4.create_rectangle(5, 135, 295, 295, width=5, tags="setupPlate")
        setup = Button(self, text="Setup Plate", command=lambda: self.to_PCR_page(),
                        style="configure.TButton")
        self.workarea4.create_window(150, 320, window=setup)
        # self.workarea4.create_text(150, 320, text="Setup Plate", tags="setupPlate", font=NORM_FONT_BOLD)
        # self.workarea4.tag_bind("setupPlate", '<ButtonPress-1>', self.to_PCR_page)
        self.workarea4.grid(row=3, column=5, pady=(100, 0))
        self.bind("<Enter>", self.update_pipette_sizes)

    def update_pipette_sizes(self, *args):
        if self.controller.shared_data["pipettevar"].get() == " ":
            self.workarea.itemconfigure(self.pipettetext, text="Select\nPipette")
        else:
            self.workarea.itemconfigure(self.pipettetext, text="{} \nin use".format(self.controller.shared_data["pipettevar"].get()))
            self.textframe.itemconfigure(self.intro_text, text="OTTO is currently equipped with a {} pipette. Please "
                                                              "select the assay "
                                             "you wish to run as well as the plate size. Click setup plate when ready. "
                                             "If this is your first time or you need to update the configuration, please"
                                             " click the button below to configure the workspace or pipette."
                                        .format(self.controller.shared_data["pipettevar"].get()),)

    def option_change(self, *args):
        tempvar = self.menuvar.get()
        self.controller.shared_data["menuvar"].set(tempvar)
        if self.menuvar.get() != "Select":
            self.workarea4.itemconfig(self.plate, activefill="blue", stipple='gray50')

    def to_PCR_page(self):
        if self.menuvar.get() == '96 Well Plate':
            self.controller.show_frame(PCR)


class PCR(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        s = ttk.Style()
        self.bg = s.lookup('TFrame', 'background')
        self.sercheck = Canvas(self, width=150, height=20, background=self.bg)
        self.sercheck.create_text(60, 12.5, text="Serial Connection", font=SMALL_FONT)
        self.sercheck.create_oval(120, 5, 135, 20, tags="sercheck", width=3, fill="red")
        self.sercheck.grid(row=1, column=11)
        # self.controller.serial_status()
        self.grid_columnconfigure(9, weight=1)
        self.grid_columnconfigure(0, minsize=90)
        self.grid_columnconfigure(11, minsize=250)

        Label(self, textvariable=controller.shared_data["welcome"], font=NORM_FONT).grid(row=1, column=1, columnspan=2,
                                                                                         pady=(20, 55), sticky="nw")

        self.PCR_otto = Label(self, text="OTTO", font=LARGE_FONT)
        self.PCR_otto.grid(row=1, column=11, padx=10, sticky='n', pady=(20, 0))
        self.PCR_otto.bind('<Button-1>', self.controller.colorPick)

        self.plate = Canvas(self, bg='white', width=575, height=650)
        insideCount = 0
        for epiY in range(0, 9):
            for epiX in range(0, 2):
                insideCount = insideCount + 1
                self.plate.create_oval(420 + epiX * 80, 590 - (epiY * 65), 460 + epiX * 80, 630 - (epiY * 65),
                                       fill="white",
                                       activefill="red", width=3, tags="primer" + str(insideCount))
                self.plate.create_text(400 + epiX * 80, 610 - epiY * 65, text=insideCount, font=("Purisa", 12))
        insidecountPCR = 0
        for pcrZ in range(0, 2):
            for pcrX in range(0, 4):
                for pcrY in range(0, 8):
                    insidecountPCR = insidecountPCR + 1
                    self.plate.create_oval(300 - pcrX * 80, 605 - (pcrY * 30) - 325 * pcrZ, 325 - pcrX * 80,
                                           630 - (pcrY * 30) - 325 * pcrZ, fill="white", activefill="gray", width=3,
                                           tags="cdna" + str(insidecountPCR))
                    self.plate.create_text(286 - pcrX * 80, 617.5 - pcrY * 30 - 325 * pcrZ, text=insidecountPCR,
                                           font=("Purisa", 12))
        self.plate.create_text(190, 30, text="cDNA (& Standard Curves)", font=("Purisa", 15))
        self.plate.create_text(470, 30, text="Gene Master Mix", font=("Purisa", 15))
        self.plate.create_rectangle(10, 8, 570, 642, width=5)
        self.plate.grid(row=1, column=9, rowspan=8, pady=(45, 0))
        Button(self, text="Generate Plate", command=self.controller.prepare_plate).grid(row=10, column=9, padx=10,
                                                                                        pady=10)
        laserframe = Frame(self)
        lm = [
            ("off", "0"),
            ("on", "1"),
        ]
        Label(self, text="Laser_Module/Tip Checking: ", font=SMALL_FONT).grid(row=2, column=2, sticky="nw")
        for text, onoroff in lm:
            radiolm = Radiobutton(laserframe, text=text,
                                  variable=self.controller.shared_data["Laser_Module"], value=onoroff)
            radiolm.pack(side=LEFT)
        laserframe.grid(row=2, column=3, sticky="nw")

        standardframe = Frame(self)
        scurve = [
            ("no", "0"),
            ("yes", "1"),
        ]
        Label(self, text="Standard Curves: ", font=SMALL_FONT).grid(row=2, column=2, sticky="w")
        for text, yesorno in scurve:
            radioscurve = Radiobutton(standardframe, text=text,
                                      variable=self.controller.shared_data["standardcurve"], value=yesorno,
                                      command=lambda: self.standardcurve_click(self))
            radioscurve.pack(side=LEFT)
        standardframe.grid(row=2, column=3, sticky="w")

        self.l7 = Label(self, text="How many genes do you have:", font=SMALL_FONT)
        self.l7.grid(row=int(self.controller.shared_data["row_number"].get()), column=2, sticky="nw")

        self.gene_refresh = Entry(self, textvariable=self.controller.shared_data["primer_number"], width=10)
        self.gene_refresh.grid(row=int(self.controller.shared_data["row_number"].get()), column=3, sticky="nw")
        self.controller.shared_data["primer_number"].trace("w", self.primerFill)

        self.l8 = Label(self, text="How many samples do you have:", font=SMALL_FONT)
        self.l8.grid(row=int(self.controller.shared_data["row_number"].get()) + 1, column=2, sticky="nw")
        self.e8 = Entry(self, textvariable=self.controller.shared_data["cdna_number"], width=10)
        self.e8.grid(row=int(self.controller.shared_data["row_number"].get()) + 1, column=3, sticky="nw")
        self.controller.shared_data["cdna_number"].trace("w", self.cdnaFill)

        self.replicateframe = ttk.Frame(self)
        self.l9 = Label(self, text="Number of Replicates: ", font=SMALL_FONT)
        self.l9.grid(row=int(self.controller.shared_data["row_number"].get()) + 2, column=2, sticky="nw")

        MODES = [
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ]

        self.controller.shared_data["replicates"].set("3")
        self.controller.shared_data["standardcurve"].set("0")
        self.controller.shared_data["Laser_Module"].set("0")

        for text, mode in MODES:
            radioreplicates = Radiobutton(self.replicateframe, text=text,
                                          variable=self.controller.shared_data["replicates"], value=mode)
            radioreplicates.pack(side=LEFT)
        self.replicateframe.grid(row=int(self.controller.shared_data["row_number"].get()) + 2, column=3, sticky="nw")

        self.l1 = Label(self, text="uL of cDNA per well:", font=SMALL_FONT)
        self.l1.grid(row=int(self.controller.shared_data["row_number"].get()) + 3, column=2, sticky="nw")
        self.e1 = Entry(self, textvariable=self.controller.shared_data["cdna_volume"], width=10)
        self.e1.grid(row=int(self.controller.shared_data["row_number"].get()) + 3, column=3, sticky="nw")
        self.controller.shared_data["cdna_volume"].trace_variable('w', self.correct_pipette_size_window)

        self.l2 = Label(self, text="uL of Primer/Master Mix per well:", font=SMALL_FONT)
        self.l2.grid(row=int(self.controller.shared_data["row_number"].get()) + 4, column=2, sticky="nw")
        self.e2 = Entry(self, textvariable=self.controller.shared_data["primer_volume"], width=10)
        self.e2.grid(row=int(self.controller.shared_data["row_number"].get()) + 4, column=3, sticky="nw")
        self.controller.shared_data["primer_volume"].trace_variable('w', self.correct_pipette_size_window)

        self.l3 = Label(self, text="Plate Barcode (Optional): ", font=SMALL_FONT)
        self.l3.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=2, sticky="nw")
        self.e3 = Entry(self, textvariable=self.controller.shared_data["barcode"], width=10)
        self.e3.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=3, sticky="nw")

        reminder = Text(self, width=55, height=8, font="Helvetica 12")
        reminder.grid(row=1, column=2, columnspan=2, pady=(50, 0), sticky="n")

        reminder.tag_configure("bold", font="Helvetica 12 bold")
        reminder.tag_configure("underline", font="Helvetica 12 underline")
        reminder.tag_configure("bold", font="Helvetica 12 bold")
        reminder.tag_configure("italics", font="Helvetica 12 italic")

        reminder.insert("end", "This is a ")
        reminder.insert("end", "96_Well", "bold")
        reminder.insert("end", " PCR reaction.")
        reminder.insert("end",
                        "\n \nSample #  \u00D7  Gene #  \u00D7  Replicates  \u2264  96.\ncDNA + Primer/Master Mix < Pipette Size\n \nTurning standard curves ")
        reminder.insert("end", "on", "underline")
        reminder.insert("end",
                        " will occupy: Logarithm #  \u00D7  Gene #  \u00D7 \nReplicate # additional wells. A standard curve will be run for all genes.\nOTTO does not have a brain, use yours!")
        reminder.config(state=DISABLED)

        style = ttk.Style()
        style.configure("well.TLabel", foreground='black')
        self.l4 = Label(self, text="Occupied wells:", font=SMALL_FONT_BOLD)
        self.l4.grid(row=int(self.controller.shared_data["row_number"].get()) + 6, column=2, sticky="ne", pady=1)
        self.occupied_wells_label = Label(self, font=SMALL_FONT_BOLD,
                                          textvariable=self.controller.shared_data["occupied_wells"],
                                          style="well.TLabel")
        self.occupied_wells_label.grid(row=int(self.controller.shared_data["row_number"].get()) + 6, column=3,
                                       sticky="nw", pady=1)

        self.controller.shared_data["replicates"].trace_variable('w', self.plate_capacity)

    def correct_pipette_size_window(self, *args):
        pipette_size = self.controller.shared_data["pipettevar"].get()
        try:
            if float(self.controller.shared_data["cdna_volume"].get() > int(pipette_size[1:]) or float(
                    self.controller.shared_data["primer_volume"].get())) > int(pipette_size[1:]):
                self.win = Toplevel()
                self.win.geometry("%dx%d+%d+%d" % (400, 200, 650, 300))
                self.win.wm_title("Reminder!")
                self.win.attributes('-topmost', 'true')
                self.win.configure(background=self.bg)
                self.win.grid_columnconfigure(0, weight=1)
                self.win.grid_columnconfigure(2, weight=1)
                textframe = Canvas(self.win, background=self.bg, width=400, height=500)
                Label(self.win, font=("Helvetica", 20), text="Reminder:").grid(row=1, column=1, padx=20, pady=10)
                textframe.create_text(200, 20,
                                      text="Your primer + cDNA volume exceeds the pipette size. Please either switch to a "
                                           "larger volume pipette or decrease the amount of primer or cDNA.",
                                      font="Helvetica 12", width=350, anchor="n")
                textframe.configure(state="disabled")
                textframe.grid(row=2, column=1)
        except ValueError:
            pass

    def standardcurve_click(self, event):
        global cdna_locations
        global logarithm_locations
        global standard_curve_locations
        self.controller.shared_data["logarithm_number"].set("0")
        self.controller.shared_data["dilution_factor_number"].set("0")

        if int(self.controller.shared_data["standardcurve"].get()) == 1:
            print("standardcurve")
            self.l1.destroy()
            self.l2.destroy()
            self.l3.destroy()
            self.l4.destroy()
            self.e1.destroy()
            self.e2.destroy()
            self.e3.destroy()
            self.l7.destroy()
            self.gene_refresh.destroy()
            self.l8.destroy()
            self.e8.destroy()
            self.l9.destroy()
            self.replicateframe.destroy()
            self.occupied_wells_label.destroy()
            self.controller.shared_data["row_number"].set("5")

            self.l5 = Label(self, text="How many logarithms:")
            self.l5.grid(row=3, column=2, sticky="nw")
            self.e5 = Entry(self, textvariable=self.controller.shared_data["logarithm_number"], width=10)
            self.e5.grid(row=3, column=3, sticky="nw")
            self.controller.shared_data["logarithm_number"].trace("w", self.standardcurveFill)

            self.l6 = Label(self, text="What dilution factor:")
            self.l6.grid(row=4, column=2, sticky="nw")
            self.e6 = Entry(self, textvariable=self.controller.shared_data["dilution_factor_number"], width=10)
            self.e6.grid(row=4, column=3, sticky="nw")

            self.l7 = Label(self, text="How many genes do you have:")
            self.l7.grid(row=int(self.controller.shared_data["row_number"].get()), column=2, sticky="nw")

            self.gene_refresh = Entry(self, textvariable=self.controller.shared_data["primer_number"], width=10)
            self.gene_refresh.grid(row=int(self.controller.shared_data["row_number"].get()), column=3, sticky="nw")
            self.controller.shared_data["primer_number"].trace("w", self.primerFill)

            self.l8 = Label(self, text="How many samples do you have:")
            self.l8.grid(row=int(self.controller.shared_data["row_number"].get()) + 1, column=2, sticky="nw")
            self.e8 = Entry(self, textvariable=self.controller.shared_data["cdna_number"], width=10)
            self.e8.grid(row=int(self.controller.shared_data["row_number"].get()) + 1, column=3, sticky="nw")
            self.controller.shared_data["cdna_number"].trace("w", self.cdnaFill)

            self.replicateframe = Frame(self)
            self.l9 = Label(self, text="Number of Replicates: ")
            self.l9.grid(row=int(self.controller.shared_data["row_number"].get()) + 2, column=2, sticky="nw")

            MODES = [
                ("1", "1"),
                ("2", "2"),
                ("3", "3"),
            ]

            self.controller.shared_data["replicates"].set("3")

            for text, mode in MODES:
                radioreplicates = Radiobutton(self.replicateframe, text=text,
                                              variable=self.controller.shared_data["replicates"], value=mode)
                radioreplicates.pack(side=LEFT)
            self.replicateframe.grid(row=int(self.controller.shared_data["row_number"].get()) + 2, column=3,
                                     sticky="nw")

            self.l1 = Label(self, text="uL of cDNA per well:")
            self.l1.grid(row=int(self.controller.shared_data["row_number"].get()) + 3, column=2, sticky="nw")
            self.e1 = Entry(self, textvariable=self.controller.shared_data["cdna_volume"], width=10)
            self.e1.grid(row=int(self.controller.shared_data["row_number"].get()) + 3, column=3, sticky="nw")

            self.l2 = Label(self, text="uL of Primer/Master Mix per well:")
            self.l2.grid(row=int(self.controller.shared_data["row_number"].get()) + 4, column=2, sticky="nw")
            self.e2 = Entry(self, textvariable=self.controller.shared_data["primer_volume"], width=10)
            self.e2.grid(row=int(self.controller.shared_data["row_number"].get()) + 4, column=3, sticky="nw")

            self.l3 = Label(self, text="Plate Barcode (Optional): ")
            self.l3.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=2, sticky="nw")
            self.e3 = Entry(self, textvariable=self.controller.shared_data["barcode"], width=10)
            self.e3.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=3, sticky="nw")

            self.l4 = Label(self, text="Occupied wells:")
            self.l4.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=2, sticky="ne",
                         pady=(20, 0))
            self.occupied_wells_label = Label(self, textvariable=self.controller.shared_data["occupied_wells"],
                                              style="well.TLabel")
            self.occupied_wells_label.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=3,
                                           sticky="nw", pady=(20, 0))
            self.controller.shared_data["replicates"].trace_variable('w', self.plate_capacity)

        if int(self.controller.shared_data["standardcurve"].get()) == 0:
            print("notstandardcurve")
            self.l1.destroy()
            self.l2.destroy()
            self.l3.destroy()
            self.l4.destroy()
            self.e1.destroy()
            self.e2.destroy()
            self.e3.destroy()
            self.l5.destroy()
            self.e5.destroy()
            self.l6.destroy()
            self.e6.destroy()
            self.l7.destroy()
            self.gene_refresh.destroy()
            self.l8.destroy()
            self.e8.destroy()
            self.l9.destroy()
            self.replicateframe.destroy()
            self.occupied_wells_label.destroy()
            self.controller.shared_data["row_number"].set("3")

            for i in range(37, 165, 2):
                self.plate.itemconfig(i, fill="white")
                standard_curve_locations = []
                cdna_locations = []
            self.controller.shared_data["cdna_number"].set("0")

            self.l7 = Label(self, text="How many genes do you have:")
            self.l7.grid(row=int(self.controller.shared_data["row_number"].get()), column=2, sticky="nw")

            self.gene_refresh = Entry(self, textvariable=self.controller.shared_data["primer_number"],
                                      width=10)
            self.gene_refresh.grid(row=int(self.controller.shared_data["row_number"].get()), column=3, sticky="nw")
            self.controller.shared_data["primer_number"].trace("w", self.primerFill)

            self.l8 = Label(self, text="How many samples do you have:")
            self.l8.grid(row=int(self.controller.shared_data["row_number"].get()) + 1, column=2, sticky="nw")
            self.e8 = Entry(self, textvariable=self.controller.shared_data["cdna_number"], width=10)
            self.e8.grid(row=int(self.controller.shared_data["row_number"].get()) + 1, column=3, sticky="nw")
            self.controller.shared_data["cdna_number"].trace("w", self.cdnaFill)

            self.replicateframe = Frame(self)
            self.l9 = Label(self, text="Number of Replicates: ")
            self.l9.grid(row=int(self.controller.shared_data["row_number"].get()) + 2, column=2, sticky="nw")

            MODES = [
                ("1", "1"),
                ("2", "2"),
                ("3", "3"),
            ]

            self.controller.shared_data["replicates"].set("3")

            for text, mode in MODES:
                radioreplicates = Radiobutton(self.replicateframe, text=text,
                                              variable=self.controller.shared_data["replicates"], value=mode)
                radioreplicates.pack(side=LEFT)
            self.replicateframe.grid(row=int(self.controller.shared_data["row_number"].get()) + 2, column=3,
                                     sticky="nw")

            self.l1 = Label(self, text="uL of cDNA per well:")
            self.l1.grid(row=int(self.controller.shared_data["row_number"].get()) + 3, column=2, sticky="nw")
            self.e1 = Entry(self, textvariable=self.controller.shared_data["cdna_volume"], width=10)
            self.e1.grid(row=int(self.controller.shared_data["row_number"].get()) + 3, column=3, sticky="nw")

            self.l2 = Label(self, text="uL of Primer/Master Mix per well:")
            self.l2.grid(row=int(self.controller.shared_data["row_number"].get()) + 4, column=2, sticky="nw")
            self.e2 = Entry(self, textvariable=self.controller.shared_data["primer_volume"], width=10)
            self.e2.grid(row=int(self.controller.shared_data["row_number"].get()) + 4, column=3, sticky="nw")

            self.l3 = Label(self, text="Plate Barcode (Optional): ")
            self.l3.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=2, sticky="nw")
            self.e3 = Entry(self, textvariable=self.controller.shared_data["barcode"], width=10)
            self.e3.grid(row=int(self.controller.shared_data["row_number"].get()) + 5, column=3, sticky="nw")

            self.l4 = Label(self, text="Occupied wells:")
            self.l4.grid(row=int(self.controller.shared_data["row_number"].get()) + 6, column=2, sticky="ne")
            self.occupied_wells_label = Label(self, textvariable=self.controller.shared_data["occupied_wells"],
                                              style="well.TLabel")
            self.occupied_wells_label.grid(row=int(self.controller.shared_data["row_number"].get()) + 6, column=3,
                                           sticky="nw")
            self.controller.shared_data["replicates"].trace_variable('w', self.plate_capacity)

    def plate_capacity(self, event, index, mode):
        style = ttk.Style()
        try:
            if int(self.controller.shared_data["primer_number"].get()) > 0 and (int(
                    self.controller.shared_data["cdna_number"].get()) > 0 or (int(
                self.controller.shared_data["logarithm_number"].get()) > 0)):
                try:
                    self.controller.shared_data["occupied_wells"].set(str((int(
                        self.controller.shared_data["primer_number"].get()) * (int(self.controller.shared_data[
                                                                                       "logarithm_number"].get()) + int(
                        self.controller.shared_data["cdna_number"].get())) * int(
                        self.controller.shared_data["replicates"].get()))))
                except ValueError:
                    self.controller.shared_data["occupied_wells"].set(str((int(
                        self.controller.shared_data["primer_number"].get()) * int(
                        self.controller.shared_data["cdna_number"].get()) * int(
                        self.controller.shared_data["replicates"].get()))))
        except ValueError:
            pass
        try:
            if int(self.controller.shared_data["occupied_wells"].get()) > 96:
                style.configure("well.TLabel", foreground='red')
            if int(self.controller.shared_data["occupied_wells"].get()) < 97:
                style.configure("well.TLabel", foreground='black')
        except ValueError:
            pass

    def primerFill(self, *args):
        global primer_locations
        try:
            if not self.controller.shared_data["primer_number"].get() == '':
                for i in range(1, 36, 2):
                    self.plate.itemconfig(i, fill="white")
                    primer_locations = []
                pnumber = int(self.controller.shared_data["primer_number"].get())
                colorindex = 0
                if pnumber > 0:
                    for i in range(1, 2 * (pnumber) + 1, 2):
                        colorindex += 1
                        self.plate.itemconfig(i, fill=colors[colorindex])
                        primer_locations.append(self.plate.gettags(i)[0])
                        print(self.plate.gettags(i)[0])
        except (ValueError, IndexError) as error:
            pass
        self.controller.shared_data["primer_number"].trace_variable('w', self.plate_capacity)

    def standardcurveFill(self, *args):
        global standard_curve_locations
        cv = (0, 50, 0)
        try:
            if int(self.controller.shared_data["standardcurve"].get()) == 1:
                if not self.controller.shared_data["logarithm_number"].get() == '':
                    for i in range(37, 165, 2):
                        self.plate.itemconfig(i, fill="white")
                        standard_curve_locations = []
                    lnumber = int(self.controller.shared_data["logarithm_number"].get())
                    if lnumber > 0:
                        for i in range(37, 37 + (2 * (lnumber)), 2):
                            ongoing = True
                            print(cv)
                            if cv[0] == 200:
                                ongoing = False
                            if ongoing == True:
                                if cv[1] < 250:
                                    cv = (cv[0], cv[1] + 25, cv[2])
                                if cv[1] == 250:
                                    cv = (cv[0] + 50, cv[1], cv[2] + 50)
                            self.plate.itemconfig(i, fill="#%02x%02x%02x" % cv)
                            standard_curve_locations.append(self.plate.gettags(i)[0])
                            print(self.plate.gettags(i)[0])
        except (ValueError, IndexError) as error:
            pass
        self.controller.shared_data["logarithm_number"].trace_variable('w', self.plate_capacity)

    def cdnaFill(self, *args):
        global cdna_locations
        snumber = 0
        try:
            if int(self.controller.shared_data["standardcurve"].get()) == 1:

                if not self.controller.shared_data["logarithm_number"].get() == '':
                    snumber = int(self.controller.shared_data["logarithm_number"].get())

                if not self.controller.shared_data["cdna_number"].get() == '':
                    cnumber = int(self.controller.shared_data["cdna_number"].get())
                    if cnumber > 0:
                        for i in range(37 + snumber * 2, 165, 2):
                            self.plate.itemconfig(i, fill="white")
                            cdna_locations = []
                        for i in range(37 + snumber * 2, 37 + snumber * 2 + (2 * (cnumber)), 2):
                            self.plate.itemconfig(i, fill="blue")
                            cdna_locations.append(self.plate.gettags(i)[0])
                            print(self.plate.gettags(i)[0])

            if int(self.controller.shared_data["standardcurve"].get()) == 0:
                if not self.controller.shared_data["cdna_number"].get() == '':
                    for i in range(37, 165, 2):
                        self.plate.itemconfig(i, fill="white")
                        cdna_locations = []
                    cnumber = int(self.controller.shared_data["cdna_number"].get())
                    if cnumber > 0:
                        for i in range(37, 37 + (2 * (cnumber)), 2):
                            self.plate.itemconfig(i, fill="blue")
                            cdna_locations.append(self.plate.gettags(i)[0])
                            print(self.plate.gettags(i)[0])
        except (ValueError, IndexError) as error:
            pass
        self.controller.shared_data["cdna_number"].trace_variable('w', self.plate_capacity)


class MotionControl(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        s = ttk.Style()
        self.bg = s.lookup('TFrame', 'background')
        self.sercheck = Canvas(self, width=150, height=20, background=self.bg)
        self.sercheck.create_text(60, 12.5, text="Serial Connection", font=SMALL_FONT)
        self.sercheck.create_oval(120, 5, 135, 20, tags="sercheck", width=3, fill="red")
        self.sercheck.grid(row=1, column=11, pady=(60, 0))
        # self.controller.serial_status()
        self.grid_columnconfigure(9, minsize=50)
        self.grid_columnconfigure(2, minsize=60)
        self.grid_columnconfigure(0, minsize=30)
        self.grid_columnconfigure(11, minsize=250)
        Label(self, text="Motion Controller", font=NORM_FONT).grid(row=1, column=1, padx=20, pady=20, sticky="nw")
        self.otto_label = Label(self, text="OTTO", font=LARGE_FONT)
        self.otto_label.grid(row=1, column=11, padx=20, sticky="nw")
        self.otto_label.bind('<Button-1>', self.controller.colorPick)
        print(self.controller.shared_data["led_color"].get())

        self.workarea = Canvas(self, bg='white', width=710, height=680)

        # Rectangle surrounding primers and cDNAs
        self.workarea.create_rectangle(400, 5, 700, 410, width=5)
        # Rectangle indicating 96 well plate
        self.workarea.create_rectangle(400, 430, 700, 600, width=5)
        # Top 2 Pipette Tip Boxes
        self.workarea.create_rectangle(10, 210, 370, 420, width=5)
        # Bottom 2 Pipette Tip Boxes
        self.workarea.create_rectangle(10, 420, 370, 630, width=5)
        # Tip Remover box
        self.workarea.create_rectangle(10, 650, 40, 680, width=5)
        # Mastermix Box
        # self.workarea.create_rectangle(280, 140, 340, 190, width=5)
        # Water Box
        # self.workarea.create_rectangle(280, 5, 340, 120, width=5)
        # Laser Module box
        self.workarea.create_rectangle(180, 150, 220, 180, width=5)
        # Pallet Box
        self.workarea.create_rectangle(630, 650, 700, 680, width=5)

        # Tip Hover height Indicators
        # Pipette Shape
        self.workarea.create_line(15, 35, 30, 110, width=3)
        self.workarea.create_line(50, 35, 35, 110, width=3)
        self.workarea.create_oval(16, 26, 50, 41, width=4)
        self.workarea.create_oval(30, 108, 36, 112, width=2)

        # Tip
        self.workarea.create_line(26, 132, 31, 161, width=1)
        self.workarea.create_line(39, 132, 34, 161, width=1)
        self.workarea.create_oval(26, 128, 39, 136, width=1)
        self.workarea.create_oval(31, 160, 34, 162, width=1)

        # Well Shape
        self.workarea.create_oval(16, 130, 50, 140, width=3)
        self.workarea.create_oval(16, 155, 50, 165, width=3)
        self.workarea.create_line(16, 133, 16, 159, width=3)
        self.workarea.create_line(50, 137, 50, 162, width=3)

        # Double Headed Arrow indicating height
        self.workarea.create_line(60, 93, 60, 130, width=3, arrow=BOTH, fill="red", activefill="gray",
                                  tags="Tip_Box_Hover_Height")

        # Hover Height Indicators
        # Pipette Shape
        self.workarea.create_line(90, 15, 105, 90, width=3)
        self.workarea.create_line(125, 15, 110, 90, width=3)
        self.workarea.create_oval(91, 6, 125, 21, width=4)
        self.workarea.create_oval(105, 88, 111, 92, width=2)

        # Tip
        self.workarea.create_line(101, 86, 106, 115, width=1)
        self.workarea.create_line(114, 86, 109, 115, width=1)
        self.workarea.create_oval(101, 82, 114, 90, width=1)
        self.workarea.create_oval(106, 114, 109, 116, width=1)

        # Well Shape
        self.workarea.create_oval(91, 130, 125, 140, width=3)
        self.workarea.create_oval(91, 155, 125, 165, width=3)
        self.workarea.create_line(91, 133, 91, 159, width=3)
        self.workarea.create_line(125, 137, 125, 162, width=3)

        # Double Headed Arrow indicating height
        self.workarea.create_line(135, 93, 135, 130, width=3, arrow=BOTH, fill="red", activefill="gray",
                                  tags="Hover_Height")

        for controlY in range(0, 9):
            for controlX in range(0, 2):
                self.workarea.create_oval(583.33333 + 58.3333 * controlX, 23 + 43 * controlY,
                                          608.3333 + 58.3333 * controlX, 48 + 43 * controlY, width=2)
        for controlZ in range(0, 2):
            for controlX in range(0, 4):
                for controlY in range(0, 8):
                    self.workarea.create_oval(426 + controlX * 30, 50 + (controlY * 17.5) + 186 * controlZ,
                                              436 + controlX * 30,
                                              60 + (controlY * 17.5) + 186 * controlZ, fill="white", width=2)
        for controlY in range(0, 8):
            for controlX in range(0, 12):
                self.workarea.create_oval(418.0769 + 23.0769 * controlX, 443.8889 + 18.889 * controlY,
                                          428.0769 + 23.0769 * controlX, 453.889 + 18.889 * controlY, width=2)
        for controlZ in range(0, 2):
            for controlY in range(0, 12):
                for controlX in range(0, 8):
                    self.workarea.create_oval(25 + 20 * controlX + 185 * controlZ, 215 + 17.25 * controlY,
                                              35 + 20 * controlX + 185 * controlZ, 224. + 17.25 * controlY,
                                              width=2)
        for controlZ in range(0, 2):
            for controlY in range(0, 12):
                for controlX in range(0, 8):
                    self.workarea.create_oval(25 + 20 * controlX + 185 * controlZ, 425 + 17.25 * controlY,
                                              35 + 20 * controlX + 185 * controlZ, 434. + 17.25 * controlY,
                                              width=2)
        self.workarea.create_text(355, 219.5, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Upper_Right_Tip_Box")
        self.workarea.create_line(355, 243, 355, 283, fill="red", activefill="gray",
                                  tags="Tip_Spacing", width=3, arrow=BOTH, arrowshape=(10.6, 13.3, 4))
        self.workarea.create_text(170, 219.5, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Upper_Left_Tip_Box")
        self.workarea.create_text(355, 429.5, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Bottom_Right_Tip_Box")
        self.workarea.create_text(170, 429.5, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Bottom_Left_Tip_Box")
        self.workarea.create_text(423, 448, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="96_Well")
        self.workarea.create_line(457, 449, 503, 449, fill="red", activefill="gray",
                                  tags="Well_Spacing", width=3, arrow=BOTH, arrowshape=(10.6, 13.3, 4))
        self.workarea.create_text(596, 379, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Primer")
        self.workarea.create_text(521, 363, text="X", font=("Purisa", 22), fill="red", activefill="gray", tags="cDNA")
        self.workarea.create_text(650, 665, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Mastermix")
        self.workarea.create_text(200, 165, text="X", font=("Purisa", 22), fill="red", activefill="gray",
                                  tags="Laser_Module")
        self.workarea.create_text(680, 665, text="X", font=("Purisa", 22), fill="red", activefill="gray", tags="Water")
        self.workarea.create_text(25, 665, text="X", font=("Purisa", 22), fill="red", activefill="gray", tags="Remover")
        # self.workarea.create_text(685, 665, text="X", font=("Purisa", 22), fill="red", activefill="gray", tags="pallet")

        self.workarea.grid(row=1, column=5, rowspan=2, pady=(30, 0))

        self.motionFrame = Frame(self)
        Label(self.motionFrame, text="Cursor Position: ", font=SMALL_FONT).pack(side=LEFT)
        Label(self.motionFrame, textvariable=controller.shared_data["cursor_position"], font=SMALL_FONT).pack(side=LEFT)
        self.motionFrame.grid(row=3, column=5)

        style = ttk.Style()
        style.configure("bright.TButton", font=("Helvetica", 13), foreground="black")

        Button(self, text="Return to Start", command=lambda: self.controller.show_frame(Config1),
               style="bright.TButton").grid(row=4, column=5)

        self.APositionFrame = Frame(self)
        Label(self.APositionFrame, text="Current Absolute Position:", font="Helvetica 12").pack(side=LEFT)
        Label(self.APositionFrame, textvariable=self.controller.shared_data["legible_current_position"],
              font="Helvetica 12").pack(side=LEFT)
        self.APositionFrame.grid(column=1, row=1, columnspan=6, pady=(100,0), padx=(25,0), sticky="w")

        self.manualmoveFrame = Frame(self)
        self.manualmoveFrame.grid(column=1, row=2, rowspan=1)
        Label(self.manualmoveFrame, text="XY Motion:", font=SMALL_FONT).grid(column=2, row=5)
        Button(self.manualmoveFrame, text="-- X ", command=lambda: self.controller.motioncontroller("x-")).grid(
            column=1, row=7)
        Button(self.manualmoveFrame, text="++ X", command=lambda: self.controller.motioncontroller("x+")).grid(column=3,
                                                                                                               row=7)
        Button(self.manualmoveFrame, text="++ Y", command=lambda: self.controller.motioncontroller("y+")).grid(column=2,
                                                                                                               row=6)
        Button(self.manualmoveFrame, text="-- Y ", command=lambda: self.controller.motioncontroller("y-")).grid(
            column=2, row=8)
        Label(self.manualmoveFrame, text="Z Motion:", font=SMALL_FONT).grid(column=5, row=5)
        Button(self.manualmoveFrame, text="++ Z", command=lambda: self.controller.motioncontroller("z+")).grid(column=5,
                                                                                                               row=6)
        Button(self.manualmoveFrame, text="-- Z ", command=lambda: self.controller.motioncontroller("z-")).grid(
            column=5, row=8)
        Button(self.manualmoveFrame, text="Home Axes", command=self.controller.home).grid(column=3, row=10,
                                                                                          columnspan=3)
        Label(self.manualmoveFrame, text="Pipette:", font=SMALL_FONT).grid(column=7, row=5)
        Button(self.manualmoveFrame, text="++ P", command=lambda: self.controller.motioncontroller("p+")).grid(column=7,
                                                                                                               row=6)
        Button(self.manualmoveFrame, text="-- P ", command=lambda: self.controller.motioncontroller("p-")).grid(
            column=7, row=8)
        self.manualmoveFrame3 = Frame(self.manualmoveFrame)
        Label(self.manualmoveFrame3, text="Millimeter per Click:", font=SMALL_FONT).grid(column=0, row=0, sticky="e")
        Entry(self.manualmoveFrame3, textvariable=self.controller.shared_data["step_size"]).grid(column=1, row=0)
        self.manualmoveFrame5 = Frame(self.manualmoveFrame3)
        Button(self.manualmoveFrame5, text="0.1", command=lambda: self.save_step_size(0.1)).pack(side=LEFT)
        Button(self.manualmoveFrame5, text="1", command=lambda: self.save_step_size(1)).pack(side=LEFT)
        Button(self.manualmoveFrame5, text="5", command=lambda: self.save_step_size(5)).pack(side=LEFT)
        Button(self.manualmoveFrame5, text="10", command=lambda: self.save_step_size(10)).pack(side=LEFT)
        self.manualmoveFrame5.grid(column=1, row=2)
        Label(self.manualmoveFrame3, text="Absolute Coordinate:", font=SMALL_FONT).grid(column=0, row=3, pady=(30, 10),
                                                                               sticky="e")

        self.absolute_coordinate_entry = Entry(self.manualmoveFrame3,
                                               textvariable=self.controller.shared_data["absolute_coordinate"])
        self.absolute_coordinate_entry.grid(column=1, row=3, pady=(30, 10))
        self.absolute_coordinate_entry.bind('<Return>', lambda event: self.controller.absolutepositioning)

        Button(self.manualmoveFrame3, text="Go!", command=self.controller.absolutepositioning).grid(column=1, row=4)
        self.manualmoveFrame3.grid(column=1, row=12, columnspan=6, sticky="w")
        self.manualmoveFrame4 = Frame(self.manualmoveFrame)
        self.commandList = Listbox(self.manualmoveFrame4, height=10)
        Label(self.manualmoveFrame4, text="Communication Log:", font=SMALL_FONT_BOLD).grid(column=0, row=0,
                                                                                           columnspan=2,
                                                                                           sticky="e")
        self.commandList.grid(column=0, row=1, sticky=(N, E, S))
        s = ttk.Scrollbar(self.manualmoveFrame4, orient=VERTICAL, command=self.commandList.yview)
        s.grid(column=1, row=1, sticky=(N, S))
        self.commandList['yscrollcommand'] = s.set
        self.manualmoveFrame4.grid(column=6, row=12, columnspan=7, padx=(60, 0))
        #
        # self.manualmoveFrame6 = Frame(self.manualmoveFrame)
        # Label(self.manualmoveFrame6, text="Global Offset:     ", font=SMALL_FONT).pack(side=LEFT)
        # Label(self.manualmoveFrame6, text="X:", font=SMALL_FONT).pack(side=LEFT)
        # Entry(self.manualmoveFrame6, width=8, textvariable=self.controller.shared_data["global_x"]).pack(
        #     side=LEFT)
        # Label(self.manualmoveFrame6, text="Y:", font=SMALL_FONT).pack(side=LEFT)
        # Entry(self.manualmoveFrame6, width=8, textvariable=self.controller.shared_data["global_y"]).pack(
        #     side=LEFT)
        # Label(self.manualmoveFrame6, text="Z:", font=SMALL_FONT).pack(side=LEFT)
        # Entry(self.manualmoveFrame6, width=8, textvariable=self.controller.shared_data["global_z"]).pack(
        #     side=LEFT)
        # Button(self.manualmoveFrame6, text="Offset", command=self.controller.global_offset).pack(side=LEFT)
        # self.manualmoveFrame6.grid(column=0, row=18, columnspan=7, sticky="w")
        #
        # self.manualmoveFrame8 = Frame(self.manualmoveFrame)
        # Label(self.manualmoveFrame8, text="Step Change:     ", font=SMALL_FONT).pack(side=LEFT)
        # Label(self.manualmoveFrame8, text="X:", font=SMALL_FONT).pack(side=LEFT)
        # Entry(self.manualmoveFrame8, width=8, textvariable=self.controller.shared_data["step_change_x"]).pack(side=LEFT)
        # Label(self.manualmoveFrame8, text="Y:", font=SMALL_FONT).pack(side=LEFT)
        # Entry(self.manualmoveFrame8, width=8, textvariable=self.controller.shared_data["step_change_y"]).pack(side=LEFT)
        # Label(self.manualmoveFrame8, text="Z:", font=SMALL_FONT).pack(side=LEFT)
        # Entry(self.manualmoveFrame8, width=8, textvariable=self.controller.shared_data["step_change_z"]).pack(side=LEFT)
        # Button(self.manualmoveFrame8, text="Multiply", command=self.controller.step_change).pack(side=LEFT)
        # self.manualmoveFrame8.grid(column=0, row=19, columnspan=7, sticky="w")

        self.manualmoveFrame7 = Frame(self)

        Label(self.manualmoveFrame7, text="Pipette Calibration", font=SMALL_FONT_BOLD).grid(row=0, column=0, padx=10,
                                                                                            pady=20, columnspan=2)

        self.pipettevar = StringVar()
        style.configure("big.TMenubutton", font=("Helvetica", 10))
        dropdown = OptionMenu(self.manualmoveFrame7, self.pipettevar, 'P10', 'P10', 'P20', 'P200', 'P1000',
                              style="big.TMenubutton")
        print(self.controller.shared_data["pipettevar"].get())
        if self.controller.shared_data["pipettevar"].get() == " ":
            self.pipettevar.set("Select Pipette Size")
        else:
            self.pipettevar.set(self.controller.shared_data["pipettevar"].get())
            tempvar = self.controller.shared_data["pipettevar"].get()
            self.controller.pcal["pcalstep1"].set(self.controller.pick[tempvar]["pcalstep1_pick"])
            self.controller.pcal["pcalvol1"].set(self.controller.pick[tempvar]["pcalvol1_pick"])
            self.controller.pcal["pcalstep2"].set(self.controller.pick[tempvar]["pcalstep2_pick"])
            self.controller.pcal["pcalvol2"].set(self.controller.pick[tempvar]["pcalvol2_pick"])
            self.controller.pcal["pcalstep3"].set(self.controller.pick[tempvar]["pcalstep3_pick"])
            self.controller.pcal["pcalvol3"].set(self.controller.pick[tempvar]["pcalvol3_pick"])
            self.controller.pcal["pcalstep4"].set(self.controller.pick[tempvar]["pcalstep4_pick"])
            self.controller.pcal["pcalvol4"].set(self.controller.pick[tempvar]["pcalvol4_pick"])
            self.controller.pcal["pcalstep5"].set(self.controller.pick[tempvar]["pcalstep5_pick"])
            self.controller.pcal["pcalvol5"].set(self.controller.pick[tempvar]["pcalvol5_pick"])
            self.controller.pcal["linear_coefficient"].set(self.controller.pick[tempvar]["linear_coefficient_pick"])
            self.controller.pcal["linear_intercept"].set(self.controller.pick[tempvar]["linear_intercept_pick"])
        self.pipettevar.trace("w", self.pipette_change)
        dropdown.grid(row=1, column=0, columnspan=2, padx=20, sticky='nw')
        self.tempvar = self.pipettevar.get()

        Label(self.manualmoveFrame7, text="Distance (mm)", font=SMALL_FONT).grid(row=2, column=0, padx=20,
                                                                          pady=5, sticky="nw")
        Label(self.manualmoveFrame7, text="Volume (uL):", font=SMALL_FONT).grid(row=2, column=1, padx=20,
                                                                                pady=5, sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalstep1"]).grid(row=3, column=0,
                                                                                                   padx=20,
                                                                                                   pady=1,
                                                                                                   sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalvol1"]).grid(row=3, column=1,
                                                                                                  padx=20,
                                                                                                  pady=1,
                                                                                                  sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalstep2"]).grid(row=4,
                                                                                                   column=0,
                                                                                                   padx=20,
                                                                                                   pady=1,
                                                                                                   sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalvol2"]).grid(row=4,
                                                                                                  column=1,
                                                                                                  padx=20,
                                                                                                  pady=1,
                                                                                                  sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalstep3"]).grid(row=5,
                                                                                                   column=0,
                                                                                                   padx=20,
                                                                                                   pady=1,
                                                                                                   sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalvol3"]).grid(row=5,
                                                                                                  column=1,
                                                                                                  padx=20,
                                                                                                  pady=1,
                                                                                                  sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalstep4"]).grid(row=6,
                                                                                                   column=0,
                                                                                                   padx=20,
                                                                                                   pady=1,
                                                                                                   sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalvol4"]).grid(row=6,
                                                                                                  column=1,
                                                                                                  padx=20,
                                                                                                  pady=1,
                                                                                                  sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalstep5"]).grid(row=7,
                                                                                                   column=0,
                                                                                                   padx=20,
                                                                                                   pady=1,
                                                                                                   sticky="nw")
        Entry(self.manualmoveFrame7, width=8, textvariable=self.controller.pcal["pcalvol5"]).grid(row=7,
                                                                                                  column=1,
                                                                                                  padx=20,
                                                                                                  pady=1,
                                                                                                  sticky="nw")
        Button(self.manualmoveFrame7, text="Calibrate", command=self.Best_Fit).grid(row=8,
                                                                                    column=0,
                                                                                    padx=20,
                                                                                    pady=5,
                                                                                    sticky="nesw",
                                                                                    rowspan=2)

        self.manualmoveFrame7.grid(row=2, column=11, pady=20, sticky="nw")

        self.manualmoveFrame.grid_columnconfigure(4, minsize=30)
        self.manualmoveFrame.grid_columnconfigure(6, minsize=30)
        self.manualmoveFrame.grid_rowconfigure(4, minsize=30)
        self.manualmoveFrame.grid_rowconfigure(9, minsize=30)
        self.manualmoveFrame.grid_rowconfigure(11, minsize=30)
        self.manualmoveFrame.grid_rowconfigure(15, minsize=30)
        self.manualmoveFrame.grid_rowconfigure(17, minsize=30)
        self.manualmoveFrame.grid(row=2, column=1)

        self.workarea.tag_bind("Upper_Right_Tip_Box", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Upper_Right_Tip_Box", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Upper_Right_Tip_Box", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Upper_Left_Tip_Box", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Upper_Left_Tip_Box", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Upper_Left_Tip_Box", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Bottom_Right_Tip_Box", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Bottom_Right_Tip_Box", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Bottom_Right_Tip_Box", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Bottom_Left_Tip_Box", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Bottom_Left_Tip_Box", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Bottom_Left_Tip_Box", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Tip_Spacing", '<Enter>', self.on_entertspace)
        self.workarea.tag_bind("Tip_Spacing", '<Leave>', self.on_leavetspace)
        self.workarea.tag_bind("Tip_Spacing", '<ButtonPress-1>', self.change_tip_spacing)

        self.workarea.tag_bind("96_Well", '<Enter>', self.on_enter)
        self.workarea.tag_bind("96_Well", '<Leave>', self.on_leave)
        self.workarea.tag_bind("96_Well", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Well_Spacing", '<Enter>', self.on_enterwspace)
        self.workarea.tag_bind("Well_Spacing", '<Leave>', self.on_leavewspace)
        self.workarea.tag_bind("Well_Spacing", '<ButtonPress-1>', self.change_well_spacing)

        self.workarea.tag_bind("Primer", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Primer", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Primer", '<ButtonPress-1>', self.change_coord)


        self.workarea.tag_bind("cDNA", '<Enter>', self.on_enter)
        self.workarea.tag_bind("cDNA", '<Leave>', self.on_leave)
        self.workarea.tag_bind("cDNA", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Water", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Water", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Water", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Mastermix", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Mastermix", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Mastermix", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Laser_Module", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Laser_Module", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Laser_Module", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Remover", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Remover", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Remover", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Hover_Height", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Hover_Height", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Hover_Height", '<ButtonPress-1>', self.change_coord)

        self.workarea.tag_bind("Tip_Box_Hover_Height", '<Enter>', self.on_enter)
        self.workarea.tag_bind("Tip_Box_Hover_Height", '<Leave>', self.on_leave)
        self.workarea.tag_bind("Tip_Box_Hover_Height", '<ButtonPress-1>', self.change_coord)

        self.occurred = False
        self.bind('<Enter>', self.reminder_window)

    def pipette_change(self, *args):
        tempvar = self.pipettevar.get()
        self.controller.shared_data["pipettevar"].set(tempvar)

        self.controller.pcal["pcalstep1"].set(self.controller.pick[tempvar]["pcalstep1_pick"])
        self.controller.pcal["pcalvol1"].set(self.controller.pick[tempvar]["pcalvol1_pick"])
        self.controller.pcal["pcalstep2"].set(self.controller.pick[tempvar]["pcalstep2_pick"])
        self.controller.pcal["pcalvol2"].set(self.controller.pick[tempvar]["pcalvol2_pick"])
        self.controller.pcal["pcalstep3"].set(self.controller.pick[tempvar]["pcalstep3_pick"])
        self.controller.pcal["pcalvol3"].set(self.controller.pick[tempvar]["pcalvol3_pick"])
        self.controller.pcal["pcalstep4"].set(self.controller.pick[tempvar]["pcalstep4_pick"])
        self.controller.pcal["pcalvol4"].set(self.controller.pick[tempvar]["pcalvol4_pick"])
        self.controller.pcal["pcalstep5"].set(self.controller.pick[tempvar]["pcalstep5_pick"])
        self.controller.pcal["pcalvol5"].set(self.controller.pick[tempvar]["pcalvol5_pick"])
        self.controller.pcal["linear_coefficient"].set(self.controller.pick[tempvar]["linear_coefficient_pick"])
        self.controller.pcal["linear_intercept"].set(self.controller.pick[tempvar]["linear_intercept_pick"])

    def reminder_window(self, event):
        if self.occurred is False:
            self.win = Toplevel()
            self.win.geometry("%dx%d+%d+%d" % (400, 500, 650, 100))
            self.win.wm_title("Reminder!")
            self.win.attributes('-topmost', 'true')
            self.win.configure(background=self.bg)
            self.win.grid_columnconfigure(0, weight=1)
            self.win.grid_columnconfigure(2, weight=1)
            textframe = Canvas(self.win, background=self.bg, width=400, height=400)
            Label(self.win, font=("Helvetica", 20), text="Reminders:").grid(row=1, column=1, padx=20, pady=10)
            textframe.create_text(200, 20,
                                  text="1. Please ensure valid coordinates are entered for every location marked with a red X"
                                       "\n\n2. The Z coordinate is defined as right above the tip boxes and as in the well for "
                                       "every other location \n\n3. For the laser module located at the top, please manually "
                                       "position the pipette with a straight tip on so the tip touches the laser. Then back off 5 mm in "
                                       "the X direction and set that location as the X coordinate for the laser module. "
                                       "Please repeat for the Y and Z directions\n\n4. Please remember to calibrate the pipette\n\n5. If OTTO is ever moved or "
                                       "accidentally hit, we recommend rechecking all coordinates to minimize possible errors",
                                  font="Helvetica 12", width=350, anchor="n")
            textframe.configure(state="disabled")
            textframe.grid(row=2, column=1)
            Button(self.win, text="Got it and home!", command=lambda: [self.win.destroy(), self.controller.home()])\
                .grid(row=3, column=1)
            self.occurred = True

    def on_enter(self, event):
        item = self.workarea.find_closest(event.x, event.y)[0]
        tag = self.workarea.itemcget(item, "tags")
        tag = tag[:-8]
        string_cord = tag + "_coord"
        if string_cord == "_coord":
            string_cord = "error_message"
        else:
            cursortext = self.controller.shared_data[string_cord].get()
            self.controller.shared_data["cursor_position"].set(cursortext)

    def on_leave(self, enter):
        self.controller.shared_data["cursor_position"].set("")

    def on_leavetspace(self, enter):
        self.controller.shared_data["cursor_position"].set("")

    def on_entertspace(self, event):
        cursortext = self.controller.shared_data["Tip_Spacing"].get()
        self.controller.shared_data["cursor_position"].set(cursortext)

    def change_tip_spacing(self, event):
        item = self.workarea.find_closest(event.x, event.y)[0]
        tag = self.workarea.itemcget(item, "tags")
        tag = tag[:-8]
        string_cat = "Set position of " + tag
        string_cat = string_cat.replace("_", " ")
        self.win = Toplevel()
        self.win.geometry("%dx%d+%d+%d" % (300, 300, 700, 400))
        self.win.wm_title(string_cat)
        self.win.configure(background=self.bg)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(4, weight=1)
        self.win.grid_columnconfigure(5, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_rowconfigure(6, weight=1)
        Label(self.win, text="Tip Spacing:").grid(row=2, column=2, padx=20, pady=10)
        Label(self.win, text="Tip Spacing is between the center points of\ntip box holes.").grid(row=3, column=2, padx=20, pady=(0,10))
        self.win.tspaceentry = Entry(self.win, textvariable=self.controller.shared_data["Tip_Spacing"])
        self.win.tspaceentry.grid(row=4, column=2, pady=10)
        Button(self.win, text="Save Spacing", command=lambda: self.trigger_spacing(tag)).grid(row=5,
                                                                                           column=2,
                                                                                           pady=10,
                                                                                           padx=(0, 0))
        print(self.win.tspaceentry)

    def on_leavewspace(self, enter):
        self.controller.shared_data["cursor_position"].set("")

    def on_enterwspace(self, event):
        cursortext = self.controller.shared_data["Well_Spacing"].get()
        self.controller.shared_data["cursor_position"].set(cursortext)

    def change_well_spacing(self, event):
        item = self.workarea.find_closest(event.x, event.y)[0]
        tag = self.workarea.itemcget(item, "tags")
        tag = tag[:-8]
        string_cat = "Set position of " + tag
        string_cat = string_cat.replace("_", " ")
        self.win = Toplevel()
        self.win.geometry("%dx%d+%d+%d" % (300, 300, 700, 400))
        self.win.wm_title(string_cat)
        self.win.configure(background=self.bg)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(4, weight=1)
        self.win.grid_columnconfigure(5, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_rowconfigure(6, weight=1)
        Label(self.win, text="Well Spacing:").grid(row=2, column=2, padx=20, pady=10)
        Label(self.win, text="Well Spacing is between the center points of\ntwo wells. Typically this is 9mm.").grid(row=3, column=2, padx=20,
                                                                                           pady=(0,10))
        self.win.wspaceentry = Entry(self.win, textvariable=self.controller.shared_data["Well_Spacing"])
        self.win.wspaceentry.grid(row=4, column=2, pady=10)
        Button(self.win, text="Save Spacing", command=lambda: self.trigger_spacing(tag)).grid(row=5,
                                                                                           column=2,
                                                                                           pady=10,
                                                                                           padx=(0, 0))
        print(self.win.wspaceentry)

    def change_coord(self, event):
        item = self.workarea.find_closest(event.x, event.y)[0]
        tag = self.workarea.itemcget(item, "tags")
        tag = tag[:-8]
        string_cat = "Set position of " + tag
        string_cat = string_cat.replace("_", " ")
        name = tag
        name = name.replace("_", " ")
        self.win = Toplevel()
        self.win.geometry("%dx%d+%d+%d" % (300, 325, 700, 200))
        self.win.wm_title(string_cat)
        self.win.configure(background=self.bg)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(4, weight=1)
        self.win.grid_columnconfigure(5, weight=1)
        self.win.grid_rowconfigure(8, weight=1)

        Label(self.win, text="{} Coordinate".format(name), font="Helvetica 12").grid(row=1, column=2, sticky="NESW",  pady=(10,20))
        if tag == "96_Well" or tag == "cDNA" or tag == "Primer":
            extra_text = Label(self.win, text="Please ensure tip is at the bottom of\nwell when measuring Z",
                               font="Helvetica 8").grid(row=1, column=2, columnspan=2, pady=(50, 5), sticky="NESW")
        if tag == "Hover_Height":
            extra_text = Label(self.win, text="The lowest Z the pipettor, WITH a tip,\ncan "
                                              "move around at without hitting any object",
                               font="Helvetica 8").grid(row=1, column=2, columnspan=2, pady=(50, 5), sticky="NESW")
        if tag == "Tip_Box_Hover_Height":
            extra_text = Label(self.win, text="The lowest Z the pipettor, WITHOUT a tip,\ncan "
                                              "move around at without hitting any object",
                               font="Helvetica 8").grid(row=1, column=2, columnspan=2, pady=(50, 5), sticky="NESW")
        if tag == "Remover":
            extra_text = Label(self.win, text="The fastest way to remove a tip is if the\n Remover is postioned at the"
                                              " hover height.",
                               font="Helvetica 8").grid(row=1, column=2, columnspan=2, pady=(50, 5), sticky="NESW")

        Button(self.win, text="Load Current Position", command=self.trigger_current_position).grid(row=2,
                                                                                                   column=2,
                                                                                                   pady=10, )
        Label(self.win, text="X:").grid(row=3, column=1, padx=20, pady=10)
        Label(self.win, text="Y:").grid(row=4, column=1, padx=20, pady=10)
        Label(self.win, text="Z:").grid(row=5, column=1, padx=20, pady=10)
        self.win.xcoordentry = Entry(self.win, textvariable=self.controller.shared_data["x_change"])
        self.win.xcoordentry.grid(row=3, column=2, pady=10)
        self.win.ycoordentry = Entry(self.win, textvariable=self.controller.shared_data["y_change"])
        self.win.ycoordentry.grid(row=4, column=2, pady=10)
        self.win.zcoordentry = Entry(self.win, textvariable=self.controller.shared_data["z_change"])
        self.win.zcoordentry.grid(row=5, column=2, pady=10)
        Button(self.win, text="Save Position", command=lambda: self.trigger_change_coord(tag)).grid(row=6, column=2)

        string_cord = tag + "_coord"
        xyz_coord_entry = self.controller.shared_data[string_cord].get()
        xyz_coord_entry = xyz_coord_entry.split()

        this_position = self.controller.shared_data[string_cord].get()
        Button(self.win, text="Move to this Position", command=lambda: self.move_to_this_position(this_position)).grid(
            row=7,
            column=2,
            pady=(0, 5))
        print(xyz_coord_entry)

        self.win.xcoordentry.delete(0, 'end')
        self.win.ycoordentry.delete(0, 'end')
        self.win.zcoordentry.delete(0, 'end')

        try:
            xcoordinate = xyz_coord_entry[0]
        except IndexError:
            xcoordinate = 0

        try:
            ycoordinate = xyz_coord_entry[1]
        except IndexError:
            ycoordinate = 0

        try:
            zcoordinate = xyz_coord_entry[2]
        except IndexError:
            zcoordinate = 0
        self.win.xcoordentry.insert(0, xcoordinate)
        self.win.ycoordentry.insert(0, ycoordinate)
        self.win.zcoordentry.insert(0, zcoordinate)

    def move_to_this_position(self, this_position):
        hoverheight = list(self.controller.shared_data["Hover_Height_coord"].get().split())
        hoverheight = [float(b) for b in hoverheight]
        this_position = list(this_position.split())
        this_position = [float(b) for b in this_position]
        self.controller.shared_data["absolute_coordinate"].set(
            str(this_position[0]) + " " + str(this_position[1]) + " " + str(hoverheight[2]) + " 0")
        print(hoverheight[2])
        print(this_position[0])
        print(self.controller.shared_data["absolute_coordinate"])
        self.controller.absolutepositioning

    def trigger_current_position(self):

        xyzcoordinate = self.controller.shared_data["current_position"].get()
        print(xyzcoordinate)
        xyzcoordinate = xyzcoordinate.split()
        print(xyzcoordinate)

        self.win.xcoordentry.delete(0, 'end')
        self.win.ycoordentry.delete(0, 'end')
        self.win.zcoordentry.delete(0, 'end')
        self.win.xcoordentry.insert(0, xyzcoordinate[0])
        self.win.ycoordentry.insert(0, xyzcoordinate[1])
        self.win.zcoordentry.insert(0, xyzcoordinate[2])

    def trigger_spacing(self, tag):
        entry = self.controller.shared_data["{}".format(tag)].get()
        self.controller.shared_data["{}".format(tag)].set(entry)
        self.controller.pick["main_data"]["{}_pick".format(tag)] = (
            self.controller.shared_data["{}".format(tag)].get())
        with open('coordinates.pickle', 'wb') as handle:
            pickle.dump(self.controller.pick, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.commandList.insert(0, "{} Coordinate Saved".format(tag))
        self.win.destroy()

    def trigger_change_coord(self, tag):
        x_coord_entry = self.controller.shared_data["x_change"].get()
        y_coord_entry = self.controller.shared_data["y_change"].get()
        z_coord_entry = self.controller.shared_data["z_change"].get()
        if not x_coord_entry:
            print("List is empty")
        if not y_coord_entry:
            print("List is empty")
        if not z_coord_entry:
            print("List is empty")
        else:
            string_cord = tag + "_coord"
            print(string_cord)
            if string_cord == "_coord":
                string_cord = "error_message"
            else:
                print(string_cord)
                new_coord = x_coord_entry + " " + y_coord_entry + " " + z_coord_entry
                self.controller.shared_data[string_cord].set(new_coord)
                self.win.destroy()
        self.controller.pick["main_data"]["{}_pick".format(tag)] = (
            self.controller.shared_data["{}_coord".format(tag)].get())
        with open('coordinates.pickle', 'wb') as handle:
            pickle.dump(self.controller.pick, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.commandList.insert(0, "{} Coordinate Saved".format(tag))

    def save_step_size(self, value):
        self.controller.shared_data["step_size"].set(value)

    def Best_Fit(self):
        tempvar = self.pipettevar.get()
        lm = linear_model.LinearRegression()
        x_steps = [self.controller.pcal["pcalstep1"].get(), self.controller.pcal["pcalstep2"].get(),
                   self.controller.pcal["pcalstep3"].get(), self.controller.pcal["pcalstep4"].get(),
                   self.controller.pcal["pcalstep5"].get()]
        y_vol = [self.controller.pcal["pcalvol1"].get(), self.controller.pcal["pcalvol2"].get(),
                 self.controller.pcal["pcalvol3"].get(), self.controller.pcal["pcalvol4"].get(),
                 self.controller.pcal["pcalvol5"].get()]
        x_steps = np.array(x_steps).reshape((len(x_steps), 1))
        y_vol = np.array(y_vol)
        model = lm.fit(x_steps, y_vol)
        self.controller.pcal["linear_coefficient"].set(lm.coef_[0])
        self.controller.pcal["linear_intercept"].set(lm.intercept_)
        print(self.controller.pcal["linear_coefficient"].get())
        print(self.controller.pcal["linear_intercept"].get())
        self.commandList.insert(0, str(self.controller.pcal["linear_coefficient"].get()) + "x + " + str(
            self.controller.pcal["linear_intercept"].get()))
        self.controller.pick["main_data"]["pipettevar_pick"] = (self.controller.shared_data["pipettevar"].get())
        self.controller.pick[tempvar]["pcalstep1_pick"] = (self.controller.pcal["pcalstep1"].get())
        self.controller.pick[tempvar]["pcalvol1_pick"] = (self.controller.pcal["pcalvol1"].get())
        self.controller.pick[tempvar]["pcalstep2_pick"] = (self.controller.pcal["pcalstep2"].get())
        self.controller.pick[tempvar]["pcalvol2_pick"] = (self.controller.pcal["pcalvol2"].get())
        self.controller.pick[tempvar]["pcalstep3_pick"] = (self.controller.pcal["pcalstep3"].get())
        self.controller.pick[tempvar]["pcalvol3_pick"] = (self.controller.pcal["pcalvol3"].get())
        self.controller.pick[tempvar]["pcalstep4_pick"] = (self.controller.pcal["pcalstep4"].get())
        self.controller.pick[tempvar]["pcalvol4_pick"] = (self.controller.pcal["pcalvol4"].get())
        self.controller.pick[tempvar]["pcalstep5_pick"] = (self.controller.pcal["pcalstep5"].get())
        self.controller.pick[tempvar]["pcalvol5_pick"] = (self.controller.pcal["pcalvol5"].get())
        self.controller.pick[tempvar]["linear_coefficient_pick"] = (self.controller.pcal["linear_coefficient"].get())
        self.controller.pick[tempvar]["linear_intercept_pick"] = (self.controller.pcal["linear_intercept"].get())

        with open('coordinates.pickle', 'wb') as handle:
            pickle.dump(self.controller.pick, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self.commandList.insert(1, "Pipette Calibration Saved")


class GCode(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        s = ttk.Style()
        self.bg = s.lookup('TFrame', 'background')
        self.sercheck = Canvas(self, width=150, height=20, background=self.bg)
        self.sercheck.create_text(60, 12.5, text="Serial Connection", font=SMALL_FONT)
        self.sercheck.create_oval(120, 5, 135, 20, tags="sercheck", width=3, fill="red")
        self.sercheck.grid(row=1, column=11, pady=(100, 0))
        # self.controller.serial_status()
        self.otto_label = Label(self, text="OTTO", font=LARGE_FONT)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(6, weight=2)

        self.otto_label.grid(row=1, column=11, padx=20, pady=20, sticky="w")

        self.leftFrame = Frame(self)
        self.leftFrame.grid(row=2, column=1, sticky="n")
        self.leftFrame.grid_rowconfigure(5, weight=1)

        lastminute = Canvas(self.leftFrame, width=450, height=250, background="white")

        lastminute.create_text(225, 20, text="Final Checklist:", font="Helvetica 14")
        checkvar1 = IntVar()
        checkvar2 = IntVar()
        checkvar3 = IntVar()
        checkvar4 = IntVar()
        checkvar5 = IntVar()
        self.checklist = [
            [1, "Tip boxes are full.", checkvar1],
            [2, "Used tip bin is empty.", checkvar2],
            [3, "96 Well plate and reagent tubes are fully seated.", checkvar3],
            [4, "Reagent tubes are open", checkvar4],
            [5, "There are no obstructions above Otto.", checkvar5]
        ]
        self.vars = [row[2].get() for row in self.checklist]
        s.configure("c.TCheckbutton", background="white", font="Helvetica 14")
        for val, text, var in self.checklist:
            checks = Checkbutton(self, text=text, variable=var, style="c.TCheckbutton", command=self.check_button)
            checks.grid(sticky='w')
            lastminute.create_window(10, 50 + 30 * val, window=checks, anchor="w")
        lastminute.grid(row=0, column=0)

        self.run_plate = Button(self.leftFrame, text="Run Plate", command=self.controller.test_run)
        self.run_plate.grid(row=2, column=0, padx=20, pady=5, rowspan=2)
        self.run_plate.config(state=DISABLED)
        self.gcode_text = Button(self.leftFrame, text="Save GCode Text file", command=self.print_gcode)
        self.gcode_text.grid(row=4, column=0, padx=20, pady=5, rowspan=2)
        self.gcode_text.config(state=DISABLED)

        self.workarea = Canvas(self, bg='white', width=600, height=650)
        self.workarea.create_text(5, 10, text="Plate Map", font=NORM_FONT_BOLD, anchor="nw")
        self.date_canvas = self.workarea.create_text(300, 10,
                                                     text="Date: " + self.controller.shared_data["now_date"].get(),
                                                     font=("Purisa", 18), anchor="nw")
        self.controller.shared_data["now_date"].trace_variable('w', self.on_date_change)
        self.barcode_canvas = self.workarea.create_text(300, 40,
                                                        text="Barcode: " + self.controller.shared_data["barcode"].get(),
                                                        font=("Purisa", 18), anchor="nw")
        self.controller.shared_data["barcode"].trace_variable('w', self.on_barcode_change)

        self.workarea.create_rectangle(50, 80, 550, 400, width=3)

        insideCount = 0
        for controlY in range(0, 8):
            for controlX in range(0, 12):
                self.workarea.create_oval(65.38 + 40.38 * controlX, 93.3333 + 38.333 * controlY,
                                          90.38 + 40.38 * controlX, 118.333 + 38.333 * controlY, width=2,
                                          tags="final_plate" + str(insideCount))
                self.workarea.create_text(69.88 + 40.50 * controlX, 96.3333 + 38.333 * controlY,
                                          tags="text" + str(insideCount), font=("Purisa", 12), anchor="nw")
                # self.workarea.create_text(66.88 + 40.50 * controlX, 91.3333 + 38.333 * controlY, text=unicode_symbols[insideCount], font=("Purisa", 22), anchor="nw")
                insideCount = insideCount + 1
        self.workarea.create_text(5, 425, text="Legend:", font=NORM_FONT_BOLD, anchor="nw")
        self.workarea.create_text(5, 500, tags="legend1", anchor="nw")

        self.workarea.grid(row=1, column=5, rowspan=2, pady=(45, 0))
        # Button(self, text="Save Plate Layout", command=self.save_plate).grid(row=3, column=5, pady=20)

        self.comFrame = Frame(self)
        self.comFrame.grid(row=2, column=10, columnspan=2)
        self.comFrame.grid_rowconfigure(10, weight=1)
        self.comlist = Listbox(self.comFrame, height=30, width=40)
        Label(self.comFrame, text="Communication Log:", font=SMALL_FONT_BOLD).grid(row=0, column=0, sticky="w")
        self.comlist.grid(row=1, column=0, sticky=(N, W, E, S))
        s2 = ttk.Scrollbar(self.comFrame, orient=VERTICAL, command=self.comlist.yview)
        s2.grid(column=1, row=1, sticky=(N, S), padx=(0, 30))
        self.comlist['yscrollcommand'] = s2.set

    def check_button(self):
        self.vars = [row[2].get() for row in self.checklist]
        print(sum(self.vars))
        if sum(self.vars) == 5:
            self.run_plate.config(state=NORMAL)
            self.gcode_text.config(state=NORMAL)
        else:
            self.run_plate.config(state=DISABLED)
            self.gcode_text.config(state=DISABLED)

    def print_gcode(self):
        self.controller.shared_data["gcode_save"].set(1)
        self.controller.test_run()
        self.controller.shared_data["gcode_save"].set(0)

    def on_date_change(self, event, index, mode):
        self.workarea.itemconfigure(self.date_canvas, text="Date: " + self.controller.shared_data["now_date"].get())

    def on_barcode_change(self, event, index, mode):
        self.workarea.itemconfigure(self.barcode_canvas,
                                    text="Barcode: " + self.controller.shared_data["barcode"].get())

    def save_plate(self):
        x1 = 300
        y1 = 150
        self.workarea.postscript(file="test.ps", colormode='color')


# 600x825

# canvas.postscript(file="tmp.ps", colormode='color')
app = OTTO()
app.state("zoomed")
# app.set_theme("plastik")
# app.set_theme("smog")
app.mainloop()