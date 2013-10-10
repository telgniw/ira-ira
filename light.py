import serial, time
from threading import Thread

class Light():

  def __init__(self):
    self.port = [
        '/dev/tty.usbmodemfd121', 
        '/dev/tty.usbmodemfd1211', 
        '/dev/tty.usbmodemfa1341', 
        '/dev/tty.usbmodemfa1311']
    self.connect()

  def connect(self):
    for port in self.port:
      try:
        self.ser = serial.Serial(port, 9600)
        print 'serial port connected '
        return
      except:
        print 'serial port connected fail' + port
        pass
    print 'serial port connected fail'

  def on(self):
    self.ser.write('O')

  def off(self):
    self.ser.write('X')

  def flash(self, second=1, times=1, block=True):
    if block is True:
      for _ in range(times):
        self.on()
        time.sleep(second)
        self.off()
        time.sleep(second)
    else:
      t = Thread(target=self.flash, args=(second, times, True))
      t.start()
