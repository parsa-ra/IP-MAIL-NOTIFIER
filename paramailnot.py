# Author: Parsa Noshafagh

import subprocess 
import re 
import os 
from datetime import datetime
import sys
import json


root_dir = "/var/log/"
ip_file = "paraMailNot.tmp"
log_file_name = "paraMailNot_logs.log"
api_key = "your api key"
your_mail = "yourmail@yourdomain"
your_mail_name = "yourname"

def iso_curr_time():
    return datetime.now().isoformat() 


def write_ips(ip_match):
    try:
        with open(root_dir + ip_file, 'w') as file:
            for ip in ip_match:
                file.write(ip+'\n')

            file.close()
            to_log_file("Successfully ips written to log file")
    
    except:
        to_log_file("Something went wrong writing ips")

def to_log_file(msg: str):
    # this function will write the message to log file    
    time = iso_curr_time() 
    with open(root_dir + log_file_name, 'a') as file: 
        file.write(time + "\t" + msg + "\n")
        file.close()

def connect():
    """ This function will try to connect to the internet through the authentication method which your 
    University Provide.
    I scrap the login webpage to see input forums to check id of the username password inputs. in my case 
    It was the simply username and password. fill the following fields in POST request corresponding to your 
    data and login URL 

    
    Returns:
        [type] -- [description]
    """
    for iter in range(3):
        try: 
            curl_out = subprocess.check_output(["curl", 
            "--data", 
            "username=YOUR_USERNAME&password=YOUR_PASSWORD", 
            "https://net2.sharif.edu/login"])
            curl_out_str = str(curl_out)
        
            # Check if login was successfull 
            loggin_list = re.findall(r'You\sare\slogged\sin', curl_out_str)

            if len(loggin_list) > 0:
                to_log_file("Successfully Connected") 
                return True
            else: 
                to_log_file("Connection Failed Try #%d"%(iter))
        except:
            to_log_file("Connection Try #%d Failed" % (iter)) 


# Init Log File
if not os.path.exists(root_dir + log_file_name):
    with open(root_dir+ log_file_name, 'w') as file:
        file.write("%s \tInit ParaMailNot Logfile at\n" %(iso_curr_time()))
        file.close()

ifconf_out = subprocess.check_output(["ifconfig"])
ifconf_out_str = str(ifconf_out) 

# Check internet connectivity
chk_connec_str = ""
try:
    chk_connec = subprocess.check_output(["ping", "-c", "5", "google.com"])
    chk_connec_str = str(chk_connec) 
except: 
    to_log_file("Seems Not having Internet Connectivity, will try to connect")
    chk_loggedin = connect()
    if not chk_loggedin:
        to_log_file("Connection Failed")
        sys.exit(0)
    #print("Seems not having internet connectivity")
    

ping_time = re.findall(r'time=\d', chk_connec_str)
if len(ping_time) == 0:
    to_log_file("Can't Ping Google, will retry to connect")
    chk_loggedin = connect()
    if not chk_loggedin:
        to_log_file("Connection Failed")
        sys.exit(0)

# Find the Ip Addresses from the output of the ifconfig command
ip_match = re.findall(r'inet\saddr:[\w+.+]+', ifconf_out_str)

# Checking if the IPs not changed from previous runs
SEND_MAIL = True #True 
if os.path.exists(root_dir + ip_file):
    # print("Path Exists") 
    # Loading File
    with open(root_dir + ip_file, 'r') as file:
        perv_ips = file.read().splitlines()
        # Checking if the ips are the same in this run
        # print(perv_ips)
        if  perv_ips == ip_match: 
            to_log_file("Same Ips No need to resend mail")
            SEND_MAIL = False
        else:
            write_ips(ip_match)
else: 
    to_log_file("No ip file is found will write them to ip file and later send them")
    write_ips(ip_match)


if SEND_MAIL: 
    try: 
        lis = "" 
        # Generating unordered list of IPs 
        for ip in ip_match: 
            lis += "<ul>" + ip.split()[1] + "</ul>"

        sending_meta = '{ "sender":{"name":"IPStatus","email":"Labserver@gmail.com"},"to":[  {  "email":"%s", "name":"%s" }], "subject":"IP Status","htmlContent":"<html><head></head><body><p>IP Status,</p> <ul> %s </ul> </body></html>" }' % (your_mail, your_mail_name ,lis)
        send_mail_res = subprocess.check_output([
            "curl",
            "--request",
            "POST",
            "--url", "https://api.sendinblue.com/v3/smtp/email",
            "--header", "accept:application/json",
            "--header", "api-key:{}".format(api_key), 
            "--header", "content-type:application/json", 
            "--data", sending_meta
        ])
        
        error_mail = re.findall(r'error', str(send_mail_res))
        if len(error_mail) > 0:
            to_log_file("Something Went Wrong Sending Mail")
    except:   
        to_log_file("Something Went Wrong Sending Mail")
        #print("Something Went Wrong")


    to_log_file(str(send_mail_res))


#print(ip_match)