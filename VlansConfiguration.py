import getpass
import telnetlib

f = open('myaccesspoints.txt')
user = input("Enter your remote account: ")
password = getpass.getpass()

for IP in f:
    print('Configuring Access Point ' + str(IP))
    HOST = IP.strip('\n')
    print(HOST)
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b"configure terminal\n")
    for n in range (1,3):
        tn.write(b"dot11 ssid SSID_" + str(n).encode('ascii') + "\n")
        tn.write(b"vlan " + str(n).encode('ascii') + "\n")
        tn.write(b"authentication open\n")
        tn.write(b"mbssid guest-mode\n")
        tn.write(b"exit\n")
# codigo para la asignacion de las VLANs a la interface Dot11radio0
# codigo para la asignacion de las subinterfaces para la interface Dot11radio0
# codigo para la asignacion de las subinterfaces para la interface Fastethernet0
    tn.write(b"end\n")
    tn.write(b"write\n")
    tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
