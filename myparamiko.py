import paramiko
import time
import ast
from yaml import safe_load
from netmiko import ConnectHandler

def get_list_from_file(filename):
    with open(filename) as f:
        data = ast.literal_eval(f.read())
        f.close()
        return data

def connect(router_info):
    connection = ConnectHandler(**router_info)
	prompt = connection.find_prompt()
	if ">" in prompt:
		connection.enable()
	return connection

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command):
    print(f'Sending command: {command}')
    shell.send(command + '\n')
    #time.sleep(timeout)  

def show(shell, command, n=10000, timeout = 1):
    shell.send('terminal length 0\n')
    shell.send(command + '\n')
    time.sleep(timeout)
    output = shell.recv(n)
    output = output.decode()
    return output

def backup(router):
	client = connect(**router)
        shell = get_shell(client)
        file = show(shell, "show run")
        with open(router_name + 'backup.txt', 'w') as f:
		f.write(file)
        	f.close()
        

def close(ssh_client):    
    if ssh_client.get_transport().is_active() == True:
        print('Closing connection')
        ssh_client.close()

if __name__ == '__main__':
    router1 = {'server_ip': '192.168.122.10', 'server_port': '22', 'user':'cisco', 'passwd':'cisco', 'router_name':'R1'}
    client = connect(**router1)
    shell = get_shell(client)

    send_command(shell, 'enable')
    send_command(shell, 'cisco') # this is the enable password
    send_command(shell, 'term len 0')
    send_command(shell, 'sh version')
    send_command(shell, 'sh ip int brief')
    get_list_from_file('routers.txt')




