# Generated by Django 5.0.4 on 2024-05-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caricamentoDati', '0002_customuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rivistaeccellente',
            old_name='isbn',
            new_name='issn1',
        ),
        migrations.AddField(
            model_name='rivistaeccellente',
            name='issn2',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]