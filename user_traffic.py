import re
from operator import itemgetter
from netmiko import Netmiko
from getpass import getpass
i = 1
userlist = []
gig = 1024**3
meg = 1024**2
data = ''

un = input('Username: ')
pw = getpass('Password: ')
ip = input('IP address: ')

device = {
      'host': ip,
      'username': un,
      'password': pw,
      'device_type': 'cisco_asa',
        }
try:
    net_conn = Netmiko(**device)
    print('Connected to:',  ip)
    data = net_conn.send_command('show vpn- anyconnect')
    net_conn.cleanup()
    net_conn.disconnect()
    print('Closed connection to device')
except Exception as e:
    print(e)


lines = data.splitlines()
for line in lines:
    userstats = []
    if re.match('\AUser', line):
        userline = line.split()
        user = ' '
        for x in userline:
            if x != 'Index':
                user = user + ' ' + x
            elif x == 'Index':
                break


    if re.match('\ABytes', line):
        tx = int(line.split()[3])
        rx = int(line.split()[7])
        userstats = [user, tx, rx, rx+tx]
        userlist.append(userstats)

sortedlist = sorted(userlist, key=itemgetter(3), reverse=True)

with open(ip+'.txt', 'w') as output:
    for item in sortedlist:
        if item[3] > gig:
            string = (str(i)+'- '+item[0]+'  Volume of traffic: '+ str(item[3]/(gig))+ ' GBytes')
            print(string)
            output.write(string+'\n')
        else:
            string = (str(i)+'- '+item[0]+'  Volume of traffic: '+ str(item[3]/(meg))+ ' MBytes')
            print(string)
            output.write(string+'\n')
        i+=1
