from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_eventplaceholder'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleaningservicepage',
            name='cta_en',
            field=models.CharField(blank=True, default='Tell us your schedule and property details — we’ll get back with a quote.', max_length=200),
        ),
        migrations.AddField(
            model_name='cleaningservicepage',
            name='cta_ja',
            field=models.CharField(blank=True, default='日程と物件情報をお知らせください。お見積もりをご連絡します。', max_length=200),
        ),
        migrations.CreateModel(
            name='CleaningFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_en', models.CharField(max_length=200)),
                ('text_ja', models.CharField(blank=True, max_length=200)),
                ('color', models.CharField(blank=True, help_text='Optional token e.g. primary/accent/secondary', max_length=20)),
                ('order', models.PositiveIntegerField(default=0)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='core.cleaningservicepage')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]

