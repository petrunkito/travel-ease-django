from django.db import migrations


def create_additional_groups(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    group_model.objects.get_or_create(name='GERENTE')
    group_model.objects.get_or_create(name='CLIENTE')


def remove_additional_groups(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')
    group_model.objects.filter(name__in=['GERENTE', 'CLIENTE']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_default_groups'),
    ]

    operations = [
        migrations.RunPython(create_additional_groups, remove_additional_groups),
    ]
