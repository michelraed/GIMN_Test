# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 02:02:27 2021

@author: Michel Raed
"""
import uproot3
from GIMNTools import Utils, Read
import sys
from time import time



File = Utils.OpenFileDialog()
File=File[0]
    
if sys.platform == 'win32':
    File=File.replace("/","\\")

t1=time()
objeto = uproot3.open(File)
print(objeto.items())
singles = objeto['Singles'].pandas.df().to_records()
t2=time()

print(t2-t1)