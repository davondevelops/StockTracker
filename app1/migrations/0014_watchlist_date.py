# Generated by Django 2.2.4 on 2021-03-07 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_auto_20210305_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='date',
            field=models.CharField(max_length=20, null=True),
        ),
    ]