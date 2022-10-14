# Generated by Django 4.0.5 on 2022-10-13 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_id', models.SlugField(max_length=70)),
                ('short_description', models.TextField()),
                ('further_information', models.TextField(null=True)),
                ('requirements', models.TextField()),
                ('references', models.TextField(null=True)),
                ('category_url', models.CharField(max_length=50)),
                ('next_page', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea_name', models.CharField(max_length=200)),
                ('idea_id', models.SlugField(max_length=70)),
                ('brief_description', models.TextField()),
                ('technology', models.TextField()),
                ('implementation_steps', models.TextField(null=True)),
                ('teacher_effort', models.TextField()),
                ('recommendations', models.TextField()),
                ('resources', models.TextField()),
                ('testimony', models.TextField(null=True)),
                ('use_cases', models.TextField()),
                ('references', models.TextField(null=True)),
                ('reusable', models.TextField(null=True)),
                ('task_complexity', models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlanCategoryOnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(max_length=500, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_category_onlide_idea_category', to='tbcore.category')),
                ('idea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan_category_onlide_idea_i', to='tbcore.onlineidea')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_category_onlide_idea_plan', to='tbcore.plan')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryOnlineIdea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tbcore.category')),
                ('online_idea', models.ManyToManyField(to='tbcore.onlineidea')),
            ],
        ),
        migrations.AddConstraint(
            model_name='plancategoryonlineidea',
            constraint=models.UniqueConstraint(fields=('plan', 'category', 'idea'), name='plancategoryonlineidea_constraint'),
        ),
        migrations.AddConstraint(
            model_name='plan',
            constraint=models.UniqueConstraint(fields=('plan_name', 'user'), name='plan_constraint'),
        ),
    ]
