# Post processor voor LasRobot van TCR
# Gebaseerd op de Panasonic G3 CSR post processor
# Gemaakt door: Joeri Chantrel
# Datum: 24-09-2020

from robodk import *
from tkinter import *
from tkinter import filedialog
import sys
import os

def get_safe_name(progname, max_chars=32):
    """Get a safe program name"""
    for c in '-[]/\\;,><&*:%=+@!#^()|?^':
        progname = progname.replace(c, '')

    if len(progname) <= 0:
        progname = 'Program'
    if progname[0].isdigit():
        progname = 'P' + progname
    if len(progname) > max_chars:
        progname = progname[:max_chars]
    return progname

def Pose_2_Panasonic(pose):
    return Pose_2_Motoman(pose)

class UI():

    Window = tkinter.Tk()
    Window.title('Instellingen')

    def getFolderPath():
        folder_selected = filedialog.askdirectory()
        Folder.set(folder_selected)

    VArc = StringVar()
    IArc = StringVar()
    TArc = StringVar()
    VKra = StringVar()
    IKra = StringVar()
    TKra = StringVar()
    Tafel = StringVar()
    TorchHoek = StringVar()
    LaagHoogte = StringVar()
    DummyRegels = StringVar()
    global Folder
    Folder = StringVar()
    Folder.set('C:/Users/joeri/Documents/RoboDK/gen')
    FolderSize = StringVar()
    Puls_Kort = StringVar()
    Puls_Kort.set('Pulserend')

    Label(Window, text='Vul hieronder de gewenste waarde in').grid(row=0, columnspan=2)
    Label(Window, text='Arc stroom:').grid(row=1, sticky=E)
    Label(Window, text='Arc spanning:').grid(row=2, sticky=E)
    Label(Window, text='Arc tijd:').grid(row=3, sticky=E)
    Label(Window, text='Krater stroom:').grid(row=4, sticky=E)
    Label(Window, text='Krater spanning:').grid(row=5, sticky=E)
    Label(Window, text='Krater tijd:').grid(row=6, sticky=E)
    Label(Window, text='Z hoogte plaat:').grid(row=7, sticky=E)
    Label(Window, text='Z Hoek torch:').grid(row=8, sticky=E)
    Label(Window, text='Laag hoogte:').grid(row=9, sticky=E)
    Label(Window, text='Dummy regels:').grid(row=10, sticky=E)
    Label(Window, text='Folder:').grid(row=11, sticky=E)
    Label(Window, text='Programmas per subfolder:').grid(row=12, sticky=E)
    Label(Window, text='Pulserend/Kortsluit:').grid(row=13, sticky=E)

    Button(Window, text='OK', width=10, command=Window.destroy).grid(row=14, columnspan=2, pady=5)

    e0 = Entry(Window, textvariable = IArc)
    e1 = Entry(Window, textvariable = VArc)
    e2 = Entry(Window, textvariable = TArc)
    e3 = Entry(Window, textvariable = IKra)
    e4 = Entry(Window, textvariable = VKra)
    e5 = Entry(Window, textvariable = TKra)
    e6 = Entry(Window, textvariable = Tafel)
    e7 = Entry(Window, textvariable = TorchHoek)
    e8 = Entry(Window, textvariable = LaagHoogte)
    e9 = Entry(Window, textvariable = DummyRegels)
    b10 = Button(Window, text = 'Browse', command=getFolderPath)
    e11 = Entry(Window, textvariable = FolderSize)
    w12 = OptionMenu(Window, Puls_Kort, 'Pulserend', 'Kortsluit')

    e0.insert(END, '60')
    e1.insert(END, '20.5')
    e2.insert(END, '0.25')
    e3.insert(END, '60')
    e4.insert(END, '21')
    e5.insert(END, '0.3')
    e6.insert(END, '230.654')
    e7.insert(END, '67')
    e8.insert(END, '2')
    e9.insert(END, '5')
    e11.insert(END, '20')

    e0.grid(row=1, column=1, padx=7, pady=3)
    e1.grid(row=2, column=1, padx=7, pady=3)
    e2.grid(row=3, column=1, padx=7, pady=3)
    e3.grid(row=4, column=1, padx=7, pady=3)
    e4.grid(row=5, column=1, padx=7, pady=3)
    e5.grid(row=6, column=1, padx=7, pady=3)
    e6.grid(row=7, column=1, padx=7, pady=3)
    e7.grid(row=8, column=1, padx=7, pady=3)
    e8.grid(row=9, column=1, padx=7, pady=3)
    e9.grid(row=10, column=1, padx=7, pady=3)
    b10.grid(row=11, column=1, padx=7, pady=3)
    e11.grid(row=12, column=1, padx=7, pady=3)
    w12.grid(row=13, column=1, padx=7, pady=3)

    Window.mainloop()

class RobotPost(object):
    """Robot post object defined for Panasonic robots"""
    #Bestand eigenschappen
    PROG_EXT = 'csr'
    MAX_LINES_X_PROG = 500
    INCLUDE_SUB_PROGRAMS = True

    #Maximun snelheden
    STR_V = '15.00, m/min'
    STR_VJ = '50.00, %%'

    STR_CNT = ''

    #Active frame ,tool input
    ACTIVE_FRAME = 0
    ACTIVE_TOOL = 3
    TL_NAME = 'MIG 17mm'

    SPARE_PR = 95

    #Variabele voor het lassen
    VArc = float(UI.VArc.get())               #Las spanning
    IArc = float(UI.IArc.get())             #Las stroom
    TArc = float(UI.TArc.get())             #Voorloopsnelheid

    VKra = float(UI.VKra.get())               #Krater spanning
    IKra = float(UI.IKra.get())             #Krater stroom
    TKra = float(UI.TKra.get())             #Krater tijd

    Tafel = float(UI.Tafel.get())           #Z coordinaat van de tafel

    TorchHoek = float(UI.TorchHoek.get())   #De hoek van de Torch

    LaagHoogte = float(UI.LaagHoogte.get()) #Om de hoeveel lagen checken voor hoogte

    DummyRegels = int(UI.DummyRegels.get()) #Extra regels toevoegen om errors te voorkomen

    Folder = str(Folder.get())              #In welke folder alles opgeslagen moet worden

    Puls_Kort = str(UI.Puls_Kort.get())     #Pulserend of kortsluit lassen

    FolderSize = int(UI.FolderSize.get())   #Hoveel programmas's per folder

    Timeout = 120           #Maximaal wachten op de input
    TempInput = '5'         #Input nummer voor de Temp sensor
    StandOutTemp = 'ON'     #De standaard waarde die gegeven wordt door de Temp sensor
                            #Dus de waarde als de temp niet te hoog is

    REGISTER_DIGITS = 5

    PULSES_X_DEG = [1, 1, 1, 1, 1, 1]

    #Variabel voor dingen bij te houden
    LINE_COUNT = 0
    P_COUNT = 0
    C_COUNT = 0
    nProgs = 0
    LBL_ID_COUNT = 0
    Extrude = 0
    Weld = False
    Laag = 0
    LayerCount = 0
    Laatste_Doc = False
    F_COUNT = 1


    ROBOT_POST = ''
    ROBOT_NAME = ''
    PROG_FILES = []

    PROG_NAMES = []
    PROG_LIST = []

    PROG_NAME = 'unknown'
    PROG_NAME_CURRENT = 'unknown'

    nPages = 0
    PROG_NAMES_MAIN = []

    PROG = []
    PROG_TARGETS = []
    LOG = ''

    #Robot eigenschappen
    nAxes = 6
    AXES_TYPE = ['R', 'R', 'R', 'R', 'R', 'R']
    AXES_TRACK = []
    AXES_TURNTABLE = []
    HAS_TRACK = False
    HAS_TURNTABLE = False

    SPEED_BACKUP = None
    LAST_POSE = None
    POSE_FRAME = eye(4)
    POSE_FRAME = eye(4)
    LAST_CONFDATA = [None, None, None, None]

    def __init__(self, robotpost=None, robotname=None, robot_axes=6, **kwargs):
        self.ROBOT_POST = robotpost
        self.ROBOT_NAME = robotname
        self.nAxes = robot_axes
        self.PROG = []
        self.LOG = ''
        for k, v in kwargs.items():
            if k == 'lines_x_prog':
                self.MAX_LINES_X_PROG = v
            if k == 'axes_type':
                self.AXES_TYPE = v
            if k == 'pulses_x_deg':
                self.PULSES_X_DEG = v

        for i in range(len(self.AXES_TYPE)):
            if self.AXES_TYPE[i] == 'T':
                self.AXES_TRACK.append(i)
                self.HAS_TRACK = True
            elif self.AXES_TYPE[i] == 'J':
                self.AXES_TURNTABLE.append(i)
                self.HAS_TURNTABLE = True

    def ProgStart(self, progname, new_page=False):
        progname = get_safe_name(progname)
        progname_i = progname
        if new_page:
            if self.nPages == 0:
                if len(self.PROG_NAMES_MAIN) > 0:
                    print ("Can't split %s: Two or more programs are split into smaller programs" % progname)
                    print (self.PROG_NAMES_MAIN)
                    raise Exception('Only one program at a time can be split into smaller programs')
                self.PROG_NAMES_MAIN.append(self.PROG_NAME)
                self.nPages = self.nPages + 1
            self.nPages = self.nPages + 1
            progname_i = '%s%i' % (self.PROG_NAME, self.nPages)
            self.PROG_NAMES_MAIN.append(progname_i)
        else:
            if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
                return
            self.PROG_NAME = progname
            self.nProgs = self.nProgs + 1
        self.PROG_NAME_CURRENT = progname_i
        self.PROG_NAMES.append(progname_i)

    def ProgFinish(self, progname, new_page=False):
        progname = get_safe_name(progname)
        if not new_page:
            self.nPages = 0
        header = ''
        header += '[Description]\n'
        header += 'Robot, %s' % self.ROBOT_NAME + '\n'
        header += 'Comment,\n'
        header += 'Mechanism,1(0000)\n'
        header += 'Tool, %i:' % self.ACTIVE_TOOL + self.TL_NAME + '\n'
        header += 'Creator, RoboDK\n'
        header += 'Welder, 1:TAWERS\n'
        header += 'User coordinates, None' + '\n'
        header += 'Create, 2020, 1, 1, 2, 38, 19' + '\n'
        header += 'Update, 2020, 1, 1, 2, 38, 19' + '\n'
        header += 'Original,RoboDK\n'
        header += 'Edit, 0\n'
        header += '\n'
        header += '[Pose]\n'
        header += '/Name, Type, X, Y, Z, U, V, W'
        import time
        Extrude = 0
        datestr = time.strftime('%Y/%m/%d %H:%M')
        header_ins = '\n'
        header_ins += '[Variable]\n'            #Hier kunnen variabele in opgeslagen worden
        header_ins += 'LB, LB001, Byte, 0\n'    #Handig voor de delay of de input voor de
        header_ins += 'LB, LB002, Byte, 0\n'    #Temp enz
        header_ins += 'LB, LB003, Byte, 0\n'
        header_ins += 'LB, LB004, Byte, 0\n'
        header_ins += 'LB, LB005, Byte, 0\n'
        header_ins += 'LI, LI001, Int, 0\n'
        header_ins += 'LI, LI002, Int, 0\n'
        header_ins += 'LI, LI003, Int, 0\n'
        header_ins += 'LI, LI004, Int, 0\n'
        header_ins += 'LI, LI005, Int, 0\n'
        header_ins += 'LL, LL001, Long, 0\n'
        header_ins += 'LL, LL002, Long, 0\n'
        header_ins += 'LL, LL003, Long, 0\n'
        header_ins += 'LL, LL004, Long, 0\n'
        header_ins += 'LL, LL005, Long, 0\n'
        header_ins += 'LR, LR001, Real, 0\n'
        header_ins += 'LR, LR002, Real, 0\n'
        header_ins += 'LR, LR003, Real, 0\n'
        header_ins += 'LR, LR004, Real, 0\n'
        header_ins += 'LR, LR005, Real, 0\n'
        header_ins += '\n'
        header_ins += '[Command]'

        self.PROG.insert(0, header_ins)
        self.PROG_TARGETS.insert(0, header)
        self.PROG = self.PROG_TARGETS + self.PROG
        self.PROG_LIST.append(self.PROG)
        self.PROG = []
        self.PROG_TARGETS = []
        self.LINE_COUNT = 0
        self.P_COUNT = 0
        self.C_COUNT = 0
        self.LAST_CONFDATA = [None, None, None, None]
        self.LBL_ID_COUNT = 0
        return

    def progsave(self, folder, progname, ask_user=False, show_result=False):
        print (folder)
        if not folder.endswith('/'):
            folder = folder + '/'
        progname = progname + '.' + self.PROG_EXT
        if ask_user or not DirExists(folder):
            filesave = getSaveFile(folder, progname, 'Save program as...')
            if filesave is not None:
                filesave = filesave.name
            else:
                return
        else:
            filesave = folder + progname
        fid = open(filesave, 'w')
        for line in self.PROG:
            fid.write(line)
            fid.write('\n')

        fid.close()
        print ('SAVED: %s\n' % filesave)
        self.PROG_FILES.append(filesave)
        if show_result:
            if type(show_result) is str:
                import subprocess
                p = subprocess.Popen([show_result, filesave])
            elif type(show_result) is list:
                import subprocess
                p = subprocess.Popen(show_result + [filesave])
            else:
                import os
                os.startfile(filesave)
        return

    def ProgSave(self, folder, progname, ask_user=False, show_result=False):
        progname = get_safe_name(progname)
        nfiles = len(self.PROG_LIST)
        if nfiles >= 1:
            for i in range(len(self.PROG_LIST)):
                if i % self.FolderSize == 0:
                    directory = 'test %i' % self.F_COUNT
                    parent_dir = self.Folder
                    path = os.path.join(parent_dir, directory)
                    os.mkdir(path)
                    self.F_COUNT = self.F_COUNT + 1
            if self.LINE_COUNT > 0:
                print ('Warning: ProgFinish was not called properly')
                self.PROG_LIST.append(self.PROG)
                self.PROG_NAMES.append('Unknown')
                self.PROG = []
                self.LINE_COUNT = 0

            if len(self.PROG_NAMES_MAIN) > 1:
                for i in range(1,self.F_COUNT):
                    progname_main = 'M_Print3D_%i' % i
                    self.ProgStart(progname_main)
                    j = 0
                    for prog_call in self.PROG_NAMES_MAIN:
                        j = j + 1
                        if j <= i * self.FolderSize and j > i * self.FolderSize -self.FolderSize:
                            self.RunCode(prog_call, True)
                    self.ProgFinish(progname_main)
                for i in range(self.F_COUNT-1,0,-1):
                    self.PROG = self.PROG_LIST.pop()
                    progname_last = self.PROG_NAMES.pop()
                    self.progsave('%s%s%i' % (self.Folder, '/test ', i), progname_last, ask_user, show_result)
            if len(self.PROG_FILES) == 0:
                return
            first_file = self.PROG_FILES[0]
            folder_user = getFileDir(first_file)

            FolderNum = 0
            for i in range(len(self.PROG_LIST)):
                if i % self.FolderSize == 0:
                    FolderNum = FolderNum + 1
                self.PROG = self.PROG_LIST[i]
                self.progsave('%s%s%i' % (self.Folder, '/test ', FolderNum), self.PROG_NAMES[i], False, show_result)

        elif nfiles == 1:
            self.PROG = self.PROG_NAMES[0]
            self.progsave(folder, progname, ask_user, show_result)
        else:
            print ('Warning! Program has not been properly finished')
            self.progsave(folder, progname, ask_user, show_result)
        if show_result and len(self.LOG) > 0:
            mbox('Program generation LOG:\n\n' + self.LOG)

    def ProgSendRobot(self, robot_ip, remote_path, ftp_user, ftp_pass):
        """Send a program to the robot using the provided parameters. This method is executed right after ProgSave if we selected the option "Send Program to Robot".
        The connection parameters must be provided in the robot connection menu of RoboDK"""
        UploadFTP(self.PROG_FILES, robot_ip, remote_path, ftp_user, ftp_pass)

    def MoveJ(self, pose, joints, conf_RLF=None):
        """Add a joint movement"""
        self.page_size_control()
        target_id = self.add_target_cartesian(pose, joints, conf_RLF)
        self.addline('MOVEP, P%i, %s, ' % (target_id, self.STR_V) + 'N')
        self.LAST_POSE = pose

    def MoveL(self, pose, joints, conf_RLF=None):
        """Add a linear movement"""
        self.page_size_control()
        target_id = self.add_target_cartesian(pose, joints, conf_RLF)

        if self.STR_V == '1.80, m/min' or self.STR_V == '1.20, m/min':
            if self.Weld == False:
                self.PROG[-1] = self.PROG[-1].replace('N', 'W')
                self.addline('ARC-SET, %i, %.1f, %.2f' % (self.IArc, self.VArc, self.TArc))
                self.addline('ARC-ON, ArcStart1.prg, 1')
                self.Weld = True
        else:
            if self.Weld == True:
                self.PROG[-1] = self.PROG[-1].replace('W', 'N')
                self.addline('CRATER, %i, %.1f, %.2f' % (self.IKra, self.VKra, self.TKra))
                self.addline('ARC-OFF, ArcEnd1.prg, 1')
                self.Weld = False
                if self.nPages % self.FolderSize == 0 and self.nPages > 0:
                    self.Laatste_Doc = True;
        if self.Weld == True:
            WeldMove = 'W'
        else:
            WeldMove = 'N'
        self.addline('MOVEL, P%i, %s%s' % (target_id, self.STR_V, self.STR_CNT) + ' , 0, %s' % (WeldMove))
        self.LAST_POSE = pose
        if self.Laatste_Doc == True:
            self.Laatste_Doc = False
            self.LINE_COUNT = self.MAX_LINES_X_PROG

    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        """Add a circular movement"""
        self.page_size_control()
        target_id1 = self.add_target_joints(joints1)
        target_id2 = self.add_target_joints(joints2)
        if self.Weld == True:
            WeldMove = 'W'
        else:
            WeldMove = 'N'
        self.addline('MOVEC, P%i, %s%s' % (target_id1, self.STR_V, self.STR_PL) + ', 0, %s' % (WeldMove))
        self.addline('MOVEC, P%i, %s%s' % (target_id2, self.STR_V, self.STR_PL) + ', 0, %s' % (WeldMove))
        self.LAST_POSE = None
        return

    def setFrame(self, pose, frame_id, frame_name):
        """Change the robot reference frame"""
        xyzwpr = Pose_2_Panasonic(pose)
        self.POSE_FRAME = pose
        return
        if frame_id is None or frame_id < 0:
            self.RunMessage('Setting Frame %i (%s):' % (self.ACTIVE_FRAME, str(frame_name)), True)
            self.addline('FRAME %i:%s' % (self.ACTIVE_FRAME, str(frame_name)))
        else:
            self.ACTIVE_FRAME = frame_id
            self.TL_NAME = str(frame_name)
            self.RunMessage('Frame %i (%s) should be close to:' % (self.ACTIVE_FRAME, str(frame_name)), True)
            self.RunMessage('%.1f,%.1f,%.1f,%.1f,%.1f,%.1f' % (xyzwpr[0], xyzwpr[1], xyzwpr[2], xyzwpr[3], xyzwpr[4], xyzwpr[5]), True)
        return

    def setTool(self, pose, tool_id, tool_name):
        """Change the robot TCP"""
        if tool_id > 0:
            self.ACTIVE_TOOL = tool_id
        xyzwpr = Pose_2_Panasonic(pose)
        self.addline('TOOL, %i:%s' % (self.ACTIVE_TOOL, str(self.TL_NAME)))

    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms <= 0:
            self.addline('STOP')
        else:
            self.addline('DELAY, %.2f,' % (time_ms * 0.001))

    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""
        speed_m_min = speed_mms * 60.0 * 0.001
        speed = max(0.01, min(speed_m_min, 120.0))
        self.STR_V = '%.2f, m/min' % speed

    def setAcceleration(self, accel_mmss):
        """Changes the robot acceleration (in mm/s2)"""
        self.addlog('Set acceleration not defined')

    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        speedj = max(0.01, min(speed, 100.0))
        self.STR_VJ = '%.2f, mm' % speedj

    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        self.addlog('Set acceleration not defined')

    def setZoneData(self, zone_mm):
        """Changes the zone data approach (makes the movement more smooth)"""
        if zone_mm < 0:
            self.STR_PL = ''
        else:
            self.STR_PL = ''

    def setDO(self, io_var, io_value):
        """Set a Digital Output"""
        if type(io_var) != str:
            io_var = '%01d' % io_var
        if type(io_value) != str:
            if io_value > 0:
                io_value = 'ON'
            else:
                io_value = 'OFF'
        self.addline('OUT, o1#(%s:), %s' % (io_var, io_value))

    def setAO(self, io_var, io_value):
        """Set an Analog Output"""
        self.addline('Analog output')

    def waitDI(self, io_var, io_value, timeout_ms=0):
        """Waits for an input io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if type(io_var) != str:
            io_var = '%01d' % io_var
        if type(io_value) != str:
            if io_value > 0:
                io_value = 'ON'
            else:
                io_value = 'OFF'
        self.addline('WAIT_IP, i1#(%s:), %s, %.2f, NOP' % (io_var, io_value, timeout_ms * 0.001))

    def RunCode(self, code, is_function_call=False):
        """Turns call's for extruder to ARC"""
        code = get_safe_name(code)
        if code.find('M_RunCode') != -1:
            code = code.replace('M_RunCode', '')
            if code == '12345':
                #code die per laag moet afspelen
                #self.addline('WAIT_IP, i1#(%s:), %s, %.2f, NOP' % (self.TempInput, self.StandOutTemp, self.Timeout))
                self.LayerCount = self.LayerCount +1
                if self.LayerCount > 1:
                    self.addline('CNVSET, GD#(4:GD004), P%i' % (self.C_COUNT + 3))
                    self.addline('CALL, Z HOOGTE CHECK.prg')
                #if self.Laag == self.CheckLaag:
                #    self.addline('Laag checken')
                #    self.Laag = 0
                #else:
                #    self.Laag = self.Laag + 1
                return
            else:
                return
        if code.find('onFinish') != -1:
            self.addline('MOVEP, GP#(100:GP HOME), 80.0, %, N')
            return
        if code.find('Extruder') == -1:
            code.replace(' ', '_')
            self.addline('CALL, %s' % code + '.prg')
        else:
            return


    def RunMessage(self, message, iscomment=False):
        """Turn Show Weld gun into WPLS, ON"""
        if message == 'Show Weld gun':
            if self.Puls_Kort == 'Pulserend':
                self.addline('WPLS, ON')
            self.addline('CLEAR, GD#(ALL)')
            self.addline('CLEAR, GR#(ALL)')
            self.addline('MOVEP, GP#(100:GP HOME), 80.0, %, N')
            for i in range(self.DummyRegels):
                self.addline('MOVEP, GP#(100:GP HOME), 80.0, %, N')
        else:
            return

    def page_size_control(self):
        if self.LINE_COUNT >= self.MAX_LINES_X_PROG:
            self.ProgFinish(self.PROG_NAME, True)
            self.ProgStart(self.PROG_NAME, True)
            self.addline('TOOL, 3:MIG 17mm')
            if self.Puls_Kort == 'Pulserend':
                self.addline('WPLS, ON')

    def addline(self, newline, movetype=' '):
        """Add a program line"""
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
        self.page_size_control()
        self.LINE_COUNT = self.LINE_COUNT + 1
        self.PROG.append(newline)

    def rewriteline(self, newline, movetype=' '):
        """Add a program line"""
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
        self.page_size_control()
        self.PROG[-1] = (newline)

    def addline_targets(self, newline):
        """Add a line at the end of the program (used for targets)"""
        self.PROG_TARGETS.append(newline)

    def addlog(self, newline):
        """Add a log message"""
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
        self.LOG = self.LOG + newline + '\n'

    def setCartesian(self, confdata):
        if self.ACTIVE_FRAME is not None and self.ACTIVE_FRAME != self.LAST_CONFDATA[1]:
            self.LAST_CONFDATA[1] = self.ACTIVE_FRAME
        if self.ACTIVE_TOOL != self.LAST_CONFDATA[2]:
            self.LAST_CONFDATA[2] = self.ACTIVE_TOOL
        if self.LAST_CONFDATA[0] != 2:
            self.LAST_CONFDATA[3] = confdata
        elif self.LAST_CONFDATA[3] != confdata:
            self.LAST_CONFDATA[3] = confdata
        self.LAST_CONFDATA[0] = 2
        return

    def setPulses(self):
        if self.LAST_CONFDATA[0] is None:
            self.LAST_CONFDATA[2] = self.ACTIVE_TOOL
        if self.LAST_CONFDATA[0] != 1:
            self.LAST_CONFDATA[0] = 1
        self.LAST_CONFDATA[0] = 1
        self.LAST_CONFDATA[1] = None
        self.LAST_CONFDATA[2] = None
        self.LAST_CONFDATA[3] = None
        return

    def add_target_joints(self, joints):
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
        self.setPulses()
        self.C_COUNT = self.C_COUNT + 1
        cid = self.C_COUNT
        str_pulses = []
        for i in range(len(joints)):
            str_pulses.append('%f' % (joints[i] * self.PULSES_X_DEG[i]))

        self.addline_targets('P%i, AU, ' % cid + (',').join(str_pulses))
        return cid

    def add_target_cartesian(self, pose, joints, conf_RLF):
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
        else:
            xyzwpr = Pose_2_Panasonic(pose)
            xyzwpr[2] = xyzwpr[2] - self.Tafel
            if xyzwpr[3] - 180 <= -180:
                xyzwpr[3] = xyzwpr[3] + 180
            else:
                xyzwpr[3] = xyzwpr[3] - 180
            xyzwpr[5] = self.TorchHoek
            if conf_RLF is None:
                conf_RLF = [
                 0, 0, 0]
            turns = [0, 0, 0]
            if len(joints) >= 6:
                turnJ4 = (joints[3] + 180) // 360
                turnJ6 = (joints[5] + 180) // 360
                turnJ1 = (joints[0] + 180) // 360
                turns = [turnJ4, turnJ6, turnJ1]
            confdata = '%i,%i,%i,%i,%i,%i,0,0' % tuple(conf_RLF[:3] + turns[:3])
            self.setCartesian(confdata)
            self.C_COUNT = self.C_COUNT + 1
            cid = self.C_COUNT
            self.addline_targets('P%i, AU, ' % cid + '%.3f,%.3f,%.3f,%.2f,%.2f,%.2f' % tuple(xyzwpr))
            return cid


def Pose(xyzrpw):
    x, y, z, r, p, w = xyzrpw
    a = r * math.pi / 180
    b = p * math.pi / 180
    c = w * math.pi / 180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb * ca, ca * sc * sb - cc * sa, sc * sa + cc * ca * sb, x], [cb * sa, cc * ca + sc * sb * sa, cc * sb * sa - ca * sc, y], [-sb, cb * sc, cc * cb, z], [0, 0, 0, 1]])


def test_post():
    """Test the post with a basic program"""
    robot = RobotPost('Panasonic', 'Panasonic robot', 6)
    robot.ProgStart('Program')
    robot.RunMessage('Program generated by RoboDK', True)
    robot.setFrame(Pose([807.766544, -963.699898, 41.478944, 0, 0, 0]), None, 0)
    robot.setTool(Pose([62.5, -108.253175, 100, -60, 90, 0]), None, 0)
    robot.MoveJ(Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -6.77518, -20.54925, 71.38674, 49.58727, -302.54752])
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418])
    robot.MoveL(Pose([200, 200, 262.132034, 180, 0, -150]), [-43.73892, -3.91728, -35.77935, 58.57566, 54.11615, -253.81122])
    robot.RunMessage('Setting air valve 1 on')
    robot.RunCode('TCP_On', True)
    robot.Pause(1000)
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418])
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677])
    robot.MoveL(Pose([250, 250, 191.421356, 180, 0, -150]), [-39.75778, -1.04537, -40.37883, 52.09118, 54.15317, -246.94403])
    robot.RunMessage('Setting air valve off')
    robot.RunCode('TCP_Off', True)
    robot.Pause(1000)
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677])
    robot.MoveL(Pose([250, 200, 278.023897, 180, 0, -150]), [-41.85389, -1.95619, -34.89154, 57.43912, 52.34162, -253.73403])
    robot.MoveL(Pose([250, 150, 191.421356, 180, 0, -150]), [-43.82111, 3.29703, -40.29493, 56.02402, 56.61169, -249.23532])
    robot.ProgFinish('Program')
    robot.setDO
    robot.waitDI
    robot.PROG = robot.PROG_LIST.pop()
    for line in robot.PROG:
        print (line)

    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)
    input('Press Enter to close...')
    return


if __name__ == '__main__':
    test_post()
