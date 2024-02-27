from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .forms import ProductsForm, CategoryForm, SupplierProductFormSet, SupplierProduct
from .models import Products, Category
from django.db import IntegrityError
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin

def index(request):
    products = Products.objects.order_by("-id")
    
    # Aplicando a paginação
    paginator = Paginator(products, 100)
    # /fornecedores?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = { "products": page_obj }
    return render(request, "products/index.html", context)

def search(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip() # para remover os espaços .strip
    
    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:index")

    # Filtrando os produtos por nome
    products = Products.objects \
        .filter(Q(name__icontains=search_value) | Q(category__name__icontains=search_value)) \
        .order_by("-id")

    # Aplicando a paginação
    paginator = Paginator(products, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = { "products": page_obj }
    return render(request, "products/index.html", context)

def create(request):
    form_action = reverse("products:create")
    # POST
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save()
            supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)
            
            if supplier_product_formset.is_valid():
                supplier_product_formset.save()
                messages.success(request, "O produto foi cadastrado com sucesso!")
            else:
                messages.error(request, "Falha ao cadastrar o produto.")
                product.delete()
                supplier_product_formset = SupplierProductFormSet(request.POST)
                context = { 
                    "form": form,
                    "form_action": form_action,
                    "supplier_product_formset": supplier_product_formset
                }
                return render(request, "products/create.html", context)

            return redirect("products:index")
        
        messages.error(request, "Falha ao cadastrar o produto. Verifique o preenchimento dos campos.")
        supplier_product_formset = SupplierProductFormSet(request.POST)
        context = { 
            "form": form,
            "form_action": form_action,
            "supplier_product_formset": supplier_product_formset
        }
        return render(request, "products/create.html", context)

    # GET
    form = ProductsForm()
    supplier_product_formset = SupplierProductFormSet()

    context = { 
        "form": form, 
        "form_action": form_action,
        "supplier_product_formset": supplier_product_formset

    }
    
    return render(request, "products/create.html", context)

def update(request, slug):
    product = get_object_or_404(Products, slug=slug)
    form_action = reverse("products:update", args=(slug,))

    #POST 
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES, instance=product)
        supplier_product_formset = SupplierProductFormSet(request.POST, instance=product)

        if form.is_valid():
            try:
                if form.cleaned_data["photo"] is False:
                    product.thumbnail.delete(save=False)
                form.save()
                if supplier_product_formset.is_valid():
                    supplier_product_formset.save()
                    messages.success(request,"Produto atualizado com sucesso!")
                    return redirect("products:index")
                else:
                    messages.error(request, "Erro ao atualizar o produto. Verifique os campos de fornecedor.")
            except IntegrityError:
                messages.error(request,"Não é possível cadastrar o mesmo fornecedor para o mesmo produto.")
        else:
            messages.error(request, "Erro ao atualizar o produto. Verifique os campos.")

        supplier_product_formset = SupplierProductFormSet(instance=product)
        context = { 
            "form_action": form_action,
            "form": form, 
            "supplier_product_formset": supplier_product_formset,
        }
        return render(request, "products/create.html", context)

    #GET
    form = ProductsForm(instance=product)
    supplier_product_formset = SupplierProductFormSet(instance=product)
    context = { 
        "form_action": form_action,
        "form": form, 
        "supplier_product_formset": supplier_product_formset,
    }
    return render(request, "products/create.html", context)

@require_POST
def delete(request, id):
    products = get_object_or_404(Products, pk=id)
    products.delete()

    return redirect("products:index")

@require_POST
def toggle_enabled(request, id):
    product = get_object_or_404(Products, pk=id)

    product.enabled = not product.enabled
    product.save()

    JsonResponse({ "message": "sucess" })

    return JsonResponse({ "message": "sucess" })

###################### Categorias #################
    
class CategoryListView(PermissionRequiredMixin, ListView):
    model = Category
    template_name = "categories/index.html"
    paginate_by = 100
    permission_required = "products.view_category"


def search_categories(request):
    # Obtendo o valor da requisição (Formulário)
    search_value = request.GET.get("q").strip() # para remover os espaços .strip
    
    # Verificando se algo foi digitado
    if not search_value:
        return redirect("products:categories")

    # Filtrando os produtos por nome
    categories = Category.objects.filter(name__icontains=search_value).order_by("-id")

    # Aplicando a paginação
    paginator = Paginator(categories, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = { "categories": page_obj }
    return render(request, "categories/index.html", context)

def create_category(request):
    form_action = reverse("products:category_create")

    # POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "A categoria foi cadastrada com sucesso!")
            return redirect("products:categories")
        
        messages.error(request, "Falha ao cadastrar a categoria. Verifique o preenchimento dos campos.")

        context = { 
            "form": form,
            "form_action": form_action,
        }

        return render(request, "categories/create.html", context)

    # GET
    form = CategoryForm()
    context = { 
        "form": form, 
        "form_action": form_action 
    }
    return render(request, "categories/create.html", context)

def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form_action = reverse("products:category_update", args=(slug,))

    #POST 
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request,"Categoria atualizado com sucesso!")
            return redirect("products:categories")
        else:
            messages.error(request, "Erro ao atualizar a categoria. Verifique os dados informados.")
        
        context = { 
            "form_action": form_action,
            "form": form, 
        }

        return render(request, "categories/create.html", context)

    #GET
    form = CategoryForm(instance=category)
    context = { 
        "form_action": form_action,
        "form": form, 
    }
    return render(request, "categories/create.html", context)

@require_POST
def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()

    return redirect("products:categories")

@require_GET
def get_suppliers_from_product(request, id):
    suppliers = SupplierProduct.objects.filter(product__id=id).order_by("-id")

    # Serialização
    suppliers_serialized = [{
        "id": supplierProduct.id,
        "name": supplierProduct.supplier.fantasy_name,
        "cost_price": supplierProduct.cost_price
    } for supplierProduct in suppliers]
    
    return JsonResponse(suppliers_serialized, safe=False)