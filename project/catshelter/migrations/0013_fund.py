# Generated by Django 4.2.4 on 2024-07-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catshelter', '0012_cat_gender_cat_health_condition_cat_neuter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]