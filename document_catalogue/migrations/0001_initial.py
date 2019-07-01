# Generated by Django 2.2.2 on 2019-06-21 07:14

import constrainedfilefield.fields.file
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import document_catalogue.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='document_catalogue.DocumentCategory')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.SmallIntegerField(default=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('file', constrainedfilefield.fields.file.ConstrainedFileField(content_types=('application/pdf', 'image/png', 'image/jpg', 'image/jpeg'), max_length=200, max_upload_size=10485760, mime_lookup_length=4096, upload_to=document_catalogue.models.document_upload_path_callback)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document_catalogue.DocumentCategory')),
                ('user', models.ForeignKey(on_delete=models.SET(1), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('category', 'sort_order'),
            },
        ),
    ]