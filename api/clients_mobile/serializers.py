from rest_framework import serializers

class ValoracionSerializer(serializers.Serializer):
    idReserva = serializers.IntegerField(min_value=1)
    puntaje = serializers.IntegerField(min_value=1, max_value=5)
    comentario = serializers.CharField(max_length=1000, allow_blank=False, trim_whitespace=True)


class SugerenciaSerializer(serializers.Serializer):
    comentario = serializers.CharField(max_length=1000, allow_blank=False, trim_whitespace=True)
