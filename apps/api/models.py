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
    county = models.IntegerField(help_text="County identifier.")
    href = models.CharField(max_length=150, help_text="Link to NVDB for this unique segment")
    category = models.CharField(max_length=4, help_text="Road segment category.")
    municipality = models.IntegerField(help_text="Municipality number for that county.")
    startdate = models.DateField(help_text="Start date for the road segment.")
    region = models.IntegerField(help_text="Region number.")
    status = models.CharField(max_length=4, help_text="Road status.")
    stretchdistance = models.IntegerField(help_text="Length of the road segment.")
    typeofroad = models.CharField(max_length=100, help_text="A description of the road type.")
    roadsectionid = models.IntegerField(help_text="Unique identifier for the road segment.")
    vrefshortform = models.CharField(max_length=255, help_text="A combination of multiple fields.")
    the_geom = models.LineStringField(help_text="Linestring according to ISO 19162:2015.")


class ProductionData(BaseModel):
    time = models.DateTimeField(help_text="When the production data was generated.")
    startlat = models.FloatField(help_text="Start latitude.")
    startlong = models.FloatField(help_text="Start longitute.")
    endlat = models.FloatField(help_text="End latitude.")
    endlong = models.FloatField(help_text="End longitude.")
    dry_spreader_active = models.NullBooleanField(help_text="Dry spreader active boolean. Optional.")
    plow_active = models.NullBooleanField(help_text="Plow boolean. Optional.")
    wet_spreader_active = models.NullBooleanField(help_text="Wet spreader boolean. Optional.")
    brush_active = models.NullBooleanField(help_text="Brush boolean. Optional.")
    material_type_code = models.IntegerField(null=True, help_text="Material type boolean. Optional")
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, help_text="Segment ID to mapped segment. "
                                "Will be autocompleted by the code. Enter dummy value.")
