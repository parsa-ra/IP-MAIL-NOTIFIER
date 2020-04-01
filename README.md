# What is this? 
Assume that your university have a Web login in order for you to access the internet from devices on the universities network. There is high probability that the connected devices to network will be assigned different IPs over time, due to DHCP reset or something like that.

How you can know access your workstation(Over SSH or any other remote protocol) which is probably currently run a training task XD When there is IP change event. of course you can check the entire network for your username & password but this is cumbersome.

Another way is to setup a service which will check regularly for IP change and mail to you if the ip doesn't match previous ones, this Script do this for you. For sending mail you should utilize some external or internal SMTP server. 

In this script I will use the sendinblue service and their generous 300 mail free a day offer. you could use any SMTP service provider with or without API. you can even send them from the local machine but it's probably categorized as spam. 

This is just Proof of Concept, I think it can be improved alot. the Remote Machine Running Ubuntu 16.04 LTS. 


# TD;DR
A service for sending mail on event of IP change(the main script will be running every 2 hours check .timer unit ) in your working remote machine.


# Setup Process

* Modify the paramailnot.py and fill the authentication variables.
* Compile the paramailnot.py with compile.py script this will create compiled code on the ```__pycache__``` directory copy and paste it to current working directory.
* Run the setup.sh file. This will put the service files in correct directories(for example systemd directory).
* Make the paramailnot.sh file executable with: 
    ```
        sudo chmod + /usr/local/bin/paramailnot.sh
    ```
# Make the shell file executable
```
    sudo chmod +x /usr/local/bin/paramailnot.sh
```

# Sample Received Mail
Here is a mail that me and my friend received when the IP changed. 

<img src="./sample.png" height="400px"/>


# Monitoring 
You can check the log files and temporary IP addresses from previous runs at /var/log directory. 
* with tail command:
    ```
        tail /var/log/paraMailNot_logs.log 
    ```


