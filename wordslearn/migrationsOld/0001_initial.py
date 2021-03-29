# Generated by Django 3.0.4 on 2020-12-19 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WordEng',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(help_text='Enter the word', max_length=200)),
                ('date_of_add', models.DateTimeField(auto_now=True, help_text='date added')),
                ('word_type', models.CharField(choices=[('noun', 'Noun'), ('verb', 'Verb'), ('adjective', 'Adjective'), ('adverb', 'Adverb'), ('preposition', 'Preposition'), ('Conjunctions', 'Conjunctions'), ('other', 'Other')], help_text='Select type of word', max_length=30)),
            ],
            options={
                'ordering': ['word'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WordPol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(help_text='Enter the word', max_length=200)),
                ('date_of_add', models.DateTimeField(auto_now=True, help_text='date added')),
                ('word_type', models.CharField(choices=[('Noun', 'rzeczownik'), ('Verb', 'czasownik'), ('Adjective', 'przymiotnik'), ('Adverb', 'przyslowek'), ('Preposition', 'przyimek'), ('Conjunctions', 'spójnik'), ('Other', 'inne')], help_text='Select type of word', max_length=30)),
                ('wordsEng', models.ManyToManyField(to='wordslearn.WordEng')),
            ],
            options={
                'ordering': ['word'],
                'abstract': False,
            },
        ),
    ]