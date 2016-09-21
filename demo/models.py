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
    county = models.CharField(max_length=20, blank=True, null=True)

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
    provider_type = models.CharField(max_length=12, blank=True, null=True)
    county = models.CharField(max_length=20, blank=True, null=True)

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


class CountyWidget(models.Model):
    widget_name = models.CharField(max_length=20)
    category = models.CharField(max_length=40, blank=True, null=True)
    measure_name = models.CharField(max_length=40)
    description = models.TextField(blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    val1_ref = models.CharField(max_length=20, blank=True, null=True)
    val2_ref = models.CharField(max_length=20, blank=True, null=True)
    val3_ref = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.widget_name + "_" + str(self.display_order) + "_" + self.measure_key


class CountyData(models.Model):
    year = models.IntegerField()
    fips = models.IntegerField()
    state_name = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=40)
    death_1 = models.IntegerField(blank=True, null=True)
    death_2 = models.IntegerField(blank=True, null=True)
    death_lo = models.IntegerField(blank=True, null=True)
    death_hi = models.IntegerField(blank=True, null=True)
    death_q = models.IntegerField(blank=True, null=True)
    health_1 = models.IntegerField(blank=True, null=True)
    health_lo = models.IntegerField(blank=True, null=True)
    health_hi = models.IntegerField(blank=True, null=True)
    health_q = models.IntegerField(blank=True, null=True)
    phealthdays_1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    phealthdays_lo = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    phealthdays_hi = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    phealthdays_q = models.IntegerField(blank=True, null=True)
    mhealthdays_1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mhealthdays_lo = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mhealthdays_hi = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mhealthdays_q = models.IntegerField(blank=True, null=True)
    bweight_na = models.NullBooleanField(blank=True, null=True)
    bweight_1 = models.IntegerField(blank=True, null=True)
    bweight_2 = models.IntegerField(blank=True, null=True)
    bweight_e = models.IntegerField(blank=True, null=True)
    bweight_lo = models.IntegerField(blank=True, null=True)
    bweight_hi = models.IntegerField(blank=True, null=True)
    bweight_q = models.IntegerField(blank=True, null=True)
    smoke_1 = models.IntegerField(blank=True, null=True)
    smoke_lo = models.IntegerField(blank=True, null=True)
    smoke_hi = models.IntegerField(blank=True, null=True)
    smoke_q = models.IntegerField(blank=True, null=True)
    obese_1 = models.IntegerField(blank=True, null=True)
    obese_lo = models.IntegerField(blank=True, null=True)
    obese_hi = models.IntegerField(blank=True, null=True)
    obese_q = models.IntegerField(blank=True, null=True)
    food_1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    food_q = models.IntegerField(blank=True, null=True)
    inact_1 = models.IntegerField(blank=True, null=True)
    inact_lo = models.IntegerField(blank=True, null=True)
    inact_hi = models.IntegerField(blank=True, null=True)
    inact_q = models.IntegerField(blank=True, null=True)
    exopp_1 = models.IntegerField(blank=True, null=True)
    exopp_q = models.IntegerField(blank=True, null=True)
    drink_1 = models.IntegerField(blank=True, null=True)
    drink_lo = models.IntegerField(blank=True, null=True)
    drink_hi = models.IntegerField(blank=True, null=True)
    drink_q = models.IntegerField(blank=True, null=True)
    dwid_1 = models.IntegerField(blank=True, null=True)
    dwid_2 = models.IntegerField(blank=True, null=True)
    dwid_3 = models.IntegerField(blank=True, null=True)
    dwid_lo = models.IntegerField(blank=True, null=True)
    dwid_hi = models.IntegerField(blank=True, null=True)
    dwid_q = models.IntegerField(blank=True, null=True)
    std_1 = models.IntegerField(blank=True, null=True)
    std_2 = models.IntegerField(blank=True, null=True)
    std_q = models.IntegerField(blank=True, null=True)
    tbirth_1 = models.IntegerField(blank=True, null=True)
    tbirth_2 = models.IntegerField(blank=True, null=True)
    tbirth_3 = models.IntegerField(blank=True, null=True)
    tbirth_lo = models.IntegerField(blank=True, null=True)
    tbirth_hi = models.IntegerField(blank=True, null=True)
    tbirth_q = models.IntegerField(blank=True, null=True)
    unins_1 = models.IntegerField(blank=True, null=True)
    unins_2 = models.IntegerField(blank=True, null=True)
    unins_lo = models.IntegerField(blank=True, null=True)
    unins_hi = models.IntegerField(blank=True, null=True)
    unins_q = models.IntegerField(blank=True, null=True)
    pcp_1 = models.IntegerField(blank=True, null=True)
    pcp_2 = models.IntegerField(blank=True, null=True)
    pcp_3 = models.CharField(max_length=10, blank=True, null=True)
    pcp_q = models.IntegerField(blank=True, null=True)
    dent_1 = models.IntegerField(blank=True, null=True)
    dent_2 = models.IntegerField(blank=True, null=True)
    dent_3 = models.CharField(max_length=10, blank=True, null=True)
    dent_q = models.IntegerField(blank=True, null=True)
    mhp_1 = models.IntegerField(blank=True, null=True)
    mhp_2 = models.IntegerField(blank=True, null=True)
    mhp_3 = models.CharField(max_length=10, blank=True, null=True)
    mhp_q = models.IntegerField(blank=True, null=True)
    phosp_1 = models.IntegerField(blank=True, null=True)
    phosp_2 = models.IntegerField(blank=True, null=True)
    phosp_lo = models.IntegerField(blank=True, null=True)
    phosp_hi = models.IntegerField(blank=True, null=True)
    phosp_q = models.IntegerField(blank=True, null=True)
    diab_1 = models.IntegerField(blank=True, null=True)
    diab_2 = models.IntegerField(blank=True, null=True)
    diab_lo = models.IntegerField(blank=True, null=True)
    diab_hi = models.IntegerField(blank=True, null=True)
    diab_q = models.IntegerField(blank=True, null=True)
    mamm_1 = models.IntegerField(blank=True, null=True)
    mamm_2 = models.IntegerField(blank=True, null=True)
    mamm_lo = models.IntegerField(blank=True, null=True)
    mamm_hi = models.IntegerField(blank=True, null=True)
    mamm_q = models.IntegerField(blank=True, null=True)
    hs_1 = models.IntegerField(blank=True, null=True)
    hs_2 = models.IntegerField(blank=True, null=True)
    hs_q = models.IntegerField(blank=True, null=True)
    coll_1 = models.IntegerField(blank=True, null=True)
    coll_2 = models.IntegerField(blank=True, null=True)
    coll_3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    coll_lo = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    coll_hi = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    coll_q = models.IntegerField(blank=True, null=True)
    unem_1 = models.IntegerField(blank=True, null=True)
    unem_2 = models.IntegerField(blank=True, null=True)
    unem_3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unem_q = models.IntegerField(blank=True, null=True)
    cpov_1 = models.IntegerField(blank=True, null=True)
    cpov_2 = models.IntegerField(blank=True, null=True)
    cpov_lo = models.IntegerField(blank=True, null=True)
    cpov_hi = models.IntegerField(blank=True, null=True)
    cpov_q = models.IntegerField(blank=True, null=True)
    ineq_1 = models.IntegerField(blank=True, null=True)
    ineq_2 = models.IntegerField(blank=True, null=True)
    ineq_3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ineq_q = models.IntegerField(blank=True, null=True)
    spar_1 = models.IntegerField(blank=True, null=True)
    spar_2 = models.IntegerField(blank=True, null=True)
    spar_3 = models.IntegerField(blank=True, null=True)
    spar_lo = models.IntegerField(blank=True, null=True)
    spar_hi = models.IntegerField(blank=True, null=True)
    spar_q = models.IntegerField(blank=True, null=True)
    assoc_1 = models.IntegerField(blank=True, null=True)
    assoc_2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    assoc_q = models.IntegerField(blank=True, null=True)
    vcrime_1 = models.IntegerField(blank=True, null=True)
    vcrime_2 = models.IntegerField(blank=True, null=True)
    vcrime_q = models.IntegerField(blank=True, null=True)
    indeath_1 = models.IntegerField(blank=True, null=True)
    indeath_2 = models.IntegerField(blank=True, null=True)
    indeath_lo = models.IntegerField(blank=True, null=True)
    indeath_hi = models.IntegerField(blank=True, null=True)
    indeath_q = models.IntegerField(blank=True, null=True)
    air_1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    air_q = models.IntegerField(blank=True, null=True)
    water_1 = models.NullBooleanField(blank=True, null=True)
    water_q = models.IntegerField(blank=True, null=True)
    house_1 = models.IntegerField(blank=True, null=True)
    house_2 = models.IntegerField(blank=True, null=True)
    house_lo = models.IntegerField(blank=True, null=True)
    house_hi = models.IntegerField(blank=True, null=True)
    house_q = models.IntegerField(blank=True, null=True)
    drive_1 = models.IntegerField(blank=True, null=True)
    drive_2 = models.IntegerField(blank=True, null=True)
    drive_3 = models.IntegerField(blank=True, null=True)
    drive_lo = models.IntegerField(blank=True, null=True)
    drive_hi = models.IntegerField(blank=True, null=True)
    drive_q = models.IntegerField(blank=True, null=True)
    commute_1 = models.IntegerField(blank=True, null=True)
    commute_2 = models.IntegerField(blank=True, null=True)
    commute_lo = models.IntegerField(blank=True, null=True)
    commute_hi = models.IntegerField(blank=True, null=True)
    commute_q = models.IntegerField(blank=True, null=True)
