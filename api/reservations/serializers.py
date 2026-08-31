from rest_framework import serializers
from django.contrib.auth.models import User
from api.clients.models import Client
from api.packages.models import TouristPackage, PackageDetail
from .models import (
    Reservation, ReservationDetail, ReservationStatus,
    ReservationStatusHistory, PaymentType, Invoice
)


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name', 'code']


class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationStatus
        fields = ['id', 'name', 'code']


class ReservationDetailSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = ReservationDetail
        fields = [
            'id', 'service_type', 'service_type_display',
            'service_id', 'quantity', 'unit_price', 'total'
        ]
        read_only_fields = ['id', 'total']


class ReservationDetailCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear detalles de reserva a partir de detalles de paquete."""

    class Meta:
        model = ReservationDetail
        fields = [
            'service_type', 'service_id', 'quantity',
            'unit_price', 'package_id'
        ]


class ReservationStatusHistorySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = ReservationStatusHistory
        fields = ['id', 'status', 'status_display', 'date']
        read_only_fields = ['id', 'date']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'issue_date', 'total']
        read_only_fields = ['id', 'issue_date']


class ReservationCreateSerializer(serializers.Serializer):
    """Serializer para crear una nueva reserva."""
    client_id = serializers.IntegerField()
    package_id = serializers.IntegerField()
    payment_type_id = serializers.IntegerField()
    seller_user_id = serializers.IntegerField()
    status_id = serializers.IntegerField()

    def validate_client_id(self, value):
        try:
            Client.objects.get(id=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError("El cliente no existe.")
        return value

    def validate_package_id(self, value):
        try:
            TouristPackage.objects.get(id=value)
        except TouristPackage.DoesNotExist:
            raise serializers.ValidationError("El paquete turístico no existe.")
        return value

    def validate_payment_type_id(self, value):
        try:
            PaymentType.objects.get(id=value)
        except PaymentType.DoesNotExist:
            raise serializers.ValidationError("El tipo de pago no existe.")
        return value

    def validate_seller_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario vendedor no existe.")
        return value

    def validate_status_id(self, value):
        try:
            ReservationStatus.objects.get(id=value)
        except ReservationStatus.DoesNotExist:
            raise serializers.ValidationError("El estado de reserva no existe.")
        return value

    def create(self, validated_data):
        client = Client.objects.get(id=validated_data['client_id'])
        package = TouristPackage.objects.get(id=validated_data['package_id'])
        payment_type = PaymentType.objects.get(id=validated_data['payment_type_id'])
        seller_user = User.objects.get(id=validated_data['seller_user_id'])
        initial_status = ReservationStatus.objects.get(id=validated_data['status_id'])

        # Calcular el total del paquete
        package_details = PackageDetail.objects.filter(package=package)
        total = sum(detail.total for detail in package_details)

        # Crear la reserva
        reservation = Reservation.objects.create(
            client=client,
            payment_type=payment_type,
            seller_user=seller_user,
            total=total
        )

        # Crear detalles de reserva a partir de detalles del paquete
        for detail in package_details:
            ReservationDetail.objects.create(
                reservation=reservation,
                package_id=package.id,
                service_type=detail.service_type,
                service_id=detail.service_id,
                quantity=detail.quantity,
                unit_price=detail.unit_price,
                total=detail.total
            )

        # Crear el registro inicial en el historial de estados con el estado enviado
        ReservationStatusHistory.objects.create(
            reservation=reservation,
            status=initial_status
        )

        # Crear la factura automáticamente
        last_invoice = Invoice.objects.all().order_by('-id').first()
        invoice_number = f"FAC-{last_invoice.id + 1 if last_invoice else 1:06d}"
        Invoice.objects.create(
            reservation=reservation,
            invoice_number=invoice_number,
            total=total
        )

        return reservation


class ReservationDetailedSerializer(serializers.ModelSerializer):
    """Serializer detallado para listar reservas con todos sus detalles."""
    details = ReservationDetailSerializer(many=True, read_only=True)
    status_history = ReservationStatusHistorySerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    package_name = serializers.SerializerMethodField()
    package_reserved_id = serializers.SerializerMethodField()
    client_name = serializers.CharField(source='client.name', read_only=True)
    payment_type_name = serializers.CharField(source='payment_type.name', read_only=True)
    seller_user_name = serializers.CharField(source='seller_user.get_full_name', read_only=True)
    current_status = serializers.SerializerMethodField()
    package_id = serializers.IntegerField(write_only=True, required=False, help_text="ID del paquete turístico para cambiar")

    class Meta:
        model = Reservation
        fields = [
            'id', 'package_reserved_id', 'package_name', 'client', 'client_name', 'payment_type', 'payment_type_name',
            'seller_user', 'seller_user_name', 'date', 'total', 'active',
            'details', 'status_history', 'current_status', 'invoice', 'package_id'
        ]
        read_only_fields = ['id', 'date', 'total']

    def validate_package_id(self, value):
        """Validar que el paquete turístico existe."""
        if value is not None:
            try:
                TouristPackage.objects.get(id=value)
            except TouristPackage.DoesNotExist:
                raise serializers.ValidationError("El paquete turístico no existe.")
        return value

    def update(self, instance, validated_data):
        """Actualizar la reserva, incluyendo cambio de paquete si se proporciona."""
        package_id = validated_data.pop('package_id', None)

        # Actualizar campos normales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Si se proporciona un nuevo paquete, cambiar los detalles y recalcular el total
        if package_id is not None:
            package = TouristPackage.objects.get(id=package_id)
            package_details = PackageDetail.objects.filter(package=package)

            # Eliminar detalles anteriores de la reserva
            ReservationDetail.objects.filter(reservation=instance).delete()

            # Crear nuevos detalles basados en el nuevo paquete
            total = 0
            for detail in package_details:
                ReservationDetail.objects.create(
                    reservation=instance,
                    package_id=package.id,
                    service_type=detail.service_type,
                    service_id=detail.service_id,
                    quantity=detail.quantity,
                    unit_price=detail.unit_price,
                    total=detail.total
                )
                total += detail.total

            # Actualizar el total de la reserva
            instance.total = total

            # Actualizar la factura con el nuevo total
            try:
                invoice = instance.invoice
                invoice.total = total
                invoice.save()
            except Invoice.DoesNotExist:
                pass

        instance.save()
        return instance

    def get_package_name(self, obj):
        """Obtener el nombre del paquete turístico asociado a la reserva."""
        first_detail = obj.details.first()
        if not first_detail or not first_detail.package_id:
            return None

        return TouristPackage.objects.filter(id=first_detail.package_id).values_list('name', flat=True).first()

    def get_package_id(self, obj):
        """Obtener el id del paquete turístico asociado a la reserva."""
        first_detail = obj.details.first()
        if not first_detail:
            return None

        return first_detail.package_id

    def get_package_reserved_id(self, obj):
        """Alias del id del paquete turístico reservado para la respuesta."""
        return self.get_package_id(obj)

    def get_current_status(self, obj):
        latest_status = obj.status_history.order_by('-date').first()
        if latest_status:
            return ReservationStatusSerializer(latest_status.status).data
        return None


class ReservationUpdateStatusSerializer(serializers.Serializer):
    """Serializer para actualizar el estado de una reserva."""
    status_id = serializers.IntegerField()

    def validate_status_id(self, value):
        try:
            ReservationStatus.objects.get(id=value)
        except ReservationStatus.DoesNotExist:
            raise serializers.ValidationError("El estado de reserva no existe.")
        return value
