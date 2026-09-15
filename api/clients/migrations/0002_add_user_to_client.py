import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(
                blank=True,
                db_column='IdUsuarioCliente',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='client_account',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]