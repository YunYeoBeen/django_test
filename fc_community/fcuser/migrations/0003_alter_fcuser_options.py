# Generated by Django 3.2.6 on 2021-09-05 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fcuser', '0002_alter_fcuser_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fcuser',
            options={'verbose_name': '패스트캠퍼스 사용자', 'verbose_name_plural': '패스트캠퍼스 사용자'},
        ),
    ]