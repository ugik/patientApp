from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from Crypto.Cipher import Blowfish
import binascii
import datetime


class EncryptedString(str):
    """A subclass of string so it can be told whether a string is
       encrypted or not (if the object is an instance of this class
       then it must [well, should] be encrypted)."""
    pass
1
class BaseEncryptedField(models.Field):
    def __init__(self, *args, **kwargs):
        cipher = kwargs.pop('cipher', 'AES')
        imp = __import__('Crypto.Cipher', globals(), locals(), [cipher], -1)
        self.cipher = getattr(imp, cipher).new(settings.SECRET_KEY[:32])
        models.Field.__init__(self, *args, **kwargs)
        
    def to_python(self, value):
        return self.cipher.decrypt(binascii.a2b_hex(str(value))).split('\0')[0]
    
    def get_db_prep_value(self, value):
        if value is not None and not isinstance(value, EncryptedString):
            padding  = self.cipher.block_size - len(value) % self.cipher.block_size
            if padding and padding < self.cipher.block_size:
                value += "\0" + ''.join([random.choice(string.printable) for index in range(padding-1)])
            value = EncryptedString(binascii.b2a_hex(self.cipher.encrypt(value)))
        return value

class EncryptedTextField(BaseEncryptedField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self): 
        return 'TextField'
    
    def formfield(self, **kwargs):
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super(EncryptedTextField, self).formfield(**defaults)

class EncryptedCharField(BaseEncryptedField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"
    
    def formfield(self, **kwargs):
        defaults = {'max_length': self.max_length}
        defaults.update(kwargs)
        return super(EncryptedCharField, self).formfield(**defaults)



GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Patient(models.Model):
    user            = models.OneToOneField(User)    # import User
    name          = models.CharField(max_length=100)
    birthday      = models.DateField()
    gender        = models.CharField(max_length=1, choices=GENDER_CHOICES) 
    email           = models.EmailField(blank=True, verbose_name='e-mail')
    cell              = models.CharField(max_length=10, blank=True, verbose_name='cell #')
    created       = models.DateField(editable=False)
    updated      = models.DateTimeField(editable=False)

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
    entry          = models.CharField(max_length=15)
    description  = EncryptedTextField(blank=True)
    patient        = models.ForeignKey('Patient')
    created       = models.DateField(editable=False)

    def _get_desc(self):
        enc_obj = Blowfish.new( settings.SECRET_KEY )
        return u"%s" % enc_obj.decrypt( binascii.a2b_hex(self.description).rstrip())

    def _set_desc(self, desc_value):
        enc_obj = Blowfish.new( settings.SECRET_KEY )
        repeat = 8 - (len( desc_value ) % 8)
        desc_value = desc_value + " " * repeat
        self.description = binascii.b2a_hex(enc_obj.encrypt( desc_value ))

    desc = property(_get_desc, _set_desc)

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
        return u'%s (%s)' % (self.entry, self.desc)



