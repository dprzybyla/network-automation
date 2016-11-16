from __future__ import unicode_literals

from django.db import models

class Credentials(models.Model):
    username        = models.CharField(max_length=50)
    password        = models.CharField(max_length=50)
    secret          = models.CharField(max_length=50, blank=True, null=True)
    description     = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.username)

class NetworkDevice(models.Model):
    ip_address      = models.GenericIPAddressField(primary_key=True)
    device_name     = models.CharField(max_length=80)
    device_type     = models.CharField(max_length=50)
    port            = models.IntegerField(blank=True, null=True)
    vendor          = models.CharField(max_length=50, blank=True, null=True)
    model           = models.CharField(max_length=50, blank=True, null=True)
    os_version      = models.CharField(max_length=100, blank=True, null=True)
    serial_number   = models.CharField(max_length=50, blank=True, null=True)
    credentials     = models.ForeignKey(Credentials, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.ip_address)
