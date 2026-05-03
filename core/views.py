import json
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Q
from .models import Customer, Produk, Transaksi, DetailTransaksi

def kasir_view(request):
    customers = Customer.objects.all()
    produks = Produk.objects.all()
    context = {
        'customers': customers,
        'produks': produks,
    }
    return render(request, 'kasir.html', context)

@csrf_exempt
def create_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer_id')
            status = data.get('status', 'bayar')
            items = data.get('items', [])
            total = data.get('total', 0)

            customer = None
            if customer_id:
                customer = Customer.objects.filter(id=customer_id).first()

            transaksi = Transaksi.objects.create(
                customer=customer,
                total=total,
                status=status
            )

            for item in items:
                produk = Produk.objects.get(id=item['id'])
                DetailTransaksi.objects.create(
                    transaksi=transaksi,
                    produk=produk,
                    jumlah=item['qty'],
                    subtotal=item['subtotal']
                )

            return JsonResponse({'status': 'success', 'message': 'Transaksi berhasil disimpan'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def riwayat_transaksi(request):
    today = timezone.localtime().date()
    
    status_filter = request.GET.get('status', 'semua')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Base query
    transaksi = Transaksi.objects.all()

    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            transaksi = transaksi.filter(tanggal__date__range=[start, end])
        except ValueError:
            start = today - timedelta(days=7)
            end = today
            transaksi = transaksi.filter(tanggal__date__range=[start, end])
            start_date = start.strftime('%Y-%m-%d')
            end_date = end.strftime('%Y-%m-%d')
    else:
        start = today - timedelta(days=7)
        end = today
        transaksi = transaksi.filter(tanggal__date__range=[start, end])
        start_date = start.strftime('%Y-%m-%d')
        end_date = end.strftime('%Y-%m-%d')

    if status_filter == 'lunas':
        transaksi = transaksi.filter(status='bayar')
    elif status_filter == 'piutang':
        transaksi = transaksi.filter(status='nanti')

    transaksi = transaksi.order_by('-tanggal')

    total_pemasukan = transaksi.filter(status='bayar').aggregate(Sum('total'))['total__sum'] or 0
    total_piutang = transaksi.filter(status='nanti').aggregate(Sum('total'))['total__sum'] or 0

    context = {
        'transaksi_list': transaksi,
        'total_pemasukan': total_pemasukan,
        'total_piutang': total_piutang,
        'status_filter': status_filter,
        'start_date': start_date,
        'end_date': end_date,
        'total_transaksi': transaksi.count(),
    }
    return render(request, 'riwayat.html', context)

def laporan_mingguan(request):
    today = timezone.localtime().date()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        # Default to last 7 days
        start = today - timedelta(days=7)
        end = today

    # We want total transaction per customer
    customers_report = Customer.objects.annotate(
        total_trx=Count('transaksi', filter=Q(transaksi__tanggal__date__range=[start, end])),
        total_nominal=Sum('transaksi__total', filter=Q(transaksi__tanggal__date__range=[start, end])),
        sudah_bayar=Count('transaksi', filter=Q(transaksi__tanggal__date__range=[start, end], transaksi__status='bayar')),
        nanti=Count('transaksi', filter=Q(transaksi__tanggal__date__range=[start, end], transaksi__status='nanti')),
        total_piutang=Sum('transaksi__total', filter=Q(transaksi__tanggal__date__range=[start, end], transaksi__status='nanti')),
    ).filter(total_trx__gt=0).order_by('-total_nominal')

    transaksi_range = Transaksi.objects.filter(tanggal__date__range=[start, end])
    total_lunas = transaksi_range.filter(status='bayar').aggregate(Sum('total'))['total__sum'] or 0
    total_belum_bayar = transaksi_range.filter(status='nanti').aggregate(Sum('total'))['total__sum'] or 0
    total_trx_tertunda = transaksi_range.filter(status='nanti').count()

    context = {
        'customers_report': customers_report,
        'start_date': start.strftime('%Y-%m-%d'),
        'end_date': end.strftime('%Y-%m-%d'),
        'total_lunas': total_lunas,
        'total_belum_bayar': total_belum_bayar,
        'total_trx_tertunda': total_trx_tertunda,
    }
    return render(request, 'laporan.html', context)

def lunasi_piutang_customer(request, customer_id):
    if request.method == 'POST':
        Transaksi.objects.filter(customer_id=customer_id, status='nanti').update(status='bayar')
    return redirect('laporan')

def cetak_laporan_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    transaksi = Transaksi.objects.filter(customer=customer).order_by('-tanggal')
    total_nominal = transaksi.aggregate(Sum('total'))['total__sum'] or 0
    total_piutang = transaksi.filter(status='nanti').aggregate(Sum('total'))['total__sum'] or 0
    
    context = {
        'customer': customer,
        'transaksi_list': transaksi,
        'total_nominal': total_nominal,
        'total_piutang': total_piutang,
        'tanggal_cetak': timezone.localtime().date()
    }
    return render(request, 'cetak_laporan.html', context)

from django.shortcuts import render, redirect, get_object_or_404

def produk_view(request):
    produks = Produk.objects.all().order_by('-id')
    context = {
        'produks': produks,
        'total_produk': produks.count(),
        'stok_aman': produks.count(), # dummy logic
        'stok_menipis': 0, # dummy logic
    }
    return render(request, 'produk.html', context)

def tambah_produk(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kategori = request.POST.get('kategori')
        harga = request.POST.get('harga')
        if nama and kategori and harga:
            Produk.objects.create(nama=nama, kategori=kategori, harga=harga)
            return redirect('produk')
    return render(request, 'produk_form.html', {'title': 'Tambah Produk Baru'})

def edit_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.nama = request.POST.get('nama')
        produk.kategori = request.POST.get('kategori')
        produk.harga = request.POST.get('harga')
        produk.save()
        return redirect('produk')
    return render(request, 'produk_form.html', {'title': 'Edit Produk', 'produk': produk})

def hapus_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        produk.delete()
        return redirect('produk')
    return render(request, 'produk_confirm_delete.html', {'produk': produk})
