# Generated by Django 4.2.5 on 2024-11-10 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_product_photo_url_product_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='product_photos/'),
        ),
    ]