# Generated by Django 5.2 on 2025-05-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('entertainment', 'Entertainment'), ('utilities', 'Utilities'), ('health', 'Health'), ('sales', 'Sales'), ('salary', 'Salary'), ('investment', 'Investment'), ('education', 'Education'), ('shopping', 'Shopping'), ('travel', 'Travel'), ('gifts', 'Gifts'), ('donations', 'Donations'), ('bills', 'Bills'), ('subscriptions', 'Subscriptions'), ('savings', 'Savings'), ('loans', 'Loans'), ('insurance', 'Insurance'), ('taxes', 'Taxes'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category_other',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
