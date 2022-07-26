from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )  # dateField는 날짜만, datetimeField는 날짜와 시간  // auto_now_add는 만들자마자 생성일시 추가되는 것, auto_now는 수정될 때 추가
    updated = models.DateTimeField(auto_now=True)

    class Meta:  #  추상화된 데이터값, 이렇게 해놓으면 데이터베이스에 얘만 따로 만들지 않아서 데이터 효율성 up
        abstract = True
