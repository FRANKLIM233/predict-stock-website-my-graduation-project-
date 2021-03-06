# Generated by Django 3.1.2 on 2021-06-10 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('msg', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='msg',
            options={'ordering': ('-create_at',), 'verbose_name': '反馈管理', 'verbose_name_plural': '反馈管理'},
        ),
        migrations.AlterField(
            model_name='msg',
            name='content',
            field=models.TextField(verbose_name='反馈内容'),
        ),
        migrations.CreateModel(
            name='Liuyan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='留言内容')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '留言管理',
                'verbose_name_plural': '留言管理',
                'ordering': ('-create_at',),
            },
        ),
    ]
