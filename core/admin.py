from django.contrib import admin
from .models import Customer, Produk, Transaksi, DetailTransaksi

class DetailTransaksiInline(admin.TabularInline):
    model = DetailTransaksi
    extra = 1

class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('id', 'tanggal', 'customer', 'total', 'status')
    list_filter = ('status', 'tanggal')
    inlines = [DetailTransaksiInline]

admin.site.register(Customer)
admin.site.register(Produk)
admin.site.register(Transaksi, TransaksiAdmin)
admin.site.register(DetailTransaksi)
