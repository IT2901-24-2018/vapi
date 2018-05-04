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
    stretchdistance = models.IntegerField(help_text="Length of the road segment. Example 31")
    typeofroad = models.CharField(max_length=100, help_text="A description of the road type. Example: gangOgSykkelvei")
    roadsectionid = models.IntegerField(help_text="Unique identifier for the road segment. Example: 171712")
    vrefshortform = models.CharField(max_length=255, help_text="A combination of multiple fields. "
                                     "Example: 5001 Kg97587 hp1 m349-380")
    the_geom = models.LineStringField(help_text="Linestring according to ISO 19162:2015. "
                                      "Example: SRID=4326;LINESTRING (10.37634290477487 63.3478716972899, "
                                      "10.37656821856063 63.34786722088941)")


class ProductionData(BaseModel):
    time = models.DateTimeField(help_text="When the production data was generated. Example: 2016-11-04T08:45:15Z")
    startlat = models.FloatField(help_text="Start latitude. Example: 63.3870750023729")
    startlong = models.FloatField(help_text="Start longitute. Example: 10.3277250005425")
    endlat = models.FloatField(help_text="End latitude. Example: 63.3874419990294")
    endlong = models.FloatField(help_text="End longitude. Example: 10.3290930003037")
    dry_spreader_active = models.NullBooleanField(help_text="Dry spreader active boolean. Optional.")
    plow_active = models.NullBooleanField(help_text="Plow boolean. Optional.")
    wet_spreader_active = models.NullBooleanField(help_text="Wet spreader boolean. Optional.")
    brush_active = models.NullBooleanField(help_text="Brush boolean. Optional.")
    material_type_code = models.IntegerField(null=True, help_text="Material type boolean. Optional")
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, help_text="Segment ID to mapped segment. "
                                "Will be autocompleted by the code. Enter dummy value.")


class WeatherData(BaseModel):
    start_time_period = models.DateTimeField()
    end_time_period = models.DateTimeField()
    county_and_municipality_id = models.IntegerField()
    value = models.IntegerField()
    unit = models.CharField(max_length=2)
    degrees = models.IntegerField()
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
