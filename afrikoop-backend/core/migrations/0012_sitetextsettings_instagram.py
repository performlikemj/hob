from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0011_volunteergroup_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitetextsettings',
            name='instagram_url',
            field=models.URLField(blank=True, help_text='Full URL to your Instagram profile (e.g., https://instagram.com/yourhandle)'),
        ),
    ]

