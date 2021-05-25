#                                 EYE MAGIC GUI APP

#---------------------------------IMPORTS---------------------------------
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.font as tkFont
import tkinter.filedialog
from PIL import Image, ImageTk
import time
import functools
import webbrowser


#---------------------------------MODULES---------------------------------
import serial_comms_module as serial_comms


class EyeMagicApp(tk.Tk):
    # current build version
    build_version = 'version : 1.6 | build : 25/05/2021'

    # COLORS USED
    color_black = '#1a1a1a'
    color_light_grey = '#e6e6e6'
    color_dark_grey = '#787878'
    color_dark_grey_activated = '#8f8f8f'
    button_highlight_color = '#e3f7ff'

    # LOGO - ICON
    iconbitmap_file = 'files\\icon-logo\\Digitune.ico'
    logo_image_path = 'files\\icon-logo\\logo.png'

    # INITIALIZING
    def __init__(self):
        super().__init__()
        self.title('EYE-MAGIC DIGITUNE')
        self.iconbitmap(default=self.iconbitmap_file)
        # GUI resolution 500x600
        self.WIDTH = 500
        self.HEIGHT = 600
        # 2 second timeout
        timeout = 2
        self.serial = serial_comms.serial_comms_module(timeout=timeout)

        # 10 - slot message history for teminal-like functionality display
        self.msg_list = ['' for _ in range(10)]
        self.create_GUI()




    def create_GUI(self):
        # main canvas to attach everything on
        self.main_canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg=self.color_light_grey)
        self.main_canvas.pack()
        # font for X AXIS / Y AXIS labels
        axis_label_font = tkFont.Font(family='Helvetica', size=11, weight='bold')
        # X AXIS
        x_axis_label = tk.Label(self.main_canvas, text='X AXIS', font=axis_label_font, bg=self.color_light_grey)
        x_axis_label.place(anchor='n', relx=0.2, rely=0.005, relwidth=0.15, relheight=0.04)
        # Y AXIS
        y_axis_label = tk.Label(self.main_canvas, text='Y AXIS', font=axis_label_font, bg=self.color_light_grey)
        y_axis_label.place(anchor='n', relx=0.48, rely=0.005, relwidth=0.15, relheight=0.04)

        # GUI value names to >>> serial communication names dictionary (X axis)
        self.serial_send_names_dict_X = {'Kp' : 'kp', 'Kd' : 'kd', 'Td' : 'td', 'N' : 'dn', 'H Damp' : 'kaff',
                                       'HPx' : 'hpfx', 'Kvff' : 'kvff', 'ErrClip' : 'eclp', 'Clip' : 'hclp',
                                       'Slope' : 'eslp', 'Scale' : 'scale', 'Sym' : 'sym', 'Power' : 'p1',
                                       'SafeVel' : 'p2', 'F-Theta' : 'p4', 'Pincusion' : 'p3'}
        
        # GUI value names to >>> serial communication names dictionary (Y axis)
        self.serial_send_names_dict_Y = {'Kp' : 'kp', 'Kd' : 'kd', 'Td' : 'td', 'N' : 'dn', 'H Damp' : 'kaff',
                                        'HPy' : 'hpfx', 'Kvff' : 'kvff', 'ErrClip' : 'eclp', 'Clip' : 'hclp',
                                        'Slope' : 'eslp', 'Scale' : 'scale', 'Sym' : 'sym', 'Power' : 'p1',
                                        'Cycles' : 'p2', 'F-Theta' : 'p3', 'Roll-Off' : 'p4'}


        # NAME - DEFAULT_VALUE - INCREMENT_AMOUNT - MINIMUM_VALUE - MAXIMUM_VALUE for X axis widgets
        self.tuning_values_list_X = [{'name':'Kp', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':10000},
                                {'name':'Kd', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':10000},
                                {'name':'Td', 'default_value':'0.000000', 'increment':0.00001, 'min_value': 0, 'max_value':1},
                                {'name':'N', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':100},
                                {'name':'H Damp', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':100},
                                {'name':'HPx', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1},
                                {'name':'Kvff', 'default_value':'0', 'increment':1, 'min_value': 0, 'max_value':3000},
                                {'name':'ErrClip', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':10},
                                {'name':'Clip', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1},
                                {'name':'Slope', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1},
                                {'name':'Scale', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':10},
                                {'name':'Sym', 'default_value':'0.500', 'increment':0.001, 'min_value': 0.5, 'max_value':1.5},
                                {'name':'Power', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':100},
                                {'name':'SafeVel', 'default_value':'0.000000', 'increment':0.000001, 'min_value': 0, 'max_value':1}, 
                                {'name':'F-Theta', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':1},
                                {'name':'Pincusion', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':1}]      

        # NAME - DEFAULT_VALUE - INCREMENT_AMOUNT - MINIMUM_VALUE - MAXIMUM_VALUE for Y axis widgets
        self.tuning_values_list_Y = [{'name':'Kp', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':10000},
                                {'name':'Kd', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':10000},
                                {'name':'Td', 'default_value':'0.000000', 'increment':0.00001, 'min_value': 0, 'max_value':1},
                                {'name':'N', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':100},
                                {'name':'H Damp', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':100},
                                {'name':'HPy', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1},
                                {'name':'Kvff', 'default_value':'0', 'increment':1, 'min_value': 0, 'max_value':3000},
                                {'name':'ErrClip', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':10},
                                {'name':'Clip', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1},
                                {'name':'Slope', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1},
                                {'name':'Scale', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':10},
                                {'name':'Sym', 'default_value':'0.500', 'increment':0.001, 'min_value': 0.5, 'max_value':1.5},
                                {'name':'Power', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':100},
                                {'name':'Cycles', 'default_value':'0.0', 'increment':0.1, 'min_value': 0, 'max_value':300},      
                                {'name':'F-Theta', 'default_value':'0.000', 'increment':0.001, 'min_value': 0, 'max_value':1},
                                {'name':'Roll-Off', 'default_value':'0.00', 'increment':0.01, 'min_value': 0, 'max_value':1}]  


        # way of accessing individual widgets when using a FOR loop to create them <<< find a better way (?)
        self.tuning_values_spinbox_list_x = []
        self.tuning_values_spinbox_list_y = []

        # font used for the value labels
        label_font = tkFont.Font(family='Helvetica', size=9)

        for i, value_dict in enumerate(self.tuning_values_list_X):
            # relative height of labels - wigdets *** if-else to create spacing in the right places
            rely = (i*0.045)
            if i < 4: rely += 0.04
            elif i < 6: rely += 0.065
            elif i < 7: rely += 0.09
            elif i < 10: rely += 0.115
            elif i < 12: rely += 0.14
            elif i < 13: rely += 0.165
            else: rely += 0.19

            label_text = value_dict['name']
            self.x_value_label = tk.Label(self.main_canvas, text=label_text, font=label_font, bg=self.color_light_grey)
            self.x_value_label.place(anchor='n', relx=0.07, rely=rely, relwidth=0.11, relheight=0.04)

            spinbox_text_value = value_dict['default_value']
            val_min, val_max = value_dict['min_value'], value_dict['max_value']

            self.x_spinbox = tk.Spinbox(self.main_canvas, from_=val_min, to=val_max)
            self.x_spinbox.configure(relief='groove', command=functools.partial(self.change_value_func, self.x_value_label['text'], self.x_spinbox, 'x'))
            self.x_spinbox.bind('<Return>', lambda event, name=self.x_value_label['text'], widget=self.x_spinbox, axis='x' : self.change_value_func(name, widget, axis))
            self.x_spinbox.bind('<MouseWheel>', lambda event, x=self.x_spinbox : self.mouse_wheel_spinbox(x, event))
            self.x_spinbox.bind('<Enter>', lambda event, x=self.x_spinbox : self.button_on_hover(x))
            self.x_spinbox.bind('<Leave>', lambda event, x=self.x_spinbox, y='white' : self.button_on_hover_leave(x, y))
            self.x_spinbox.delete(0, 'end')
            self.x_spinbox.insert(0, spinbox_text_value)
            self.x_spinbox.configure(state='disabled')
            inc = value_dict['increment']
            self.x_spinbox.configure(increment=inc)
            self.x_spinbox.place(anchor='n', relx=0.2, rely=rely+0.005, relwidth=0.15, relheight=0.032)
            self.tuning_values_spinbox_list_x.append(self.x_spinbox)


        for i, value_dict in enumerate(self.tuning_values_list_Y):
            rely = (i*0.045)
            if i < 4: rely += 0.04
            elif i < 6: rely += 0.065
            elif i < 7: rely += 0.09
            elif i < 10: rely += 0.115
            elif i < 12: rely += 0.14
            elif i < 13: rely += 0.165
            else: rely += 0.19
            # add separator widget on these iterations >>> spacing / grouping widgets
            if i == 4 or i == 6 or i == 7 or i == 10 or i == 12 or i == 13:
                self.valSeparator = ttk.Separator(self.main_canvas)
                self.valSeparator.place(relx=0.05, rely=rely-0.015, relwidth=0.5)

            label_text = value_dict['name']
            self.y_value_label = tk.Label(self.main_canvas, text=label_text, font=label_font, bg=self.color_light_grey)
            self.y_value_label.place(anchor='n', relx=0.35, rely=rely, relwidth=0.11, relheight=0.04)

            spinbox_text_value = value_dict['default_value']
            val_min, val_max = value_dict['min_value'], value_dict['max_value']

            self.y_spinbox = tk.Spinbox(self.main_canvas, from_=val_min, to=val_max)
            self.y_spinbox.configure(relief='groove', command=functools.partial(self.change_value_func, self.y_value_label['text'], self.y_spinbox, 'y'))
            self.y_spinbox.bind('<Return>', lambda event, name=self.y_value_label['text'], widget=self.y_spinbox, axis='y' : self.change_value_func(name, widget, axis))
            self.y_spinbox.bind('<MouseWheel>', lambda event, x=self.y_spinbox : self.mouse_wheel_spinbox(x, event))
            self.y_spinbox.bind('<Enter>', lambda event, x=self.y_spinbox : self.button_on_hover(x))
            self.y_spinbox.bind('<Leave>', lambda event, x=self.y_spinbox, y='white' : self.button_on_hover_leave(x, y))
            self.y_spinbox.delete(0, 'end')
            self.y_spinbox.insert(0, spinbox_text_value)
            self.y_spinbox.configure(state='disabled')
            inc = value_dict['increment']
            self.y_spinbox.configure(increment=inc)
            self.y_spinbox.place(anchor='n', relx=0.48, rely=rely+0.005, relwidth=0.15, relheight=0.032)
            self.tuning_values_spinbox_list_y.append(self.y_spinbox)      

        self.save_button = tk.Button(self.main_canvas, text='Save', font='Helvetica 10 bold', bg=self.color_light_grey, 
            relief='groove', command=self.save_button_func)
        self.save_button.bind('<Enter>', lambda event, x=self.save_button : self.button_on_hover(x))
        self.save_button.bind('<Leave>', lambda event, x=self.save_button : self.button_on_hover_leave(x))
        self.save_button.place(anchor='n', relx=0.23, rely=0.94, relwidth=0.4, relheight=0.045)

        self.mute_button = tk.Button(self.main_canvas, text='Mute', bg=self.color_light_grey,
            relief='groove', command=self.mute_button_func)
        self.mute_button.bind('<Enter>', lambda event, x=self.mute_button : self.button_on_hover(x))
        self.mute_button.bind('<Leave>', lambda event, x=self.mute_button : self.button_on_hover_leave(x))
        self.mute_button.place(anchor='n', relx=0.5, rely=0.94, relwidth=0.1, relheight=0.045)

        # Vertical SEPARATOR
        self.Separator1 = ttk.Separator(self.main_canvas)
        self.Separator1.place(relx=0.57, rely=0.05, relheight=0.91)
        self.Separator1.configure(orient="vertical")

        # LOGO image
        logo_image = Image.open(self.logo_image_path)
        logo_image = logo_image.resize((185, 60), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo_image)
        
        logo_image_label = tk.Label(self.main_canvas, image=logo_image, bg=self.color_light_grey)
        logo_image_label.image = logo_image
        logo_image_label.place(anchor='n', relx=0.78, rely=0.05, relwidth=0.37, relheight=0.1)

        self.build_version_label = tk.Label(self.main_canvas, text=self.build_version, bg=self.color_light_grey)
        self.build_version_label.place(anchor='n', relx=0.78, rely=0.15, relwidth=0.35, relheight=0.03)


        font_bold = tkFont.Font(family='Helvetica', size=10, weight='bold')
        # COM PORT LABEL AND MENU
        self.com_port_label = tk.Label(self.main_canvas, text="COM PORT:", font=font_bold, bg=self.color_light_grey)
        self.com_port_label.place(anchor='n', relx=0.68, rely=0.19, relwidth=0.155, relheight=0.05)
        
        self.com_port_stringvar = tk.StringVar(self.main_canvas)
        self.com_port_stringvar.set(self.serial.com_port)

        self.com_port_menu = tk.OptionMenu(self.main_canvas, self.com_port_stringvar, *self.serial.available_ports_list)
        self.com_port_menu.config(font=font_bold, bg=self.color_light_grey, relief='groove')
        self.com_port_menu.place(anchor='n', relx=0.88, rely=0.19, relwidth=0.2, relheight=0.05)
        

        # CONNECT - REFRESH PORTS BUTTON
        self.connect_button = tk.Button(self.main_canvas, text='Connect', font=font_bold, bg=self.color_black, fg='white',
            relief='groove', activebackground=self.color_light_grey, command=self.connect_button_func)
        self.connect_button.place(anchor='n', relx=0.88, rely=0.27, relwidth=0.15, relheight=0.045)

        self.refresh_com_ports_button = tk.Button(self.main_canvas, text='Refresh ports', bg=self.color_light_grey,
            relief='groove', command=self.refresh_com_ports_button_func)
        self.refresh_com_ports_button.bind('<Enter>', lambda event, x=self.refresh_com_ports_button : self.button_on_hover(x))
        self.refresh_com_ports_button.bind('<Leave>', lambda event, x=self.refresh_com_ports_button : self.button_on_hover_leave(x))
        self.refresh_com_ports_button.place(anchor='n', relx=0.68, rely=0.27, relwidth=0.15, relheight=0.045)

        # BACKUP - RESTORE BUTTONS
        self.backup_button = tk.Button(self.main_canvas, text='Backup', bg=self.color_light_grey, relief='groove', command=self.backup_button_func)
        self.backup_button.bind('<Enter>', lambda event, x=self.backup_button : self.button_on_hover(x))
        self.backup_button.bind('<Leave>', lambda event, x=self.backup_button : self.button_on_hover_leave(x))
        self.backup_button.place(anchor='n', relx=0.68, rely=0.34, relwidth=0.15, relheight=0.045)

        self.restore_button = tk.Button(self.main_canvas, text='Restore', bg=self.color_light_grey, relief='groove', command=self.restore_button_func)
        self.restore_button.bind('<Enter>', lambda event, x=self.restore_button : self.button_on_hover(x))
        self.restore_button.bind('<Leave>', lambda event, x=self.restore_button : self.button_on_hover_leave(x))
        self.restore_button.place(anchor='n', relx=0.88, rely=0.34, relwidth=0.15, relheight=0.045)

        # Horizontal SEPARATOR
        self.Separator2 = ttk.Separator(self.main_canvas)
        self.Separator2.place(relx=0.585, rely=0.4, relwidth=0.4)
        
        # Serial comms section / Receive button / 'Enter' to send
        comm_text_font = tkFont.Font(family='Helvetica', size=10)
        
        self.comm_text = tk.Text(self.main_canvas, bg=self.color_light_grey, font=comm_text_font, relief='groove')
        self.comm_text.insert('end', 'Received :\n\n')
        self.comm_text.configure(state='disabled')
        self.comm_text.place(anchor='n', relx=0.785, rely=0.415, relwidth=0.39, relheight=0.445)

        self.comm_send_text = tk.Entry(self.main_canvas, bg=self.color_light_grey, font=comm_text_font, relief='groove')
        self.comm_send_text.bind('<Return>', lambda event : self.send_serial_button_func())
        self.comm_send_text.place(anchor='n', relx=0.785, rely=0.870, relwidth=0.39, relheight=0.06)
        
        # write current firmware version ~here~
        self.firmware_version_label = tk.Label(self.main_canvas, text='--version--', font=label_font, bg=self.color_light_grey)
        self.firmware_version_label.place(anchor='n', relx=0.78, rely=0.96, relwidth=0.35, relheight=0.03)


    #--------------------------------------------------------------------------------------
    #---------------------------------- BUTTON FUNCTIONS ----------------------------------
    #--------------------------------------------------------------------------------------

    # CONNECT BUTTON FUNCTIONALITY
    def connect_button_func(self):
        if self.connect_button['text'] == 'Connect':
            self.serial.com_port = self.com_port_stringvar.get()
            self.serial.connect()
            if self.serial.connected:
                self.connect_button['text'] = 'Close'
                self.run_on_connect()
            else:
                self.throw_custom_error(title='Error', message=f'Could not connect to : COM Port {self.serial.com_port} - Baud Rate {self.serial.baud_rate}')
        else:
            self.serial.disconnect()
            if not self.serial.connected:
                self.connect_button['text'] = 'Connect'
                self.change_widget_state(state='disabled')
            else:
                self.throw_custom_error(title='Error', message=f'Error while trying to disconnect from : COM Port {self.serial.com_port}')

    # enable / disable widgets upon connecting / disconnecting
    def change_widget_state(self, state='normal'):
        for spinbox_x, spinbox_y in zip(self.tuning_values_spinbox_list_x, self.tuning_values_spinbox_list_y):
            spinbox_x.configure(state=state)
            spinbox_y.configure(state=state)

    # widget +/- functionality >>> send data through serial port
    def change_value_func(self, name, widget, axis):
        try:
            widget_value = widget.get()
            print(f'axis {axis} : {name} {widget_value}')
            # get widget text value > send it > receive value and compare
            # if equal > keep change > else > widget text value -> received value
            if self.serial.connected:
                set_axis_str = f'axis {axis}\n'
                self.serial.send_data(set_axis_str)
                axis_reply = self.serial.receive_data()
                if axis_reply != None and axis_reply != '':
                    if 'Axis' in axis_reply:
                        if axis == 'x':
                            send_str = f'{self.serial_send_names_dict_X[name]} {widget_value}\n'
                        elif axis == 'y':
                            send_str = f'{self.serial_send_names_dict_Y[name]} {widget_value}\n'
                        self.serial.send_data(send_str)
                        received_str = self.serial.receive_data()
                        if received_str != None and received_str != '':
                            print(f'Got : {received_str}')
                            received_value = float(received_str.split('=')[1].replace(' ', ''))
                            if received_value != float(widget_value):
                                widget.delete(0, 'end')
                                widget.insert('end', str(received_value))
                            self.update_comm_text([set_axis_str, axis_reply])
                            self.update_comm_text([send_str, received_str])
                    else:
                        print("error while changing the axis... function : change_value_func")
                else:
                    self.throw_no_response_error()
            else:
                self.throw_not_connected_error()
        except:
            self.throw_no_response_error()


    # USE MOUSE WHEEL TO ADJUST SPINBOX VALUES
    def mouse_wheel_spinbox(self, spinbox, event):
        if event.delta >= 120:
            spinbox.invoke('buttonup')
        elif event.delta <= -120:
            spinbox.invoke('buttondown')


    # save button functionality
    def save_button_func(self):
        try:
            if self.serial.connected:
                send = 'save\n'
                self.serial.send_data(send)
                received = self.serial.receive_data()
                if received != None and received != '':
                    self.update_comm_text([send, received])
                else:
                    self.throw_no_response_error()
            else:
                self.throw_not_connected_error()
        except:
            self.throw_no_response_error()


    # mute button functionality
    def mute_button_func(self):      # <<<<<<<<<<< FIX <<< if button is pressed and no response < button state is bugged (?) check received earlier in func
        try:
            state = self.mute_button['text']
            if self.serial.connected:
                if state == 'Mute':
                    send = 'mute\n'
                    self.serial.send_data(send)
                    received = self.serial.receive_data()
                    if 'Servo OFF' in received:
                        self.mute_button['text'] = 'Unmute'
                    else:
                        self.throw_no_response_error()
                else:
                    send = 'unmute\n'
                    self.serial.send_data(send)
                    received = self.serial.receive_data()
                    if 'Servo ON' in received:
                        self.mute_button['text'] = 'Mute'
                    else:
                        self.throw_no_response_error()
                if received != None and received != '':
                    self.update_comm_text([send, received])
                else:
                    self.throw_no_response_error()
            else:
                self.throw_not_connected_error()
        except:
            self.throw_no_response_error()

    # backup button functionality
    def backup_button_func(self):
        if self.serial.connected:
            backup_lines = []
            backup_lines.append('axis X')
            for dictionary, widget in zip(self.tuning_values_list_X, self.tuning_values_spinbox_list_x):
                line = self.serial_send_names_dict_X[dictionary['name']] + f' {widget.get()}'
                backup_lines.append(line)
            backup_lines.append('axis Y')
            for dictionary, widget in zip(self.tuning_values_list_Y, self.tuning_values_spinbox_list_y):
                line = self.serial_send_names_dict_Y[dictionary['name']] + f' {widget.get()}'
                backup_lines.append(line)
            backup_lines = '\n'.join(backup_lines)
            try:
                allowed_files = [('Text Document', '*.txt'),                        #<<<<<<<<< doesnt work
                                ('Eye magic backup', '*.eye')]
                backup_file = tk.filedialog.asksaveasfilename(filetypes=allowed_files, defaultextension=allowed_files)
                print(f'saving at : {backup_file} ...')
                with open(backup_file, 'w') as f:
                    f.write(backup_lines)
            except Exception as e:
                print(f'error in backup_button_func : {e}')
        else:
            self.throw_not_connected_error()
        

    # restore button functionality
    def restore_button_func(self):
        if self.serial.connected:
            try:
                restore_filename = tk.filedialog.askopenfilename()
                with open(restore_filename, 'r') as f:
                    lines = f.readlines()
                lines = [line.replace('\n', '') for line in lines]
                xaxisindex = lines.index('axis X')
                yaxisindex = lines.index('axis Y')
                xlines = lines[xaxisindex+1:yaxisindex]
                xlines = [line for line in xlines if line != '']
                ylines = lines[yaxisindex+1:]
                ylines = [line for line in ylines if line != '']
                for line, widget in zip(xlines, self.tuning_values_spinbox_list_x):
                    widget.delete(0, 'end')
                    widget.insert('end', str(line.split(' ')[1]))
                for line, widget in zip(ylines, self.tuning_values_spinbox_list_y):
                    widget.delete(0, 'end')
                    widget.insert('end', str(line.split(' ')[1]))
                self.serial.send_data('axis x\n')
                _ = self.serial.receive_data()
                for line in xlines:
                    self.serial.send_data(f'{line}\n')
                    _ = self.serial.receive_data()
                self.serial.send_data('axis y\n')
                _ = self.serial.receive_data()
                for line in ylines:
                    self.serial.send_data(f'{line}\n')
                    _ = self.serial.receive_data()
            except Exception as e:
                print(f'error in restore_button_func : {e}')
                self.throw_custom_error(title='Error', message='Something went wrong while loading the restore file.')
        else:
            self.throw_not_connected_error()


    # refresh com ports button functionality
    def refresh_com_ports_button_func(self):
        available_ports = self.serial.refresh_ports()
        menu = self.com_port_menu.children['menu']
        menu.delete(0, 'end')
        for port in available_ports:
            menu.add_command(label=port, command=lambda p=port : self.com_port_stringvar.set(p))
        if not self.serial.connected:
            self.com_port_stringvar.set(available_ports[0])
        

    # run on enter press and widget focus
    def send_serial_button_func(self):
        try:
            if self.serial.connected:
                data = self.comm_send_text.get() + '\n'
                self.serial.send_data(data)
                received_line = self.serial.receive_data()
                if received_line != None and received_line != '':
                    sent_received_list = [data, received_line]
                    self.update_comm_text(sent_received_list)
                else:
                    self.throw_no_response_error()
            else:
                self.throw_not_connected_error()
        except:
            self.throw_no_response_error()

    # update comm_text messages
    def update_comm_text(self, text):
        write = f'>>> {text[0]}{text[1]}\n' 
        self.msg_list = self.msg_list[:-1]
        self.msg_list.insert(0, write)
        write = ''.join(self.msg_list)
        write += '\n-----end of 10-message history----'
        self.comm_text.configure(state='normal')
        self.comm_text.delete('1.0', 'end')
        self.comm_text.insert('end', write)
        self.comm_text.configure(state='disabled')

    # highlight buttons / widgets on mouse hover
    def button_on_hover(self, button, highlight_color=button_highlight_color):
        button.configure(bg=highlight_color)

    # de-highlight buttons / widgets on mouse leave
    def button_on_hover_leave(self, button, init_color=color_light_grey):
        button.configure(bg=init_color)

    #--------------------------------------------------------------------------------------
    #---------------------------------- BUTTON FUNCTIONS ----------------------------------
    #--------------------------------------------------------------------------------------

    # to-do list when connecting to a serial port
    def run_on_connect(self):
        # make spinboxes active upon connection
        self.change_widget_state()
        # get firmware version to display
        self.update_firmware_version_label()
        # get parx / pary dump to display loaded values on the spinboxes
        self.get_dump()

    # receive parx / pary dump on connect
    def get_dump(self):
        try:
            self.serial.send_data('parx\n')
            par_x = self.serial.receive_data()
            if par_x != None and par_x != '':
                par_x = par_x.split(',')[1:]
                for val, widget in zip(par_x, self.tuning_values_spinbox_list_x):
                    val = val.replace(' ', '')
                    widget.delete(0, 'end')
                    widget.insert('end', str(val))
                    
                self.serial.send_data('pary\n')
                par_y = self.serial.receive_data()
                if par_y != None and par_y != '':
                    par_y = par_y.split(',')[1:]
                    for val, widget in zip(par_y, self.tuning_values_spinbox_list_y):
                        widget.delete(0, 'end')
                        widget.insert('end', str(val))
                else:
                    self.throw_no_response_error()
            else:
                self.throw_no_response_error()        
        except Exception as e:
            print(e)
            self.throw_custom_error(title='Error', message='Something went wrong while loading the dump values.')


    # update label text with the firmware version on connect
    def update_firmware_version_label(self):
        try:
            version_command = 'vers\n'
            version = 'version: '
            version += self.serial.ask_for_version(version_command)
            print(f'got version : {version}')
            self.firmware_version_label['text'] = version
        except:
            self.throw_custom_error(title='Error', message='Something went wrong while loading the device version.')

    
    #--------------------------------------------------------------------------------------
    #------------------------------ ERROR / WARNING MESSAGES ------------------------------
    #--------------------------------------------------------------------------------------
    def throw_not_connected_error(self):
        tk.messagebox.showwarning(title='Error', message='You are not currently connected to a COM port.')


    def throw_no_response_error(self):
        tk.messagebox.showwarning(title='Error', message='Did not receive response ... check your connection.')

    
    def throw_custom_error(self, title, message):
        tk.messagebox.showwarning(title=title, message=message)
    
    #--------------------------------------------------------------------------------------
    #------------------------------ ERROR / WARNING MESSAGES ------------------------------
    #--------------------------------------------------------------------------------------


    # run when exiting the program
    def exit(self):
        if self.serial.connected:
            self.serial.disconnect()
        try:
            com, baud = self.com_port_stringvar.get(), 9600
            self.serial.create_save(com, baud)
        except Exception as e:
            print(f'Error saving to config : {e}')
        self.quit()
        self.destroy()




if __name__=='__main__':
    app = EyeMagicApp()
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", app.exit)
    app.mainloop()