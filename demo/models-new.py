from django.db import models
# from django.utils import timezone

# SC: see UserProfile below
# from django.contrib.auth.models import User

# SC: date
# from datetime import date
import Member
import Provider

# Create your models here.


class Pharmacy(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    pharmacy_key = models.CharField(max_length=20)
    pharmacy_name = models.CharField(max_length=20)
    pharmacy_chain = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40)

    def __str__(self):
        return str(self.pharmacy_key) + "_" + self.pharmacy_name


class DrugInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    drug_ndc = models.CharField(max_length=12)
    drug_name = models.CharField(max_length=20)
    drug_details = models.CharField(max_length=40)
    drug_type = models.CharField(max_length=20)
    therapeutic_class = models.CharField(max_length=20)
    pkg_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    pkg_units = models.CharField(max_length=10)
    days_supply = models.DecimalField(max_digits=4, decimal_places=0)
    dose = models.DecimalField(max_digits=10, decimal_places=4)
    dose_units = models.CharField(max_length=10)
    take_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    take_units = models.CharField(max_length=10)
    take_frequency = models.DecimalField(max_digits=2, decimal_places=0)
    frequency_units = models.CharField(max_length=10)
    take_instructions = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id) + "_" + self.drug_name + "_" + str(
            self.drug_ndc)


class RxClaim(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    biller = models.ForeignKey(Provider, related_name='billed_claims')
    # druginfo = models.ForeignKey(DrugInfo, on_delete=models.CASCADE)
    # pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    prescription_ref = models.CharField(max_length=20)
    source_code = models.CharField(max_length=12)

    provider_code = models.CharField(max_length=12)
    provider_npi = models.CharField(max_length=10)
    provider_name = models.CharField(max_length=50)
    practice_name = models.CharField(max_length=50)

    drug_ndc = models.CharField(max_length=12)
    drug_name = models.CharField(max_length=20)
    drug_details = models.CharField(max_length=40)  # package dose etc
    drug_type = models.CharField(max_length=20)  # brand generic
    therapeutic_class = models.CharField(max_length=20)  # hepatitis

    pharmacy_key = models.CharField(max_length=20)
    pharmacy_name = models.CharField(max_length=20)
    pharmacy_chain = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40)

    prescribed_date = models.DateTimeField()
    refills_prescribed = models.DecimalField(max_digits=2, decimal_places=0)
    refills_remaining = models.DecimalField(max_digits=2, decimal_places=0)
    script_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    script_units = models.CharField(max_length=10)
    days_supply = models.DecimalField(max_digits=4, decimal_places=0)
    dose = models.DecimalField(max_digits=10, decimal_places=4)
    dose_units = models.CharField(max_length=10)
    take_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    take_units = models.CharField(max_length=10)
    take_frequency = models.DecimalField(max_digits=2, decimal_places=0)
    frequency_units = models.CharField(max_length=10)
    take_instructions = models.CharField(max_length=40)

    service_date = models.DateTimeField()  # date filled
    received_date = models.DateTimeField()
    paid_date = models.DateTimeField(blank=True, null=True)
    adjusted_date = models.DateTimeField(blank=True, null=True)
    billed = models.DecimalField(max_digits=8, decimal_places=2)
    allowed = models.DecimalField(max_digits=8, decimal_places=2)
    denied = models.DecimalField(max_digits=8, decimal_places=2)
    plan_paid = models.DecimalField(max_digits=8, decimal_places=2)
    member_paid = models.DecimalField(max_digits=8, decimal_places=2)
    plan_deductible = models.DecimalField(max_digits=8, decimal_places=2)
    adjusted = models.NullBooleanField(blank=True, null=True)
    initial_paid_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    adjusted_by = models.ForeignKey('auth.User')
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
    biller = models.ForeignKey(Provider, related_name='billed_claims')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    claim_ref = models.CharField(max_length=20)
    claim_line = models.DecimalField(max_digits=4, decimal_places=0)
    claim_type = models.CharField(max_length=20)  # script, professional, institutional
    source_code = models.CharField(max_length=12)

    provider_type = models.CharField(max_length=12, blank=True, null=True)
    provider_code = models.CharField(max_length=12)
    provider_npi = models.CharField(max_length=10)
    provider_name = models.CharField(max_length=50)
    practice_name = models.CharField(max_length=50)

    facility_type = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40)

    service_type    # snf level, inpatient stay type
    procedure_code
    procedure_desc
    primary_diagnosis
    primary_diag_desc
    primary_diag_group
    all_diag_code

    drg_code
    drg_desc
    diagnosis_poa  # present on admission
    discharge_date
    discharge_status
    readmit_date
    length_of_stay
    allowed_stay
    capitated_amt

    service_date = models.DateTimeField()
    received_date = models.DateTimeField()
    paid_date = models.DateTimeField(blank=True, null=True)
    adjusted_date = models.DateTimeField(blank=True, null=True)
    billed = models.DecimalField(max_digits=8, decimal_places=2)
    allowed = models.DecimalField(max_digits=8, decimal_places=2)
    denied = models.DecimalField(max_digits=8, decimal_places=2)
    plan_paid = models.DecimalField(max_digits=8, decimal_places=2)
    member_paid = models.DecimalField(max_digits=8, decimal_places=2)
    plan_deductible = models.DecimalField(max_digits=8, decimal_places=2)
    adjusted = models.NullBooleanField(blank=True, null=True)
    initial_paid_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    initial_denied_amt = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    adjusted_by = models.ForeignKey('auth.User')
    is_current = models.NullBooleanField(blank=True, null=True)
    status = models.CharField(max_length=10)
    info_code = models.CharField(max_length=10, blank=True, null=True)  # denial_code
    info_desc = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.member_id) + "_" + self.drug_name + "_" + str(
            self.filled_date.strftime('%y%m%d'))
