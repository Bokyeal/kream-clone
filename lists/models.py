from django.db import models
from core.models import TimeStampedModel
from products.models import Product
# Create your models here.

class List(TimeStampedModel):
    """관심상품 모델"""
    products=models.ManyToManyField("products.Product", related_name="lists") # 다대다관계  related_name은 다른 클래스에서 사용할 수 있는 이름
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="list") #일대일관계

    def __str__(self):
        return f"{self.user}의 장바구니 {self.products.first()}" # 다대다관계라서 리스트에 담겨있기 때문에 어떤것을 말하는지 정확히 명시해줘야됨

    def count_products(self):
        return self.products.count()

    count_products.short_description="상품 수" # 정의한 함수가 페이지에 보여지는 변수
