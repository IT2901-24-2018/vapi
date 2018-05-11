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
    municipality = models.IntegerField(help_text="County and municipality number for that municipality."
                                       "Example: 5001 for Trondheim")
    startdate = models.DateField(help_text="Start date for the road segment. Example: 2018-04-20")
    region = models.IntegerField(help_text="Region number. Example: 4")
    status = models.CharField(max_length=4, help_text="Road status. Example: G")
    stretchdistance = models.IntegerField(help_text="Length of the road segment. Example 111")
    typeofroad = models.CharField(max_length=100, help_text="A description of the road type. Example: gangOgSykkelvei")
    roadsectionid = models.IntegerField(help_text="Unique identifier for the road segment. Example: 1205433")
    vrefshortform = models.CharField(max_length=255, help_text="A combination of multiple fields. "
                                     "Example: 5001 Kg1324 hp1 m0-111")
    the_geom = models.LineStringField(help_text="Linestring according to ISO 19162:2015. "
                                      "Example: SRID=32633;LINESTRING(271160.30566 7042104.25293,"
                                                "271164.5 7042102.1001,271167.6001 7042101.8999,"
                                                "271171.1001 7042102.69971,271177.1001 7042106.5,"
                                                "271182.69995 7042111.30029,271186.80005 7042115.5,"
                                                "271188.8999 7042118.5,271195.69995 7042124.0,"
                                                "271204.69995 7042131.19971,271213.6001 7042137.3999,"
                                                "271221.1001 7042142.6001,271227.3999 7042147.0,271230."
                                                "6001 7042148.3999,271234.5 7042147.6001,271239.8999 7042146.8999,"
                                                "271245.8999 7042147.3999,271249.69995 7042149.30029,"
                                                "271252.8 7042152.2)")


class ProductionData(BaseModel):
    time = models.DateTimeField()
    startlat = models.FloatField()
    startlong = models.FloatField()
    start_point = models.PointField()
    endlat = models.FloatField()
    endlong = models.FloatField()
    end_point = models.PointField()
    dry_spreader_active = models.NullBooleanField()
    plow_active = models.NullBooleanField()
    wet_spreader_active = models.NullBooleanField()
    brush_active = models.NullBooleanField()
    material_type_code = models.IntegerField(null=True)
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)


class WeatherData(BaseModel):
    start_time_period = models.DateTimeField()
    end_time_period = models.DateTimeField()
    county_and_municipality_id = models.IntegerField()
    value = models.IntegerField()
    unit = models.CharField(default='mm', max_length=2)
    degrees = models.IntegerField()
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
