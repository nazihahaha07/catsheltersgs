from django import forms
from .models import Image,Cat,Report,VolunteerDate,VolunteerApplication,Inventory,Fund

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'description', 'image', 'gender', 'neuter', 'health_condition']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_text']
        widgets = {
            'report_text': forms.Textarea(attrs={'rows': 4}),
        }

class VolunteerDateForm(forms.ModelForm):
    class Meta:
        model = VolunteerDate
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['name', 'email', 'volunteer_date', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'volunteer_date': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item_name', 'description', 'quantity', 'price']

class UpdateInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item_name', 'description', 'quantity', 'price']

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['fund_name', 'description', 'price']

class UpdateFundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['fund_name', 'description','price']