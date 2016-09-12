from django.db import models
from django.utils import timezone

# SC: see UserProfile below
from django.contrib.auth.models import User

# SC: date
from datetime import date

# Create your models here.


# SC: extend standard user with url for picture
# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/
# http://stackoverflow.com/questions/11377424/django-add-field-to-user-profile-admin-form
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # phone = models.CharField(max_length=20, blank=True, null=True)
    # works for using the media directory
    # but not doing that for ease with heroku
    # picture = models.ImageField(
    #   upload_to='user_pictures', blank=True, null=True)
    # picture = models.ImageField(
    #     upload_to='user_pictures', blank=True, null=True)

    # class Meta:
    #     db_table = "demo_user_profile"
    picture_path = models.CharField(max_length=50, blank=True, null=True)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('demo.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Message(models.Model):
    message_type = models.CharField(max_length=20)
    message_from = models.CharField(max_length=20)
    message_to = models.CharField(max_length=20)
    text = models.TextField()
    # query_url = models.TextField(blank=True, null=True)
    sent = models.BooleanField(default=True)
    member = models.ForeignKey('Member', blank=True, null=True)
    user = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    smssid = models.CharField(max_length=40, blank=True, null=True)
    smsstatus = models.CharField(max_length=20, blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user_id) + "_" + str(
            self.message_type) + "_" + self.created_date.strftime('%y%m%d')


class Member(models.Model):
    member_id = models.CharField(max_length=12)
    tax_id = models.CharField(max_length=12)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    birth_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User')
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    social = models.CharField(max_length=40, blank=True, null=True)
    medical_risk = models.DecimalField(
        max_digits=6, decimal_places=4, blank=True, null=True)
    pharmacy_risk = models.DecimalField(
        max_digits=6, decimal_places=4, blank=True, null=True)
    plan_name = models.CharField(max_length=40, blank=True, null=True)
    plan_start = models.DateTimeField(
        blank=True, null=True)
    plan_end = models.DateTimeField(
        blank=True, null=True)
    plan_deductible = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    plan_oop_max = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    picture_path = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.member_id

    def calculate_age(self, born):
        today = date.today()
        before_bd = ((today.month, today.day) < (born.month, born.day))
        return today.year - born.year - before_bd

    def age(self):
        return self.calculate_age(self.birth_date)

    def provider(self, role):
        return self.provider_set.get(providermember__role__exact=role)

    def pcp(self):
        # return self.provider_set.get(providermember__role__exact="PCP")
        return self.provider_set.filter(providermember__role__exact="PCP").first()

    def vitals(self):
        return self.membermedical_set.filter(record_type="Vitals", is_current=True).order_by('id')

    def height(self):
        return self.vitals().get(measure_type="Height")

    def weight(self):
        return self.vitals().get(measure_type="Weight")

    def bp(self):
        return self.vitals().get(measure_type="Blood Pressure")

    def hr(self):
        return self.vitals().get(measure_type="Heart Rate")

    def reported(self):
        return self.membermedical_set.filter(
            record_type="Reported", is_current=True).order_by('id')


class Provider(models.Model):
    provider_id = models.CharField(max_length=12)
    tax_id = models.CharField(max_length=12)
    npi = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    practice_name = models.CharField(max_length=50)
    term_date = models.DateTimeField(
        blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User')
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    social = models.CharField(max_length=40, blank=True, null=True)
    specialty = models.CharField(max_length=40, blank=True, null=True)
    languages = models.CharField(max_length=20, blank=True, null=True)
    next_appt = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(Member, through='ProviderMember')
    picture_path = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.provider_id


class ProviderMember(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    role = models.CharField(max_length=40)
    start_date = models.DateField(default='2000-01-01')
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.provider_id) + "_" + str(self.member_id)


class MemberMedical(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=40)
    measure_type = models.CharField(max_length=40)
    measure_label = models.CharField(max_length=40, blank=True, null=True)
    is_current = models.NullBooleanField(blank=True, null=True)
    value_str = models.CharField(max_length=40, blank=True, null=True)
    value_1 = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_2 = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_1_tgt_hi = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_2_tgt_hi = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_1_tgt_lo = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_2_tgt_lo = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_1_alert_hi = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_2_alert_hi = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_1_alert_lo = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    value_2_alert_lo = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True)
    measure_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    value_1_history = models.TextField(blank=True, null=True)
    value_1_trend = models.DecimalField(
        max_digits=1, decimal_places=0, blank=True, null=True)
    value_2_trend = models.DecimalField(
        max_digits=1, decimal_places=0, blank=True, null=True)

    def __str__(self):
        # return str(self.member_id) + "_" + self.record_type + "_" + str(
        #     self.measure_type) + "_" + str(self.measure_date)
        return str(self.member_id) + "_" + self.record_type + "_" + str(
            self.measure_type) + "_" + self.measure_date.strftime('%y%m%d')

    def value_str_or_num(self):
        return self.value_str or self.value_1

    def display(self):
        return self.value_str or '%.4g' % self.value_1

    def value_1_has_tgt(self):
        return not(self.weight().value_1_tgt_hi is None) or (
            not(self.weight().value_1_tgt_lo is None))

    def value_1_in_tgt(self):
        tgthi = (self.weight().value_1_tgt_hi is None) or (
            self.weight().value_1 <= self.weight().value_1_tgt_hi)
        tgtlo = (self.weight().value_1_tgt_lo is None) or (
            self.weight().value_1 >= self.weight().value_1_tgt_lo)
        return tgthi and tgtlo

    def value_1_has_alert(self):
        return not(self.weight().value_1_alert_hi is None) or (
            not(self.weight().value_1_alert_lo is None))

    def value_1_oo_alert(self):
        alerthi = (self.weight().value_1_alert_hi is None) or (
            self.weight().value_1 > self.weight().value_1_alert_hi)
        alertlo = (self.weight().value_1_alert_lo is None) or (
            self.weight().value_1 < self.weight().value_1_alert_lo)
        return alerthi and alertlo


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
    druginfo = models.ForeignKey(DrugInfo, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    drug_ndc = models.CharField(max_length=12)
    drug_name = models.CharField(max_length=20)
    drug_details = models.CharField(max_length=40)
    drug_type = models.CharField(max_length=20)
    therapeutic_class = models.CharField(max_length=20)
    pharmacy_key = models.CharField(max_length=20)
    pharmacy_name = models.CharField(max_length=20)
    pharmacy_chain = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    prescription_ref = models.CharField(max_length=20)
    prescribed_date = models.DateTimeField()
    filled_date = models.DateTimeField()
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
    billed = models.DecimalField(max_digits=8, decimal_places=2)
    allowed = models.DecimalField(max_digits=8, decimal_places=2)
    plan_paid = models.DecimalField(max_digits=8, decimal_places=2)
    member_paid = models.DecimalField(max_digits=8, decimal_places=2)
    plan_deductible = models.DecimalField(max_digits=8, decimal_places=2)
    is_current = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return str(self.member_id) + "_" + self.drug_name + "_" + str(
            self.filled_date.strftime('%y%m%d'))
