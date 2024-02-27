from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import SuppliersForm
from .models import Suppliers
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class SuppliersListView(LoginRequiredMixin, ListView):
    model = Suppliers
    template_name = "suppliers/index.html"
    paginate_by = 1
    ordering = "-id"


class SuppliersSearchView(ListView):
    model = Suppliers
    template_name = "suppliers/search.html"
    paginate_by = 1

    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        if not search_value:
            return Suppliers.objects.all().order_by("-id")
        return Suppliers.objects.filter(Q(fantasy_name__icontains=search_value)|
                                            Q(company_name__icontains=search_value)).order_by("-id")


class SuppliersCreateView(CreateView):
    model = Suppliers
    template_name = "suppliers/create.html"
    form_class = SuppliersForm
    success_url = reverse_lazy("suppliers:index")

    def form_valid(self, form):
        messages.success(self.request, "Fornecedor cadastrado com sucesso!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_action"] = reverse("suppliers:create")
        return context


class SuppliersUpdateView(UpdateView):
    model = Suppliers
    form_class = SuppliersForm
    template_name = "suppliers/update.html"
    success_url = reverse_lazy("suppliers:index")

    def form_valid(self, form):
        messages.success(self.request, "Fornecedor atualizado com sucesso!")
        return super().form_valid(form)
    

class SuppliersDeleteView(DeleteView):
    model = Suppliers
    success_url = reverse_lazy("suppliers:index")


@require_POST
def toggle_enabled(request, id):
    supplier = get_object_or_404(Suppliers, pk=id)

    supplier.enabled = not supplier.enabled
    supplier.save()

    JsonResponse({ "message": "sucess" })

    return JsonResponse({ "message": "sucess" })