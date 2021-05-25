#                        GENERIC PYTHON SERIAL COMMUNICATIONS MODULE
import serial
import time


class serial_comms_module():
#---------------------------------GENERIC VARIABLES----------------------------------

    last_save = 'files\\last_save.txt'

#---------------------------------GENERIC VARIABLES----------------------------------

#----------------------------------- __INIT__ ----------------------------------------
    def __init__(self, timeout):
        self.timeout = timeout
        self.connected = False
        self.com_port = '---'
        self.baud_rate = 9600
        
        self.available_ports_list = []
        self.available_ports_list = self.refresh_ports()

        saved_com_port = self.read_last_save()

        if saved_com_port in self.available_ports_list:
            self.com_port = saved_com_port
        else:
            self.com_port = self.available_ports_list[-1]

#----------------------------------- __INIT__ ----------------------------------------


#---------------------------------REFRESH AVAILABLE PORTS------------------------------
    def refresh_ports(self):
        self.available_ports_list.clear()
        for i in range(1, 40):
            com_str = 'COM'+str(i)
            if com_str == self.com_port and self.connected:
                self.available_ports_list.append('COM' + str(i))
            else:
                try:
                    s = serial.Serial(com_str)
                    self.available_ports_list.append('COM'+str(i))
                    s.close()
                except:
                    pass
        if len(self.available_ports_list) == 0:
            self.available_ports_list.append('---')
        print("available ports:", self.available_ports_list)
        return self.available_ports_list

#---------------------------------REFRESH AVAILABLE PORTS------------------------------

#----------------------READ/WRITE TO last_save FILE FOR DEFAULTS--------------------------
    # handle reading / saving COM port last used
    def read_last_save(self):
        try:
            with open(self.last_save, 'r') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                for line in lines:
                    if 'DEFAULT_COM_PORT' in line:
                        saved_com_port = line.split('=')[1].strip()
                        return saved_com_port
        except Exception as e:
            print(f'Error trying to read last_save file : {e}')
                

    def create_save(self, com_port, baud_rate):
        try:
            with open(self.last_save, 'w') as file:
                file.write(f'DEFAULT_COM_PORT={com_port}\nDEFAULT_BAUD_RATE={baud_rate}')
        except Exception as e:
            print(f'error trying to save to last_save : {e}')
                
    
#----------------------READ/WRITE TO last_save FILE FOR DEFAULTS--------------------------



#---------------------------------CONNECT / DISCONNECT---------------------------------

    def connect(self):
        if not self.connected:
            try:
                self.serial = serial.Serial(self.com_port, self.baud_rate, timeout=self.timeout)
                self.connected = True
                print(f'Connected successfully to {self.com_port} !')
            except Exception as e:
                self.connected = False
                print(f'Error while trying to connect to {self.com_port}')
                print(f'error : {e}')
        else:
            print('You are already connected!')



    def disconnect(self):
        if self.connected:
            try:
                self.serial.close()
                self.connected = False
                print(f'Disconnected successfully from {self.com_port} !')
            except Exception as e:
                print(f'Error while trying to disconnect from {self.com_port}')
        else:
            print('You are not currently connected to any com port')

#---------------------------------CONNECT / DISCONNECT---------------------------------



#---------------------------------SEND / RECEIVE DATA-----------------------------------

    def send_data(self, data):
        if self.connected:
            try:
                self.serial.write(data.encode())
                print(f'Sending data : {data}')
            except Exception as e:
                print(f'error while sending data : {e}')
        else:
            print(f'You are not currently connected to any com port to send data')


    def receive_data(self):
        if self.connected:
            try:
                line = self.serial.readline().decode()
                return line
            except Exception as e:
                print(f'Error while trying to receive data : {e}')
                return None
        else:
            print('You are not currently connected to a com port to receive data')      


    # ask for current firmware version
    def ask_for_version(self, cmd):
        if self.connected:
            self.send_data(cmd)
            version = self.receive_data().replace('\n', '')
            print(f'VERSION : {version}')
            return version
        else:
            print('You are not currently connected to a COM port to receive data')

#---------------------------------SEND / RECEIVE DATA-----------------------------------


