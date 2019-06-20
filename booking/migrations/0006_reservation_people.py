# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_restaurant_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='people',
            field=models.IntegerField(default=1),
        ),
    ]
