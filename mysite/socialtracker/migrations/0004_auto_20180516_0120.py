# Generated by Django 2.0.4 on 2018-05-16 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialtracker', '0003_auto_20180516_0119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name_text',
            new_name='username',
        ),
    ]
