from rest_framework import serializers

from .models import SatisfactionSurvey, Sugerencia, Valoracion

class ValoracionSerializer(serializers.Serializer):
    idReserva = serializers.IntegerField(min_value=1)
    puntaje = serializers.IntegerField(min_value=1, max_value=5)
    comentario = serializers.CharField(max_length=1000, allow_blank=False, trim_whitespace=True)


class ValoracionDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracion
        fields = [
            'id',
            'client_id',
            'client_national_id',
            'client_name',
            'client_phone_number',
            'reservation_id',
            'score',
            'comment',
            'package_name',
            'package_description',
            'price',
            'flight',
            'hotel',
            'transportation',
        ]


class SugerenciaSerializer(serializers.ModelSerializer):
    comentario = serializers.CharField(
        source='comment',
        max_length=1000,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model = Sugerencia
        fields = ['comentario']


class EncuestaSatisfaccionSerializer(serializers.ModelSerializer):
    idReserva = serializers.IntegerField(
        source='reservation_id',
        min_value=1,
        required=False,
        allow_null=True,
    )
    atencionAlCliente = serializers.IntegerField(
        source='customer_service',
        min_value=1,
        max_value=5,
    )
    facilidadReserva = serializers.IntegerField(
        source='reservation_ease',
        min_value=1,
        max_value=5,
    )
    relacionCalidadPrecio = serializers.IntegerField(
        source='value_for_money',
        min_value=1,
        max_value=5,
    )
    calidadServicioProporcionado = serializers.IntegerField(
        source='service_quality',
        min_value=1,
        max_value=5,
    )
    caracteristicaFav = serializers.CharField(
        source='favorite_feature',
        max_length=1000,
        allow_blank=False,
        trim_whitespace=True,
    )
    informacionProporcionadaSencilla = serializers.BooleanField(source='simple_information')
    recomendarAOtros = serializers.BooleanField(source='recommend_to_others')
    volverContratar = serializers.BooleanField(source='would_hire_again')

    class Meta:
        model = SatisfactionSurvey
        fields = [
            'idReserva',
            'atencionAlCliente',
            'facilidadReserva',
            'relacionCalidadPrecio',
            'calidadServicioProporcionado',
            'caracteristicaFav',
            'informacionProporcionadaSencilla',
            'recomendarAOtros',
            'volverContratar',
        ]
