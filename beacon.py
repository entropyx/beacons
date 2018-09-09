from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
   def __init__(self):
       DefaultDelegate.__init__(self)

   def handleDiscovery(self, dev, isNewDev, isNewData):
       if isNewDev:
           print("Discovered device", dev.addr)
       elif isNewData:
           print("Received new data from", dev.addr)



scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)


def calculateDistance(rssi):
   txPower = -59
   if rssi == 0:
       return -1
   else:
       ratio = rssi*1.0/txPower
       if ratio < 1.0:
           return ratio**10
       else:
           distance = 0.89976 * ratio**7.7095 + 0.111;
           return distance


for dev in devices:
   print("Device %s (%s), Distance = %d" % (dev.addr, dev.addrType, calculateDistance(dev.rssi)))
   for (adtype, desc, value) in dev.getScanData():
       print(desc, value)
