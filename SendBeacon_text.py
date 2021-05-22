from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump

netSSID = 'cafe'       #Network name here
iface = 'en0'       #Interface name here

info = ('Just text'.encode('utf-8'))

sender = '8c:85:90:5d:f1:54'

dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff',addr2=sender, addr3=sender)

beacon = Dot11Beacon(cap='ESS+privacy')
essid = Dot11Elt(ID='SSID',info=netSSID, len=len(netSSID))
rsn = Dot11Elt(ID='RSNinfo', info=info)

frame = RadioTap()/dot11/beacon/essid/rsn

frame.show()
print("\nHexdump of frame:")
hexdump(frame)

sendp(frame, iface=iface, inter=0.100, loop=1, monitor=True)
