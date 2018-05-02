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
    county = models.IntegerField(help_text="County identifier.  Example: 50")
    href = models.CharField(max_length=150, help_text="Link to NVDB for this unique segment")
    category = models.CharField(max_length=4, help_text="Road segment category. Example: K")
    municipality = models.IntegerField(help_text="Municipality number for that county."
                                       "Example: 01 for Trondheim")
    startdate = models.DateField(help_text="Start date for the road segment. Example: 2018-04-20")
    region = models.IntegerField(help_text="Region number. Example: 4")
    status = models.CharField(max_length=4, help_text="Road status. Example: G")
    stretchdistance = models.IntegerField(help_text="Length of the road segment. Example 31")
    typeofroad = models.CharField(max_length=100, help_text="A description of the road type. Example: gangOgSykkelvei")
    roadsectionid = models.IntegerField(help_text="Unique identifier for the road segment. Example: 171712")
    vrefshortform = models.CharField(max_length=255, help_text="A combination of multiple fields. "
                                     "Example: 5001 Kg97587 hp1 m349-380")
    the_geom = models.LineStringField(help_text="Linestring according to ISO 19162:2015. "
                                      "Example: SRID=4326;LINESTRING (10.37634290477487 63.3478716972899, "
                                      "10.37656821856063 63.34786722088941)")


class ProductionData(BaseModel):
    time = models.DateTimeField()
    startlat = models.FloatField()
    startlong = models.FloatField()
    closest_point = models.PointField()
    endlat = models.FloatField()
    endlong = models.FloatField()
    dry_spreader_active = models.NullBooleanField()
    plow_active = models.NullBooleanField()
    wet_spreader_active = models.NullBooleanField()
    brush_active = models.NullBooleanField()
    material_type_code = models.IntegerField(null=True)
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
