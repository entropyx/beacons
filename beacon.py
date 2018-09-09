from bluepy.btle import Scanner, DefaultDelegate
from google.cloud import firestore
import datetime
import firebase_admin
import time
import os
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/home/pi/hack/beacons/cred.json")
firebase_admin.initialize_app(cred, {
        'projectId': 'test-215901' 
    })

db = firestore.client()

def insert_data(db, mac, distance):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    doc_ref = db.collection(u'devices').document(mac)
    doc_ref.set({
        u'distance': distance,
        u'timestamp': timestamp
    })


class ScanDelegate(DefaultDelegate):
   def __init__(self):
       DefaultDelegate.__init__(self)

   def handleDiscovery(self, dev, isNewDev, isNewData):
       if isNewDev:
           print("Discovered device", dev.addr)
       elif isNewData:
           print("Received new data from", dev.addr)


def calculateDistance(rssi):
    txPower = -61
    if rssi == 0:
        return -1
    else:
        ratio = rssi*1.0/txPower
        if ratio < 1.0:
            return ratio**10
        else:
            distance = 0.89976 * ratio**7.7095 + 0.111;
            return distance


while True:
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)
    os.system('sudo hcitool -i hci0 cmd 0x08 0x0008 1b 02 01 06 03 03 aa fe 13 16 aa fe 10 00 03 62 62 76 61 00 74 75 74 69 63 6b 65 74 00 00 00 00')
    for dev in devices:
        insert_data(db, dev.addr, calculateDistance(dev.rssi))
        print(dev.addr)
