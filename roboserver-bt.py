from bluetooth import *
import RPi.GPIO as GPIO
from time import sleep
import os, sys
GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03, 50)
pwm.start(0)
os.system("hciconfig hci0 piscan")
def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
running = True
status = "";
while running:
    print "Waiting for connection on RFCOMM channel %d" % port
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info
    status = "Connected :)"
    try:
        while running:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            # prepend any partial command from last time, then split commands
            commands = data.rstrip().split('$$')
            number = len(commands)

            # loop through commands
            for i in range(number):

                # parse the command
                command = commands[i]
                if command == '':
                    continue
                
                elif command == 'open':
                    print "Opening door"
                    status = client_sock.send("Attempting to Open Door...")
                    SetAngle(210)
                    status = client_sock.send("Successfully Opened")
                elif command == "close":
                    print "Closing door"
                    client_sock.send("Closing...")
                    SetAngle(0)
                    client_sock.send("Closed!")
                elif command == "stop":
                    client_sock.send("stopping server")
                    print "stopping server"
                    running = False
                else:
                    print "received [%s]" % data
    except IOError:
        SERIAL_PORT_CLASS

    print "disconnected"

    client_sock.close()
	
server_sock.close()
print "all done"
