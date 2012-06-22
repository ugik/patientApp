from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Patient(models.Model):
    user = models.OneToOneField(User) # import User
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True, verbose_name='e-mail')
    cell = models.CharField(max_length=10, blank=True, verbose_name='cell #')
    created = models.DateField(editable=False)
    updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if not 'force_update' in kwargs:
            kwargs['force_update'] = False
        if not self.id:
            self.created = datetime.date.today()
        self.updated = datetime.datetime.today()
        super(Patient, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Entry(models.Model):
    entry = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    patient = models.ForeignKey('Patient')
    created = models.DateField(editable=False)

    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if not 'force_update' in kwargs:
            kwargs['force_update'] = False
        if not self.id:
            self.created = datetime.date.today()
        self.updated = datetime.datetime.today()
        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s (patient id:%s)' % (self.entry, self.patient)


