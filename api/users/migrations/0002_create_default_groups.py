from django.db import migrations


def create_default_groups(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    group_model.objects.get_or_create(name='ADMIN')
    group_model.objects.get_or_create(name='ASISTENTE')


def remove_default_groups(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    group_model.objects.filter(name__in=['ADMIN', 'ASISTENTE']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_default_groups, remove_default_groups),
    ]
