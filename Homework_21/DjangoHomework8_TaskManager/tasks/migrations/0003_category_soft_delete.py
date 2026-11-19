from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_homework9_meta_and_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="Удалена"),
        ),
        migrations.AddField(
            model_name="category",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Дата удаления",
            ),
        ),
    ]
