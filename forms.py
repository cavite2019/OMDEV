from django import forms
from .models import *
import ipaddress


class SSRinitForm(forms.ModelForm):
    IDC_CHOICES = [
    ]

    for i in SSRIDCModel.objects.all():
        IDC_CHOICES.append((i.IDC,i.IDC))

    IP = forms.CharField(max_length=960, widget=forms.Textarea(attrs={'rows':5, 'cols': 16, 'placeholder': "Enter SSR IP"}), label="SSR IP")
    PORT= forms.CharField(max_length=5, initial=22)
    USER = forms.CharField(max_length=15, initial='root')
    PASSWORD = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle' : 'password'}))
    IDC = forms.ChoiceField(
        choices=IDC_CHOICES, label="IDC", initial='---'
    )

    class Meta:
        model = SSRinitModel
        fields = [
            'IP',
            'PORT',
            'USER',
            'PASSWORD',
            'IDC'
        ]


    def clean_IP(self):
        IP = self.cleaned_data.get("IP")
        for IP_list in IP.split('\n'):
            try:
                return str(ipaddress.ip_address(IP_list.strip()))
            except:
                raise forms.ValidationError("Invalid input! It should be IP!")


    def clean_PORT(self):
        PORT = self.cleaned_data.get("PORT")
        try:
            if int(PORT) <= 65535 and int(PORT) > 0:
                return PORT
            else:
                raise forms.ValidationError("Port is out of range.")
        except ValueError:
            raise forms.ValidationError("Invalid Input! It should be PORT!")

    def clean_IDC(self):
        IDC = self.cleaned_data.get("IDC")
        if IDC == '---':
            raise forms.ValidationError("Incorrect IDC!")
        else:
            return IDC







