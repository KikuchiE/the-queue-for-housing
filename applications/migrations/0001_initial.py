# Generated by Django 5.1.7 on 2025-03-17 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_number', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('UNDER_REVIEW', 'Under Review'), ('VERIFIED', 'Verified'), ('IN_QUEUE', 'In Queue'), ('HOUSING_OFFERED', 'Housing Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('EXPIRED', 'Expired')], default='DRAFT', max_length=20)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('current_address', models.TextField()),
                ('is_homeless', models.BooleanField(default=False)),
                ('current_residence_condition', models.CharField(choices=[('GOOD', 'Good'), ('ADEQUATE', 'Adequate'), ('POOR', 'Poor'), ('UNSAFE', 'Unsafe')], max_length=50)),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_veteran', models.BooleanField(default=False)),
                ('is_single_parent', models.BooleanField(default=False)),
                ('waiting_years', models.PositiveSmallIntegerField(default=0)),
                ('current_living_area', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('has_disability', models.BooleanField(default=False)),
                ('disability_details', models.TextField(blank=True)),
                ('adults_count', models.PositiveSmallIntegerField(default=1)),
                ('children_count', models.PositiveSmallIntegerField(default=0)),
                ('elderly_count', models.PositiveSmallIntegerField(default=0)),
                ('priority_score', models.IntegerField(default=0)),
                ('queue_position', models.PositiveIntegerField(blank=True, null=True)),
                ('documents_valid_until', models.DateField(blank=True, null=True)),
                ('document_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('UNDER_REVIEW', 'Under Review'), ('VERIFIED', 'Verified'), ('IN_QUEUE', 'In Queue'), ('HOUSING_OFFERED', 'Housing Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('EXPIRED', 'Expired')], max_length=20)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('new_status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('UNDER_REVIEW', 'Under Review'), ('VERIFIED', 'Verified'), ('IN_QUEUE', 'In Queue'), ('HOUSING_OFFERED', 'Housing Offered'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('EXPIRED', 'Expired')], max_length=20)),
                ('change_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
    ]
