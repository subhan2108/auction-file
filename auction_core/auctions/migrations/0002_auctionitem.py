# Generated by Django 5.1.5 on 2025-06-26 06:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('sold', 'Sold'), ('closed', 'Closed')], default='active', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
