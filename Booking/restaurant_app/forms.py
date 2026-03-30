from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,Restaurant,Booking,Menu


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}
    ))

    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES,
                             widget=forms.Select(
                                 attrs={'class':'form-control'}
                             ))

    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = ['name','location','cuisine','description','opening_time','closing_time','image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date','timeslot','guests']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description','category', 'price', 'image']