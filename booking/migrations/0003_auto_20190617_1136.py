# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_restaurant_total_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
    ]
