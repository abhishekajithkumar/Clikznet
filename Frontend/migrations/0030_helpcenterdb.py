# Generated by Django 3.2.10 on 2023-12-24 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0029_auto_20231224_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpCenterDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Issue', models.CharField(blank=True, max_length=50, null=True)),
                ('Details', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Frontend.registerdb')),
            ],
        ),
    ]
