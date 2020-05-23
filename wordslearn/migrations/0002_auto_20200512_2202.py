# Generated by Django 3.0.4 on 2020-05-12 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordslearn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordpol',
            name='word_type',
            field=models.CharField(choices=[('Noun', 'rzeczownik'), ('Verb', 'czasownik'), ('Adjective', 'przymiotnik'), ('Adverb', 'przyslowek'), ('Other', 'inne')], help_text='Select type of word', max_length=30),
        ),
    ]