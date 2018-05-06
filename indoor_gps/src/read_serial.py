# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/tommy/.spyder2/.temp.py
"""

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
        
    
        