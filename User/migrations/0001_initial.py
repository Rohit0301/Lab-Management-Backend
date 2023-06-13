# Generated by Django 4.2.2 on 2023-06-12 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=100)),
                ('email_id', models.CharField(default='', max_length=100)),
                ('password', models.TextField(default='', max_length=300)),
            ],
        ),
    ]
