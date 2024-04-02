# Generated by Django 5.0.3 on 2024-04-01 15:44

import django.db.models.deletion
import mailings.methods
import timezone_field.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE SCHEMA IF NOT EXISTS content;",
            reverse_sql="DROP SCHEMA content;",
        ),
        migrations.CreateModel(
            name='MailingTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('source_code', models.TextField(blank=True, validators=[mailings.methods.validate_jinja2_syntax], verbose_name='html source code')),
            ],
            options={
                'verbose_name': 'Mailing template',
                'verbose_name_plural': 'Mailing templates',
                'db_table': 'content"."mailing_template',
            },
        ),
        migrations.CreateModel(
            name='MailingTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, default='', max_length=255, verbose_name='description')),
                ('timezone', timezone_field.fields.TimeZoneField(default='UTC', help_text='Timezone to Run the Cron Schedule on. Default is UTC.', use_pytz=False, verbose_name='cron timezone')),
                ('cron_expression', models.CharField(help_text='cron expression "MINUTE HOUR DAY MONTH DAY OF WEEK", for example: "* * * * *" (every minute), "30 6 * * *" (every day at 6:30), "0 12 * * 1-5" (at 12:00 on Monday through Friday); more details here: https://en.wikipedia.org/wiki/Cron', max_length=32, validators=[mailings.methods.validate_cron_expression], verbose_name='schedule')),
                ('crontab_schedule', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_celery_beat.crontabschedule', verbose_name='periodic task')),
                ('periodic_task', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_celery_beat.periodictask', verbose_name='periodic task')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mailings.mailingtemplate', verbose_name='template')),
            ],
            options={
                'verbose_name': 'Mailing task',
                'verbose_name_plural': 'Mailing tasks',
                'db_table': 'content"."mailing_task',
            },
        ),
    ]