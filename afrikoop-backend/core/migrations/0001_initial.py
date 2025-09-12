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
            name='MissionPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(blank=True, max_length=200)),
                ('title_ja', models.CharField(blank=True, max_length=200)),
                ('body_en', models.TextField(blank=True)),
                ('body_ja', models.TextField(blank=True)),
                ('hero_image', models.ImageField(blank=True, upload_to='mission/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Mission Page',
                'verbose_name_plural': 'Mission Pages',
            },
        ),
        migrations.CreateModel(
            name='CleaningServicePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(blank=True, max_length=200)),
                ('title_ja', models.CharField(blank=True, max_length=200)),
                ('description_en', models.TextField(blank=True)),
                ('description_ja', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='cleaning/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cleaning Service Page',
                'verbose_name_plural': 'Cleaning Service Pages',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=200)),
                ('title_ja', models.CharField(max_length=200)),
                ('description_en', models.TextField(blank=True)),
                ('description_ja', models.TextField(blank=True)),
                ('start_datetime', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=200)),
                ('capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['start_datetime'],
            },
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
        migrations.CreateModel(
            name='TranslatableString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.CharField(db_index=True, default='common', max_length=50)),
                ('key', models.CharField(db_index=True, max_length=100)),
                ('language', models.CharField(choices=[('en', 'English'), ('ja', '日本語')], db_index=True, max_length=10)),
                ('text', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Translatable String',
                'verbose_name_plural': 'Translatable Strings',
                'ordering': ['namespace', 'key', 'language'],
                'unique_together': {('namespace', 'key', 'language')},
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='core.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'event')},
            },
        ),
    ]

