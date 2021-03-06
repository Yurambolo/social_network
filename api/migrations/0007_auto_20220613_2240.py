# Generated by Django 3.2.8 on 2022-06-13 19:40
import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_post_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now()),
            preserve_default=False,
        ),
    ]
