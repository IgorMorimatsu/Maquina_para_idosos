#!/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as gpio
import time
import math
import datetime
import perifericos
import manutencao
from Adafruit_CharLCD import Adafruit_CharLCD
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
saida = (17,27,22,5,6,13,26)  #tupla de saídas
for s in saida:
    gpio.setup(s, gpio.OUT)
    gpio.output(s, gpio.LOW)
gpio.setup(15, gpio.OUT)
gpio.output(15, gpio.HIGH)
gpio.setup(10, gpio.IN, pull_up_down = gpio.PUD_UP) #sensor do disco 1 - vai de 0 para 1
gpio.setup(9, gpio.IN, pull_up_down = gpio.PUD_UP) #sensor do disco 2
gpio.setup(11, gpio.IN, pull_up_down = gpio.PUD_UP) #sensor do disco 3
gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_UP) #sensor do copo
gpio.setup(16, gpio.IN, pull_up_down = gpio.PUD_UP) #chave fim de curso 1 - vai de 1 para 0
gpio.setup(20, gpio.IN, pull_up_down = gpio.PUD_UP) #chave fim de curso 2
gpio.setup(21, gpio.IN, pull_up_down = gpio.PUD_UP) #chave fim de curso 3
pwm1 = gpio.PWM(5, 15)
pwm2 = gpio.PWM(6, 15) #15 hz
pwm3 = gpio.PWM(13, 15)
pwm1.start(0)
pwm2.start(0) #dutycycle inicial em "0"
pwm3.start(0)
x1 = 0
x2 = 0              #auxiliar sensor do motor
x3 = 0
sensor_copo = 0     #auxiliar do sensor do copo
aux_alarme1 = 0
aux_alarme2 = 0     #auxiliar de alarme ativado
aux_alarme3 = 0
alarme1 = ['0']
alarme2 = ['0']     #vetor de alarmes
alarme3 = ['0']
ledbuzzer = 0
format = "%H:%M:%S"
auxaviso = 0        #auxiliar para aviso de tempo maximo
aviso = 0           #auxiliar do tempo para aviso de tempo maximo
lcd = Adafruit_CharLCD.Adafruit_CharLCD(rs=18,en=23,d4=24,d5=25,d6=8,d7=7,cols=20,lines=4)
auxi1 = 0
auxi2 = 0           #auxiliar info copo 
auxi3 = 0
t = 0               #auxiliar tempo display linha 2
aux = 1             #auxiliar display linha 2
horario1 = ['0']
horario2 = ['0']    #vetor de alarmes transformados para string para o display linha 2
horario3 = ['0']
cont = 0            #auxiliar display linha 3
refuel1 = ''
refuel2 = ''        #auxiliar para info display linha 3
refuel3 = ''
agora = ''
DIS = perifericos.Display()             #Objeto do display
LB = perifericos.LedBuzzer(ledbuzzer)   #Objeto do Led e do Buzzer
a11 = '00:00:00'
a22 = '00:00:00'    #auxiliar para salvar horario
a33 = '00:00:00'
auxg1 = 0
auxg2 = 0           #auxiliar para publicar sobre a gaveta
auxg3 = 0
nome11 = ''
nome22 = ''         #auxiliar nome fixo do remedio
nome33 = ''
i1 = 0
i2 = 0              #auxiliar vetor
i3 = 0
pw1 = 0
pw2 = 0             #auxiliar pwm
pw3 = 0
cont1 = 0
cont2 = 0           #contador para o pwm
cont3 = 0
manutencao1 = 0
manutencao2 = 0     #botão para habilitar a manutenção
manutencao3 = 0
edit1 = 0
edit2 = 0           #boitão para editar alarmes
edit3 = 0
bot1 = 0
bot2 = 0            #botão para confirmar horário
bot3 = 0
nal11 = 0
nal22 = 0           #botão para confirmar n alarmes
nal33 = 0
npill1 = 21
npill2 = 21         #numero de compartimentos cheios
npill3 = 21
nal1 = 1
nal2 = 1            #numero de alarmes configurados
nal3 = 1
a1 = '00:00:00'
a2 = '00:00:00'     #alarme digitado
a3 = '00:00:00'
gaveta1 = ''
gaveta2 = ''        #info da gaveta
gaveta3 = ''
nome1 = ''
nome2 = ''          #info nome do remedio
nome3 = ''
th = 0
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
    
    if message.topic=="manutencao1":
        manutencao1 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="manutencao2":
        manutencao2 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="manutencao3":
        manutencao3 = int(message.payload.decode("utf-8")=='true')
    elif message.topic=="npill1":
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
client = mqtt.Client("TCC")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, 1883)
client.loop_start()
time.sleep(1)

client.publish("manutencao1",'false')
client.publish("edit1",'false')
client.publish("bot1",'false')
client.publish("nal11",'false')
client.publish("manutencao2",'false')
client.publish("edit2",'false')
client.publish("bot2",'false')
client.publish("nal22",'false')
client.publish("manutencao3",'false')
client.publish("edit3",'false')
client.publish("bot3",'false')
client.publish("nal33",'false')
client.publish("copo",'Presente')
client.publish("medicamento",'Vazio')
client.publish("gaveta1",'Fechada')
client.publish("tempolimite",'não ultrapassado')
client.publish("nal1",1)
client.publish("nal2",1)
client.publish("nal3",1)
time.sleep(1)
try:
    while True:
        now = datetime.datetime.now()
        agora = now.strftime('%H:%M:%S  %d/%m/%Y')
        if (th==20):
            t, aux, cont = DIS.Escreve(agora, nome11, nome22, nome33, horario1, horario2, horario3, nal1, nal2, nal3, refuel1, refuel2, refuel3, auxi1, auxi2, auxi3, t, aux, cont)              
            th = 0
        th = th+1
        LB.led_rgb()                                #Liga/Desliga o LED
        LB.buzzer()                                #Liga/Desliga o Buzzer 
        if (gpio.input(12)==gpio.HIGH):                     #Sensor do copo
            sensor_copo = 0                             #Copo presente
            client.publish("copo",'Presente')
        else:
            sensor_copo = 1                             #Copo ausente
            client.publish("copo",'Ausente')
            
        if(sensor_copo==1 and LB.ledbuzzer==1):    #Lógica para desligar sinalizadores
            LB.ledbuzzer = 0                                    #Desliga auxiliar do Led/Buzzer
            auxi1 = 0                                           #Auxiliar para apagar uma informação no display
            auxi2 = 0
            auxi3 = 0
            client.publish("medicamento",'Vazio')
            client.publish("tempolimite",'não ultrapassado')
            auxaviso = 0
            aviso = 0
            
        if (auxaviso==1):
            aviso = aviso+1
            if (aviso==200):
                client.publish("tempolimite",'ultrapassado')            
        time.sleep(0.05)                

        if (manutencao1==1):                          #Manutenção disco 1
            nome11, alarme1, horario1 = manutencao.AlteraD1(manutencao1, alarme1, horario1)
        if (manutencao2==1):                          #Manutenção disco 2
            nome22, alarme2, horario2 = manutencao.AlteraD2(manutencao2, alarme2, horario2)
        if (manutencao3==1):                          #Manutenção disco 3
            nome33, alarme3, horario3 = manutencao.AlteraD3(manutencao3, alarme3, horario3)
        
        if (manutencao1==0):                #Lógica disco 1
            if gpio.input(16)==gpio.LOW:
                if (auxg1==0):
                    client.publish("gaveta1",'Fechada')
                    auxg1 = 1
                if (i1<nal1):
                    hora1 = alarme1[i1].hour
                    minuto1 = alarme1[i1].minute
                    sec1 = alarme1[i1].second
                    if(now.hour==hora1 and now.minute==minuto1 and now.second==sec1):   #Lógica para verificar se deu a hora do alarme
                        aux_alarme1 = 1
                    else:
                        aux_alarme1 = 0
                    i1 = i1+1
                    if (i1==nal1):
                        i1 = 0
                if (gpio.input(10)==gpio.HIGH):                             #Sensor do motor
                    x1 = 1
                else:
                    x1 = 0 
                if (npill1<=5):                     #Lógica para avisar sobre o reabastecimento                                        #Auxiliar para não entrar no loop
                    refuel1 = 'Reabastecer Disco 1'                       #Mensagem para aviso da necessidade de reabastecimento
                else:
                    refuel1 = ''
                if(x1==1 and aux_alarme1==1 and sensor_copo==0 and npill1>0 and pw1==1):    #Lógica para ligar o motor
                    pwm1.ChangeDutyCycle(90)                            #Liga motor
                    LB.ledbuzzer = 1                                    #Liga auxiliar do Led/Buzzer
                    npill1 = npill1 - 1                                 #Decrementa 1 do número de pílulas
                    auxi1 = 1                                           #Auxiliar para escrever uma informação no display
                    client.publish("medicamento",'Abastecido')
                    client.publish("npill1",npill1)
                    auxaviso = 1
                    cont1 = 0
                    pw1 = 0
##                if (cont1>1): 
                if(x1==1 and aux_alarme1==0 and pw1==0):                       #Lógica para desligar o motor
                    pwm1.ChangeDutyCycle(0)                             #Desliga motor
                    pw1 = 1
                cont1 = cont1+1
            else:
                if (auxg1==1):
                    client.publish("gaveta1",'Aberta')
                    auxg1 = 0

        if (manutencao2==0):                #Lógica disco 2
            if gpio.input(20)==gpio.LOW:
                if (auxg2==0):
                    client.publish("gaveta2",'Fechada')
                    auxg2 = 1
                if (i2<nal2):
                    hora2 = alarme2[i2].hour
                    minuto2 = alarme2[i2].minute
                    sec2 = alarme2[i2].second
                    if(now.hour==hora2 and now.minute==minuto2 and now.second==sec2):   #Lógica para verificar se deu a hora do alarme
                        aux_alarme2 = 1
                    else:
                        aux_alarme2 = 0
                    i2 = i2+1
                    if (i2==nal2):
                        i2 = 0
                if (gpio.input(9)==gpio.HIGH):                             #Sensor do motor
                    x2 = 1                                              
                else:
                    x2 = 0
                if (npill2<=5):                     #Lógica para avisar sobre o reabastecimento
                    refuel2 = 'Reabastecer Disco 2'                       #Mensagem para aviso da necessidade de reabastecimento
                else:
                    refuel2 = ''                     
                if(x2==1 and aux_alarme2==1 and sensor_copo==0 and npill2>0 and pw2==1):    #Lógica para ligar o motor
                    pwm2.ChangeDutyCycle(90)                            #Liga motor
                    LB.ledbuzzer = 1
                    npill2 = npill2 - 1                                 #Decrementa 1 do número de pílulas
                    auxi2 = 1                                           #Auxiliar para escrever uma informação no display
                    client.publish("medicamento",'Abastecido')
                    client.publish("npill2",npill2)
                    auxaviso = 1
                    cont2 = 0
                    pw2 = 0
##                if (cont2>1):                
                if(x2==1 and aux_alarme2==0 and pw2==0):                       #Lógica para desligar o motor
                    pwm2.ChangeDutyCycle(0)                             #Desliga motor        
                    pw2 = 1
                cont2 = cont2+1
            else:
                if (auxg2==1):
                    client.publish("gaveta2",'Aberta')
                    auxg2 = 0

        if (manutencao3==0):                #Lógica disco 3
            if gpio.input(21)==gpio.LOW:
                if (auxg3==0):
                    client.publish("gaveta3",'Fechada')
                    auxg3 = 1
                if (i3<nal3):
                    hora3 = alarme3[i3].hour
                    minuto3 = alarme3[i3].minute
                    sec3 = alarme3[i3].second
                    if(now.hour==hora3 and now.minute==minuto3 and now.second==sec3):   #Lógica para verificar se deu a hora do alarme
                        aux_alarme3 = 1
                    else:
                        aux_alarme3 = 0
                    i3 = i3+1
                    if (i3==nal3):
                        i3 = 0
                if (gpio.input(11)==gpio.HIGH):                             #Sensor do motor
                    x3 = 1                                              
                else:
                    x3 = 0
                if (npill3<=5):                     #Lógica para avisar sobre o reabastecimento
                    refuel3 = 'Reabastecer Disco 3'                       #Mensagem para aviso da necessidade de reabastecimento
                else:
                    refuel3 = '' 
                if(x3==1 and aux_alarme3==1 and sensor_copo==0 and npill3>0 and pw3==1):    #Lógica para ligar o motor
                    pwm3.ChangeDutyCycle(90)                            #Liga motor
                    LB.ledbuzzer = 1                                      #Liga auxiliar do Buzzer
                    npill3 = npill3 - 1                                 #Decrementa 1 do número de pílulas
                    auxi3 = 1                                           #Auxiliar para escrever uma informação no display
                    client.publish("medicamento",'Abastecido')
                    client.publish("npill3",npill3)
                    auxaviso = 1         
                    cont3 = 0
                    pw3 = 0
##                if (cont3>1): 
                if(x3==1 and aux_alarme3==0 and pw3==0):                       #Lógica para desligar o motor
                    pwm3.ChangeDutyCycle(0)                             #Desliga motor
                    pw3 = 1
                cont3 = cont3+1                                         
            else:
                if (auxg3==1):
                    client.publish("gaveta3",'Aberta')
                    auxg3 = 0
except KeyboardInterrupt:
    pwm1.stop()
    pwm2.stop()
    pwm3.stop()
    gpio.cleanup() #limpa portas gpio
    client.disconnect()
    client.loop_stop()
