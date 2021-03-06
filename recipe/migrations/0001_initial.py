# Generated by Django 3.1.2 on 2020-10-08 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('BREAD', 'Bread')], max_length=255, verbose_name='category')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('reference', models.CharField(blank=True, max_length=255, verbose_name='reference')),
                ('instructions_markdown', models.TextField(verbose_name='instructions')),
                ('instructions_html', models.TextField(blank=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
