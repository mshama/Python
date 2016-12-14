# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-13 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseTable',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name_c', models.CharField(db_column='Name_C', max_length=50)),
                ('denomincation_c', models.CharField(db_column='Denomination_C', max_length=50)),
                ('datasource_c', models.CharField(db_column='DataSource_C', max_length=10)),
            ],
            options={
                'managed': False,
                'db_table': 'DatabaseTable',
            },
        ),
        migrations.CreateModel(
            name='DatabaseTable_DataSourceField_Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'DatabaseTable_Field_Mapping',
            },
        ),
        migrations.CreateModel(
            name='DatabaseTable_GoldenRecordField_Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'DatabaseTable_Field_Mapping',
            },
        ),
        migrations.CreateModel(
            name='DatasourceField',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name_c', models.CharField(db_column='Name_C', max_length=50)),
                ('data_source_c', models.CharField(db_column='data_source_c', max_length=10)),
                ('fieldtype_c', models.CharField(db_column='FieldType_C', max_length=50)),
                ('fieldparameters_c', models.CharField(db_column='FieldParameters_C', max_length=50)),
            ],
            options={
                'managed': False,
                'db_table': 'DatasourceField',
            },
        ),
        migrations.CreateModel(
            name='GoldenRecordField',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name_c', models.CharField(db_column='Name_C', max_length=50)),
                ('fieldtype_c', models.CharField(db_column='FieldType_C', max_length=50)),
                ('fieldparameters_c', models.CharField(db_column='FieldParameters_C', max_length=50)),
            ],
            options={
                'managed': False,
                'db_table': 'GoldenRecordField',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Currency_VW',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='Date_D')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Currency_VW',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Derivative_Bloomberg_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('px_last', models.DecimalField(db_column='PX_LAST', decimal_places=6, max_digits=12)),
                ('fut_cur_gen_ticker', models.CharField(db_column='FUT_CUR_GEN_TICKER', max_length=50)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Derivative_Bloomberg_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Derivative_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Derivative_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Derivative_DataStream_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('ps', models.DecimalField(db_column='PS', decimal_places=6, max_digits=12)),
                ('mp', models.DecimalField(db_column='MP', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Derivative_DataStream_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Derivative_VW',
            fields=[
                ('date', models.DateField(db_column='date_d', primary_key=True, serialize=False)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(auto_now=True, db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Derivative_VW',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Equity_Bloomberg_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('px_last', models.DecimalField(db_column='PX_LAST', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Equity_Bloomberg_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Equity_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
                ('time_t', models.TimeField(db_column='time_t')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Equity_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Equity_DataStream_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('p', models.DecimalField(db_column='P', decimal_places=6, max_digits=12)),
                ('p_ib', models.DecimalField(db_column='[P.IB]', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Equity_DataStream_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Equity_VW',
            fields=[
                ('date', models.DateField(db_column='date_d', primary_key=True, serialize=False)),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(blank=True, db_column='time_t', null=True)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Equity_VW',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Fixed_Income_Bloomberg_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('key_rate_dur_6mo', models.DecimalField(db_column='Key_Rate_Dur_6MO', decimal_places=6, max_digits=12)),
                ('key_rate_dur_1yr', models.DecimalField(db_column='Key_Rate_Dur_1YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_2yr', models.DecimalField(db_column='Key_Rate_Dur_2YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_3yr', models.DecimalField(db_column='Key_Rate_Dur_3YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_4yr', models.DecimalField(db_column='Key_Rate_Dur_4YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_5yr', models.DecimalField(db_column='Key_Rate_Dur_5YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_6yr', models.DecimalField(db_column='Key_Rate_Dur_6YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_7yr', models.DecimalField(db_column='Key_Rate_Dur_7YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_8yr', models.DecimalField(db_column='Key_Rate_Dur_8YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_9yr', models.DecimalField(db_column='Key_Rate_Dur_9YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_10yr', models.DecimalField(db_column='Key_Rate_Dur_10YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_15yr', models.DecimalField(db_column='Key_Rate_Dur_15YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_20yr', models.DecimalField(db_column='Key_Rate_Dur_20YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_25yr', models.DecimalField(db_column='Key_Rate_Dur_25YR', decimal_places=6, max_digits=12)),
                ('key_rate_dur_30yr', models.DecimalField(db_column='Key_Rate_Dur_30YR', decimal_places=6, max_digits=12)),
                ('dur_adj_oas_mid', models.DecimalField(db_column='DUR_ADJ_OAS_MID', decimal_places=6, max_digits=12)),
                ('px_last', models.DecimalField(db_column='PX_LAST', decimal_places=6, max_digits=12)),
                ('px_dirty_bid', models.DecimalField(db_column='PX_DIRTY_BID', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Fixed_Income_Bloomberg_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Fixed_Income_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('eod_price_dirty_n', models.DecimalField(db_column='EOD_Price_Dirty_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_6mo_n', models.DecimalField(db_column='Key_Rate_Dur_6Mo_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_1yr_n', models.DecimalField(db_column='Key_Rate_Dur_1YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_2yr_n', models.DecimalField(db_column='Key_Rate_Dur_2YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_3yr_n', models.DecimalField(db_column='Key_Rate_Dur_3YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_4yr_n', models.DecimalField(db_column='Key_Rate_Dur_4YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_5yr_n', models.DecimalField(db_column='Key_Rate_Dur_5YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_6yr_n', models.DecimalField(db_column='Key_Rate_Dur_6YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_7yr_n', models.DecimalField(db_column='Key_Rate_Dur_7YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_8yr_n', models.DecimalField(db_column='Key_Rate_Dur_8YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_9yr_n', models.DecimalField(db_column='Key_Rate_Dur_9YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_10yr_n', models.DecimalField(db_column='Key_Rate_Dur_10YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_15yr_n', models.DecimalField(db_column='Key_Rate_Dur_15YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_20yr_n', models.DecimalField(db_column='Key_Rate_Dur_20YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_25yr_n', models.DecimalField(db_column='Key_Rate_Dur_25YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_30yr_n', models.DecimalField(db_column='Key_Rate_Dur_30YR_n', decimal_places=6, max_digits=12)),
                ('effective_duration_n', models.DecimalField(db_column='Effective_Duration_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Fixed_Income_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Fixed_Income_DataStream_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('cmpm', models.DecimalField(db_column='CMPM', decimal_places=6, max_digits=12)),
                ('gp', models.DecimalField(db_column='GP', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Fixed_Income_DataStream_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Fixed_Income_VW',
            fields=[
                ('date', models.DateField(db_column='date_d', primary_key=True, serialize=False)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('eod_price_dirty_n', models.DecimalField(db_column='EOD_Price_Dirty_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_6mo_n', models.DecimalField(db_column='Key_Rate_Dur_6Mo_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_1yr_n', models.DecimalField(db_column='Key_Rate_Dur_1YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_2yr_n', models.DecimalField(db_column='Key_Rate_Dur_2YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_3yr_n', models.DecimalField(db_column='Key_Rate_Dur_3YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_4yr_n', models.DecimalField(db_column='Key_Rate_Dur_4YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_5yr_n', models.DecimalField(db_column='Key_Rate_Dur_5YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_6yr_n', models.DecimalField(db_column='Key_Rate_Dur_6YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_7yr_n', models.DecimalField(db_column='Key_Rate_Dur_7YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_8yr_n', models.DecimalField(db_column='Key_Rate_Dur_8YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_9yr_n', models.DecimalField(db_column='Key_Rate_Dur_9YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_10yr_n', models.DecimalField(db_column='Key_Rate_Dur_10YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_15yr_n', models.DecimalField(db_column='Key_Rate_Dur_15YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_20yr_n', models.DecimalField(db_column='Key_Rate_Dur_20YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_25yr_n', models.DecimalField(db_column='Key_Rate_Dur_25YR_n', decimal_places=6, max_digits=12)),
                ('key_rate_dur_30yr_n', models.DecimalField(db_column='Key_Rate_Dur_30YR_n', decimal_places=6, max_digits=12)),
                ('effective_duration_n', models.DecimalField(db_column='Effective_Duration_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(auto_now=True, db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Fixed_Income_VW',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Index_Bloomberg_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('px_last', models.DecimalField(db_column='PX_LAST', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Index_Bloomberg_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Index_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Index_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Index_DataStream_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('pi', models.DecimalField(db_column='PI', decimal_places=6, max_digits=12)),
                ('ri', models.DecimalField(db_column='RI', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Index_DataStream_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_Index_VW',
            fields=[
                ('date', models.DateField(db_column='date_d', primary_key=True, serialize=False)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(auto_now=True, db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('eod_log_return_n', models.FloatField(db_column='EOD_Log_Return_N')),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_Index_VW',
            },
        ),
        migrations.CreateModel(
            name='MarketData_InterestRate_Bloomberg_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('px_last', models.DecimalField(db_column='PX_LAST', decimal_places=6, max_digits=12)),
                ('dur_adj_mid', models.DecimalField(db_column='DUR_ADJ_MID', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_InterestRate_Bloomberg_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_InterestRate_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('modified_duration_n', models.DecimalField(db_column='Modified_Duration_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_InterestRate_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_InterestRate_DataStream_C',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date_d')),
                ('dm', models.DecimalField(db_column='DM', decimal_places=6, max_digits=12)),
                ('ir', models.DecimalField(db_column='IR', decimal_places=6, max_digits=12)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_InterestRate_DataStream_C',
            },
        ),
        migrations.CreateModel(
            name='MarketData_InterestRate_VW',
            fields=[
                ('date', models.DateField(db_column='date_d', primary_key=True, serialize=False)),
                ('modified_duration_n', models.DecimalField(db_column='Modified_Duration_n', decimal_places=6, max_digits=12)),
                ('eod_price_n', models.DecimalField(db_column='EOD_Price_n', decimal_places=6, max_digits=12)),
                ('time_t', models.TimeField(auto_now=True, db_column='time_t')),
                ('intraday_price_n', models.DecimalField(db_column='Intraday_Price_n', decimal_places=6, max_digits=12)),
                ('intra_log_return_n', models.FloatField(db_column='Intra_Log_Return_N')),
            ],
            options={
                'managed': False,
                'db_table': 'MarketData_InterestRate_VW',
            },
        ),
        migrations.CreateModel(
            name='MarketDataField_Mapping',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('valid_from_d', models.DateField(db_column='valid_from_d')),
                ('valid_to_d', models.DateField(blank=True, db_column='valid_to_d', null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'MarketDataField_Mapping',
            },
        ),
    ]
