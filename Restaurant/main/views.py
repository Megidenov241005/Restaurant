from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Q


@staff_member_required
def add_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('edit_tables')
    else:
        form = TableForm()
    
    return render(request, 'add_table.html', {'form': form})

@staff_member_required
def edit_tables(request):
    tables = Table.objects.all()
    return render(request, 'edit_tables.html', {'tables': tables})

@staff_member_required
def edit_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('edit_tables')
    else:
        form = TableForm(instance=table)

    return render(request, 'edit_table.html', {'form': form, 'table': table})

@staff_member_required
def delete_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table.delete()
    return redirect('edit_tables')

def main_view(request):
    if not request.user.is_authenticated:
        return render(request, 'welcome.html')
 
    if request.user.is_staff:
        reserves = Reserve.objects.filter(end__gte=timezone.now()) \
                              .select_related('table', 'owner') \
                              .order_by('start')  # сортировка по дате начала
        return render(request, 'admin_reserves.html', {'reserves': reserves})


    reserves = Reserve.objects.filter(owner=request.user).order_by('start')
    return render(request, 'my_reserves.html', {'reserves': reserves})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введенные данные.')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def choose_time(request):
    if request.method == 'POST':
        form = ReserveTimeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']

            # находим столики, которые уже зарезервированы в это время
            reserved_tables = Reserve.objects.filter(
                Q(start__lt=end) & Q(end__gt=start)
            ).values_list('table_id', flat=True)

            # исключаем зарезервированные
            available_tables = Table.objects.exclude(id__in=reserved_tables)

            return render(request, 'select_table.html', {
                'tables': available_tables,
                'start': start,
                'end': end
            })
    else:
        form = ReserveTimeForm()
    return render(request, 'choose_time.html', {'form': form})

@login_required
def finalize_reserve(request):
    if request.method == 'POST':
        table_id = request.POST.get('table')
        start = request.POST.get('start')
        end = request.POST.get('end')

        reserve = Reserve.objects.create(
            table_id=table_id,
            start=start,
            end=end,
            owner=request.user
        )
        return redirect('main')