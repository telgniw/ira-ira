#!/usr/bin/python

# http://pyserial.sourceforge.net/

import serial
import time
from threading import Thread

#port = '/dev/tty.usbserial-DAWR13BI'
port = '/dev/tty.usbserial-DAWR0Y8X'

class PumpSpark:

  ser = None
  
  airKit = [0, 3]
  cleanKit = [1, 4]
  blueKit = [2, 5]

  def __init__(self):
    self.connect()

  def connect(self):
    try:
      self.ser = serial.Serial(port, 9600, timeout=1)
      print 'connected serial port.'
    except: 
      print 'connected fail.'
      pass

  def turnOff(self, *args):
    if len(args) == 0:
      for i in range(0, 8):
        self.write(i,0)
    else:
      for i in args:
        self.write(i,0)

  def turnOn(self, kit_powers):
    for kit, power in kit_powers:
      self.write(kit, power)

  def clean(self):
    for kit in self.cleanKit:
      self.write(kit, 254)

  def pump_core(self, kit_powers, second):
    for kit, power in kit_powers:
      self.write(kit, power)
    time.sleep(second)
    for kit, power in kit_powers:
      self.write(kit, 0)

  def pump2_core(self, queue):
    for q in queue:
      self.pump_core(q[0], q[1])

  # ps.pump2([([(1, 254), (4, 254)],5), ([(2, 100), (3, 100)], 10)])
  # clean water and then bule
  def pump2(self, queue):
    print queue
    t = Thread(target=self.pump2_core, args=(queue, ))
    t.start()

  def pump(self, kit_powers, second):
    t = Thread(target=self.pump_core, args=(kit_powers, second))
    t.start()

  def play(self):
    self.pump2([
      ([(1, 254), (4, 254)],10), 
      ([(0, 254), (2, 254)], 1), 
      ([(2,140), (5, 100)], 10)])

  def stop(self):
    self.turnOff()

  def write(self, kit, power):
    self.ser.write(bytearray([255, kit, power]))

