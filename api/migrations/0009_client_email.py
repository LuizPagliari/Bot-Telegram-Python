# Generated by Django 4.2.5 on 2024-11-20 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=255, unique=True),
        ),
    ]
