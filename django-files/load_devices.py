#!/usr/bin/python

# Load new devices into the database.

import django
import sys, os        # Required to set PATH and environmental variables.

# Add the path to the manage.py executable.
sys.path.append("/root/local-automation/network")

# Tell django the location of the settings file.
os.environ['DJANGO_SETTINGS_MODULE'] = 'network.settings'

def main():
    django.setup()

    # Once django set up with environmental variables, import models.
    from devices.models import Device

    new_device1 = Device.objects.get_or_create(
        ip_address = '192.168.1.111',
        device_name = 'AAGC-Workroom-3560X-48P',
        os_type = 'cisco_ios',
        device_type = 'switch',
        vendor = 'Cisco'
    )
    
    # Verify devices that currently exist
    print
    all_devices = Device.objects.all()
    for a_device in all_devices:
        print a_device
    print

if __name__ == "__main__":
    main()
