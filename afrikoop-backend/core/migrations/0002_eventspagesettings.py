from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsPageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(blank=True, default='Upcoming Events', max_length=200)),
                ('title_ja', models.CharField(blank=True, default='イベント情報', max_length=200)),
                ('subtitle_en', models.TextField(blank=True, default='Join community gatherings, volunteer days, and workshops. New dates drop regularly — check back soon!')),
                ('subtitle_ja', models.TextField(blank=True, default='コミュニティイベント、ボランティア、ワークショップなど。最新情報をお見逃しなく！')),
                ('hero_image', models.ImageField(blank=True, upload_to='events/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Events Page Settings',
                'verbose_name_plural': 'Events Page Settings',
            },
        ),
    ]

