from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms
from math import ceil
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q
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
    #page_kwarg='bok'    #      /?'변수이름'
    #paginate_orphans   페이지를 이루기 위한 최소 단위       https://ccbv.co.uk/projects/Django/3.2/django.views.generic.list/ListView/

    #변수를 html에서 사용하기 위한 메서드. []안에 이름과 = 뒤에 값을 쓴다.
    def get_context_data(self, **kwargs):#다른 변수를 추가적으로 사용하기 위한 메서드
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["hans"]= 'im hans' # 추가하고 싶으면 context[] 해서 더 추가하면 됨
        return context


def test(request):
    return render(request, 'products/test.html')


#FBV
# def detail(request, pk):
#     #에러처리법
#     # try:
#     #     product=models.Product.objects.get(pk=pk)
#     #     return render(request, 'products/detail.html', {'product': product})
#     # except models.Product.DoesNotExist:  #범위를 넘는 요청
#     #     return redirect("/products")
#     # except Exception:               #모든 에러
#     #     return redirect("/products")

#     product=models.Product.objects.get(pk=pk)
#     print(product)
#     return render(request, 'products/detail.html', {'product': product})

class ProductDetail(DetailView):
    model=models.Product
    template_name='products/detail.html'


def search(request):
    keyword = request.GET.get('keyword', None) # keyword는 html의 name값 두번째는 디폴트값
    price=request.GET.getlist('price', None) # html form에서 여러 값을 받을 경우 getlist
    form=forms.SearchForm(request.GET) #request.GET을 쓰면 검색해도 값이 그대로 유지
    brands=request.GET.getlist('brands', None)
    q=Q()
    filter_args={}
    if form.is_valid():
        if len(brands) > 0:
            filter_args['brand__id__in']=brands
            # models.Product.objects.filter(brand__id__in=brands)

        if len(price)>0:
            if '-100000' in price: # '-100000'은 html input에 value로 쓴 값임
                q.add(Q(released_price__lt=100000), q.OR) 
            #    results=models.Product.objects.filter(released_price__lt=100000)
            if '100000-300000' in price:
                q.add(Q(released_price__lt=300000, released_price__gt=100000), q.OR)
            #    results=models.Product.objects.filter(released_price__lt=300000, released_price__gt=100000)
            if '300000-500000' in price:
                q.add(Q(released_price__lt=500000, released_price__gt=300000), q.OR) # lt gt는 미만 초과, 이상 이하는 lte, gte
            #    results=models.Product.objects.filter(released_price__lt=500000, released_price__gt=300000)
            if '500000' in price:
                q.add(Q(released_price__gt=500000), q.OR)
            #    results=models.Product.objects.filter(released_price__gt=500000)
        if keyword is not None and keyword !="":
        #     results= models.Product.objects.filter(Q(name_en__icontains=keyword) | Q(brand__name__icontains=keyword))  #name_en 뒤에 __contains(대소문자 구분) 혹은 __icontains(대소문자 구분x) 넣으면 내장 메서드 사용                                        brand는 Product 내 변수 이름이고 언더바 두번 쓰면 브랜드 변수와 포린키 관계인 모델의 변수 이름 사용가능
        # # 검색에서 두개 이상의 조건에서 하나라도 만족하는 경우를 설정할 경우 Q 객체를 사용한다.
        # else:
        #     results=models.Product.objects.all()
            q.add(
                Q(name_en__icontains=keyword) 
                | Q(model_number__contains=keyword)
                | Q(brand__name__icontains=keyword),
                q.AND
            )
            # results=models.Product.objects.filter(q, **filter_args) # 여기서 오름차순 등 하고 싶으면 order_by()로 해결/ **는 중괄호 벗기는 거
            # else:
            #     results=models.Product.objects.all()
    results=models.Product.objects.filter(q, **filter_args)   # 앞에 q에 조건을 넣어서 마지막에 q로 필터링. q.OR는 두개 이상의 조건중 하나라도 부합된다면 이라는 뜻
    # else:
    #     results=models.Product.objects.all()

    
    return render(request, 'products/search.html', {'results': results, 'keyword': keyword, 'price': price, 'form': form})