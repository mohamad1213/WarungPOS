from django.core.management.base import BaseCommand
from core.models import Customer, Produk
import random

class Command(BaseCommand):
    help = 'Seeds the database with 10 dummy customers and 10 dummy products'

    def handle(self, *args, **kwargs):
        # Data Customer Dummy
        customers_data = [
            {'nama': 'Budi Santoso', 'no_hp': '081234567890'},
            {'nama': 'Siti Aminah', 'no_hp': '081298765432'},
            {'nama': 'Agus Pratama', 'no_hp': '085612341234'},
            {'nama': 'Dewi Lestari', 'no_hp': '087812345678'},
            {'nama': 'Rudi Hermawan', 'no_hp': '081198761234'},
            {'nama': 'Sri Wahyuni', 'no_hp': '089612349876'},
            {'nama': 'Joko Widodo', 'no_hp': '082112345678'},
            {'nama': 'Nia Ramadhani', 'no_hp': '083812341234'},
            {'nama': 'Ahmad Fauzi', 'no_hp': '085712349876'},
            {'nama': 'Ratna Sari', 'no_hp': '081312345678'},
        ]

        # Data Produk Dummy (Warung)
        produk_data = [
            {'nama': 'Beras 1 Kg', 'harga': 15000, 'kategori': 'lainnya'},
            {'nama': 'Telur Ayam 1 Kg', 'harga': 28000, 'kategori': 'lainnya'},
            {'nama': 'Minyak Goreng 1L', 'harga': 16000, 'kategori': 'lainnya'},
            {'nama': 'Indomie Goreng', 'harga': 3000, 'kategori': 'makanan'},
            {'nama': 'Indomie Kuah Soto', 'harga': 3000, 'kategori': 'makanan'},
            {'nama': 'Gula Pasir 1 Kg', 'harga': 17000, 'kategori': 'lainnya'},
            {'nama': 'Kopi Kapal Api Sachet', 'harga': 1500, 'kategori': 'minuman'},
            {'nama': 'Teh Pucuk Harum', 'harga': 4000, 'kategori': 'minuman'},
            {'nama': 'Roti Tawar', 'harga': 12000, 'kategori': 'makanan'},
            {'nama': 'Sabun Mandi Lifebuoy', 'harga': 4000, 'kategori': 'lainnya'},
        ]

        self.stdout.write('Menghapus data lama...')
        Customer.objects.all().delete()
        Produk.objects.all().delete()

        self.stdout.write('Membuat 10 Customer...')
        for data in customers_data:
            Customer.objects.create(**data)

        self.stdout.write('Membuat 10 Produk...')
        for data in produk_data:
            Produk.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Berhasil menambahkan 10 Customer dan 10 Produk dummy!'))
