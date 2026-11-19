from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="category",
            table="task_manager_category",
        ),
        migrations.AlterModelTable(
            name="task",
            table="task_manager_task",
        ),
        migrations.AlterModelTable(
            name="subtask",
            table="task_manager_subtask",
        ),
        migrations.AlterField(
            model_name="subtask",
            name="title",
            field=models.CharField(
                max_length=200,
                unique=True,
                verbose_name="Название подзадачи",
            ),
        ),
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["name"],
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="task",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
            },
        ),
        migrations.AlterModelOptions(
            name="subtask",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "SubTask",
                "verbose_name_plural": "SubTasks",
            },
        ),
    ]
