# CNIT-381-Chatbot

### How to Install and Run:

For our testing purpose we have tested on a linux based virtual machine, however you can use whatever OS you see fit, but keep in mind the steps for initial setup may vary.

1. The following screenshot indicates all libraries that are going to need to be installed prior to running the chatbot. 

![alt text](https://github.com/Remlin1/CNIT-381-Chatbot/blob/main/readme_IMG/Imports.PNG "Imports")

2. A webex developer account will need to be created and keep note of the API token that you are given from webex.

3. Using the command "ngrok http 5000" will create a local server webook that you can use to interact with webex, keep track of your webhook URL.

4. In the webex.py file, change whats listed in the following screeshot to the data you wrote down in the previous steps

![alt_text](https://github.com/Remlin1/CNIT-381-Chatbot/blob/main/readme_IMG/BotRequirements.PNG "Requirements")

5. Update the IP addresses in the routers.py file to the addresses of your 

6. After downloading all files and adjusting the files as needed run with "python3 webexbot.py" and your bot will be functional and ready to go!

### Paramiko Skill:
This Skill was initially going to be an automated backup of the router once the VPN tunnel was setup again, but after running into some thread errors, it became a manual backup of the router.

### NETCONF/RESTCONF Skill:
This still utilises NETCONF to query both routers NETCONF interfaces and return information about NAT. It will then parse out the usefull information and format it in a way that is easily readable within Webex chat function.

### Ansible Skill:
For our ansible skill, we decided to try and view the health of the routers and ensure that they are operating at healthy levels. To do this, we use an ansible playbook to view the cpu and memory utilization. There is also another ansible playbook that is set up to show the current version and different license packages that is contained in the router to show the commands that the routers are capable of using. These playbooks then create files that the bot uses to form its response. The show version command will view the file showing the versioning for each device and the router utilization command will show the files shwoing the memroy and cpu utilization on each router.

### Monitoring Skill:
In a situation similar to the topology in the image below, a network may have a VPN over a leased tunnel, where one interface get's a DHCP address from the isp. Since this would break the VPN configuration on the otherside of the tunnel, the monitoring skill solves that. Every 10 seconds it checks to see if the IP address of the router has chagned, if it has changed then it runs an ansible playbook to update the VPN configuration with new address recieved from DHCP. The timer can be changed on the script if desired by simply changing the time function at the bottom of the script to be longer or shorter. The monitor skill will run in a seperate thread in the background of the bot, so other commands can still be run during that time.

![alt_text](https://github.com/Remlin1/CNIT-381-Chatbot/blob/main/readme_IMG/RouterExample.PNG "Requirements")
