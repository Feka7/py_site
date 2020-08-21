# Generated by Django 3.0.5 on 2020-08-21 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200710_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(blank=True, max_length=30, null=True)),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
    ]
