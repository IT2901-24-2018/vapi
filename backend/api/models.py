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
    time = models.DateTimeField()
    startlat = models.FloatField()
    startlong = models.FloatField()
    endlat = models.FloatField()
    endlong = models.FloatField()
    torrsprederaktiv = models.BooleanField()
    plogaktiv = models.BooleanField()
    vatsprederaktiv = models.BooleanField()
    materialtype_kode = models.BooleanField()
    from_vegref = models.CharField(max_length=22)
    to_vegref = models.CharField(max_length=22)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)


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


class DummyModel(BaseModel):
    the_geom = models.LineStringField(srid=32633)
