from django.db import models
from django.utils import timezone

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nama

class Produk(models.Model):
    KATEGORI_CHOICES = (
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
        ('lainnya', 'Lainnya'),
    )
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=0)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='lainnya')

    def __str__(self):
        return f"{self.nama} - Rp{self.harga}"

class Transaksi(models.Model):
    STATUS_CHOICES = (
        ('bayar', 'Bayar'),
        ('nanti', 'Nanti'),
    )
    tanggal = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='bayar')

    def __str__(self):
        cust_name = self.customer.nama if self.customer else "Umum"
        return f"Trx {self.id} - {cust_name} - Rp{self.total}"

class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, related_name='details', on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.PROTECT)
    jumlah = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return f"{self.transaksi.id} - {self.produk.nama} x{self.jumlah}"
