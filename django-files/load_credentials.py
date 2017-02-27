#!/usr/bin/python

# Add device login credentials to the database.

import django
import sys, os        # Required to set PATH and environmental variables.

# Add the path to the manage.py executable.
sys.path.append("/root/local-automation/network")

# Tell django the location of the settings file.
os.environ['DJANGO_SETTINGS_MODULE'] = 'network.settings'

def main():
    django.setup()

    # Once django set up with environmental variables, import models.
    from devices.models import Credentials

    standard_credentials = Credentials.objects.get_or_create(
        description = 'standard',
        username = 'admin',
        password = 'XXXXXX',
        secret = 'XXXXXX'
    )
    print standard_credentials

#    x = Credentials.objects.get(username='admin')
#    x.delete()
    
    # Verify credentials that currently exist
    print
    all_credentials = Credentials.objects.all()
    for a_credential in all_credentials:
        print a_credential
    print

if __name__ == "__main__":
    main()
