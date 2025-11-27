# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils.crypto import get_random_string


class Route(models.Model):
    """Marshrut modeli"""
    name = models.CharField(max_length=200, verbose_name="Marshrut nomi")
    start_point = models.CharField(max_length=150, verbose_name="Boshlanish nuqtasi")
    end_point = models.CharField(max_length=150, verbose_name="Tugash nuqtasi")
    distance_km = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Masofa (km)",
        validators=[MinValueValidator(0.1)]
    )
    estimated_time = models.DurationField(verbose_name="Taxminiy vaqt")

    def __str__(self):
        return f" {self.start_point} → {self.end_point}"

    class Meta:
        verbose_name = "Marshrut"
        verbose_name_plural = "Marshrutlar"


class Vehicle(models.Model):
    """Transport vositasi"""
    VEHICLE_TYPES = [
        ('bus', 'Avtobus'),
        ('minibus', 'Mikroavtobus'),
        ('taxi', 'Taksi'),
        ('train', 'Poyezd'),
    ]

    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Davlat raqami")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, verbose_name="Transport turi")
    capacity = models.PositiveIntegerField(verbose_name="O‘rinlar soni")
    driver_name = models.CharField(max_length=100, verbose_name="Haydovchi ismi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    def __str__(self):
        return f"{self.get_vehicle_type_display()} "

    class Meta:
        verbose_name = "Transport vositasi"
        verbose_name_plural = "Transport vositalari"


class Trip(models.Model):
    """Reyss (marshrut + transport + vaqt)"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Marshrut")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Transport")
    departure_time = models.DateTimeField(verbose_name="Jo‘nash vaqti")
    arrival_time = models.DateTimeField(verbose_name="Yetib borish vaqti")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Narxi (so‘m)")

    def __str__(self):
        return f"{self.route} | {self.vehicle} | {self.departure_time.strftime('%d.%m %H:%M')}"

    class Meta:
        verbose_name = "Reyss"
        verbose_name_plural = "Reysslar"
        ordering = ['departure_time']


class Ticket(models.Model):
    """QR-kodli chipta"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi", null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Reyss")
    seat_number = models.PositiveIntegerField(
        verbose_name="O‘rindiq raqami",
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan vaqt")
    is_used = models.BooleanField(default=False, verbose_name="Ishlatilganmi")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, verbose_name="QR-kod")
    ticket_code = models.CharField(max_length=12, unique=True, verbose_name="Chipta kodi")

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = self.generate_ticket_code()

        if not self.qr_code:
            self.generate_qr_code()

        super().save(*args, **kwargs)

    def generate_ticket_code(self):
        """12 belgidan iborat unikal kod generatsiyasi"""
        while True:
            code = get_random_string(length=12, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            if not Ticket.objects.filter(ticket_code=code).exists():
                return code

    def generate_qr_code(self):
        """QR-kod yaratish va saqlash"""
        qr_data = f"""
        CHIPTA: {self.ticket_code}
        Reyss: {self.trip}
        O'rindiq: {self.seat_number}
        Foydalanuvchi: {self.user.get_full_name() if self.user else 'Mehmon'}
        Sotib olingan: {self.purchase_date.strftime('%d.%m.%Y %H:%M')}
        """.strip()

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f"qr_{self.ticket_code}.png"
        self.qr_code.save(file_name, File(buffer), save=False)

    def __str__(self):
        return f"Chipta #{self.ticket_code} | {self.trip}"

    class Meta:
        verbose_name = "Chipta"
        verbose_name_plural = "Chiptalar"
        unique_together = ('trip', 'seat_number')  # Bir reysda bir o‘rindiq faqat bitta chipta


class TicketValidation(models.Model):
    """Chiptani tekshirish jurnali"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Chipta")
    validated_at = models.DateTimeField(auto_now_add=True, verbose_name="Tekshirilgan vaqt")
    validator = models.CharField(max_length=100, verbose_name="Tekshiruvchi (masalan, haydovchi)")
    is_valid = models.BooleanField(default=True, verbose_name="Haqiqiyligi")

    def __str__(self):
        status = "Haqiqiy" if self.is_valid else "NoHaqiqiy"
        return f"{self.ticket} - {status} ({self.validated_at})"

    class Meta:
        verbose_name = "Tekshiruv"
        verbose_name_plural = "Tekshiruvlar"