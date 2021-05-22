from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40, label="Имя", required=True)
    last_name = forms.CharField(max_length=40, label="Фамиля", required=False)
    address = forms.CharField(label="Адрес", max_length=40, required=True)
    phone = forms.CharField(max_length=17, label="Номер телефона", required=True)
    comment = forms.CharField(max_length=255, label="Комментарий", required=False)
    ready_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Дата готовности заказа')
    ready_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label='Время готовности заказа')

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'address', 'phone', 'orderType', 'payment', 'ready_date', 'ready_time', 'comment'
        )
