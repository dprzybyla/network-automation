#!/usr/bin/python

# Input switch data from a django database and execute command(s).

import django
import sys, os                                          # Required to set PATH and environmental variables.
from getpass import getpass                             # Input from keyboard without an echo.
from netmiko import ConnectHandler                      # Create an ssh connection to a device.
from multiprocessing import Process, current_process    # Multiprocessing functions.
from datetime import datetime                           # Used to measure elapsed time.
from pyping import ping                                 # Provides the ping command.

# Add the path to the manage.py executable.
sys.path.append("/root/local-automation/network")

# Tell django the location of the settings file.
os.environ['DJANGO_SETTINGS_MODULE'] = 'network.settings'

def my_command(device):
    # Log into device.
    ssh_connection = ConnectHandler(**device)

    # Enter enable mode.
    ssh_connection.enable()

    # Get the command prompt to identify the device.
    prompt = ssh_connection.find_prompt() + "\n"

    # Enter config mode.
    #ssh_connection.config_mode()

    # Execute configuration command(s), separated by a comma.
    #ssh_connection.send_command('no logging monitor')

    # Execute multiple configuration commands.
    #commands = ['no logging console', 'no logging monitor']
    #ssh_connection.send_config_set(commands)

    # Exit configuration mode.
    #ssh_connection.exit_config_mode()

    # Execute non-configuration command(s).
    #ssh_connection.send_command('write')
    output1 = ssh_connection.send_command('sh run | inc vlan 202')

    # Only print command result if there is output.
    if output1:
        print
        print "--------------------------------------------------------------------------------"
        print prompt
        print output1
        print "--------------------------------------------------------------------------------"

    # Exit enable mode. Arista switches generate error if we don't do this.
    ssh_connection.exit_enable_mode()

    # Close SSH connection
    ssh_connection.disconnect()


def main():
    django.setup()

    # Once django set up with environmental variables, import models.
    from devices.models import Device, Credentials

    # Start counting the elapsed time to run the command(s).
    start_time = datetime.now()

    # Create an empty list to hold the processes.
    processes = []

    # Get all the devices from the django database.
    all_devices = Device.objects.all()

    # Iterate through the devices.
    for a_device in all_devices:
        creds = a_device.credentials
        ip = a_device.ip_address

        device = {
            'device_type': a_device.os_type,
            'ip': a_device.ip_address,
            'username': creds.username,
            'password': creds.password,
            'secret': creds.secret
        }

        # Check whether the switch is up with a ping.
        pingstatus = ping(ip)
        #print pingstatus.ret_code

        # If the switch is up, execute the desired command(s).
        if pingstatus.ret_code == 0:
            my_process = Process(target=my_command, args=(device,))    # Spawn a process to run the command(s).
            my_process.start()                                         # Start the process.
            processes.append(my_process)                               # Add the process to the list of processes.

    # End the processes.
    for a_process in processes:
        #print a_process
        a_process.join()                                               # Process completes, return to main thread.

    # Determine how long it took to run the command(s).
    elapsed_time = datetime.now() - start_time
    print "Elapsed time: {}".format(elapsed_time)

if __name__ == "__main__":
    main()

