from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, hexdump
import datetime, os


ssid = 'cafe'
iface = 'en0'
sender = '8c:85:90:5d:f1:54'
# channel = 1

now = datetime.datetime.now()

dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=sender, addr3=sender)
beacon = Dot11Beacon()
essid = Dot11Elt(ID='SSID', info=ssid, len=len(ssid))

# rates = Dot11Elt(ID='Rates', info='/x82/x84/x8b/x96/x0c/x12/x18')
# esrates = Dot11Elt(ID='ESRates', info='/x30/x48/x60/x6c')
# channel = Dot11Elt(ID='DSset', info=chr(1))
# channel = Dot11Elt(ID='DSset', info=(b"\x01"))

# os.system('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -c' + str(channel))

# info = (f'time is {now}')
# rsn = Dot11Elt(ID='RSNinfo', info=info)

frame = RadioTap()/dot11/beacon/essid#/rates/esrates/channel#/rsn

sendp(frame, iface=iface, inter=0.100, loop=1, monitor=True)
