import getpass
import telnetlib

f = open('myaccesspoints.txt')
user = input("Enter your remote account: ")
password = getpass.getpass()
numeroinicio = int(input("Ingrese el numero inicial de la vlans: "))
numerofinal = int(input("Ingrese el numero final de la vlans: ")) + 1
numeronativo = int(input("Ingrese el numero nativo para las vlans: "))

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
    #tn.write(b"enable\n")
    #tn.write(b"class\n")
    tn.write(b"configure terminal\n")
    if numeroinicio <= numeronativo < numerofinal:
        for n in range (numeroinicio,numerofinal):
            tn.write(b"dot11 ssid JPSSID_" + str(n).encode("ascii") + b"\n")
#            tn.write(b"dot11 ssid SSID_" + str(n).encode('ascii') + "\n")
            tn.write(b"vlan " + str(n).encode('ascii') + b"\n")
            tn.write(b"authentication open" + b"\n")
            tn.write(b"mbssid guest-mode" + b"\n")
            tn.write(b"exit\n")
    #codigo para la asigancion de vlans a la interface dot11radio
            tn.write(b"interface dot11radio 0\n")
            tn.write(b"mbssid\n")
            tn.write(b"ssid JPSSID_" + str(n).encode('ascii') + b"\n")
            tn.write(b"exit\n")
    #codigo para la asiganacion de las subinterfaces para la interface dot11radio
            tn.write(b"interface dot11radio 0." + str(n).encode('ascii') + b"\n")
            if n == numeronativo:
                tn.write(b"encap dot1q " + str(n).encode('ascii') + b" native\n")
            else:
                tn.write(b"encap dot1q " + str(n).encode('ascii') + b"\n")
            tn.write(b"exit\n")
    #codigo para la asigancion de subinterfaces para la interface fastethernet
            tn.write(b"interface fastethernet 0." + str(n).encode('ascii') + b"\n")
            if n == numeronativo:
                tn.write(b"encap dot1q " + str(n).encode('ascii') + b" native\n")
            else:
                tn.write(b"encap dot1q " + str(n).encode('ascii') + b"\n")
            tn.write(b"exit\n")
    #Levantar interface wifi
        tn.write(b"int dot11radio 0\n")
        tn.write(b"no shut\n")
        tn.write(b"exit\n")
    tn.write(b"end\n")
    tn.write(b"write\n")
    tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
