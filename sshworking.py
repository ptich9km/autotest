#!/usr/bin/python
import paramiko, time, os

#host = '192.168.0.8'
#user = 'login'
#secret = 'password'
#port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect(hostname=host, username=user, password=secret, port=port)
#stdin, stdout, stderr = client.exec_command('ls -l')
#data = stdout.read() + stderr.read()
#client.close()


# Connect to device using ssh
def ssh_connect_to_board(host, user, secret, port):
    try:
        Chost = host
        Cuser = user
        Csecret = secret
        Cport = port
        if (client.connect(hostname=Chost, username=Cuser, password=Csecret, port=Cport) == False):
            client.connect(hostname=Chost, username=Cuser, password=Csecret, port=Cport)
        return True
    except Exception as e:
        print("Error open ssh connection: " + str(e))
        return False

# Connect to device using ssh with number of try
def try_ssh_connect_to_board(count_of_Try):
    tryCount = count_of_Try
    connection = ssh_connect_to_board(host, user, secret, port)
    while tryCount > 0 and connection == False:
        connection = ssh_connect_to_board(host, user, secret, port)
        tryCount = tryCount - 1
        time.sleep(1)
    if tryCount == 0 and connection == False:
        print("Critical error in open ssh connection")
        exit()

# Close ssh connection
def ssh_close_connection():
    try:
        client.close()
        return True
    except Exception as e:
        print("Error close ssh connection: " + str(e))
        return False

# Write and read information
def ssh_write_and_read_info(command):
    try:
        lineState = 0
        stdin, stdout, stderr = client.exec_command('{}'.format(command))
        data = stdout.read() + stderr.read()
        print(data)
        if data != '':
            lineState = 1
    except Exception as e:
        print("There is a problem in reseting line state: " + str(e))
    return lineState

# Get info from ssh connection
def ssh_get_parameter(command):
    try:
        stdin, stdout, stderr = client.exec_command('{}'.format(command))
        data = stdout.read() + stderr.read()
        data = int(data)
    except Exception as e:
        print("There is a problem in reseting line state: " + str(e))
    return data

ssh_connect_to_board('192.168.7.1', 'root', 'p92YSjsi', 22)
time.sleep(1)
time.sleep(1)
get_proces_id = ssh_get_parameter('ps aux | grep "/sbin/kolind" | head -1 | awk \'{ print $1 }\'')
get_proces_id = str(get_proces_id)
f = open("result.txt", "a", encoding="utf8")

def start_working_night():

    for i in range(1,3000):
        print(i)
        time.sleep(1)
        os.system('curl -i -X POST 192.168.7.1:6000 -d "@OpenCheck.xml"')
        time.sleep(3)
        os.system('curl -i -X POST 192.168.7.1:6000 -d "@Document.xml"')
        time.sleep(3)
        os.system('curl -i -X POST 192.168.7.1:6000 -d "@FiscalStrings.xml"')
        time.sleep(3)
        os.system('curl -i -X POST 192.168.7.1:6000 -d "@CloseCheck.xml"')
        time.sleep(3)
        get_proces_memory = ssh_get_parameter('cat /proc/kolin/status | grep VmSize | awk \'{ print $2 }\''.replace('kolin', get_proces_id))

        f.write(str(get_proces_memory))
        f.write(str("\n"))
        time.sleep(1)

#os.system('curl -i -X POST 192.168.7.1:6000 -d "@CloseShift.xml"')
#os.system('curl -i -X POST 192.168.7.1:6000 -d "@OpenShift.xml"')
start_working_night()

f.close()
ssh_close_connection()




