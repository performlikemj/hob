from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_alter_cleaningfeature_color'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('description', models.TextField(blank=True)),
                ('priority', models.PositiveIntegerField(default=0, help_text='Smaller number appears first')),
                ('active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('members', models.ManyToManyField(blank=True, related_name='volunteer_tiers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Volunteer Tier',
                'verbose_name_plural': 'Volunteer Tiers',
                'ordering': ['priority', 'name'],
            },
        ),
    ]

