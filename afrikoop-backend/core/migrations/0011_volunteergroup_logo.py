from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_volunteergroup_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteergroup',
            name='logo',
            field=models.ImageField(blank=True, upload_to='volunteers/groups/'),
        ),
    ]

