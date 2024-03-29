# Generated by Django 4.2.6 on 2023-11-21 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycatalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AlterField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(related_name='product', to='mycatalog.specification'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='product', to='mycatalog.tag'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='images_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mycatalog.product'),
        ),
    ]
