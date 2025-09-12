from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_eventspagesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPlaceholder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=200)),
                ('title_ja', models.CharField(blank=True, max_length=200)),
                ('description_en', models.TextField(blank=True)),
                ('description_ja', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='events/placeholders/')),
                ('cta_label_en', models.CharField(blank=True, max_length=100)),
                ('cta_label_ja', models.CharField(blank=True, max_length=100)),
                ('cta_url', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placeholders', to='core.eventspagesettings')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]

