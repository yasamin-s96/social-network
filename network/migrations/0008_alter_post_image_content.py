# Generated by Django 5.0.1 on 2024-01-20 17:49

import utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_post_text_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_content',
            field=models.ImageField(blank=True, upload_to='posts/%Y/%m/%d', validators=[utils.validators.validate_image]),
        ),
    ]
