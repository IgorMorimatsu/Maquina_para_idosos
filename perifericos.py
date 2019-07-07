#!/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as gpio
import time
from Adafruit_CharLCD import Adafruit_CharLCD

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
saida = (17,27,22,26)  #tupla de saídas
for s in saida:
    gpio.setup(s, gpio.OUT)
lcd = Adafruit_CharLCD.Adafruit_CharLCD(rs=18,en=23,d4=24,d5=25,d6=8,d7=7,cols=20,lines=4)

class Display:
    def __init__(self):   
        pass
    
    def Escreve(self, agora, nome11, nome22, nome33, horario1, horario2, horario3, nal1, nal2, nal3, refuel1, refuel2, refuel3, auxi1, auxi2, auxi3, t, aux, cont):
        lcd.clear()
        lcd.set_cursor(0,0)
        lcd.message(agora)                          #display linha 1
        auxnal2 = nal1+nal2
        auxnal3 = auxnal2+nal3
        nal = nal1+nal2+nal3
        if (aux>0 and aux<=nal1):                    #Lógica display linha 2
            lcd.set_cursor(0,1)
            txt = nome11+' '+horario1[aux-1]
            lcd.message(txt)
        elif (aux>nal1 and aux<=auxnal2):
            lcd.set_cursor(0,1)
            txt = nome22+' '+horario2[aux-nal1-1]
            lcd.message(txt)
        elif (aux>auxnal2 and aux<=auxnal3):
            lcd.set_cursor(0,1)
            txt = nome33+' '+horario3[aux-auxnal2-1]
            lcd.message(txt)
        else:
            aux = 1
        if t==10:
            aux = aux+1
            t = 0
        else:
            t = t+1            
        if (cont>=0 and cont<20):                   #Lṕgica display linha 3
            lcd.set_cursor(0,2)
            lcd.message(refuel1)
        elif (cont>=20 and cont<40):
            lcd.set_cursor(0,2)
            lcd.message(refuel2)
        elif (cont>=40 and cont<60):
            lcd.set_cursor(0,2)
            lcd.message(refuel3)
        else:
            cont = 0            
        cont = cont + 1        
        lcd.set_cursor(0,3)
        if auxi1==1 or auxi2==1 or auxi3==1:
            lcd.message('Copo Abastecido')             #Mensagem para aviso de que o remédio foi liberado
        else:
            lcd.message('Copo Vazio')

        return t, aux, cont
        
class LedBuzzer:
    def __init__(self, ledbuzzer):
        self.ledbuzzer = ledbuzzer

    def led_rgb(self):
        rgb = (17,27,22)
        if(self.ledbuzzer==1):
            sequencias = ((0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1))
            for seq in sequencias:
                indice = 0
                for p in rgb:
                    gpio.output(p, seq[indice])
                    indice = indice + 1
                    time.sleep(0.02)
        else:
            for p in rgb:
                gpio.output(p, gpio.LOW) 
            
    def buzzer(self):
        if(self.ledbuzzer==1):
            gpio.output(26, gpio.HIGH)
            time.sleep(0.3)
            gpio.output(26, gpio.LOW)
        else:
            gpio.output(26, gpio.LOW)
