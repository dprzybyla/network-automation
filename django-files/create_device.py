#!/usr/bin/python

# Create new NetworkDevices in the database.

from devices.models import NetworkDevice
import django

def main():
    django.setup()

    new_device1 = NetworkDevice.objects.get_or_create(
        ip_address = '192.168.1.111',
        device_name = 'AAGC-Workroom-3560X-48P',
        device_type = 'cisco_ios',
        vendor = 'Cisco'
    )
    
    # Verify devices that currently exist
    print
    devices = NetworkDevice.objects.all()
    for a_device in devices:
        print a_device
    print

if __name__ == "__main__":
    main()
