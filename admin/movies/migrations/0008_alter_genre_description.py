# Generated by Django 4.2.11 on 2024-06-30 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0007_alter_filmwork_options_alter_genre_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="description"),
        ),
    ]