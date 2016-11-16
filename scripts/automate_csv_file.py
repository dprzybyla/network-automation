#!/usr/bin/python

# Input switch data from csv file to support multiple device types.

import csv
from netmiko import ConnectHandler
from datetime import datetime

def main():

    # Get device file..
    print
    f = raw_input('Device File: ')
    print

    start_time = datetime.now()

    # Iterate through the switches.
    switchFile = open(f)
    switchReader = csv.reader(switchFile)
    for row in switchReader:
        device_type = row[0]
        ip = row[1]

        # Switch definition.
        switch = {
            'device_type': device_type,
            'ip': ip,
            'username': 'admin',
            'password': 'gh#$1paM',
            'secret': 'Bbn#pau4'
        }    

        # Log into switch.
        ssh_connection = ConnectHandler(**switch)

        # Enter enable mode.
        ssh_connection.enable()

        # Get the command prompt to identify the switch.
        prompt = ssh_connection.find_prompt() + "\n"

        # Enter config mode.
        #ssh_connection.config_mode()

        # Execute configuration command(s).
        #ssh_connection.send_command('no logging monitor')

        # Execute multiple configuration commands.
        #commands = ['no logging console', 'no logging monitor']
        #ssh_connection.send_config_set(commands)

        # Exit configuration mode.
        #ssh_connection.exit_config_mode()

        # Execute non-configuration command(s).
        #ssh_connection.send_command('write')
        output1 = ssh_connection.send_command('show mac address-table | inc 0023.24ae.e975')
        print
        print "--------------------------------------------------------------------------------"
        print prompt
        print output1
        print "--------------------------------------------------------------------------------"

        # Exit enable mode. Arista switches generate error if we don't do this.
        ssh_connection.exit_enable_mode()

        # Close SSH connection
        ssh_connection.disconnect()

    elapsed_time = datetime.now() - start_time
    print "Elapsed time: {}".format(elapsed_time)

if __name__ == "__main__":
    main()

