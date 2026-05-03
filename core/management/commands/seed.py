from django.core.management.base import BaseCommand
from core.models import Customer, Produk
import random

class Command(BaseCommand):
    help = 'Seeds the database with 10 dummy customers and 10 dummy products'

    def handle(self, *args, **kwargs):
        # Data Customer Dummy
        customers_data = [
            {'nama': 'Bocil', 'no_hp': '081234567890'},
            {'nama': 'Joko', 'no_hp': '081298765432'},
            {'nama': 'Rino', 'no_hp': '085612341234'},
            {'nama': 'Ari', 'no_hp': '087812345678'},
            {'nama': 'Agung', 'no_hp': '081198761234'},
            {'nama': 'Madon', 'no_hp': '089612349876'},
            {'nama': 'Tarom', 'no_hp': '082112345678'},
            {'nama': 'Dodo', 'no_hp': '083812341234'},
        ]

        # Data Produk Dummy (Warung)
        produk_data = [
            {'nama': 'Tea Jus', 'harga': 4000, 'kategori': 'minuman'},
            {'nama': 'Jasjus', 'harga': 4000, 'kategori': 'minuman'},
            {'nama': 'Es Coffemix', 'harga': 5000, 'kategori': 'minuman'},
            {'nama': 'jajanan', 'harga': 1000, 'kategori': 'makanan'},
            {'nama': 'roti', 'harga': 2000, 'kategori': 'makanan'},
            {'nama': 'Nutrisari', 'harga': 5000, 'kategori': 'minuman'},
            {'nama': 'Mie Duo + Telor', 'harga': 10000, 'kategori': 'makanan'},
            {'nama': 'Mie Duo', 'harga': 7000, 'kategori': 'makanan'},
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
