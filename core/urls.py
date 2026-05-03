from django.urls import path
from . import views

urlpatterns = [
    path('', views.kasir_view, name='kasir'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('riwayat/', views.riwayat_transaksi, name='riwayat'),
    path('laporan/', views.laporan_mingguan, name='laporan'),
    path('produk/', views.produk_view, name='produk'),
    path('produk/tambah/', views.tambah_produk, name='tambah_produk'),
    path('produk/edit/<int:pk>/', views.edit_produk, name='edit_produk'),
    path('produk/hapus/<int:pk>/', views.hapus_produk, name='hapus_produk'),
    path('laporan/lunasi/<int:customer_id>/', views.lunasi_piutang_customer, name='lunasi_piutang_customer'),
    path('laporan/cetak/<int:customer_id>/', views.cetak_laporan_customer, name='cetak_laporan_customer'),
]
