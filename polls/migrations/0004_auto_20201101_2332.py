# Generated by Django 3.1.1 on 2020-11-01 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_vote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='qestion',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
    ]
