from django.db import models


class RoadSegment(models.Model):
    id = models.AutoField(primary_key=True)
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
    # geometry_type = models.CharField()
    # geometry_coordinates_
