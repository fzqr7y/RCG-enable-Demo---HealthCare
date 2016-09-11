from django.db import models
# from django.utils import timezone

# Create your models here.


class ApiData(models.Model):
    member = models.ForeignKey('demo.Member', blank=True, null=True)
    record_type = models.CharField(max_length=40)
    record_date = models.DateTimeField()
    value = models.DecimalField(max_digits=10, decimal_places=4)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User')
    ext_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.record_type + "_" + str(
            self.member_id) + "_" + self.record_date.strftime('%y%m%d')


class IntradayData(models.Model):
    api_record = models.ForeignKey('ApiData')
    member = models.ForeignKey('demo.Member', blank=True, null=True)
    record_type = models.CharField(max_length=40)
    record_date = models.DateTimeField()
    value = models.DecimalField(max_digits=10, decimal_places=4)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User')
    ext_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + "_" + str(
            self.member_id) + "_" + self.record_type
