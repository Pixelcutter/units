# Generated by Django 4.2.7 on 2023-12-13 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_alter_category_options_alter_category_owner_id_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='category',
            name='unique_category_name_owner',
        ),
    ]