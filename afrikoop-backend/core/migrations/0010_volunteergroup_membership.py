from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_sitetextsettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Volunteer Group',
                'verbose_name_plural': 'Volunteer Groups',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='VolunteerMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('member', 'Member'), ('lead', 'Lead'), ('coordinator', 'Coordinator')], default='member', max_length=20)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='core.volunteergroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Volunteer Membership',
                'verbose_name_plural': 'Volunteer Memberships',
            },
        ),
        migrations.AlterUniqueTogether(
            name='volunteermembership',
            unique_together={('user', 'group')},
        ),
    ]

