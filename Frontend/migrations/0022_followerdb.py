# Generated by Django 4.2.4 on 2023-11-23 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0021_likedb'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FollowerId', models.IntegerField(blank=True, null=True)),
                ('FollowingId', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]