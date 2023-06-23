
from machine import Pin,SPI,PWM
import framebuf
import time,random
import os
import network

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(32768)#max 65535

LCD = LCD_1inch3()
    
keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)
    
up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

def drawmenu(selected):    
  LCD.fill(0)
  i = 0
  for line in menu:
      if (i == selected):
          LCD.fill_rect(10,i*10,150,10,LCD.red)
      LCD.text(line,10,i*10,LCD.white)
      i += 1
  LCD.show()

def choose_ascii():
    selected = 65
    selectedx = selectedy = 0
    password = ""
    while (1):
      LCD.fill(0)
      x = 0
      y = 30
      # grid of ascii
      for c in range(32,127):  
        if( x >= 200): x = 0 ; y += 20
        if (c == selected): LCD.fill_rect(x-5,y-5,20,20,LCD.red)
        LCD.text(chr(c),x,y,LCD.white)
        x += 20
    
      if (up.value() == 0):   selectedy -= 1; time.sleep(0.2)
      if (down.value() == 0): selectedy += 1; time.sleep(0.2)
      if (right.value() == 0): selectedx +=1; time.sleep(0.2)
      if (left.value() == 0):  selectedx -= 1; time.sleep(0.2)
  
      selected = 32 + selectedx + (selectedy * 10)
  
      if (keyA.value() == 0): password += chr(selected); time.sleep(0.2)
      if (keyB.value() == 0): password = password[:-1]; time.sleep(0.2)
  
      LCD.text(password,10,10,LCD.green)
      LCD.show()
      if (keyY.value() == 0):
          break
    return password

def choose_menu(menu):
    selected = 0
    drawmenu(selected)
    while (1):
      if (down.value() == 0):
          if (selected < len(menu)-1): selected += 1
          drawmenu(selected)
          time.sleep(0.2)
      if (up.value() == 0):
          if (selected > 0): selected -= 1
          drawmenu(selected)
          time.sleep(0.2)
      if (keyA.value() == 0):
          break
    return menu[selected]
     
while (1):
    wlan = network.WLAN()  
    wlan.active(True)
    networks = wlan.scan() # list withfields ssid, bssid, channel, RSSI, security, hidden
    networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)

    # make list of SSIDs
    menu = []
    for w in networks:
        menu.append(w[0].decode())
                
    ssid = choose_menu(menu)
    time.sleep(0.2)
    #enter password from grid of ascii
    password = choose_ascii()
    
    LCD.fill(0)
    text = 'connecting to ' + ssid
    LCD.text(text,10,10,LCD.white)
    LCD.show()
    wlan.connect(ssid, password)
    timeout = 0
    while (timeout  < 5):
        if wlan.isconnected() == True: break
        timeout += 1
        time.sleep(1)
    if wlan.isconnected() == True:
        LCD.text("connected",10,20,LCD.green)
        LCD.show()
        break
    else:
        LCD.text("connection error - password?",10,30,LCD.red)
        LCD.show()
        time.sleep (2)    
        # revert back to scanlist (while loop)
