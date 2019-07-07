#!/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as gpio
import time
import math
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
format = "%H:%M:%S"
a11 = '00:00:00'
alarme1 = ['0']
horario1 = ['0','0','0']
nome11 = ''
edit1 = 0
nal11 = 0
npill1 = 21
nal1 = 1
a1 = '00:00:00'
nome1 = ''
a22 = '00:00:00'
alarme2 = ['0']
horario2 = ['0','0','0']
nome22 = ''
edit2 = 0
nal22 = 0
npill2 = 21
nal2 = 1
a2 = '00:00:00'
nome2 = ''
a33 = '00:00:00'
alarme3 = ['0']
horario3 = ['0','0','0']
nome33 = ''
edit3 = 0
nal33 = 0
npill3 = 21
nal3 = 1
a3 = '00:00:00'
nome3 = ''
mqtt_manutencao = [("manutencao1",2),("manutencao2",2),("manutencao3",2)]
mqtt_npill = [("npill1",2),("npill2",2),("npill3",2)]
mqtt_nome = [("nome1",2),("nome2",2),("nome3",2)]
mqtt_nal = [("nal1",2),("nal2",2),("nal3",2),("nal11",2),("nal22",2),("nal33",2)]
mqtt_al = [("a1",2),("a2",2),("a3",2)]
mqtt_edit = [("edit1",2),("edit2",2),("edit3",2)]
mqtt_bot = [("bot1",2),("bot2",2),("bot3",2)]
mqtt_copomed = [("medicamento",2),("copo",2)]
mqtt_gaveta = [("gaveta1",2),("gaveta2",2),("gaveta3",2)]
mqtt_horario = [("horario1",2),("horario2",2),("horario3",2)]
mqtt_topics = mqtt_manutencao+mqtt_npill+mqtt_nome+mqtt_nal+mqtt_al+mqtt_edit+mqtt_bot+mqtt_copomed+mqtt_gaveta+mqtt_horario
def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topics)

def on_message(client, userdata, message):
    global manutencao1, manutencao2, manutencao3, npill1, npill2, npill3, nome1, nome2, nome3
    global nal1, nal2, nal3, a1, a2, a3, edit1, edit2, edit3, bot1, bot2, bot3, medicamento, copo
    global gaveta1, gaveta2, gaveta3, nal11, nal22, nal33

    if message.topic=="npill1":
        npill1 = int(message.payload.decode("utf-8"))
    elif message.topic=="npill2":
        npill2 = int(message.payload.decode("utf-8"))
    elif message.topic=="npill3":
        npill3 = int(message.payload.decode("utf-8"))
    elif message.topic=="nal1":
        nal1 = int(message.payload.decode("utf-8"))
    elif message.topic=="nal2":
        nal2 = int(message.payload.decode("utf-8"))
    elif message.topic=="nal3":
        nal3 = int(message.payload.decode("utf-8"))
    elif message.topic=="edit1":
        edit1 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="edit2":
        edit2 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="edit3":
        edit3 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="bot1":
        bot1 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="bot2":
        bot2 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="bot3":
        bot3 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="nal11":
        nal11 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="nal22":
        nal22 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="nal33":
        nal33 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="nome1":
        nome1 = str(message.payload.decode("utf-8"))
    elif message.topic=="nome2":
        nome2 = str(message.payload.decode("utf-8"))
    elif message.topic=="nome3":
        nome3 = str(message.payload.decode("utf-8"))
    elif message.topic=="a1":
        a1 = str(message.payload.decode("utf-8"))
    elif message.topic=="a2":
        a2 = str(message.payload.decode("utf-8"))
    elif message.topic=="a3":
        a3 = str(message.payload.decode("utf-8"))

broker_address="localhost"
clientm = mqtt.Client("D1")
clientm.on_connect = on_connect
clientm.on_message = on_message
clientm.connect(broker_address, 1883)
clientm.loop_start()

def AlteraD1(manutencao1, alarme1, horario1):
    while(edit1==1):
        while (nal11==1):
            horario1 = []
            alarme1 = []
            clientm.publish("bot1",'false')
            for i in range(nal1):
                time.sleep(1)
                while(bot1==0):
                    a11 = datetime.datetime.strptime(a1, format).time()
                    time.sleep(1)
                clientm.publish("bot1",'false')
                horario1.append(a1)
                alarme1.append(a11)
            auxh1 = str(horario1)
            clientm.publish("horario1",auxh1.strip('[]'))
            clientm.publish("manutencao1",'false')                       
            clientm.publish("nal11",'false')
            clientm.publish("edit1",'false')
            time.sleep(1)    
        time.sleep(1)
    nome11 = nome1
    return nome11, alarme1, horario1

def AlteraD2(manutencao2, alarme2, horario2):
    while(edit2==1):
        while (nal22==1):
            horario2 = []
            alarme2 = []
            clientm.publish("bot2",'false')
            for i in range(nal2):
                time.sleep(1)
                while(bot2==0):
                    a22 = datetime.datetime.strptime(a2, format).time()
                    time.sleep(1)
                clientm.publish("bot2",'false')
                horario2.append(a2)
                alarme2.append(a22)
            auxh2 = str(horario2)
            clientm.publish("horario2",auxh2.strip('[]'))
            clientm.publish("manutencao2",'false')                       
            clientm.publish("nal22",'false')
            clientm.publish("edit2",'false')
            time.sleep(1)    
        time.sleep(1)
    nome22 = nome2
    return nome22, alarme2, horario2

def AlteraD3(manutencao3, alarme3, horario3):
    while(edit3==1):
        while (nal33==1):
            horario3 = []
            alarme3 = []
            clientm.publish("bot3",'false')
            for i in range(nal3):
                time.sleep(1)
                while(bot3==0):
                    a33 = datetime.datetime.strptime(a3, format).time()
                    time.sleep(1)
                clientm.publish("bot3",'false')
                horario3.append(a3)
                alarme3.append(a33)
            auxh3 = str(horario3)
            clientm.publish("horario3",auxh3.strip('[]'))
            clientm.publish("manutencao3",'false')                       
            clientm.publish("nal33",'false')
            clientm.publish("edit3",'false')
            time.sleep(1)    
        time.sleep(1)
    nome33 = nome3
    return nome33, alarme3, horario3
