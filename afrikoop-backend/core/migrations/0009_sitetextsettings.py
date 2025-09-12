from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_volunteertier'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteTextSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_label_en', models.CharField(blank=True, default='Home', max_length=50)),
                ('home_label_ja', models.CharField(blank=True, default='ホーム', max_length=50)),
                ('events_label_en', models.CharField(blank=True, default='Events', max_length=50)),
                ('events_label_ja', models.CharField(blank=True, default='イベント', max_length=50)),
                ('cleaning_label_en', models.CharField(blank=True, default='Cleaning Service', max_length=50)),
                ('cleaning_label_ja', models.CharField(blank=True, default='清掃サービス', max_length=50)),
                ('cleaning_short_en', models.CharField(blank=True, default='Cleaning', max_length=50)),
                ('cleaning_short_ja', models.CharField(blank=True, default='清掃', max_length=50)),
                ('login_en', models.CharField(blank=True, default='Login', max_length=50)),
                ('login_ja', models.CharField(blank=True, default='ログイン', max_length=50)),
                ('register_en', models.CharField(blank=True, default='Register', max_length=50)),
                ('register_ja', models.CharField(blank=True, default='登録', max_length=50)),
                ('logout_en', models.CharField(blank=True, default='Logout', max_length=50)),
                ('logout_ja', models.CharField(blank=True, default='ログアウト', max_length=50)),
                ('browse_events_en', models.CharField(blank=True, default='Browse events', max_length=60)),
                ('browse_events_ja', models.CharField(blank=True, default='イベントを見る', max_length=60)),
                ('learn_more_en', models.CharField(blank=True, default='Learn more', max_length=60)),
                ('learn_more_ja', models.CharField(blank=True, default='詳しく見る', max_length=60)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Text Settings',
                'verbose_name_plural': 'Site Text Settings',
            },
        ),
    ]

