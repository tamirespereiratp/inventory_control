from django import forms
from .models import Suppliers
import re

class SuppliersForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = "__all__"

        error_messages = {
            "company_name": {
                "unique": "A razão social já existe"
            }
        }

    # clean_<nome_campo>
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj", "")

        # Removendo os valores não númericos
        cnpj = re.sub("[^0-9]", "", cnpj)

        return cnpj
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        
        # Removendo os valores não númericos
        phone = re.sub("[^0-9]", "", phone)

        return phone
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data.get("zipcode", "")
        
        # Removendo os valores não númericos
        zipcode = re.sub("[^0-9]", "", zipcode)

        return zipcode