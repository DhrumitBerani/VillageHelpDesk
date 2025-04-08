from django.contrib import admin
from .models import Profile, Village, Voting, Complaints, News,Tax, BirthCertificate, CastCertificate, CharacterCertificate, DeathCertificate, IncomeCertificate, LandOwnershipCertificate, NonCreamyLayerCertificate

# Register your models here.

admin.site.register(Voting)
admin.site.register(Complaints)
admin.site.register(Tax)
admin.site.register(BirthCertificate)
admin.site.register(CastCertificate)
admin.site.register(CharacterCertificate)
admin.site.register(DeathCertificate)
admin.site.register(IncomeCertificate)
admin.site.register(LandOwnershipCertificate)
admin.site.register(NonCreamyLayerCertificate)
admin.site.register(News)

class VillageAdmin(admin.ModelAdmin):
    list_display = ['VillageId','village_name']
    list_filter = ['talati_id']

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['type']

admin.site.register(Village,VillageAdmin)
admin.site.register(Profile,ProfileAdmin)
