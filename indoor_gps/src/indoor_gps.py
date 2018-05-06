
import serial
import crcmod
#import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

class read_serial:
    data_type = '0x11' # identify data type
    iteration = 0
    max_iter = 27 
    store = []
    max_dic = {'0x11':27} # look up max length
    def __init__(self,data_type):
        self.data_type = data_type
        self.iteration = 0
        self.max_iter = self.max_dic[data_type]
        self.store = []
        
        self.crc_16 = crcmod.predefined.mkPredefinedCrcFun('modbus')
    def read(self,input_data):
        
        if (self.iteration <= self.max_iter + 1):
            if ( self.exam(input_data) == False ):
                self.iteration = 0
                self.store = []
                return False,[]
            self.iteration += 1
            self.store.append(input_data)
            return False, []
        else:
            correct = self.crc_check()
            self.iteration = 0
            res = self.store
            self.store = []
            if (correct):
                return True, res
            else:
                return False,[]
            
    def exam(self,input_data):
        iteration = self.iteration
        if (iteration == 0):
            if (input_data != '0xff'): # head
                return False
            else:
                return True
        elif(iteration == 1):
            if (input_data != '0x47'): # head2
                return False
            else:
                return True
        elif(iteration == 2):
            if (input_data != self.data_type): # data_type
                return False
            else:
                return True
                
    
    def crc_check(self):
        crc16 = self.crc_16
        values = self.store
        if (len(values)):
            string = "".join(i[-2:] for i in values[0:-2])
            caled = hex(crc16(string.decode("hex")))
            last,first = "0x"+ caled[2:4],"0x"+ caled[4:6]
            #print(last,first)
            if (last == values[-1] and first == values[-2]):
                return True
            else:
                return False
        else:
            return False

        
if __name__ == "__main__":
    
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    out_put = read_serial('0x11')
    count = 0
       
    while True:
        count  += 1
        byte = ser.read()
        byte_hex = byte.encode("hex")
        byte_hex = "0x"+byte_hex
        #   print(byte_hex)
        if (byte):
            flag,res = out_put.read(byte_hex)
            if (flag): # if success
                #print(res)
                hex_x = "".join(i[-2:] for i in res[9:13])
                hex_y = "".join(i[-2:] for i in res[13:17])
                hex_z = "".join(i[-2:] for i in res[17:21])
                int_x = int("0x" + hex_x, 0)
                int_y = int("0x" + hex_y, 0)
                int_z = int("0x" + hex_z, 0)
                print(int_x,int_y,int_z)
               
        else:
            continue
    ser.close()
        
            
