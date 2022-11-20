### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import routers
import monitor as monitor
import threading
import time


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
bot_url = "https://0d5f-12-206-249-123.ngrok.io"
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
        th.terminate()
        del(th)
    time.sleep(5)
    return response



# Set the bot greeting.
bot.set_greeting(greeting)

# Add Bot's Commmands
#bot.add_command(
    #"arp list", "See what ARP entries I have in my table.", arp_list)
bot.add_command("start monitor", "Start the monitor for automatic vpn configuration update",start_monitor)
bot.add_command("stop monitor", "Stop the running monitor", stop_monitor)
# Every bot includes a default "/echo" command.  You can remove it, or any
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
