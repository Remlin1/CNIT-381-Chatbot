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

### NETCONF/RESTCONF Skill:

### Ansible Skill:
For our ansible skill, we decided to try and view the health of the routers and ensure that they are operating at healthy levels. To do this, we use an ansible playbook to view the cpu and memory utilization. There is also another ansible playbook that is set up to show the current version and different license packages that is contained in the router to show the commands that the routers are capable of using. These playbooks then create files that the bot uses to form its response. The show version command will view the file showing the versioning for each device and the router utilization command will show the files shwoing the memroy and cpu utilization on each router.

### Monitoring Skill:
