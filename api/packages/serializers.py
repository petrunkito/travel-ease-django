from django.db import transaction
from rest_framework import serializers

from api.services.models import PriceHistory

from .models import Destination, PackageDetail, TouristPackage
from .services import (
    SERVICE_GROUP_KEY_MAP,
    calculate_detail_total,
    get_service_instance,
    get_service_unit_price,
    normalize_service_type,
    serialize_package_detail,
)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'city', 'country', 'active']
        read_only_fields = ['id', 'active']


class PackageDetailInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    service_type = serializers.ChoiceField(choices=PriceHistory.ServiceType.choices)
    service_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        service_type = normalize_service_type(attrs['service_type'])
        service = get_service_instance(service_type, attrs['service_id'])
        if not service:
            raise serializers.ValidationError({'service_id': 'El servicio indicado no existe.'})

        if not getattr(service, 'active', True):
            raise serializers.ValidationError({'service_id': 'El servicio indicado esta inactivo.'})

        unit_price = get_service_unit_price(service_type, attrs['service_id'])
        if unit_price is None:
            raise serializers.ValidationError(
                {'service_id': 'El servicio no tiene un precio activo registrado.'}
            )

        attrs['unit_price'] = unit_price
        attrs['total'] = calculate_detail_total(attrs['quantity'], unit_price)
        return attrs


class PackageDetailSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()

    class Meta:
        model = PackageDetail
        fields = ['id', 'service_type', 'service_id', 'quantity', 'unit_price', 'total', 'service']
        read_only_fields = fields

    def get_service(self, obj):
        return serialize_package_detail(obj)['service']


class TouristPackageSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer()
    details = PackageDetailInputSerializer(many=True, write_only=True, required=False)
    services = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TouristPackage
        fields = [
            'id',
            'destination',
            'name',
            'description',
            'created_at',
            'active',
            'details',
            'services',
        ]
        read_only_fields = ['id', 'created_at', 'active', 'services']

    def validate(self, attrs):
        details = attrs.get('details')
        if self.instance is None and not details:
            raise serializers.ValidationError(
                {'details': 'El paquete debe incluir al menos un servicio.'}
            )

        if details is not None and len(details) == 0:
            raise serializers.ValidationError(
                {'details': 'El paquete debe incluir al menos un servicio.'}
            )

        return attrs

    def create(self, validated_data):
        destination_data = validated_data.pop('destination')
        details_data = validated_data.pop('details', [])

        with transaction.atomic():
            destination = Destination.objects.create(**destination_data)
            tourist_package = TouristPackage.objects.create(destination=destination, **validated_data)
            self._sync_details(tourist_package, details_data)
            return tourist_package

    def update(self, instance, validated_data):
        destination_data = validated_data.pop('destination', None)
        details_data = validated_data.pop('details', None)

        with transaction.atomic():
            if destination_data:
                destination_serializer = DestinationSerializer(
                    instance.destination,
                    data=destination_data,
                    partial=True,
                )
                destination_serializer.is_valid(raise_exception=True)
                destination_serializer.save()

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if details_data is not None:
                self._sync_details(instance, details_data)

            return instance

    def get_services(self, obj):
        grouped = {
            SERVICE_GROUP_KEY_MAP[PriceHistory.ServiceType.FLIGHT]: [],
            SERVICE_GROUP_KEY_MAP[PriceHistory.ServiceType.HOTEL]: [],
            SERVICE_GROUP_KEY_MAP[PriceHistory.ServiceType.TRANSPORTATION]: [],
        }
        for detail in obj.details.all():
            serialized_detail = serialize_package_detail(detail)
            grouped[SERVICE_GROUP_KEY_MAP[detail.service_type]].append(serialized_detail)
        return grouped

    def _sync_details(self, tourist_package, details_data):
        if details_data is None:
            return

        if len(details_data) == 0:
            raise serializers.ValidationError({'details': 'El paquete debe incluir al menos un servicio.'})

        existing_details = {detail.id: detail for detail in tourist_package.details.all()}
        keep_ids = set()

        for detail_data in details_data:
            detail_id = detail_data.get('id')
            detail_payload = {
                'service_type': detail_data['service_type'],
                'service_id': detail_data['service_id'],
                'quantity': detail_data['quantity'],
                'unit_price': detail_data['unit_price'],
                'total': detail_data['total'],
            }

            if detail_id and detail_id in existing_details:
                detail = existing_details[detail_id]
                for attr, value in detail_payload.items():
                    setattr(detail, attr, value)
                detail.save()
                keep_ids.add(detail.id)
                continue

            if detail_id and detail_id not in existing_details:
                raise serializers.ValidationError(
                    {'details': f'El detalle con id {detail_id} no pertenece a este paquete.'}
                )

            detail = PackageDetail.objects.create(package=tourist_package, **detail_payload)
            keep_ids.add(detail.id)

        tourist_package.details.exclude(id__in=keep_ids).delete()
