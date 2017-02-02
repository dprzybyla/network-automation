#!/usr/bin/python

# Input switch data from csv file and execute command(s).
# The file includes the switch type, the login name, and the ip address.

from csv import reader                                  # Read a text file in csv formot.
from getpass import getpass                             # Input from keyboard without an echo.
from netmiko import ConnectHandler                      # Create an ssh connection to a device.
from multiprocessing import Process, current_process    # Multiprocessing functions.
from datetime import datetime                           # Used to measure elapsed time.
from pyping import ping                                 # Provides the ping command.

def my_command(switch):
    # Log into switch.
    ssh_connection = ConnectHandler(**switch)

    # Enter enable mode.
    ssh_connection.enable()

    # Get the command prompt to identify the switch.
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
    output1 = ssh_connection.send_command('sh run | inc vlan 31')

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
    # Get device csv file and passwords.
    print
    file = raw_input('Device File: ')
    login_password = getpass('Login Password: ')
    enable_password = getpass('Enable Password: ')
    print

    # Start counting the elapsed time to run the command(s).
    start_time = datetime.now()

    # Create an empty list to hold the processes.
    processes = []

    # Open the device file.
    switchFile = open(file)

    # Read the device csv file.
    switchReader = reader(switchFile)

    # Iterate through the switches. First read the comma separated values.
    for row in switchReader:
        device_type = row[0]
        username = row[1]
        ip = row[2]

        # Switch definition.
        switch = {
            'device_type': device_type,
            'ip': ip,
            'username': username,
            'password': login_password,
            'secret': enable_password
        }    

        # Check whether the switch is up with a ping.
        pingstatus = ping(ip)
        #print pingstatus.ret_code

        # If the switch is up, execute the desired command(s).
        if pingstatus.ret_code == 0:
            my_process = Process(target=my_command, args=(switch,))    # Spawn a process to run the command(s).
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

