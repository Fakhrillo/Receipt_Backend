# Generated by Django 4.2.5 on 2023-09-25 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_checks_worker_alter_docs_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checks',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.workers'),
        ),
        migrations.AlterField(
            model_name='docs',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.workers'),
        ),
    ]
