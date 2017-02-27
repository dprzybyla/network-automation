#!/usr/bin/ python

# Update each Device object such that each Device 
# links to the correct Credentials. At this time
# we only have standard credentials.

import django
import sys, os        # Required to set PATH and environmental variables.

# Add the path to the manage.py executable.
sys.path.append("/root/local-automation/network")

# Tell django the location of the settings file.
os.environ['DJANGO_SETTINGS_MODULE'] = 'network.settings'

def main():
    django.setup()

    # Once django set up with environmental variables, import models.
    from devices.models import Device, Credentials

    devices = Device.objects.all()
    creds = Credentials.objects.all()

    standard_creds = creds[0]

    for a_device in devices:
        a_device.credentials = standard_creds    # Link credentials to each device.
        a_device.save()                          # Save database changes.

    for a_device in devices:
        print a_device, a_device.credentials

if __name__ == "__main__":
    main()

