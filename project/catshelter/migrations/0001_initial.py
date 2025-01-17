# Generated by Django 4.2.4 on 2024-05-25 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userfullname', models.CharField(max_length=225, primary_key=True, serialize=False)),
                ('useremail', models.CharField(max_length=225)),
                ('userphone', models.IntegerField()),
                ('status', models.CharField(default='Active', max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('username', models.CharField(max_length=225, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=225)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catshelter.user')),
            ],
        ),
    ]
