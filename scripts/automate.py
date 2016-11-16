#!/usr/bin/python

# Test issueing ios commands.

from netmiko import ConnectHandler

def main():

    # Get switch address.
    #print
    #ip = raw_input('Device IP: ')
    #print

    # Iterate through all the switches in the file.
    with open('switches.txt', 'r') as f:
        for ip in f:

            # Switch definition.
            switch = {
                'device_type': 'cisco_ios',
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
            ssh_connection.config_mode()

            # Execute configuration command(s).
            ssh_connection.send_command('no logging monitor')

            # Exit configuration mode.
            ssh_connection.exit_config_mode()

            # Execute non-configuration command(s).
            ssh_connection.send_command('write')
            output1 = ssh_connection.send_command('show conf | inc logging')
            print
            print "--------------------------------------------------------------------------------"
            print prompt
            print output1
            print "--------------------------------------------------------------------------------"

            # Close SSH connection
            ssh_connection.disconnect()

if __name__ == "__main__":
    main()

