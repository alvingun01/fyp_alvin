# Generated by Django 4.1 on 2022-11-14 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodies', '0004_stall_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='telp_no',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='ordermenu',
            name='order_stall_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='foodies.orderstall'),
        ),
        migrations.AlterField(
            model_name='orderstall',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stalls', to='foodies.order'),
        ),
    ]
