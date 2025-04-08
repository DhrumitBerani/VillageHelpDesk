from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    village_id = models.IntegerField(blank=True, null=True)
    verification_code = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=50,blank=True, null=True)
    signature = models.FileField(upload_to='modules/static/uploads/signatures/',blank=True, null=True)
    allocated_villages = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user.id) + " " + str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Village(models.Model):
    VillageId = models.AutoField(primary_key=True)
    village_name = models.CharField(max_length=50)
    talati_id = models.IntegerField()

    def __str__(self):
        return str(self.VillageId) + " " + str(self.village_name)

class Voting(models.Model):
    vote_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    options_list_json = models.TextField()
    status = models.CharField(max_length=50)
    result_json = models.TextField()
    result_date_time = models.DateTimeField()
    voted_user_list = models.TextField()
    village_id = models.IntegerField()

    def __str__(self):
        return self.title
    
class Complaints(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=50)
    answer = models.TextField(blank=True)
    complaint_date_time = models.DateTimeField()
    resolve_date_time = models.DateTimeField(blank=True, null=True)
    sender_username = models.TextField()
    talati_id = models.IntegerField()

    def __str__(self):
        return self.title
    
class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    news_date_time = models.DateTimeField()
    sender_id = models.IntegerField()

    def __str__(self):
        return self.title
    
class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    ward_no = models.CharField(max_length=50)
    tenament_no = models.TextField()
    amount = models.IntegerField()
    payer_username = models.CharField(max_length=50,blank=True, null=True)
    occupier_name = models.CharField(max_length=50)
    occupier_address = models.CharField(max_length=100)
    payment_date_time = models.DateTimeField(blank=True, null=True)
    order_id = models.CharField(max_length=100,blank=True, null=True)
    transaction_id = models.CharField(max_length=200,blank=True, null=True)
    payment_method = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.tenament_no
    
class BirthCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    father_name = models.TextField()
    mother_name = models.TextField()
    address = models.TextField()
    gender = models.CharField(max_length=50)
    birthdate = models.DateField(blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    birth_place = models.TextField()
    weight = models.FloatField()
    photo = models.FileField(upload_to='uploads/birthcertificate/',blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(17024000000000000+self.form_id)
          super().save()

class CastCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    gender = models.CharField(max_length=50)
    parent_name = models.TextField()
    religion = models.TextField()
    cast = models.TextField()
    subcast = models.TextField()
    district = models.TextField()
    taluka = models.TextField()
    village = models.TextField()
    photo = models.FileField(upload_to='uploads/castcertificate/',blank=True, null=True)
    leaving_certificate = models.FileField(upload_to='uploads/castcertificate/',blank=True, null=True)
    family_lc_certificate = models.FileField(upload_to='uploads/castcertificate/',blank=True, null=True)
    electricity_bill = models.FileField(upload_to='uploads/castcertificate/',blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(18025000000000000+self.form_id)
          super().save()

class CharacterCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    gender = models.CharField(max_length=50)
    parent_name = models.TextField()
    years = models.TextField(blank=True, null=True)
    religion = models.TextField()
    district = models.TextField()
    taluka = models.TextField()
    village = models.TextField()
    photo = models.FileField(upload_to='uploads/charactercertificate/',blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(19026000000000000+self.form_id)
          super().save()

class DeathCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    gender = models.CharField(max_length=50)
    father_name = models.TextField()
    mother_name = models.TextField()
    village = models.TextField(blank=True, null=True)
    taluka = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    address_of_deceased = models.TextField()
    place_of_death = models.TextField()
    remarks = models.TextField()
    deathdate = models.DateField(blank=True, null=True)
    registrationdate = models.DateField(blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    id_proof = models.FileField(upload_to='uploads/deathcertificate/',blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(20027000000000000+self.form_id)
          super().save()

class IncomeCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    gender = models.CharField(max_length=50)
    parent_name = models.TextField()
    applicant_income = models.BigIntegerField()
    parent_income = models.BigIntegerField()
    other_income = models.BigIntegerField()
    rupee_in_words = models.TextField()
    district = models.TextField()
    taluka = models.TextField()
    village = models.TextField()
    photo = models.FileField(upload_to='uploads/incomecertificate/',blank=True, null=True)
    ration_card = models.FileField(upload_to='uploads/incomecertificate/',blank=True, null=True)
    electricity_bill = models.FileField(upload_to='uploads/incomecertificate/',blank=True, null=True)
    adhar_card = models.FileField(upload_to='uploads/incomecertificate/',blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(21028000000000000+self.form_id)
          super().save()

class LandOwnershipCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    gender = models.CharField(max_length=50)
    district = models.TextField()
    taluka = models.TextField()
    village = models.TextField()
    voter_id_no = models.CharField(max_length=50,blank=True, null=True)
    land_description = models.TextField()
    land_use = models.TextField()
    age = models.IntegerField(blank=True, null=True)
    parent_name = models.TextField(blank=True, null=True)
    acres = models.TextField(blank=True, null=True)
    photo = models.FileField(upload_to='uploads/landcertificate/',blank=True, null=True)
    st_certificate = models.FileField(upload_to='uploads/landcertificate/',blank=True, null=True)
    land_posession_certi = models.FileField(upload_to='uploads/landcertificate/',blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(22029000000000000+self.form_id)
          super().save()

class NonCreamyLayerCertificate(models.Model):
    form_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    inward_id = models.CharField(max_length=50,blank=True, null=True)
    fullname = models.TextField()
    gender = models.CharField(max_length=50)
    parent_name = models.TextField()
    religion = models.TextField()
    cast = models.TextField()
    subcast = models.TextField()
    district = models.TextField()
    taluka = models.TextField()
    village = models.TextField()
    photo = models.FileField(upload_to='uploads/nclcertificate/',blank=True, null=True)
    leaving_certificate = models.FileField(upload_to='uploads/nclcertificate/',blank=True, null=True)
    income_certificate = models.FileField(upload_to='uploads/nclcertificate/',blank=True, null=True)
    cast_certificate = models.FileField(upload_to='uploads/nclcertificate/',blank=True, null=True)
    ration_card = models.FileField(upload_to='uploads/nclcertificate/',blank=True, null=True)
    electricity_bill = models.FileField(upload_to='uploads/nclcertificate/',blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    form_status = models.CharField(max_length=50)
    application_date = models.DateTimeField(blank=True, null=True)
    talati_id = models.IntegerField(blank=True, null=True)
    user_villageId = models.IntegerField()

    def __str__(self):
        return self.inward_id
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)
       
       if self.inward_id == None:
          self.inward_id = str(23030000000000000+self.form_id)
          super().save()