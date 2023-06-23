import serial
import RPi.GPIO as GPIO      
import os, time
import pyrebase 

GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=1)

config = {                                                              #define a dictionary named config with several key-value pairs that configure the connection to the database.
  "apiKey": "AIzaSyDBoj435pEFmCQEYa7ookx48S7lwaGvl2I",
  "authDomain": "raspberrypiandmodulesim.firebaseapp.com",
  "databaseURL": "https://raspberrypiandmodulesim-default-rtdb.firebaseio.com/",
  "storageBucket": "raspberrypiandmodulesim.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
        
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #thay doi port ket noi với arduino
#     ser.reset_input_buffer()
    
    while True:
        sensor = ser.readline().decode('utf-8').rstrip()
        print(sensor)
        sen_val = bytes(sensor, 'utf-8')
        
        
        db.child("Analog Value").set(sensor)
        
        status=db.child("Status").get()
        print("type: ",type(status.val()), status.val())
        if(status.val()=="SELECT"):
            locs=db.child("Location").get()
            print(locs.val())
            locs_val = bytes(locs.val(), encoding='utf-8')
            print(locs_val)
            
            
            
            port.write(b'AT\r')
            rcv = port.read(10)
            print(rcv)

            port.write(b'ATE0\r\n')      # Disable the Echo
            rcv = port.read(10)
            print(rcv)

            port.write(b'AT+CMGF=1\r\n')  # Select Message format as Text mode 
            rcv = port.read(10)
            print(rcv)

            port.write(b'AT+CNMI=2,2,0,0,0\r\n')   #hiển thị nội dung ngay khi có tin nhắn đến
            rcv = port.read(10)
            print(rcv)
            
            sdt=db.child("SDT").get()
            print(sdt.val())
            phone_num = bytes(sdt.val(), encoding='utf8')
            print(phone_num)

            port.write(b'AT+CMGS="'+phone_num+b'"\r\n')
            rcv = port.read(10)
            print(rcv)

            port.write(b'Phat hien nong do con tai vi tri: '+locs_val)  # Message
            port.write(b"\x1A") # Enable to send SMS
            
            db.child("Status").set("CANCEL")
        
        


