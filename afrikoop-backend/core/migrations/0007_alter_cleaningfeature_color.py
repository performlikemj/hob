from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_cleaning_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cleaningfeature',
            name='color',
            field=models.CharField(
                blank=True,
                choices=[('primary', 'Primary (Magenta/Rose)'), ('accent', 'Accent (Gold)'), ('secondary', 'Secondary (Teal)')],
                help_text='Optional brand color for the bullet dot. Leave blank to use Primary.',
                max_length=20,
            ),
        ),
    ]

