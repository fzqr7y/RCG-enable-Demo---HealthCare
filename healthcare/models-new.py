from django.db import models
from django.utils import timezone

# SC: date
# from datetime import date

# SC: see UserProfile below
# from django.contrib.auth.models import User
# SC: date
# from datetime import date
import Member
import Provider

# Create your models here.


# class CountyMetrics(models.Model):
#     year = models.IntegerField()
#     measure_key = models.CharField(max_length=10)
#     measure_name = models.CharField(max_length=40)
#     measure_desc = models.TextField(max_length=40)
#     val_1_key = models.CharField(max_length=10)
#     val_1_name = models.CharField(max_length=40)
#     val_1_desc = models.TextField(max_length=40)
#     val_2_key = models.CharField(max_length=10)
#     val_2_name = models.CharField(max_length=40)
#     val_2_desc = models.TextField(max_length=40)
#     val_3_key = models.CharField(max_length=10)
#     val_3_name = models.CharField(max_length=40)
#     val_3_desc = models.TextField(max_length=40)
#     val_4_key = models.CharField(max_length=10)
#     val_4_name = models.CharField(max_length=40)
#     val_4_desc = models.TextField(max_length=40)
#     val_5_key = models.CharField(max_length=10)
#     val_5_name = models.CharField(max_length=40)
#     val_5_desc = models.TextField(max_length=40)
#     val_6_key = models.CharField(max_length=10)
#     val_6_name = models.CharField(max_length=40)
#     val_6_desc = models.TextField(max_length=40)
#     val_7_key = models.CharField(max_length=10)
#     val_7_name = models.CharField(max_length=40)
#     val_7_desc = models.TextField(max_length=40)

#     def __str__(self):
#         return str(self.year) + "_" + self.measure_key #}


# class CountyData(models.Model):
#     year = models.IntegerField()
#     fips = models.IntegerField()
#     state = models.CharField(max_length=2)
#     state_name = models.CharField(max_length=20)
#     county = models.CharField(max_length=20)
#     measure_key = models.CharField(max_length=10)
#     category = models.CharField(max_length=40)
#     measure_name = models.CharField(max_length=40)
#     measure_desc = models.TextField()

#     def __str__(self):
#         return str(self.year) + "_" + self.measure_key


class Pharmacy(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    pharmacy_key = models.CharField(max_length=20, blank=True, null=True)
    pharmacy_name = models.CharField(max_length=20)
    pharmacy_chain = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.pharmacy_key) + "_" + self.pharmacy_name


class Drug(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    ndc = models.CharField(max_length=12, blank=True, null=True)
    name = models.CharField(max_length=20)
    details = models.CharField(max_length=40, blank=True, null=True)
    drug_type = models.CharField(max_length=20, blank=True, null=True)
    therapeutic_class = models.CharField(max_length=20)
    pkg_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    pkg_units = models.CharField(max_length=10)
    pkg_days_supply = models.IntegerField()
    dose = models.DecimalField(max_digits=10, decimal_places=4)
    dose_units = models.CharField(max_length=10)
    take_quantity = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    take_units = models.CharField(max_length=10, blank=True, null=True)
    take_frequency = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    frequency_units = models.CharField(max_length=10, blank=True, null=True)
    take_instructions = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.id) + "_" + self.drug_name + "_" + str(
            self.drug_ndc)


class RxClaim(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    biller = models.ForeignKey(Provider, related_name='billed_scripts', blank=True, null=True)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    prescription_ref = models.CharField(max_length=20, blank=True, null=True)
    source_code = models.CharField(max_length=12, blank=True, null=True)

    # provider_code = models.CharField(max_length=12)
    # provider_npi = models.CharField(max_length=10)
    # provider_name = models.CharField(max_length=50)
    # practice_name = models.CharField(max_length=50)

    # drug_ndc = models.CharField(max_length=12)
    # drug_name = models.CharField(max_length=20)
    # drug_details = models.CharField(max_length=40)  # package dose etc
    # drug_type = models.CharField(max_length=20)  # brand generic
    # therapeutic_class = models.CharField(max_length=20)  # hepatitis

    # pharmacy_key = models.CharField(max_length=20)
    # pharmacy_name = models.CharField(max_length=20)
    # pharmacy_chain = models.CharField(max_length=20, blank=True, null=True)
    # city = models.CharField(max_length=20)
    # state = models.CharField(max_length=2)
    # zip = models.CharField(max_length=10)
    # phone = models.CharField(max_length=20)
    # email = models.CharField(max_length=40)

    prescribed_date = models.DateTimeField()
    refills_prescribed = models.IntegerField()
    refills_remaining = models.IntegerField()
    script_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    script_units = models.CharField(max_length=10)
    days_supply = models.IntegerField()
    # dose = models.DecimalField(max_digits=10, decimal_places=4)
    # dose_units = models.CharField(max_length=10)
    # take_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    # take_units = models.CharField(max_length=10)
    # take_frequency = models.DecimalField(max_digits=2, decimal_places=0)
    # frequency_units = models.CharField(max_length=10)
    # take_instructions = models.CharField(max_length=40)

    service_date = models.DateTimeField()  # date filled
    received_date = models.DateTimeField(default=timezone.now)
    paid_date = models.DateTimeField(blank=True, null=True)
    adjusted_date = models.DateTimeField(blank=True, null=True)
    billed = models.DecimalField(max_digits=8, decimal_places=2)
    allowed = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    denied = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    plan_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    member_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    plan_deductible = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    adjusted = models.NullBooleanField(blank=True, null=True)
    initial_paid_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    adjusted_by = models.ForeignKey('auth.User', blank=True, null=True)
    is_current = models.NullBooleanField(blank=True, null=True)
    status = models.CharField(max_length=10)
    info_code = models.CharField(max_length=10, blank=True, null=True)  # denial_code
    info_desc = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.member_id) + "_" + self.drug_name + "_" + str(
            self.filled_date.strftime('%y%m%d'))


class ClaimLine(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    biller = models.ForeignKey(Provider, related_name='billed_claims', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    claim_ref = models.CharField(max_length=20)
    claim_line = models.IntegerField()
    claim_type = models.CharField(max_length=20)  # script, professional, institutional
    source_code = models.CharField(max_length=12, blank=True, null=True)

    # provider_type = models.CharField(max_length=12, blank=True, null=True)
    # provider_code = models.CharField(max_length=12)
    # provider_npi = models.CharField(max_length=10)
    # provider_name = models.CharField(max_length=50)
    # practice_name = models.CharField(max_length=50)

    # city = models.CharField(max_length=20)
    # state = models.CharField(max_length=2)
    # zip = models.CharField(max_length=10)
    # phone = models.CharField(max_length=20)
    # email = models.CharField(max_length=40)

    facility_type = models.CharField(max_length=20, blank=True, null=True)
    service_type = models.CharField(max_length=20, blank=True, null=True)
    # snf level, inpatient stay type
    procedure_code = models.CharField(max_length=10, blank=True, null=True)
    procedure_desc = models.CharField(max_length=40, blank=True, null=True)
    primary_diagnosis = models.CharField(max_length=10, blank=True, null=True)
    primary_diag_desc = models.CharField(max_length=40, blank=True, null=True)
    primary_diag_group = models.CharField(max_length=20, blank=True, null=True)
    all_diag_code = models.CharField(max_length=80, blank=True, null=True)

    drg_code = models.CharField(max_length=10, blank=True, null=True)
    drg_desc = models.CharField(max_length=40, blank=True, null=True)
    diagnosis_poa = models.NullBooleanField(blank=True, null=True)
    # present on admission
    discharge_date = models.DateTimeField(blank=True, null=True)
    discharge_status = models.CharField(max_length=10, blank=True, null=True)
    readmit_date = models.DateTimeField(blank=True, null=True)
    length_of_stay = models.IntegerField(blank=True, null=True)
    allowed_stay = models.IntegerField(blank=True, null=True)
    capitated_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    service_date = models.DateTimeField()
    received_date = models.DateTimeField()
    paid_date = models.DateTimeField(blank=True, null=True)
    adjusted_date = models.DateTimeField(blank=True, null=True)
    billed = models.DecimalField(max_digits=8, decimal_places=2)
    allowed = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    denied = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    plan_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    member_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    plan_deductible = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    adjusted = models.NullBooleanField(blank=True, null=True)
    initial_paid_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    initial_denied_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    adjusted_by = models.ForeignKey('auth.User', blank=True, null=True)
    is_current = models.NullBooleanField(blank=True, null=True)
    status = models.CharField(max_length=10)
    info_code = models.CharField(max_length=10, blank=True, null=True)  # denial_code
    info_desc = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.id) + "_" + str(self.member_id) + "_" + str(
            self.provider_id) + "_" + self.service_date.strftime('%y%m%d')
