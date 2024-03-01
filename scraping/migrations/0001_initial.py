# Generated by Django 5.0.2 on 2024-03-01 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Licitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('modalidade', models.CharField(max_length=100)),
                ('comprador', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Itens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('unidade', models.CharField(max_length=50)),
                ('quantidade', models.IntegerField()),
                ('valor', models.CharField(max_length=50)),
                ('licitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.licitacao')),
            ],
        ),
    ]