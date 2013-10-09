import serial

class Light():

  def __init__(self):
    self.port = '/dev/tty.usbmodemfa131'
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
