from django.db import models

# TODO Add appropriate max length

class RoadSegment(models.Model):
    id = models.AutoField(primary_key=True)
    coordinates = models.CharField(max_length=255)
    fra_meter = models.IntegerField()
    fylke = models.IntegerField()
    srid = models.IntegerField()
    hp = models.IntegerField()
    href = models.CharField(max_length=255)
    kategori = models.CharField(max_length=255)
    kommune = models.IntegerField()
    konnekteringslenke = models.BooleanField()
    kortform = models.CharField(max_length=255)
    medium = models.CharField(max_length=255)
    startdato = models.CharField(max_length=255)
    nummer = models.IntegerField()
    region = models.IntegerField()
    sluttnode = models.CharField(max_length=255)
    sluttposisjon = models.FloatField()
    startnode = models.IntegerField()
    startposisjon = models.FloatField()
    status = models.CharField(max_length=255)
    strekningslengde = models.IntegerField()
    temakode = models.IntegerField()
    til_meter = models.IntegerField()
    typeveg = models.CharField(max_length=255)
    vegavdeling = models.IntegerField()
    veglenkeid = models.IntegerField()
    vrefkortform = models.CharField(max_length=255)

