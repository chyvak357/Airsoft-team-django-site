# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# TODO use models from  events module 
class DOrgnizatios(models.Model):
    idorg = models.AutoField(db_column='idORG', primary_key=True)
    nameorg = models.CharField(db_column='nameORG', max_length=128)
    short_nameorg = models.CharField(db_column='short_nameORG', max_length=128)
    innorg = models.CharField(db_column='innORG', unique=True, max_length=10)
    ogrnorg = models.CharField(db_column='ogrnORG', unique=True, max_length=13)

    class Meta:
        managed = False
        db_table = 'D_ORGNIZATIOS'


class MainValues(models.Model):
    idval = models.AutoField(db_column='idVAL', primary_key=True)
    value_nameval = models.CharField(db_column='value_nameVAL', max_length=128)
    valueval = models.IntegerField(db_column='valueVAL')
    dateval = models.DateField(db_column='dateVAL')
    value_measureval = models.CharField(db_column='value_measureVAL', max_length=45)
    orgid = models.ForeignKey(DOrgnizatios, models.DO_NOTHING, db_column='orgID')
    created_atval = models.DateTimeField(db_column='created_atVAL', blank=True, null=True)
    start_timeval = models.DateTimeField(db_column='start_timeVAL', blank=True, null=True)
    end_timeval = models.DateTimeField(db_column='end_timeVAL', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MAIN_VALUES'