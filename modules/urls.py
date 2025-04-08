from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('contactusmail', views.contactusmail, name='contactusmail'),
    
    path('register', views.register, name='register'),
    path('handlesignup', views.handlesignup, name='handlesignup'),
    path('login', views.login, name='login'),
    path('handlelogin', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    
##### ----- user dashbaord -----    
    path('userdashboard', views.userdashboard, name='userdashboard'),
    
    #tax section
    path('taxpayment', views.taxpayment, name='taxpayment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    
    #voting section
    path('voting',views.voting,name='voting'),
    path('updatevoting',views.updatevoting,name='updatevoting'),
    
    #complaint section
    path('raisecomplaint',views.raisecomplaint,name='raisecomplaint'),
    path('handleuserquery',views.handleuserquery,name='handleuserquery'),
    path('viewquery/<int:querynum>',views.viewquery,name='viewquery'),
    path('viewpaymentdetails/<int:tax_id>',views.viewpaymentdetails,name='viewpaymentdetails'),

    #profile section
    path('userprofile',views.userprofile,name='userprofile'),
    path('edituserprofile',views.edituserprofile,name='edituserprofile'),
    path('handle_edit_user_profile',views.handle_edit_user_profile,name='handle_edit_user_profile'),
    
##### -----  talati Dashboard  ----- 
    path('talatidashboard',views.talatidashboard,name='talatidashboard'),
    
    path('documenthistory',views.talati_doc_history,name='talati_doc_history'),

    #profile Section
    path('talatiprofile',views.talatiprofile,name='talatiprofile'),
    path('edittalatiprofile',views.edittalatiprofile,name='edittalatiprofile'),
    path('handle_edit_talati_profile',views.handle_edit_talati_profile,name='handle_edit_talati_profile'),
    
    #voting section
    path('managevoting',views.managevoting,name='managevoting'),
    path('addvoting/<int:villageid>',views.addvoting,name='addvoting'),
    path('savevotingoptions',views.savevotingoptions,name='savevotingoptions'),
    path('deletevoting/<int:villageid>/<int:voteid>',views.deletevoting,name='deletevoting'),
    path('declareresult/<int:villageid>/<int:voteid>',views.declareresult,name='declareresult'),
    
    #news section
    path('newssection',views.managenews,name='managenews'),
    path('addnews',views.addnews,name='addnews'),
    path('handle_news_data',views.handle_news_data,name='handle_news_data'),
    path('deletenews/<int:newsid>',views.deletenews,name='deletenews'),

    #complaint section
    path('complaintsection',views.complaintsection,name='complaintsection'),
    path('replycomplaint',views.replycomplaint,name='replycomplaint'),
    path('save_reply',views.save_reply,name='save_reply'),
    path('rejectcomplaint',views.rejectcomplaint,name='rejectcomplaint'),
    
    #document management section
    path('newdocumentrequest',views.new_document_request_options,name='newdocumentrequest'),
    #path('talatidocumentrecords',views.user_doc_records,name='user_doc_records'),       #
    
    path('birthcertiform',views.birth_certificate_form,name='birthcertiform'),
    path('deathcertiform',views.death_certificate_form,name='death_certificate_form'),
    path('incomecertiform',views.income_certificate_form,name='income_certificate_form'),
    path('castcertiform',views.cast_certificate_form,name='cast_certificate_form'),
    path('charactercertiform',views.character_certificate_form,name='character_certificate_form'),
    path('nclcertiform',views.ncl_certificate_form,name='ncl_certificate_form'),
    path('landcertiform',views.land_owner_certificate_form,name='land_owner_certificate_form'),
    
    path('submitapplication',views.handleformsubmission,name='handleformsubmission'),
    path('pdf/<str:document_type>/<int:form_id>',views.MyPDFView.as_view(),name='testpdf'),
    path('viewpdf/<str:document_type>/<int:inward_id>',views.view_pdf,name='view_pdf'),
    
    path('documentrecords',views.document_records,name='document_records'),

##### ----- collector section -----
    path('collectordashboard',views.collectordashboard,name='collectordashboard'),
    
    #profile Section
    path('collectorprofile',views.collectorprofile,name='collectorprofile'),
    path('editcollectorprofile',views.editcollectorprofile,name='editcollectorprofile'),
    path('handle_edit_collector_profile',views.handle_edit_collector_profile,name='handle_edit_collector_profile'),

    path('viewtalatilist',views.viewtalatilist,name='viewtalatilist'),
    
    path('appointtalati',views.appointtalati,name='appointtalati'),
    path('handle_talati_creation',views.handle_talati_creation,name='handle_talati_creation'),
    
    path('transfertalati',views.transfertalati,name='transfertalati'),
    path('searchtalati',views.searchtalati,name='searchtalati'),
    path('update_talati_villages',views.update_talati_villages,name='update_talati_villages'),
    
    path('deletetalati',views.deletetalati,name='deletetalati'),
    path('searchtalatifortermination',views.searchtalatifortermination,name='searchtalatifortermination'),
    path('terminate_talati_process',views.terminate_talati_process,name='terminate_talati_process'),

    # 
    path('talati_doc_request',views.talati_doc_request,name='talati_doc_request'),
    path('birth_table',views.birth_table,name='birth_table'),
    path('death_table',views.death_table,name='death_table'),
    path('cast_table',views.cast_table,name='cast_table'),
    path('income_table',views.income_table,name='income_table'),
    path('land_table',views.land_table,name='land_table'),
    path('cryamy_table',views.cryamy_table,name='cryamy_table'),
    path('character_table',views.character_table,name='character_table'),
    path('approve_request',views.approve_request,name='approve_request'),
    path('reject_request',views.reject_request,name='reject_request'),
    path('user_birth_request',views.user_birth_request,name='user_birth_request'),
    path('user_income_req',views.user_income_req,name='user_income_req'),
    path('user_death_req',views.user_death_req,name='user_death_req'),
    path('user_cast_req',views.user_cast_req,name='user_cast_req'),
    path('user_cryamy_req',views.user_cryamy_req,name='user_cryamy_req'),
    path('user_character_req',views.user_character_req,name='user_character_req'),
    path('user_land_req',views.user_land_req,name='user_land_req'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)