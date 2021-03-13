# Generated by Django 2.2.4 on 2021-01-11 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_vault'),
    ]

    operations = [
        migrations.CreateModel(
            name='stockVault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=5)),
                ('sector', models.CharField(max_length=55)),
                ('open', models.DecimalField(decimal_places=2, max_digits=7)),
                ('high', models.DecimalField(decimal_places=2, max_digits=7)),
                ('low', models.DecimalField(decimal_places=2, max_digits=7)),
                ('close', models.DecimalField(decimal_places=2, max_digits=7)),
                ('previous_close', models.DecimalField(decimal_places=2, max_digits=7)),
                ('volume', models.IntegerField()),
                ('float', models.IntegerField()),
                ('catalyst', models.CharField(max_length=55)),
                ('lookUpDate', models.DateField()),
                ('year_high', models.DecimalField(decimal_places=2, max_digits=7)),
                ('year_low', models.DecimalField(decimal_places=2, max_digits=7)),
                ('market_cap', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='is_buy',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='catalyst',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='close',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='float',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='high',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='lookupdate',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='low',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='market_cap',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='open',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='previous_close',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='volume',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='year_high',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='year_low',
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='buy_or_short',
            field=models.CharField(default='buy', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stockHistory', to='app1.User'),
        ),
        migrations.AddField(
            model_name='vault',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='vault', to='app1.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='watchlist',
            name='stock',
            field=models.ManyToManyField(default={}, related_name='watchlist', to='app1.Stock'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='entry',
            field=models.DecimalField(decimal_places=3, max_digits=7),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='exit',
            field=models.DecimalField(decimal_places=3, max_digits=7),
        ),
        migrations.AddField(
            model_name='vault',
            name='stock',
            field=models.ManyToManyField(default={}, related_name='vault', to='app1.stockVault'),
        ),
    ]