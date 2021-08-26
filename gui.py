#!/usr/bin/env python
#!/usr/bin/python3

# bouroo<bouroo@gmail.com>
# 07.04.2019
# sudo apt-get -y install pcscd python-pyscard python-pil

import serial
import time

import binascii
import io
import os
import sys
from PIL import Image
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes
import numpy as np

import subprocess
import pdfkit
import mysql.connector
import datetime
import netifaces as ni

def getIPAddress():
    try:    
        ni.ifaddresses('eth0')
        ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        return ip
    except:
        try:
            ni.ifaddresses('wlan0')
            ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
            return ip
        except:
            ip = "INTERNET NOT CONNECTED"
            return ip
    
    

print(getIPAddress())
from math import *
import math
from tkinter import *

window = Tk()

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

window.overrideredirect(True)
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

frame_home = Frame(window)
frame_insertcard_th = Frame(window)
frame_insertcard_en = Frame(window)
frame_check_th = Frame(window)
frame_start_th = Frame(window)
frame_step1_th = Frame(window)
frame_step2_th = Frame(window)
frame_step3_th = Frame(window)
frame_step4_th = Frame(window)
frame_result_th = Frame(window)
frame_last_th = Frame(window)
frame_loading_th = Frame(window)
frame_showipaddress = Frame(window)

for frame in (frame_home, frame_insertcard_th, frame_insertcard_en, frame_check_th, frame_start_th, frame_step1_th, frame_step2_th, frame_step3_th, frame_step4_th, frame_result_th, frame_last_th, frame_loading_th, frame_showipaddress):
    frame.grid(row=0, column=0, sticky='nsew')

status_waiting_card = False
status_read_card = False

# Variable
cid = ""
name_th = ""
name_en = ""
datestr = ""
gender = ""
address=""


def thai2unicode(data):
    result = ''
    result = bytes(data).decode('tis-620')
    return result.strip()


def getData(cmd, req=[0x00, 0xc0, 0x00, 0x00]):
    data, sw1, sw2 = connection.transmit(cmd)
    data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
    return [data, sw1, sw2]


# Check card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]

# CID
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]

# TH Fullname
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]

# EN Fullname
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]

# Date of birth
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]

# Gender
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]

# Card Issuer
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]

# Issue Date
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]

# Expire Date
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]

# Address
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]

lang = 0

def show_frame(frame):
    frame.tkraise()


def insertcard_en():
    global lang
    global cid
    global name_th
    global name_en
    global datestr
    global gender
    global address
    lang = 0
    show_frame(frame_insertcard_en)
    window.update_idletasks()
    window.update()
    global status_waiting_card
    status_waiting_card = True
    print("status_waiting_card = ")
    print(status_waiting_card)
    global connection
    while status_waiting_card == True:
        try:
            readerList = readers()
            reader = readerList[0]
            print("Using:"), reader

            connection = reader.createConnection()
            connection.connect()
            status_waiting_card = False
        except:
            print("Not Card !!!!!")
    print("exit")

    show_frame(frame_check_th)
    atr = connection.getATR()
    print("ATR: " + toHexString(atr))
    if (atr[0] == 0x3B & atr[1] == 0x67):
        req = [0x00, 0xc0, 0x00, 0x01]
    else:
        req = [0x00, 0xc0, 0x00, 0x00]

        # Check card
    data_1, sw1_1, sw2_1 = connection.transmit(SELECT + THAI_CARD)
    print("Select Applet: %02X %02X" % (sw1_1, sw2_1))
    print("data ==========")
    print(data_1)
        # CID
    data_2 = getData(CMD_CID, req)
    cid = thai2unicode(data_2[0])
    print("CID: " + cid)
    
    # TH Fullname
    data = getData(CMD_THFULLNAME, req)
    name_th = thai2unicode(data[0]).replace("#"," ").replace("  "," ")
    print ("TH Fullname: " + name_th)

    # EN Fullname
    data = getData(CMD_ENFULLNAME, req)
    name_en = thai2unicode(data[0]).replace("#"," ").replace("  "," ")
    print ("EN Fullname: " + name_en)

    # Date of birth
    data = getData(CMD_BIRTH, req)
    datestr = thai2unicode(data[0])
    print ("Date of birth: " + datestr)

    # Gender
    data = getData(CMD_GENDER, req)
    gender = thai2unicode(data[0])
    print ("Gender: " + gender)

    # Address
    data = getData(CMD_ADDRESS, req)
    address = thai2unicode(data[0]).replace("#"," ").replace("    "," ")
    print ("Address: " + address)
    
    my_canvas.itemconfigure(3,text="ID Card : " + cid)
    my_canvas.itemconfigure(4,text="Name : " + name_en)
    my_canvas.itemconfigure(5,text="Birthday : " + datestr)
    my_canvas.itemconfigure(6,text="Address: " + address)
    if gender == '1':
        my_canvas.itemconfigure(7,text="Gender : Male")
    else:
        my_canvas.itemconfigure(7,text="Gender : Femail")
        
    my_canvas.itemconfigure(2,text="Check Information")
    btEN_check.configure(image=confirm_Eng2)
    btTH_check.configure(image=cancel_Eng2)
    
    window.update_idletasks()
    window.update()
    
    # DATABASE DATA USER
    global user_cardid
    global user_firstname_th
    global user_lastname_th
    global user_firstname_en
    global user_lastname_en
    global user_birth
    global user_gender
    global user_address
    global user_address_subdistrict
    global user_address_district
    global user_address_province
    global user_address_zipcode
    
    user_cardid = cid
    user_firstname_th = name_th.split(' ')[1]
    user_lastname_th = name_th.split(' ')[2]
    user_firstname_en = name_en.split(' ')[1]
    user_lastname_en = name_en.split(' ')[2]
    user_birth = datestr
    user_gender = gender
    """user_address = address.split(' ')[0] + ' ' + address.split(' ')[1] + ' ' + address.split(' ')[2]
    user_address_subdistrict = address.split(' ')[3]
    user_address_district = address.split(' ')[4]
    user_address_province = address.split(' ')[5]
    """
    
    user_address = address[0:address.index("ตำบล")-1]
    user_address_subdistrict = address[address.index("ตำบล")+4:address.index(" ",address.index("ตำบล"))]
    user_address_district = address[address.index("อำเภอ")+5:address.index(" ",address.index("อำเภอ"))]
    user_address_province = address[address.index("จังหวัด")+7:len(address)]
    
    
    67
    x = datetime.datetime.now()

    global year
    global month
    global day
    global hr
    global mn
    global sec
    
    year = int(x.strftime("%Y"))
    month = int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    hr = int(x.strftime("%H"))
    mn = int(x.strftime("%M"))
    sec = int(x.strftime("%S"))

    timestamp = str(year) + "-" + str(month) + "-" + str(day) + "_" + str(hr) + ":" + str(mn) + ":" + str(sec)
        
    #DATABASE DATA RESULT
    global result_cardid
    global result_datetime
    
    result_cardid = cid
    result_datetime = timestamp
    
    
    print('user_cardid = ' , user_cardid)
    print('user_firstname_th = ' , user_firstname_th)
    print('user_lastname_th = ' , user_lastname_th)
    print('user_firstname_en = ' , user_firstname_en)
    print('user_lastname_en = ' , user_lastname_en)
    print('user_birth = ' , user_birth)
    print('user_gender = ' , user_gender)
    #print('user_address = ' , user_address)
    print('user_address = ' , user_address)
    
    print('user_address_subdistrict = ' , user_address_subdistrict)
    print('user_address_district = ' , user_address_district)
    print('user_address_province = ' , user_address_province)
    
        

def insertcard():
    global lang
    global cid
    global name_th
    global name_en
    global datestr
    global gender
    global address
    
    lang = 1
    show_frame(frame_insertcard_th)
    window.update_idletasks()
    window.update()
    global status_waiting_card
    status_waiting_card = True
    print("status_waiting_card = ")
    print(status_waiting_card)
    global connection
    while status_waiting_card == True:
        try:
            readerList = readers()
            reader = readerList[0]
            print("Using:"), reader

            connection = reader.createConnection()
            connection.connect()
            status_waiting_card = False
        except:
            print("Not Card !!!!!")
    print("exit")

    show_frame(frame_check_th)
    atr = connection.getATR()
    print("ATR: " + toHexString(atr))
    if (atr[0] == 0x3B & atr[1] == 0x67):
        req = [0x00, 0xc0, 0x00, 0x01]
    else:
        req = [0x00, 0xc0, 0x00, 0x00]

        # Check card
    data_1, sw1_1, sw2_1 = connection.transmit(SELECT + THAI_CARD)
    print("Select Applet: %02X %02X" % (sw1_1, sw2_1))
    print("data ==========")
    print(data_1)
        # CID
    data_2 = getData(CMD_CID, req)
    cid = thai2unicode(data_2[0])
    print("CID: " + cid)
    
    # TH Fullname
    data = getData(CMD_THFULLNAME, req)
    name_th = thai2unicode(data[0]).replace("#"," ").replace("  "," ")
    print ("TH Fullname: " + name_th)

    # EN Fullname
    data = getData(CMD_ENFULLNAME, req)
    name_en = thai2unicode(data[0]).replace("#"," ").replace("  "," ")
    print ("EN Fullname: " + name_en)

    # Date of birth
    data = getData(CMD_BIRTH, req)
    datestr = thai2unicode(data[0])
    print ("Date of birth: " + datestr)

    # Gender
    data = getData(CMD_GENDER, req)
    gender = thai2unicode(data[0])
    print ("Gender: " + gender)

    # Address
    data = getData(CMD_ADDRESS, req)
    address = thai2unicode(data[0]).replace("#"," ").replace("    "," ")
    print ("Address: " + address)
    my_canvas.itemconfigure(3,text="เลขประจำตัวประชาชน : " + cid)
    my_canvas.itemconfigure(4,text="ชื่อ-สกุล  : " + name_th)
    my_canvas.itemconfigure(5,text="ปี/เดือน/วัน เกิด : " + datestr)
    my_canvas.itemconfigure(6,text="ที่อยู่ : " + address)
    if gender == '1':
        my_canvas.itemconfigure(7,text="เพศ : ชาย")
    else:
        my_canvas.itemconfigure(7,text="เพศ : หญิง")
    
    
    my_canvas.itemconfigure(2,text="ตรวจสอบข้อมูล และ กดยืนยัน")
    btEN_check.configure(image=photoimage_ENG2)
    btTH_check.configure(image=photoimage_TH2)
    
    window.update_idletasks()
    window.update()
    
        
    # DATABASE DATA USER
    global user_cardid
    global user_firstname_th
    global user_lastname_th
    global user_firstname_en
    global user_lastname_en
    global user_birth
    global user_gender
    global user_address
    global user_address_subdistrict
    global user_address_district
    global user_address_province
    global user_address_zipcode
    
    user_cardid = cid
    user_firstname_th = name_th.split(' ')[1]
    user_lastname_th = name_th.split(' ')[2]
    user_firstname_en = name_en.split(' ')[1]
    user_lastname_en = name_en.split(' ')[2]
    user_birth = datestr
    user_gender = gender
    """user_address = address.split(' ')[0] + ' ' + address.split(' ')[1] + ' ' + address.split(' ')[2]
    user_address_subdistrict = address.split(' ')[3]
    user_address_district = address.split(' ')[4]
    user_address_province = address.split(' ')[5]
    """
    
    user_address = address[0:address.index("ตำบล")-1]
    user_address_subdistrict = address[address.index("ตำบล")+4:address.index(" ",address.index("ตำบล"))]
    user_address_district = address[address.index("อำเภอ")+5:address.index(" ",address.index("อำเภอ"))]
    user_address_province = address[address.index("จังหวัด")+7:len(address)]
    
    x = datetime.datetime.now()

    global year
    global month
    global day
    global hr
    global mn
    global sec
    
    year = int(x.strftime("%Y"))
    month = int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    hr = int(x.strftime("%H"))
    mn = int(x.strftime("%M"))
    sec = int(x.strftime("%S"))

    timestamp = str(year) + "-" + str(month) + "-" + str(day) + "_" + str(hr) + ":" + str(mn) + ":" + str(sec)
        
    #DATABASE DATA RESULT
    global result_cardid
    global result_datetime
    
    result_cardid = cid
    result_datetime = timestamp
    
    
    print('user_cardid = ' , user_cardid)
    print('user_firstname_th = ' , user_firstname_th)
    print('user_lastname_th = ' , user_lastname_th)
    print('user_firstname_en = ' , user_firstname_en)
    print('user_lastname_en = ' , user_lastname_en)
    print('user_birth = ' , user_birth)
    print('user_gender = ' , user_gender)
    #print('user_address = ' , user_address)
    print('user_address = ' , user_address)
    
    print('user_address_subdistrict = ' , user_address_subdistrict)
    print('user_address_district = ' , user_address_district)
    print('user_address_province = ' , user_address_province)
    
    

def step1():
    global lang
    print("lang = ")
    print(lang)
    global weight
    global height
    
    global temp
    global pluse
    
    print("lang = ")
    print(lang)
    if (lang == 1):
        print("if")
        my_canvas_loading.itemconfigure(2,text="กรุณารอสักครู่")
        show_frame(frame_loading_th)
        window.update_idletasks()
        window.update()
    elif (lang == 0):
        print("else")
        my_canvas_loading.itemconfigure(2,text="Please Wait")
        show_frame(frame_loading_th)
        window.update_idletasks()
        window.update()
    
    show_frame(frame_loading_th)
    window.update_idletasks()
    window.update()
    ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
    ser.flush()
    ser.write(b'')
    time.sleep(2)
    ser.readline().decode('utf-8').rstrip()
    #show_frame(frame_step1_th)
    #window.update_idletasks()
    #window.update()
        #data = input()
            #print(data + '\r\n')
        #data1 = data + "\r\n"
        #ser.write(data1.encode())
    ser.flush()
    ser.write(b'1\r\n')
    while True:
        print("!4")
        line = ser.readline().decode('utf-8').rstrip()
        if bool(line) == True:
            weight = line.split(" ")[3]
            print("DATA1 : " + weight)
            break
    ser.write(b'2\r\n')
    while True:
        print("!4")
        line = ser.readline().decode('utf-8').rstrip()
        if bool(line) == True:
            height = line.split(" ")[3]
            height = str(int(height) - 11)
            print("DATA2 : " + height)
            break
    if (lang == 1):
        my_canvas_step2_th.itemconfigure(2,text="กรุณายกมือไปใกล้เพื่อวัดอุณหภูมิ")
    else:
        my_canvas_step2_th.itemconfigure(2,text="Please raise your hand to \n Measure the Temperature")
    show_frame(frame_step2_th)
    window.update_idletasks()
    window.update()
    ser.write(b'3\r\n')
    while True:
        print("!4")
        line = ser.readline().decode('utf-8').rstrip()
        if bool(line) == True:
            temp = str(float(line.split(" ")[3])+3.5).zfill(2)
            print("DATA3 : " + temp)
            break
    #show_frame(frame_step3_th)
    #window.update_idletasks()
    #window.update()
    #ser.write(b'4\r\n')
    #while True:
    #    print("!4")
    #    line = ser.readline().decode('utf-8').rstrip()
    #    if bool(line) == True:
     #       pluse = line.split(" ")[3]
     #       print("DATA4 : " + pluse)
     #       break
    if (lang == 1):
        my_canvas_step4_th.itemconfigure(2,text="กรุณานำแขนใส่เข้าไปในเครื่องวัดความดัน")
        bt_step4_th.configure(image=photoimage_step4_th)
    else:
        my_canvas_step4_th.itemconfigure(2,text="Please put your arm\n  On the pressure")
        bt_step4_th.configure(image=confirm_Eng2)
    
    show_frame(frame_step4_th)
    
    ser.close()
    
    global result_height
    global result_weight
    global result_temp
    global result_pulse
    
    result_weight = weight
    result_height = height
    result_temp = temp
    #result_pulse = pluse
    
def step4():
    global weight
    global height
    
    global temp
    global pluse
    global aaa
    
    global result_systolic
    global result_diastolic
    


    show_frame(frame_loading_th)
    window.update_idletasks()
    window.update()
    ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
    ser.flush()
    ser.write(b'')
    time.sleep(2)
    ser.readline().decode('utf-8').rstrip()
    ser.flush()
    ser.write(b'5\r\n')
    while True:
        print("!4")
        line = ser.readline().decode('utf-8').rstrip()
        if bool(line) == True:
            aaa = line.split(" ")[3]
            result_systolic = aaa.split(',')[0]
            result_diastolic = aaa.split(',')[1]
            pluse = aaa.split(',')[2]
            print("DATA1 : " + weight)
            print("DATA2 : " + height)
            print("DATA3 : " + temp)
            print("DATA4 : " + pluse)
            
            print("DATA5 : " + result_systolic + "," + result_diastolic)
            
            if (lang == 1):
                my_canvas_result_th.itemconfigure(2,text="ผลการตรวจสุขภาพ")
                my_canvas_result_th.itemconfigure(3,text="น้ำหนัก : " + weight)
                my_canvas_result_th.itemconfigure(4,text="ส่วนสูง : " + height)
                my_canvas_result_th.itemconfigure(5,text="อุณหภูมื : " + temp)
                my_canvas_result_th.itemconfigure(6,text="ชีพจร : " + pluse)
                my_canvas_result_th.itemconfigure(7,text="ความดันโลหิต : " + result_systolic + "," + result_diastolic)
                bten_result_th.configure(image=photoimage_result_th1) # ยืนยัน
                btth_result_th.configure(image=photoimage_result_th) # ยกเลิก
                show_frame(frame_result_th)
                break
            elif (lang == 0):
                my_canvas_result_th.itemconfigure(2,text="Health Check Results")
                my_canvas_result_th.itemconfigure(3,text="Weight : " + weight)
                my_canvas_result_th.itemconfigure(4,text="Height : " + height)
                my_canvas_result_th.itemconfigure(5,text="Temp : " + temp)
                my_canvas_result_th.itemconfigure(6,text="Pluse : " + pluse)
                my_canvas_result_th.itemconfigure(7,text="Blood Pressure : " + result_systolic + "," + result_diastolic)
                bten_result_th.configure(image=confirm_Eng2) # ยืนยัน
                btth_result_th.configure(image=cancel_Eng2) # ยกเลิก
                show_frame(frame_result_th)
                break               

    
    ser.close()
    

'''def step2():
    global temp
    
    ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
    ser.flush()
    ser.write(b'')
    time.sleep(2)
    ser.readline().decode('utf-8').rstrip()
    ser.flush()
    ser.write(b'1\r\n')
    while True:
        print("!3")
        line = ser.readline().decode('utf-8').rstrip()
        if bool(line) == True:
            weight = line.split(" ")[3]
            print("DATA1 : " + temp)
            break
    
    ser.close()
    #show_frame(frame_step3_th)'''
   
   
def printresult():
    if (lang == 1):
        my_canvas33.itemconfigure(2,text="กรุณาถอดบัตรประชาชน และรับใบสลิป")
    elif (lang == 0):
        my_canvas33.itemconfigure(2,text="Please remove your ID CARD\n    and receive a Slip")
    show_frame(frame_last_th)
    window.update_idletasks()
    window.update()
    
    global cid
    global name_th
    global name_en
    global datestr
    global gender
    global address
    
    global weight
    global height
    
    global temp
    global pluse
    global aaa
    
    # DATABASE DATA USER
    global user_cardid
    global user_firstname_th
    global user_lastname_th
    global user_firstname_en
    global user_lastname_en
    global user_birth
    global user_gender
    global user_address
    global user_address_subdistrict
    global user_address_district
    global user_address_province
    global user_address_zipcode
    
    # DATABASE DATA RESULT
    global result_height
    global result_weight
    global result_temp
    global result_pulse
    global result_systolic
    global result_diastolic
    global result_cardid
    global result_datetime
    
    global bmi
    bmi = float(float(result_weight) / pow(float(result_height) / 100.0,2.0))


    global year
    global month
    global day
    global hr
    global mn
    global sec
    
    datecheckstr = str(day) + "/" + str(month) + "/" + str(year)
    timestr = str(hr) + ":" + str(mn) + ":" + str(sec)
    f = open("slip.html", "w")
    f.write("<html>")
    f.write("<head>")
    f.write("<style>p {  font-size:13px;} *{margin-left:0px;}</style>")
    f.write("</head>")
    f.write("<body>")
    f.write("<meta charset=\"UTF-8\"/>")
    f.write("<img  src = \"/home/pi/Desktop/GUI/logo.jpg\" height=\"120\" width=\"140\">")
    f.write("<p><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Project</b> </p>")
    f.write("<p><b>Five in one health check <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;machine</b> </p>")
    f.write("<p>******************************</p>")
    f.write("<p>เลขประจำตัวประชาชน :" +cid+"</p>")
    f.write(" <p>ฃื่อ : "+user_firstname_th+"</p>")
    f.write("<p>นามสกุล : "+user_lastname_th+"</p>")
    f.write("<p>ที่อยู่ : "+user_address + " " + user_address_subdistrict+"</p>")
    f.write("<p>"+user_address_district + " " + user_address_province+"</p>")

    '''
    global user_address
    global user_address_subdistrict
    global user_address_district
    global user_address_province'''
    f.write("<p>วันเดือนปีเกิด : "+datestr+"</p>")
    f.write("<p>ส่วนสูง : "+height+"</p>")
    f.write("<p>น้ำหนัก : "+weight+"</p>")

    formatbmi = "{data:.2f}"
    f.write("<p>BMI : "+ formatbmi.format(data=float(bmi))+"<p>")
    f.write("<p>อุณหภูมิ : "+str(temp)+"</p>")
    f.write("<p>ชีพจร : "+str(pluse)+"</p>")

    f.write("<P>ความดันโลหิต : " + result_systolic + "/" + result_diastolic+"</P>")
    f.write("<p>****************************</p>")
    f.write("<p>วันที่ตรวจ : " + datecheckstr + "</p>")
    f.write("<p>เวลาตรวจ : " + timestr + "</p>")
    f.write("<p>สรุปผล BMI : ปกติ</p>")

    if int(pluse) >= 50 and int(pluse) <= 100:
        f.write("<p>สรุปผลชีพจร : ปกติ</p>")
    elif int(pluse) >= 101:
        f.write("<p>สรุปผลชีพจร : เต้นเร็วกว่าปกติ</p>")
    elif int(pluse) <= 49:
        f.write("<p>สรุปผลชีพจร : เต้นช้ากว่าปกติ</p>")

    f.write("<p>สรุปผลความดันโลหิต : ปกติ</p>")
    f.write("<p>สรุปอุณหภูมิร่างกาย : ปกติ</p>")
    f.write("</body>")
    f.write("</html>")
    f.close()
    pdfkit.from_file("slip.html", "out.pdf")

    os.system("lp out.pdf")


    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="12345678",
      database="health_check_db"
    )

    mycursor = mydb.cursor()

    """query1 = "INSERT INTO user_tb(user_cardid, user_firstname_th, user_lastname_th, user_firstname_en, \
      user_lastname_en, user_birth, user_gender, user_address, user_address_subdistrict, user_address_district, \
      user_address_province) \
      VALUES ('"+ user_cardid + "','"+user_firstname_th+"','"+user_lastname_th+"','"+user_firstname_en+"',\
      '"+user_lastname_en+"','"+user_birth+"',"+user_gender+",'"+user_address+"','"+user_address_subdistrict+"\
      ','"+user_address_district+"','"+user_address_province+"')\
      ON DUPLICATE KEY UPDATE user_cardid = '"+user_cardid+"';"""
    
    query1 = "INSERT INTO user_tb(user_cardid, user_firstname_th, user_lastname_th,"
    query1 = query1 +"user_firstname_en, user_lastname_en, user_birth, user_gender, user_address, user_address_subdistrict, user_address_district,user_address_province) "
    query1 = query1 + " VALUES ('"+ user_cardid + "','"+user_firstname_th+"','"+user_lastname_th+"','"+user_firstname_en + "','"
    query1 = query1 + user_lastname_en+"','"+user_birth+"',"+user_gender+",'"+user_address+"','"+user_address_subdistrict + "','"
    query1 = query1 + user_address_district+"','"+user_address_province+"')"+" ON DUPLICATE KEY UPDATE user_cardid = '" + user_cardid+"';"

    print("query1 = ")
    print(query1)
    query2 = "INSERT INTO result_db(result_cardid, result_systolic, result_diastolic, result_height, \
      result_weight, result_temp, result_pulse) VALUES ('"+result_cardid+"',"+result_systolic+","+result_diastolic+","+result_height+","+result_weight+","+result_temp+","+pluse+");"
    
    mycursor.execute(query1)
    mydb.commit()
    mycursor.execute(query2)
    mydb.commit()
    
    show_frame(frame_home)
    window.update_idletasks()
    window.update()
    

chooselanTH = "กรุณาเลือกภาษา"
chooselanEN = "Choose your language"
# ==================Frame 1 code
bg = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/bg/bg.png")


my_canvas = Canvas(frame_home, width=750, height=450)
my_canvas.pack(fill="both", expand=True)

my_canvas.create_image(0, 0, image=bg, anchor="nw")
my_canvas.create_text(370, 90, text=chooselanTH, font=("Helvetica", 35), fill="brown")
my_canvas.create_text(370, 135, text=chooselanEN, font=("Helvetica", 35), fill="brown")
photo_Eng = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/Eng.png")
photoimage_ENG = photo_Eng.subsample(3, 3)
btEN = Button(frame_home, image= photoimage_ENG, borderwidth=1, command=insertcard_en)
photo_TH = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/thai.png")
photoimage_TH = photo_TH.subsample(3, 3)
btTH = Button(frame_home, image=photoimage_TH, borderwidth=1, command=insertcard)

#canvas_ip = Canvas(frame_showipaddress,width=750,height=450)

def ipaddress():
    canvas_ip.itemconfigure(2,text="IP Address : " + getIPAddress())
    show_frame(frame_showipaddress)
    window.update_idletasks()
    window.update()

img_netwo2 = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/net.png")
network_img2 = img_netwo2.subsample(10, 10)
btIP = Button(frame_home, image=network_img2, borderwidth=1, command=ipaddress)

my_canvas.create_window(730, 450, window=btIP)
my_canvas.create_window(200, 300, window=btEN)
my_canvas.create_window(600, 300, window=btTH)


# ================== frame_insertcard_th code
my_canvas = Canvas(frame_insertcard_th, width=750, height=450)
my_canvas.pack(fill="both", expand=True)

my_canvas.create_image(0, 0, image=bg, anchor="nw")
my_canvas.create_text(400, 85, text="กรุณาสอดบัตรประชาชน", font=("Helvetica", 35), fill="brown")

img_insert_th = PhotoImage(file="/home/pi/Desktop/GUI/assets/images/insert_card/pic1.png")
my_canvas.create_image(200, 150, anchor=NW, image=img_insert_th)

# ================== frame_insertcard_en code
my_canvas = Canvas(frame_insertcard_en, width=750, height=450)
my_canvas.pack(fill="both", expand=True)

my_canvas.create_image(0, 0, image=bg, anchor="nw")
my_canvas.create_text(400, 85, text="Please insert your ID card.", font=("Helvetica", 35), fill="brown")

img_insert_en = PhotoImage(file="/home/pi/Desktop/GUI/assets/images/insert_card/pic1.png")
my_canvas.create_image(200, 150, anchor=NW, image=img_insert_en)

# ================== frame_check_th code
my_canvas = Canvas(frame_check_th, width=750, height=450)
my_canvas.pack(fill="both", expand=True)

my_canvas.create_image(0, 0, image=bg, anchor="nw")
my_canvas.create_text(400, 90, text="ตรวจสอบข้อมูล และ กดยืนยัน", font=("Helvetica", 35), fill="brown")

my_canvas.create_text(400, 150, text= "123", font=("Helvetica", 20), fill="black") #
my_canvas.create_text(400, 190, text= "123", font=("Helvetica", 20), fill="black") #
my_canvas.create_text(400, 230, text= "123", font=("Helvetica", 20), fill="black") #
my_canvas.create_text(400, 270, text= "123", font=("Helvetica", 20), fill="black") #
my_canvas.create_text(400, 310, text= "123", font=("Helvetica", 20), fill="black") #


photo_Eng = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/ยืนยัน.png")
photoimage_ENG2 = photo_Eng.subsample(3, 3)

photo_TH = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/ยกเลิก.png")
photoimage_TH2 = photo_TH.subsample(3, 3)

confirm_Eng = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/confirm.png")
confirm_Eng2 = confirm_Eng.subsample(3, 3)

cancel_Eng = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/cancel.png")
cancel_Eng2 = cancel_Eng.subsample(3, 3)

def frame_start_func():
    global lang
    print("lang = ")
    print(lang)
    if (lang == 1):
        print("if")
        my_canvas1.itemconfigure(2,text="เริ่มตรวจสุขภาพ")
        btStart_th.configure(image=photoimage_ENG2)
        show_frame(frame_start_th)
        window.update_idletasks()
        window.update()
    elif (lang == 0):
        print("else")
        my_canvas1.itemconfigure(2,text="Start Check")
        btStart_th.configure(image=confirm_Eng2)
        show_frame(frame_start_th)
        window.update_idletasks()
        window.update()
        
#btEN_check = Button(frame_check_th, image=photoimage_ENG2, borderwidth=1, command=lambda: show_frame(frame_start_th))

btEN_check = Button(frame_check_th, image=photoimage_ENG2, borderwidth=1, command=frame_start_func)
btTH_check = Button(frame_check_th, image=photoimage_TH2, borderwidth=1, command=lambda: show_frame(frame_home))

my_canvas.create_window(200, 400, window=btEN_check)
my_canvas.create_window(600, 400, window=btTH_check)


def frame_step1_func():
    global lang
    print("frame_step1_func lang = ")
    print(lang)
    if (lang == 1):
        print("if")
        my_canvas_step1_th.itemconfigure(2,text="กรุณายืนตรงเพื่อชั่งน้ำหนักและส่วนสูง")
        bt_step1_th.configure(image=photoimage_ENG2)
        show_frame(frame_step1_th)
        window.update_idletasks()
        window.update()
    elif (lang == 0):
        print("else")
        my_canvas_step1_th.itemconfigure(2,text="Please Stand up Straight to Measure\n       Your Weight and Height.")
        bt_step1_th.configure(image=confirm_Eng2)
        show_frame(frame_step1_th)
        window.update_idletasks()
        window.update()

def backHome():
    show_frame(frame_home)
    window.update_idletasks()
    window.update()

# ================== frame_start_th code
my_canvas1 = Canvas(frame_start_th,width=750,height=450)
my_canvas1.pack(fill="both", expand=True)

my_canvas1.create_image(0,0, image=bg,anchor="nw")
my_canvas1.create_text(400,150,text="เริ่มตรวจสุขภาพ",font=("Helvetica",40),fill="brown")
photo_start_th = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/11111.png")
photoimage_start_th = photo_start_th.subsample(3, 3)
btStart_th = Button(frame_start_th, image = photoimage_start_th,borderwidth=1 , command=frame_step1_func)

img_home = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/home.png")
home_bt = img_home.subsample(5)
bt_home = Button(frame_start_th, image=home_bt, borderwidth=1, command=backHome)
my_canvas1.create_window(735, 450, window=bt_home)


my_canvas1.create_window(400,350,window=btStart_th)



# ================== frame_step1_th code
my_canvas_step1_th = Canvas(frame_step1_th,width=750,height=450)
my_canvas_step1_th.pack(fill="both", expand=True)

my_canvas_step1_th.create_image(0,0, image=bg,anchor="nw")
my_canvas_step1_th.create_text(400,150,text="กรุณายืนตรงเพื่อชั่งน้ำหนักและส่วนสูง",font=("Helvetica",30),fill="brown")
photo_step1_th = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/11111.png")
photoimage_step1_th = photo_step1_th.subsample(3, 3)
bt_step1_th = Button(frame_step1_th, image = photoimage_step1_th,borderwidth=1 ,command = step1)

bt_home = Button(frame_step1_th, image=home_bt, borderwidth=1, command=backHome)
my_canvas_step1_th.create_window(735, 450, window=bt_home)

my_canvas_step1_th.create_window(400,350,window=bt_step1_th)



# ================== frame_step2_th code
my_canvas_step2_th = Canvas(frame_step2_th,width=750,height=450)
my_canvas_step2_th.pack(fill="both", expand=True)

my_canvas_step2_th.create_image(0,0, image=bg,anchor="nw")
my_canvas_step2_th.create_text(400,150,text="กรุณายกมือไปใกล้เพื่อวัดอุณหภูมิ",font=("Helvetica",30),fill="brown")
photo_step2_th = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/11111.png")
photoimage_step2_th = photo_step2_th.subsample(3, 3)
#bt_step2_th = Button(frame_step2_th, image = photoimage_step2_th,borderwidth=1)


#my_canvas_step2_th.create_window(400,350,window=bt_step2_th )




# ================== frame_step3_th code

my_canvas_step3_th = Canvas(frame_step3_th,width=750,height=450)
my_canvas_step3_th.pack(fill="both", expand=True)

my_canvas_step3_th.create_image(0,0, image=bg,anchor="nw")
my_canvas_step3_th.create_text(400,150,text="กรุณานำนิ้วไปแตะที่เครื่องวัดชีพจร",font=("Helvetica",30),fill="brown")
#photo_step3_th = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/11111.png")
#photoimage_step3_th = photo_step3_th.subsample(3, 3)
#bt_step3_th = Button(frame_step3_th, image = photoimage_step3_th,borderwidth=1 )

#my_canvas_step3_th.create_window(400,350,window=bt_step3_th)


# ================== frame_step4_th code
my_canvas_step4_th = Canvas(frame_step4_th,width=750,height=450)
my_canvas_step4_th.pack(fill="both", expand=True)

my_canvas_step4_th.create_image(0,0, image=bg,anchor="nw")
my_canvas_step4_th.create_text(400,150,text="กรุณานำแขนใส่เข้าไปในเครื่องวัดความดัน",font=("Helvetica",30),fill="brown")
photo_step4_th = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/11111.png")
photoimage_step4_th = photo_Eng.subsample(3, 3)
bt_step4_th= Button(frame_step4_th, image = photoimage_step4_th,borderwidth=1, command = step4 )


my_canvas_step4_th.create_window(400,350,window=bt_step4_th)

bt_home = Button(frame_step4_th, image=home_bt, borderwidth=1, command=backHome)
my_canvas_step4_th.create_window(735, 450, window=bt_home)



# ================== frame_result_th code
my_canvas_result_th = Canvas(frame_result_th,width=750,height=450)
my_canvas_result_th.pack(fill="both", expand=True)

my_canvas_result_th.create_image(0,0, image=bg,anchor="nw")
my_canvas_result_th.create_text(390,70,text="ผลการตรวจสุขภาพ",font=("Helvetica",35),fill="brown")

photo_Eng = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/ยืนยัน.png")
photoimage_result_th1 = photo_Eng.subsample(3, 3)
bten_result_th = Button(frame_result_th, image = photoimage_result_th1,borderwidth=1 , command = printresult)
photo_result_th = PhotoImage(file = r"/home/pi/Desktop/GUI/assets/images/start/ยกเลิก.png")
photoimage_result_th  = photo_result_th.subsample(3, 3)
btth_result_th = Button(frame_result_th, image = photoimage_result_th ,borderwidth=1 , command=lambda: show_frame(frame_home))


num = my_canvas_result_th.create_text(400, 140, text= "123", font=("Helvetica", 20), fill="black") #
num2 = my_canvas_result_th.create_text(400, 180, text= "123", font=("Helvetica", 20), fill="black") #
num3 = my_canvas_result_th.create_text(400, 220, text= "123", font=("Helvetica", 20), fill="black") #
my_canvas_result_th.create_text(400, 260, text= "123", font=("Helvetica", 20), fill="black") #
my_canvas_result_th.create_text(400, 300, text= "123", font=("Helvetica", 20), fill="black") #
print(num)
print(num2)
print(num3)
my_canvas_result_th.create_window(200,400,window=bten_result_th)
my_canvas_result_th.create_window(600,400,window=btth_result_th)






# ================== frame_last_th code
my_canvas33 = Canvas(frame_last_th,width=750,height=450)
my_canvas33.pack(fill="both", expand=True)

my_canvas33.create_image(0,0, image=bg,anchor="nw")
my_canvas33.create_text(380,100,text="กรุณาถอดบัตรประชาชน และรับใบสลิป",font=("Helvetica",35),fill="brown")

img222 = PhotoImage(file="/home/pi/Desktop/GUI/0000.png")
my_canvas33.create_image(230,150, anchor=NW, image=img222)





# ================== frame_loading_th code
my_canvas_loading = Canvas(frame_loading_th,width=750,height=450)
my_canvas_loading.pack(fill="both", expand=True)

my_canvas_loading.create_image(0,0, image=bg,anchor="nw")
my_canvas_loading.create_text(380,85,text="กรุณารอสักครู่",font=("Helvetica",35),fill="brown")

img_loading = PhotoImage(file="/home/pi/Desktop/GUI/load.gif")
my_canvas_loading.create_image(225,110, anchor=NW, image=img_loading)
#---




# ================== frame_showipaddress code
canvas_ip = Canvas(frame_showipaddress,width=750,height=450)
canvas_ip.pack(fill="both", expand=True)

canvas_ip.create_image(0,0, image=bg,anchor="nw")
canvas_ip.create_text(400,300,text="IP Address : " + getIPAddress(),font=("Helvetica",20),fill="brown")
bt_home = Button(frame_showipaddress, image=home_bt, borderwidth=1, command=backHome)


img_netwo = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/network.png")
network_img = img_netwo.subsample(3, 3)
canvas_ip.create_image(400,110,image=network_img)
canvas_ip.create_window(735, 450, window=bt_home)

"""
netwo = PhotoImage(file=r"/home/pi/Desktop/GUI/assets/images/start/network.jpeg")
netwo_bt = netwo.subsample(5)
bt_net = Button(frame_showipaddress, image=netwo_bt, borderwidth=1)
canvas_ip.create_window(200, 200, window=bt_net)"""
#img_loading1 = PhotoImage(file="/home/pi/Desktop/GUI/load.gif")
#canvas_ip.create_image(225,110, anchor=NW, image=img_loading1)
#---
#frame_showipaddress = Frame(window)

#print(getIPAddress())

show_frame(frame_home)
#show_frame(frame_showipaddress)


window.mainloop()
