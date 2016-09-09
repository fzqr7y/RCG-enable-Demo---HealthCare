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
    query_url = models.TextField(blank=True, null=True)
    sent = models.BooleanField(default=True)
    member = models.ForeignKey('Member', blank=True, null=True)
    user = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

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
