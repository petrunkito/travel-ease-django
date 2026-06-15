from django.db import migrations


DEPARTMENTS = [
    {'name': 'Managua', 'code': 'MAN'},
    {'name': 'León', 'code': 'LEO'},
    {'name': 'Chinandega', 'code': 'CHI'},
    {'name': 'Masaya', 'code': 'MAS'},
    {'name': 'Granada', 'code': 'GRA'},
    {'name': 'Carazo', 'code': 'CAR'},
    {'name': 'Rivas', 'code': 'RIV'},
    {'name': 'Nueva Segovia', 'code': 'NSE'},
    {'name': 'Madriz', 'code': 'MAD'},
    {'name': 'Estelí', 'code': 'EST'},
    {'name': 'Jinotega', 'code': 'JIN'},
    {'name': 'Matagalpa', 'code': 'MAT'},
    {'name': 'Boaco', 'code': 'BOA'},
    {'name': 'Chontales', 'code': 'CHO'},
    {'name': 'Río San Juan', 'code': 'RSJ'},
    {'name': 'Región Autónoma de la Costa Caribe Norte', 'code': 'RACCN'},
    {'name': 'Región Autónoma de la Costa Caribe Sur', 'code': 'RACCS'},
]


MUNICIPALITIES = [
    {'department_code': 'MAN', 'name': 'Managua', 'code': 'MAN-01'},
    {'department_code': 'MAN', 'name': 'Tipitapa', 'code': 'MAN-02'},
    {'department_code': 'MAN', 'name': 'Ciudad Sandino', 'code': 'MAN-03'},
    {'department_code': 'MAN', 'name': 'San Rafael del Sur', 'code': 'MAN-04'},
    {'department_code': 'MAN', 'name': 'Ticuantepe', 'code': 'MAN-05'},
    {'department_code': 'MAN', 'name': 'El Crucero', 'code': 'MAN-06'},
    {'department_code': 'MAN', 'name': 'Mateare', 'code': 'MAN-07'},
    {'department_code': 'MAN', 'name': 'San Francisco Libre', 'code': 'MAN-08'},
    {'department_code': 'MAN', 'name': 'Villa El Carmen', 'code': 'MAN-09'},
    {'department_code': 'LEO', 'name': 'León', 'code': 'LEO-01'},
    {'department_code': 'LEO', 'name': 'La Paz Centro', 'code': 'LEO-02'},
    {'department_code': 'LEO', 'name': 'Nagarote', 'code': 'LEO-03'},
    {'department_code': 'LEO', 'name': 'Telica', 'code': 'LEO-04'},
    {'department_code': 'LEO', 'name': 'Quezalguaque', 'code': 'LEO-05'},
    {'department_code': 'LEO', 'name': 'El Sauce', 'code': 'LEO-06'},
    {'department_code': 'LEO', 'name': 'Achuapa', 'code': 'LEO-07'},
    {'department_code': 'LEO', 'name': 'Santa Rosa del Peñón', 'code': 'LEO-08'},
    {'department_code': 'CHI', 'name': 'Chinandega', 'code': 'CHI-01'},
    {'department_code': 'CHI', 'name': 'El Viejo', 'code': 'CHI-02'},
    {'department_code': 'CHI', 'name': 'Corinto', 'code': 'CHI-03'},
    {'department_code': 'CHI', 'name': 'Chichigalpa', 'code': 'CHI-04'},
    {'department_code': 'CHI', 'name': 'Posoltega', 'code': 'CHI-05'},
    {'department_code': 'CHI', 'name': 'Puerto Morazán', 'code': 'CHI-06'},
    {'department_code': 'CHI', 'name': 'Somotillo', 'code': 'CHI-07'},
    {'department_code': 'CHI', 'name': 'Villanueva', 'code': 'CHI-08'},
    {'department_code': 'CHI', 'name': 'Cinco Pinos', 'code': 'CHI-09'},
    {'department_code': 'CHI', 'name': 'San Pedro del Norte', 'code': 'CHI-10'},
    {'department_code': 'CHI', 'name': 'San Francisco del Norte', 'code': 'CHI-11'},
    {'department_code': 'CHI', 'name': 'El Realejo', 'code': 'CHI-12'},
    {'department_code': 'CHI', 'name': 'Santo Tomás del Norte', 'code': 'CHI-13'},
    {'department_code': 'MAS', 'name': 'Masaya', 'code': 'MAS-01'},
    {'department_code': 'MAS', 'name': 'Nindirí', 'code': 'MAS-02'},
    {'department_code': 'MAS', 'name': 'Tisma', 'code': 'MAS-03'},
    {'department_code': 'MAS', 'name': 'Masatepe', 'code': 'MAS-04'},
    {'department_code': 'MAS', 'name': 'Nandasmo', 'code': 'MAS-05'},
    {'department_code': 'MAS', 'name': 'Catarina', 'code': 'MAS-06'},
    {'department_code': 'MAS', 'name': 'San Juan de Oriente', 'code': 'MAS-07'},
    {'department_code': 'MAS', 'name': 'Niquinohomo', 'code': 'MAS-08'},
    {'department_code': 'MAS', 'name': 'La Concepción', 'code': 'MAS-09'},
    {'department_code': 'GRA', 'name': 'Granada', 'code': 'GRA-01'},
    {'department_code': 'GRA', 'name': 'Diriomo', 'code': 'GRA-02'},
    {'department_code': 'GRA', 'name': 'Diriá', 'code': 'GRA-03'},
    {'department_code': 'GRA', 'name': 'Nandaime', 'code': 'GRA-04'},
    {'department_code': 'CAR', 'name': 'Jinotepe', 'code': 'CAR-01'},
    {'department_code': 'CAR', 'name': 'Dolores', 'code': 'CAR-02'},
    {'department_code': 'CAR', 'name': 'Diriamba', 'code': 'CAR-03'},
    {'department_code': 'CAR', 'name': 'San Marcos', 'code': 'CAR-04'},
    {'department_code': 'CAR', 'name': 'Santa Teresa', 'code': 'CAR-05'},
    {'department_code': 'CAR', 'name': 'La Paz de Carazo', 'code': 'CAR-06'},
    {'department_code': 'CAR', 'name': 'El Rosario', 'code': 'CAR-07'},
    {'department_code': 'CAR', 'name': 'La Conquista', 'code': 'CAR-08'},
    {'department_code': 'RIV', 'name': 'Rivas', 'code': 'RIV-01'},
    {'department_code': 'RIV', 'name': 'San Jorge', 'code': 'RIV-02'},
    {'department_code': 'RIV', 'name': 'San Juan del Sur', 'code': 'RIV-03'},
    {'department_code': 'RIV', 'name': 'Cárdenas', 'code': 'RIV-04'},
    {'department_code': 'RIV', 'name': 'Potosí', 'code': 'RIV-05'},
    {'department_code': 'RIV', 'name': 'Belén', 'code': 'RIV-06'},
    {'department_code': 'RIV', 'name': 'Buenos Aires', 'code': 'RIV-07'},
    {'department_code': 'RIV', 'name': 'Tola', 'code': 'RIV-08'},
    {'department_code': 'RIV', 'name': 'Moyogalpa', 'code': 'RIV-09'},
    {'department_code': 'RIV', 'name': 'Altagracia', 'code': 'RIV-10'},
]


def seed_departments_and_municipalities(apps, schema_editor):
    Department = apps.get_model('catalogos', 'Department')
    Municipality = apps.get_model('catalogos', 'Municipality')

    department_by_code = {}
    for department_data in DEPARTMENTS:
        department, _ = Department.objects.update_or_create(
            code=department_data['code'],
            defaults={'name': department_data['name']},
        )
        department_by_code[department.code] = department

    for municipality_data in MUNICIPALITIES:
        department = department_by_code[municipality_data['department_code']]
        Municipality.objects.update_or_create(
            code=municipality_data['code'],
            defaults={
                'name': municipality_data['name'],
                'department': department,
            },
        )


def reverse_seed_departments_and_municipalities(apps, schema_editor):
    Department = apps.get_model('catalogos', 'Department')
    Municipality = apps.get_model('catalogos', 'Municipality')

    municipality_codes = [municipality['code'] for municipality in MUNICIPALITIES]
    department_codes = [department['code'] for department in DEPARTMENTS]

    Municipality.objects.filter(code__in=municipality_codes).delete()
    Department.objects.filter(code__in=department_codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            seed_departments_and_municipalities,
            reverse_seed_departments_and_municipalities,
        ),
    ]
