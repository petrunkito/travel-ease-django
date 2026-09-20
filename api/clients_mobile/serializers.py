from rest_framework import serializers

class ValoracionSerializer(serializers.Serializer):
    idReserva = serializers.IntegerField(min_value=1)
    puntaje = serializers.IntegerField(min_value=1, max_value=5)
    comentario = serializers.CharField(max_length=1000, allow_blank=False, trim_whitespace=True)


class SugerenciaSerializer(serializers.Serializer):
    comentario = serializers.CharField(max_length=1000, allow_blank=False, trim_whitespace=True)


class EncuestaSatisfaccionSerializer(serializers.Serializer):
    idReserva = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    atencionAlCliente = serializers.IntegerField(min_value=1, max_value=5)
    facilidadReserva = serializers.IntegerField(min_value=1, max_value=5)
    relacionCalidadPrecio = serializers.IntegerField(min_value=1, max_value=5)
    calidadServicioProporcionado = serializers.IntegerField(min_value=1, max_value=5)
    caracteristicaFav = serializers.CharField(
        max_length=1000,
        allow_blank=False,
        trim_whitespace=True,
    )
    informacionProporcionadaSencilla = serializers.BooleanField()
    recomendarAOtros = serializers.BooleanField()
    volverContratar = serializers.BooleanField()
