from django.contrib.gis.db import models


class BaseModel(models.Model):
    """
    Abstract model with auto-increment id and created and updated fields that
    are automatically set and updated.
    """
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RoadSegment(BaseModel):
    from_meter = models.IntegerField()
    county = models.IntegerField()
    hp = models.IntegerField()
    href = models.CharField(max_length=150)
    category = models.CharField(max_length=4)
    municipality = models.IntegerField()
    connlink = models.BooleanField()
    shortform = models.CharField(max_length=255)
    medium = models.CharField(max_length=4)
    startdate = models.CharField(max_length=50)
    number = models.IntegerField()
    region = models.IntegerField()
    endnode = models.CharField(max_length=255)
    endposition = models.FloatField()
    startnode = models.CharField(max_length=100)
    startposition = models.FloatField()
    status = models.CharField(max_length=4)
    stretchdistance = models.IntegerField()
    themecode = models.IntegerField()
    to_meter = models.IntegerField()
    typeofroad = models.CharField(max_length=100)
    roadsection = models.IntegerField()
    roadsectionid = models.IntegerField()
    vrefshortform = models.CharField(max_length=255)
    the_geom = models.LineStringField()


class ProductionData(BaseModel):
    time = models.DateTimeField()
    startlat = models.FloatField()
    startlong = models.FloatField()
    endlat = models.FloatField()
    endlong = models.FloatField()
    dry_spreader_active = models.NullBooleanField()
    plow_active = models.NullBooleanField()
    wet_spreader_active = models.NullBooleanField()
    brush_active = models.NullBooleanField()
    material_type_code = models.IntegerField(null=True)
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
