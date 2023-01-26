# Generated by Django 4.1 on 2022-12-06 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodies', '0005_alter_order_telp_no_alter_ordermenu_order_stall_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='stall_id',
            new_name='stall',
        ),
        migrations.RenameField(
            model_name='ordermenu',
            old_name='menu_id',
            new_name='menu',
        ),
        migrations.RenameField(
            model_name='ordermenu',
            old_name='order_stall_id',
            new_name='order_stall',
        ),
        migrations.RenameField(
            model_name='orderstall',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderstall',
            old_name='stall_id',
            new_name='stall',
        ),
        migrations.AddField(
            model_name='orderstall',
            name='status',
            field=models.CharField(default='In Progress', max_length=20),
        ),
    ]
