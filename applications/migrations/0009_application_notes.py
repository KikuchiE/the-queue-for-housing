# Generated by Django 5.1.7 on 2025-04-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_remove_applicationhistory_rejection_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
