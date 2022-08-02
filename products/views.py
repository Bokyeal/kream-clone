from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from math import ceil
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.utils import timezone
# Create your views here.


# def product_list(request):
#     #파이썬으로만

#     # page= int(request.GET.get("page", 1)) # 1은 디폴트값
#     # page_size= 10
#     # limit=page_size * page
#     # offset=limit - page_size
#     # products = models.Product.objects.all()[offset:limit]
#     # page_count= ceil(models.Product.objects.count() / page_size) # 소수부가 있는 경우 무조건 올림
#     # if page > page_count:# 가진 페이지보다 많은 수를 입력할 경우 첫페이지로
#     #     return redirect('/products')
#     # return render(request, "product_list.html", {"products": products, "page": page, "page_count": page_count})
    
    
#     #장고 약간
#     page= int(request.GET.get("page", 1)) # 1은 디폴트값
#     product_list = models.Product.objects.all()
#     paginator=Paginator(product_list, 13) # 두번째는 페이지당 보여줄 게시물
#     products=paginator.get_page(page)
#     return render(request, "product_list.html", {"products": products, "page": page})

class ProductListView(ListView):
    model=models.Product
    template_name='products/product_list.html'
    context_object_name="products" # 템플릿에서 전체 데이터를 사용할 이름
    paginate_by=13 # 보여줄 페이지
    ordering=["created"]
    #page_kwarg    /?'변수이름
    #paginate_orphans   페이지를 이루기 위한 최소 단위       https://ccbv.co.uk/projects/Django/3.2/django.views.generic.list/ListView/

    #변수를 html에서 사용하기 위한 메서드. []안에 이름과 = 뒤에 값을 쓴다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["hans"]= 'im hans' # 추가하고 싶으면 context[] 해서 더 추가하면 됨
        return context
    