# Generated by Django 5.0.1 on 2024-01-21 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_follows_alter_user_saved_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='saved_posts',
        ),
    ]
