from django.contrib import admin
from .models import Suppliers

# Register your models here.
@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "fantasy_name", "email", "enabled"] # Personaliza os campos que aparecem na listagem
    exclude = ["slug"]
    ordering = ["-id"] # Modificar a ordenação
    list_filter = ["enabled", "created_at"] # Filtrando
    search_fields = ["company_name", "email"] # Fazendo uma pesquisa
    list_display_links = ["company_name"] # Criado um link
    list_editable = ["fantasy_name"] # Pode editar as informações dentro da linha já, só não pode ser o campo de display_links
    list_per_page = 100 # Quantos itens por pagina
    list_max_show_all = 1000 # Altera o mostrar tudo e limita uma quantidade