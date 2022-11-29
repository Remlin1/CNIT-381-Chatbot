### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import routers
import monitor as monitor
import threading
import time
import myparamiko as m
import botSkills as skills
from ansible_playbook_runner import Runner


#Make the thread list
global threads
threads = list()

# Router Info 
device_address = routers.router1['host']
device_username = routers.router1['username']
device_password = routers.router1['password']

# RESTCONF Setup
port = '443'
url_base = "https://{h}/restconf".format(h=device_address)
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}

# Bot Details
bot_email = 'networkbot123@webex.bot'
teams_token = 'YjE2NWUyMzctNjg2Zi00OTA4LWFiZmMtOWNmMzcxYTgwYzEzNTJiNmM3OWMtMDQ0_P0A1_da087be3-a5c4-42e0-91c2-0fc6d3da3fdb'
bot_url = "https://8aa0-12-206-249-123.ngrok.io"
bot_app_name = 'Network Bot'

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

# Create a function to respond to messages that lack any specific command
# The greeting will be friendly and suggest how folks can get started.
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm a friendly CSR1100v assistant .  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response

def start_monitor(incoming_msg):

    response = Response()
    response.markdown = "Monitor starting..."
    #Start the thread for the monitor
    th = threading.Thread(target=monitor.run_monitor)
    threads.append(th)

    th.start()

    return response


def stop_monitor(incoming_msg):

    response = Response()
    response.markdown = "Stopping the monitor, please wait...\n" 
    monitor.monitor_flag = False
    for th in threads:
        th.join()
        del(th)
    time.sleep(5)
    return response

def show_versions(incoming_msg):
    response = Response()
    response.markdown = "Here is the version information for each router\n"
    response.markdown += "+++++++++++++++ R1 +++++++++++++++\n"
    with open(('router1_version.txt')) as f:
      cpu = f.read()
      f.close()
      response.markdown += cpu + " \n"
    
    response.markdown += "+++++++++++++++ R2 +++++++++++++++\n"
    with open(('router2_version.txt')) as f:
      mem = f.read()
      f.close()
    response.markdown += mem
    return response

def run_backup(incoming_msg):
    response = Response()
    response.markdown = "All Network Devices have been backed up"
    m.start_backup()
    return response

def R1_backup(incoming_msg):
    response = Response()
    with open(('R1backup.txt')) as f:
        response.markdown = f.read()
        f.close()
    return response

def R2_backup(incoming_msg):
    response = Response()
    with open(('R2backup.txt')) as f:
        response.markdown = f.read()
        f.close()
    return response

def Router_utilization(incoming_msg):
    response = Response()
    Runner(['inventory'],'ansibleutilization.yaml').run()
    response.markdown = "R1 CPU AND MEMORY UTILIZATION:\n"
    with open(('router1_cpu.txt')) as f:
        cpu = f.readline().strip('\n')
        f.close()
        response.markdown += "CPU -> " + cpu + "\n"
    with open(('router1_memory.txt')) as f:
        mem = f.readline().strip('\n')
        f.close()
    response.markdown += "Memory -> " + mem + "\n"

    response.markdown += "R2 CPU AND MEMORY UTILIZATION:\n"

    with open(('router2_cpu.txt')) as f:
        cpu = f.readline().strip('\n')
        f.close()
        response.markdown += "CPU -> " + cpu +"\n"
    with open(('router2_memory.txt')) as f:
        mem = f.readline().strip('\n')
        f.close()
    response.markdown += "Memory -> " + mem + "\n"

    return response

def nat_status(incoming_msg):
    response = Response()
    status1 = skills.get_status("R1")
    status2 = skills.get_status("R2")

    init1 = str(status1['ip-nat-statistics']['initialized'])
    hits1 = str(status1['ip-nat-statistics']["hits"])
    misses1 = str(status1['ip-nat-statistics']["misses"])

    response.markdown = "------------ R1 ------------\n"
    response.markdown += "Initialization Status:" + init1 + "\n"
    response.markdown +=  "Hits: " + hits1 + "\n"
    response.markdown += "Misses: " + misses1 + "\n"

    init2 = str(status2['ip-nat-statistics']['initialized'])
    hits2 = str(status2['ip-nat-statistics']["hits"])
    misses2 = str(status2['ip-nat-statistics']["misses"])
    response.markdown += "------------ R2 ------------\n"
    response.markdown += "Initialization Status:" + init2 + "\n"
    response.markdown +=  "Hits: " + hits2 + "\n"
    response.markdown += "Misses: " + misses2 + "\n"

    return response


# Set the bot greeting.
bot.set_greeting(greeting)

# Add Bot's Commmands
#bot.add_command(
    #"arp list", "See what ARP entries I have in my table.", arp_list)
bot.add_command("start monitor", "Start the monitor for automatic vpn configuration update",start_monitor)
bot.add_command("stop monitor", "Stop the running monitor", stop_monitor)
bot.add_command("Run Backups", "Run paramiko script to pull backup from all devices,",run_backup)
bot.add_command("Show R1 backup", "Show the saved backup config for R1", R1_backup)
bot.add_command("Show R2 backup", "Show the saved backup config for R2", R2_backup)
bot.add_command("Show version", "Show the running version of all routers", show_versions)
bot.add_command("show router utilization","Show the Memory and CPU stats of the routers", Router_utilization)
bot.add_command("show nat status", "Show's the nat status for R1 and R2", nat_status)
# Every bot includes a default "/echo" command.  You can remove it, or any
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
