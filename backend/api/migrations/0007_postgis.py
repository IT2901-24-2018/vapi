from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0006_auto_20180409_1309'),
    ]

    operations = [
        CreateExtension('postgis'),
    ]
