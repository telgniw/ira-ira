import serial, time
from threading import Thread

class Light():

  def __init__(self):
    self.port = '/dev/tty.usbmodemfd121'
    self.connect()

  def connect(self):
    try:
      self.ser = serial.Serial(self.port, 9600)
      print 'serial port connected '
    except:
      print 'serial port connected fail'
      pass

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
