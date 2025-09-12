from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_eventimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleaningGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cleaning/gallery/')),
                ('caption_en', models.CharField(blank=True, max_length=200)),
                ('caption_ja', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='core.cleaningservicepage')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]

