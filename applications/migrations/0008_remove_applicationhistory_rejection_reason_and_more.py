# Generated by Django 5.1.7 on 2025-03-27 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_application_is_for_ward_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationhistory',
            name='rejection_reason',
        ),
        migrations.AddField(
            model_name='application',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('SUBMITTED', 'Submitted'), ('IN_QUEUE', 'In Queue'), ('HOUSING_OFFERED', 'Housing Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED_BY_APPLICANT', 'Rejected by Applicant'), ('REJECTED_BY_MANAGER', 'Rejected by Manager')], default='SUBMITTED', max_length=30),
        ),
        migrations.AlterField(
            model_name='applicationhistory',
            name='new_status',
            field=models.CharField(choices=[('SUBMITTED', 'Submitted'), ('IN_QUEUE', 'In Queue'), ('HOUSING_OFFERED', 'Housing Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED_BY_APPLICANT', 'Rejected by Applicant'), ('REJECTED_BY_MANAGER', 'Rejected by Manager')], max_length=30),
        ),
        migrations.AlterField(
            model_name='applicationhistory',
            name='previous_status',
            field=models.CharField(choices=[('SUBMITTED', 'Submitted'), ('IN_QUEUE', 'In Queue'), ('HOUSING_OFFERED', 'Housing Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED_BY_APPLICANT', 'Rejected by Applicant'), ('REJECTED_BY_MANAGER', 'Rejected by Manager')], max_length=30),
        ),
    ]
