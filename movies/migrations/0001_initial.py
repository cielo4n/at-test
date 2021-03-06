# Generated by Django 2.1 on 2018-08-29 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, default='', max_length=500)),
                ('imdb_code', models.CharField(blank=True, default='', max_length=200)),
                ('title', models.CharField(max_length=500)),
                ('title_english', models.CharField(blank=True, default='', max_length=500)),
                ('title_long', models.CharField(blank=True, default='', max_length=500)),
                ('slug', models.SlugField(blank=True, default='', max_length=500)),
                ('year', models.IntegerField()),
                ('rating', models.FloatField()),
                ('runtime', models.IntegerField(default=0)),
                ('summary', models.TextField()),
                ('description_full', models.TextField(blank=True, default='')),
                ('synopsis', models.TextField(blank=True, default='')),
                ('yt_trailer_code', models.CharField(blank=True, default='', max_length=200)),
                ('language', models.CharField(blank=True, default='', max_length=200)),
                ('mpa_rating', models.CharField(blank=True, default='', max_length=200)),
                ('background_image', models.CharField(blank=True, default='', max_length=500)),
                ('background_image_original', models.CharField(blank=True, default='', max_length=500)),
                ('small_cover_image', models.CharField(blank=True, default='', max_length=500)),
                ('medium_cover_image', models.CharField(blank=True, default='', max_length=500)),
                ('large_cover_image', models.CharField(blank=True, default='', max_length=500)),
                ('status', models.CharField(blank=True, default='', max_length=200)),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('date_uploaded_unix', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, default='', max_length=500)),
                ('hash', models.CharField(blank=True, default='', max_length=500)),
                ('quality', models.CharField(blank=True, default='', max_length=200)),
                ('seeds', models.IntegerField()),
                ('peers', models.IntegerField()),
                ('size', models.CharField(blank=True, default='', max_length=200)),
                ('size_bytes', models.IntegerField()),
                ('date_uploaded', models.DateTimeField(auto_now=True)),
                ('date_uploaded_unix', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
    ]
