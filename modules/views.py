import os
import datetime
import json
from datetime import date
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import FileResponse
from django.template import loader
from django.template.loader import get_template
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Complaints, News, Voting, Tax, Village, BirthCertificate, CastCertificate, CharacterCertificate, DeathCertificate, IncomeCertificate, LandOwnershipCertificate, NonCreamyLayerCertificate
# from xhtml2pdf import pisa
from django.contrib import messages
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from pyhanko import stamp
from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec, append_signature_field
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
import razorpay
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def getpath(path):
    first_occurrence = path.find("/uploads")
    path = path[:first_occurrence] + path[first_occurrence:].replace("/uploads", "", 1)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules/static/' + path)
    # return ('/home/dhruv/Dhruv/GMCA Sem 3/SP 2/villagehelpdesk/modules/static/' + path)

def getimagepath(path):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

def sign_pdf(path,type,save_path,sign_path):
    path_cert = getpath('pdfsignatures/newpkcs12.pfx')
    signer = signers.SimpleSigner.load_pkcs12(pfx_file=path_cert, passphrase=b'1234')
    with open(path, 'rb') as doc:
        w = IncrementalPdfFileWriter(doc, strict=False)
        
        if type=="income":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(370, 150, 500, 210)))
        elif type=="birth":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(340, 270, 485, 330)))
        elif type=="cast":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(370, 150, 500, 210)))
        elif type=="character":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(445, 580, 550, 520))) 
        elif type=="ncl":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(370, 150, 500, 210))) #
        elif type=="death":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(300, 330, 430, 240)))
        elif type=="land":
            append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(110, 160, 240, 220)))
        
        first_occurrence = sign_path.find("/uploads")
        # Replace the first occurrence of "/uploads" with an empty string
        # sign_path = sign_path[:first_occurrence] + sign_path[first_occurrence:].replace("/uploads", "", 1)

        # append_signature_field(w,sig_field_spec=SigFieldSpec(sig_field_name="sign", box=(52, 30, 200, 100)))
        meta = signers.PdfSignatureMetadata(field_name='sign')
        pdf_signer = signers.PdfSigner(
            meta, signer=signer, stamp_style=stamp.TextStampStyle(border_width=1,
                stamp_text='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDigital Signature\nSigned by: %(signer)s\nTime: %(ts)s',
                text_box_style=text.TextBoxStyle(font=opentype.GlyphAccumulatorFactory(getpath('/pdfsignatures/NotoSans-Regular.ttf')),border_width=0),
                background=images.PdfImage(sign_path)
            )   
        )
        with open(save_path, 'wb') as outf:
            pdf_signer.sign_pdf(w, output=outf)

def home(request):
   vote = Voting.objects.filter(status="Success").values().order_by('-result_date_time')
   news_list = News.objects.all().order_by('-news_date_time')
   context = {
       "votingresult" : vote,
       "news_list" : news_list,
   }
   return render(request, 'index.html',context=context)

@csrf_exempt
def contactusmail(request):
    subject = "From Village Helpdesk - Contact Us Page"
    message = "Dear sir, " + "\n     " + request.POST.get("firstname") + " " + request.POST.get("lastname") +" has submitted the below message.You may reply to described contact if necessary" + "\n\n\nSender Email: "+ request.POST.get("emailid") + "\nMobile Number: "+ request.POST.get("phonenumber") + "\nMessage: " + request.POST.get("message")
    from_email = settings.EMAIL_HOST_USER
    recepient_list = ["chauhandhruv132002@gmail.com"] #Recepient email id here
    send_mail(subject,message,from_email,recepient_list)    
    context = {
        'contactussubmitstatus' : "true",
    }
    return redirect('/')

def userdashboard(request):
   complaintcount = Complaints.objects.filter(status="Pending",sender_username=request.user.username).count()
   mypayments = Tax.objects.filter(payer_username=request.user.username)
   base_amount = 0
   for payment in mypayments:
    base_amount = base_amount + int(payment.amount)

    model1_count = IncomeCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    model2_count = BirthCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    model3_count = CharacterCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    model4_count = DeathCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    model5_count = CastCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    model6_count = NonCreamyLayerCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    model7_count = LandOwnershipCertificate.objects.filter(form_status="Pending",username=request.user.username).count()
    total_certificate_count = model1_count + model2_count + model3_count + model4_count + model5_count + model6_count + model7_count
   context = {
      'complaint_count' : complaintcount,
      'tax_amount' : base_amount,
      'certificate_count' : total_certificate_count,
   }
   return render(request, 'User/User_dashboard.html',context=context)

def user_doc_records(request):
    model1_queryset = IncomeCertificate.objects.filter(username=request.user.username)
    model2_queryset = BirthCertificate.objects.filter(username=request.user.username)
    model3_queryset = CharacterCertificate.objects.filter(username=request.user.username)
    model4_queryset = DeathCertificate.objects.filter(username=request.user.username)
    model5_queryset = CastCertificate.objects.filter(username=request.user.username)
    model6_queryset = NonCreamyLayerCertificate.objects.filter(username=request.user.username)
    model7_queryset = LandOwnershipCertificate.objects.filter(username=request.user.username)
    combined_queryset = list(model1_queryset) + list(model2_queryset) + list(model3_queryset) + list(model4_queryset) + list(model5_queryset) + list(model6_queryset) + list(model7_queryset)
    combined_queryset = sorted(combined_queryset, key=lambda obj: obj.application_date)
    p = Paginator(combined_queryset, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
            # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    return render(request, 'User/user_document_records.html',{'page_obj': page_obj})

def login(request):
   context = {}
   if( request.META.get('HTTP_REFERER') == 'http://localhost:8000/login'):
      context['redirected'] = 'True'
   return render(request, 'login.html',context=context)

@csrf_exempt
def handlelogin(request):
   if request.method == 'POST':
       loginusername = request.POST.get('username')
       loginpassword = request.POST.get('password')
       user = authenticate(username=loginusername, password=loginpassword)
       print("User Logged in : " + str(user))
       if user is not None:
           auth_login(request, user)
           if user.profile.type == 'villageuser':
              return redirect('/userdashboard')
           elif user.profile.type == 'talati':
              return redirect('/talatidashboard')
           elif user.profile.type == 'collector':
              return redirect('/collectordashboard')
       else:
           return redirect('/login')
   else: 
       return HttpResponseBadRequest("Invalid Request")
   
@csrf_exempt
def handlelogout(request):
   logout(request)
   return redirect('home')

def register(request):
   village = Village.objects.filter().values()
   context = {
      'villages' : village,
   }
   return render(request, 'register.html',context=context)

@csrf_exempt
def handlesignup(request):
   if request.method == 'POST':
       username = request.POST.get('email')
       password = request.POST.get('password')

       user = User.objects.create_user(username, username, password)
       user.first_name = request.POST.get('firstname')
       user.last_name = request.POST.get('lastname')
       user.profile.gender = request.POST.get('gender')
       user.profile.mobile_number = request.POST.get('mobilenumber')
       user.profile.address = ""
       user.profile.village_id = request.POST.get('village')
       user.profile.verification_code = 0
       user.profile.type = "villageuser"
       user.save()
       return redirect('/login')
   else: 
       return HttpResponseBadRequest("Invalid Request")

def voting(request):
   vote = Voting.objects.filter(status="Pending",village_id=request.user.profile.village_id).first()
   
   vote_status = False
   print(vote)
   if vote is not None:
    voted_list = vote.voted_user_list
    voted_list = eval(voted_list)
    if request.user.username in voted_list:
        vote_status = True
   if vote is not None:
       context = {
           'question' : vote.title,
           'optionlist' : vote.options_list_json,
           'vote_status' : vote_status
       }
   else: 
       context = {}
   return render(request, 'User/user_voting.html', context=context)

def raisecomplaint(request):
   complaints = Complaints.objects.filter(sender_username=request.user.username)
   p = Paginator(complaints, 5)
   page_number = request.GET.get('page')
   try:
      page_obj = p.get_page(page_number)  # returns the desired page object
   except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
      page_obj = p.page(1)
   except EmptyPage:
        # if page is empty then return last page
      page_obj = p.page(p.num_pages)
   context = {
       'page_obj': page_obj
   }
   return render(request, 'User/raisecomplaint.html', context=context)

def viewquery(request,querynum):
   complaint = Complaints.objects.get(sender_username=request.user.username,complaint_id=querynum)
   context = {
       'complaint': complaint
   }
   return render(request, 'User/viewcomplaint.html', context=context)

@csrf_exempt
def updatevoting(request):
   if request.is_ajax():
    try:
         resultjson = request.POST['resultjson']
         username = request.POST['username']
         print("Username is : " + username)
         vote = Voting.objects.get(status="Pending",village_id=request.user.profile.village_id)
         vote.options_list_json = resultjson
         user_list = vote.voted_user_list
         user_list = eval(user_list)
         user_list.add(username)
         vote.voted_user_list = user_list
         vote.save()
    except Exception as e:
        return HttpResponse("Error From Exception: " + str(e))
    return HttpResponse("Success")
   else:
    return HttpResponse("Error")

@csrf_exempt
def taxpayment(request):
    paidtaxlist = Tax.objects.filter(payer_username=request.user.username).values()
    p = Paginator(paidtaxlist, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
        'paidtaxlist': paidtaxlist,
        'page_obj': page_obj,
    }
    if request.method == "POST" and request.POST.get('tenament_number','NA') != "NA":
       ward = request.POST.get('ward', '')
       service = request.POST.get('service_type', '')
       tenament = request.POST.get('tenament_number', '')
       if tenament != '':
        tax = Tax.objects.get(ward_no=ward,type=service,tenament_no=tenament)
        context['tax'] = tax
        today = date.today()
        first_day = today.replace(day=1) + relativedelta(months=1)
        context['time'] = first_day
        currency = 'INR'
        amount = tax.amount * 100
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
        tax.order_id = razorpay_order['id']
        tax.save()
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        #pass these details to frontend.
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
    return render(request, 'User/tax_payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            payment = razorpay_client.payment.fetch(payment_id)
            amount = payment['amount']
            amount = amount / 100
            transaction_id = payment['acquirer_data']['upi_transaction_id']
            payment_method = payment['method']
            order_id = payment['order_id']
            print(payment)
            context = {
               'razorpay_payment_id': payment_id,
               'amount': amount,
               'transaction_id': transaction_id,
               'payment_method': payment_method,
               'datetime' : datetime.datetime.now()
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            tax = Tax.objects.get(order_id=order_id)
            if result is not None:
                tax.payment_date_time = datetime.datetime.now()
                tax.payer_username = request.user.username
                tax.transaction_id = transaction_id
                tax.payment_method = payment_method
                tax.save()
                return render(request, 'User/paymentsuccess.html',context=context)
            else:
                tax.order_id = None
                tax.save()
                return render(request, 'User/paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    
@csrf_exempt
def handleuserquery(request):
   if request.is_ajax():
    try:
        querytitle = request.POST['querytitle']
        querydescription = request.POST['querydescription']
        
        complaint = Complaints()
        complaint.title = querytitle
        complaint.description = querydescription
        complaint.status = "Pending"
        complaint.complaint_date_time = datetime.datetime.now()
        complaint.sender_username = request.user.username
        complaint.save()
    except Exception as e:
        return HttpResponse("Error From Exception: " + str(e))
    return HttpResponse("Success")
   else:
    return HttpResponse("Error")
   
def viewpaymentdetails(request,tax_id):
    taxdetails = Tax.objects.get(tax_id=tax_id)
    context={ 
       'amount': taxdetails.amount,
       'transaction_id': taxdetails.transaction_id,
       'payment_method': taxdetails.payment_method,
       'datetime' : taxdetails.payment_date_time
    }
    return render(request, 'User/paymentsuccess.html',context=context)

def talatidashboard(request):
    model1_queryset = IncomeCertificate.objects.filter(talati_id=request.user.id)
    model2_queryset = BirthCertificate.objects.filter(talati_id=request.user.id)
    model3_queryset = CharacterCertificate.objects.filter(talati_id=request.user.id)
    model4_queryset = DeathCertificate.objects.filter(talati_id=request.user.id)
    model5_queryset = CastCertificate.objects.filter(talati_id=request.user.id)
    model6_queryset = NonCreamyLayerCertificate.objects.filter(talati_id=request.user.id)
    model7_queryset = LandOwnershipCertificate.objects.filter(talati_id=request.user.id)
    combined_queryset = list(model1_queryset) + list(model2_queryset) + list(model3_queryset) + list(model4_queryset) + list(model5_queryset) + list(model6_queryset) + list(model7_queryset)
    combined_queryset = sorted(combined_queryset, key=lambda obj: obj.application_date, reverse=True)

    model1_count = IncomeCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    model2_count = BirthCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    model3_count = CharacterCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    model4_count = DeathCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    model5_count = CastCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    model6_count = NonCreamyLayerCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    model7_count = LandOwnershipCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    total_certificate_count = model1_count + model2_count + model3_count + model4_count + model5_count + model6_count + model7_count
    complaint_count = Complaints.objects.filter(talati_id=request.user.id,status="Pending").count()
    
    count = 0
    village_allocation = eval(request.user.profile.allocated_villages)
    votelist = Voting.objects.filter(village_id__in=village_allocation)
    for village in village_allocation:
        for vote in votelist:
            if vote.village_id == village and vote.status=="Pending":
                count = count + 1

    context = {
        'page_obj': combined_queryset,
        'certificate_count' : total_certificate_count,
        'complaint_count': complaint_count,
        'open_voting': count
    }
    return render(request, 'Talati/talati_user_dashboard.html',context=context)

def talati_doc_history(request):
    model1_queryset = IncomeCertificate.objects.filter(talati_id=request.user.id)
    model2_queryset = BirthCertificate.objects.filter(talati_id=request.user.id)
    model3_queryset = CharacterCertificate.objects.filter(talati_id=request.user.id)
    model4_queryset = DeathCertificate.objects.filter(talati_id=request.user.id)
    model5_queryset = CastCertificate.objects.filter(talati_id=request.user.id)
    model6_queryset = NonCreamyLayerCertificate.objects.filter(talati_id=request.user.id)
    model7_queryset = LandOwnershipCertificate.objects.filter(talati_id=request.user.id)
    combined_queryset = list(model1_queryset) + list(model2_queryset) + list(model3_queryset) + list(model4_queryset) + list(model5_queryset) + list(model6_queryset) + list(model7_queryset)
    combined_queryset = sorted(combined_queryset, key=lambda obj: obj.application_date)
    p = Paginator(combined_queryset, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, 'Talati/talati_document_history.html',{'page_obj': page_obj})

def managevoting(request):
    village_allocation = eval(request.user.profile.allocated_villages)
    villagelist = Village.objects.all()
    votelist = Voting.objects.filter(village_id__in=village_allocation)
    userlist = User.objects.all()
    filled_villagelist = list()
    for village in village_allocation:
        for vote in votelist:
            if vote.village_id == village and vote.status=="Pending":
                filled_villagelist.append(vote.village_id)
    
    empty_villagelist = list()
    for village in village_allocation:
        if village not in filled_villagelist:
            empty_villagelist.append(village)
    
    filled_villagelist = sorted(filled_villagelist)
    empty_villagelist = sorted(empty_villagelist)
    
    context = {
        'villages' : villagelist,
        'votelist' : votelist,
        'userlist' : userlist,
        'filled_list' : filled_villagelist,
        'empty_list' : empty_villagelist,
    }
    return render(request, 'Talati/managevoting.html',context=context)

def viewvoting(request):
    return render(request, 'Talati/managevoting.html')  

def addvoting(request,villageid):
    context = {
        'village_id' : villageid,
    }
    return render(request, 'Talati/addvoting.html',context=context)

def deletevoting(request,voteid,villageid):
    vote = Voting.objects.filter(vote_id=voteid).first()
    village = Village.objects.filter(VillageId=villageid).first()
    vote.delete()
    messages.add_message(request, messages.SUCCESS, "Deleted Voting Poll For " + village.village_name + " Village.")
    return redirect('/managevoting')

@csrf_exempt
def savevotingoptions(request):
    if request.method == 'POST':
        vote = Voting()
        vote.title = request.POST.get('poll-title')
        vote.options_list_json = request.POST.get('json_options')
        vote.status = "Pending"
        vote.result_json = request.POST.get('json_options')
        vote.voted_user_list = "{'guest'}"
        vote.village_id = request.POST.get('village_id')
        vote.result_date_time = datetime.datetime.now()
        vote.save()
    return redirect('/managevoting')

def declareresult(request,voteid,villageid):
    vote = Voting.objects.filter(vote_id=voteid).first()
    village = Village.objects.filter(VillageId=villageid).first()
    usercount = Profile.objects.filter(village_id=villageid).count()
    vote.result_date_time = datetime.datetime.now()
    vote.status = "Success"
    json_arr = json.loads(vote.options_list_json)
    maxvote = 0
    project_won = json_arr[0]["value"]
    
    for dataset in json_arr:
        if dataset["votes"]>maxvote:
            maxvote = dataset["votes"]
            project_won = dataset["value"]
    print(usercount)
    percentage = (maxvote*100)/usercount
    vote.result_json = "<b>Village:</b> " + village.village_name + "<br><b>Project:</b> " + project_won
    vote.save()
    messages.add_message(request, messages.SUCCESS, "Result Declared For " + village.village_name + " village at " + str(percentage) + "% voting to project: " + project_won)
    return redirect('/managevoting')

def managenews(request):
    news_list = News.objects.filter(sender_id=request.user.id).order_by('-news_date_time')
    context = {
        'news_list' : news_list,
    }
    return render(request, 'Talati/managenews.html',context=context)



def addnews(request):
    newsid = request.GET.get('newsid')
    context = {

    }
    if newsid:
        news = News.objects.get(news_id=newsid)
        context = {
            'news_title' : news.title,
            'news_description' : news.description,
            'news_id' : news.news_id
        }
    return render(request, 'Talati/addnews.html',context=context)

@csrf_exempt
def handle_news_data(request):
    if request.method == 'POST':
       news_id = request.POST.get('news_id')
       print(news_id)
       if news_id==str(0):
        print("inside new")
        news = News()
        news.title = request.POST.get('title')
        news.description = request.POST.get('description')
        news.news_date_time = datetime.datetime.now()
        news.sender_id = request.user.id
        news.save()
        messages.add_message(request, messages.SUCCESS, "News Added Successfully")
        return redirect('/newssection')
       else:
        print("inside update")
        news = News.objects.get(news_id=news_id)
        news.title = request.POST.get('title')
        news.description = request.POST.get('description')
        news.save()
        messages.add_message(request, messages.SUCCESS, "News Updated Successfully")
        return redirect('/newssection')
    return redirect('/newssection')

def deletenews(request,newsid):
    news = News.objects.get(news_id=newsid)
    news.delete()
    messages.add_message(request, messages.SUCCESS, "News Deleted Successfully")
    return redirect('/newssection')

def complaintsection(request):
    complaints = Complaints.objects.filter(talati_id=request.user.id,status="Pending")
    context = {
        'complaints' : complaints,
    }
    return render(request, 'Talati/complaintsection.html',context=context)

def replycomplaint(request):
    complaint = Complaints.objects.get(complaint_id=request.GET.get('complaintid'))
    context = {
        'complaint' : complaint,
    }
    return render(request, 'Talati/replycomplaint.html',context=context)

@csrf_exempt
def save_reply(request):
    complaint = Complaints.objects.get(complaint_id=request.POST.get('complaint_id'))
    complaint.answer = request.POST.get('replyvalue')
    complaint.resolve_date_time = datetime.datetime.now()
    complaint.status = "Success"
    complaint.save()
    subject = "From Village Helpdesk - Complaint Section"
    message = "Dear sir, " + "\n     " + "Your complaint for" + complaint.title + "has been reviewed by officer, Please Login to your account and check for the reply. Thank You."
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [complaint.sender_username]
    send_mail(subject,message,from_email,recepient_list)
    return redirect('/complaintsection')

def rejectcomplaint(request):
    complaint = Complaints.objects.get(complaint_id=request.GET.get('complaint_id'))
    complaint.answer = "Your Complaint Has Been Rejected, Please Provide Valid Information"
    complaint.resolve_date_time = datetime.datetime.now()
    complaint.status = "Success"
    complaint.save()
    subject = "From Village Helpdesk - Complaint Section"
    message = "Dear sir, " + "\n     " + "Your complaint for" + complaint.title + "has been reviewed by officer, Please Login to your account and check for the reply. Thank You."
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [complaint.sender_username]
    send_mail(subject,message,from_email,recepient_list)
    return redirect('/complaintsection')

def collectordashboard(request):
    villagecount = Village.objects.all().count()
    available_talati = Profile.objects.filter(type="talati").count()
    active_voting = Voting.objects.filter(status="Pending").count()
    talati_list = Profile.objects.filter(type="talati")[:5]
    context = {
        'villagecount' : villagecount,
        'available_talati' : available_talati,
        'active_voting' : active_voting,
        'talati_list' : talati_list,
    }
    return render(request, 'Collector/collector_dashboard.html',context=context)

def viewtalatilist(request):
    talati_list = Profile.objects.filter(type="talati")
    p = Paginator(talati_list, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
        'page_obj' : page_obj,
    }
    return render(request, 'Collector/view_talati_list.html',context=context)

def appointtalati(request):
    village = Village.objects.filter().values()
    context = {
        'villages' : village,
    }
    return render(request, 'Collector/appoint_talati.html',context=context)

@csrf_exempt
def handle_talati_creation(request):
    if request.method == 'POST':
       sign = request.FILES.get('signature')
       username = request.POST.get('emailid')
       password = request.POST.get('password')

       user = User.objects.create_user(username, username, password)
       user.first_name = request.POST.get('firstname')
       user.last_name = request.POST.get('lastname')
       user.profile.gender = request.POST.get('gender')
       user.profile.mobile_number = request.POST.get('mobilenumber')
       user.profile.address = request.POST.get('address')
       user.profile.village_id = 0
       user.profile.verification_code = 0
       user.profile.type = "talati"

       Villagelist = '(' + request.POST.get('village_id_1') + ',' + request.POST.get('village_id_2') + ',' + request.POST.get('village_id_3') + ',' + request.POST.get('village_id_4') + ',' + request.POST.get('village_id_5') + ')'
       allocated_village_list = eval(Villagelist)
       allocated_village_list = tuple(filter(lambda x: x != 0, allocated_village_list)) 

       villages = Village.objects.filter().all()

       for village in villages:
           if village.VillageId in allocated_village_list:
               village.talati_id = user.id
               village.save()
       user.profile.allocated_villages = allocated_village_list
       user.profile.signature.save(sign.name, sign)
       user.save()

       return redirect('/collectordashboard')
    else: 
       return HttpResponseBadRequest("Error: Bad Request")

def transfertalati(request):
    talati_list = User.objects.all()
    context = {
        'talati_list' : talati_list,
    }
    return render(request, 'Collector/transfer_talati.html',context=context)

@csrf_exempt
def searchtalati(request):
    talati_list = User.objects.filter()
    searched_talati = User.objects.filter(id=request.POST.get('talati_id'))
    for talati in searched_talati:
        allocated_villages = eval(talati.profile.allocated_villages)
    villages = Village.objects.filter(VillageId__in=allocated_villages)
    village_list = Village.objects.all()
    allocated_villages = ""
    for village in villages:
        allocated_villages = allocated_villages + village.village_name + ", "
    allocated_villages = allocated_villages[0:len(allocated_villages)-2]
    context = {
        'talati_list' : talati_list,
        'searched_talati' :  searched_talati,
        'allocated_villages' : allocated_villages,
        'allocation' : villages,
        'villages' : village_list
    }   
    return render(request, 'Collector/transfer_talati.html',context=context)

@csrf_exempt
def update_talati_villages(request):
    talati = User.objects.get(id=request.POST.get('talati_id'))
    allocation_list = eval(talati.profile.allocated_villages)
    
    allocation_villages = '(' + request.POST.get('village_id_1') + ',' + request.POST.get('village_id_2') + ',' + request.POST.get('village_id_3') + ',' + request.POST.get('village_id_4') + ',' + request.POST.get('village_id_5') + ')'
    allocation_villages = eval(allocation_villages)
    allocation_villages = tuple(filter(lambda x: x != 0, allocation_villages)) 
    talati.profile.allocated_villages = allocation_villages
    talati.save()

    villages = Village.objects.filter()

    for village in villages:
        if village.VillageId in allocation_list:
            village.talati_id = 0
            village.save()

    for village in villages:
        if village.VillageId in allocation_villages:
            village.talati_id = talati.id
            village.save()

    User_List = Profile.objects.filter(type="talati")
    for user in User_List:
        if user.user.id != int(request.POST.get('talati_id')):
            try:
                allocation = eval(user.allocated_villages)
                for one_village in allocation_villages:
                    if one_village in allocation:
                        my_list = list(allocation)
                        my_list.remove(one_village)
                        print("removed " + str(one_village) + " From " + str(user.user.id))
                        user.allocated_villages = tuple(my_list)
                        user.save()
            except Exception as error:
                print(error)
    return redirect('/collectordashboard')

def deletetalati(request):
    talati_list = User.objects.all()
    print(talati_list)
    context = {
        'talati_list' : talati_list,
    }
    return render(request, 'Collector/terminate_talati.html',context=context)

@csrf_exempt
def searchtalatifortermination(request):
    talati_list = User.objects.filter()
    searched_talati = User.objects.filter(id=request.POST.get('talati_id'))
    for talati in searched_talati:
        allocated_villages = eval(talati.profile.allocated_villages)
    villages = Village.objects.filter(VillageId__in=allocated_villages)
    allocated_villages = ""
    for village in villages:
        allocated_villages = allocated_villages + village.village_name + ", "
    allocated_villages = allocated_villages[0:len(allocated_villages)-2]
    context = {
        'talati_list' : talati_list,
        'searched_talati' :  searched_talati,
        'allocated_villages' : allocated_villages,
        'allocation' : villages,
    }   
    return render(request, 'Collector/terminate_talati.html',context=context)

@csrf_exempt
def terminate_talati_process(request):
    talati = User.objects.get(id=request.POST.get('talati_id'))
    try:
        allocated_villages = eval(talati.profile.allocated_villages)
        for village in allocated_villages:
            current_village = Village.objects.get(VillageId=village)
            current_village.talati_id = 0
            current_village.save()
    except Exception as error:
        print(error)
    talati.delete()
    return redirect('/deletetalati')

def new_document_request_options(request):
    return render(request, 'User/new_document_request_option.html')

def birth_certificate_form(request):
    return render(request, 'User/Forms/birth_certificate_form.html')

def income_certificate_form(request):
    villages = Village.objects.all()
    villagelist1 = ""
    villagelist2 = ""
    villagelist3 = ""
    villagelist4 = ""
    villagelist5 = ""
    for village in villages:
        if(village.VillageId<=5):
            villagelist1 = villagelist1 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>5 and village.VillageId<=10):
            villagelist2 = villagelist2 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>10 and village.VillageId<=15):
            villagelist3 = villagelist3 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>15 and village.VillageId<=20):
            villagelist4 = villagelist4 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>20):
            villagelist5 = villagelist5 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
    context = {
        "villagelist1" : villagelist1,
        "villagelist2" : villagelist2,
        "villagelist3" : villagelist3,
        "villagelist4" : villagelist4,
        "villagelist5" : villagelist5
    }
    if request.GET.get('inwardId'):
        incomecertificate = IncomeCertificate.objects.filter(inward_id=request.GET.get('inwardId')).first()
        context['incomeform'] = incomecertificate
    return render(request, 'User/Forms/income_certificate_form.html',context=context)

def death_certificate_form(request):
    villages = Village.objects.all()
    villagelist1 = ""
    villagelist2 = ""
    villagelist3 = ""
    villagelist4 = ""
    villagelist5 = ""
    for village in villages:
        if(village.VillageId<=5):
            villagelist1 = villagelist1 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>5 and village.VillageId<=10):
            villagelist2 = villagelist2 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>10 and village.VillageId<=15):
            villagelist3 = villagelist3 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>15 and village.VillageId<=20):
            villagelist4 = villagelist4 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>20):
            villagelist5 = villagelist5 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
    context = {
        "villagelist1" : villagelist1,
        "villagelist2" : villagelist2,
        "villagelist3" : villagelist3,
        "villagelist4" : villagelist4,
        "villagelist5" : villagelist5
    }
    return render(request, 'User/Forms/death_certificate_form.html',context=context)

def character_certificate_form(request):
    villages = Village.objects.all()
    villagelist1 = ""
    villagelist2 = ""
    villagelist3 = ""
    villagelist4 = ""
    villagelist5 = ""
    for village in villages:
        if(village.VillageId<=5):
            villagelist1 = villagelist1 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>5 and village.VillageId<=10):
            villagelist2 = villagelist2 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>10 and village.VillageId<=15):
            villagelist3 = villagelist3 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>15 and village.VillageId<=20):
            villagelist4 = villagelist4 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>20):
            villagelist5 = villagelist5 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
    context = {
        "villagelist1" : villagelist1,
        "villagelist2" : villagelist2,
        "villagelist3" : villagelist3,
        "villagelist4" : villagelist4,
        "villagelist5" : villagelist5
    }
    if request.GET.get('inwardId'):
        charactercertificate = CharacterCertificate.objects.filter(inward_id=request.GET.get('inwardId')).first()
        context['characterform'] = charactercertificate
    return render(request, 'User/Forms/character_certificate_form.html',context=context)

def ncl_certificate_form(request):
    villages = Village.objects.all()
    villagelist1 = ""
    villagelist2 = ""
    villagelist3 = ""
    villagelist4 = ""
    villagelist5 = ""
    for village in villages:
        if(village.VillageId<=5):
            villagelist1 = villagelist1 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>5 and village.VillageId<=10):
            villagelist2 = villagelist2 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>10 and village.VillageId<=15):
            villagelist3 = villagelist3 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>15 and village.VillageId<=20):
            villagelist4 = villagelist4 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>20):
            villagelist5 = villagelist5 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
    context = {
        "villagelist1" : villagelist1,
        "villagelist2" : villagelist2,
        "villagelist3" : villagelist3,
        "villagelist4" : villagelist4,
        "villagelist5" : villagelist5
    }
    if request.GET.get('inwardId'):
        nclcertificate = NonCreamyLayerCertificate.objects.filter(inward_id=request.GET.get('inwardId')).first()
        context['nclform'] = nclcertificate
    return render(request, 'User/Forms/non_creamy_layer_form.html',context=context)

def cast_certificate_form(request):
    villages = Village.objects.all()
    villagelist1 = ""
    villagelist2 = ""
    villagelist3 = ""
    villagelist4 = ""
    villagelist5 = ""
    for village in villages:
        if(village.VillageId<=5):
            villagelist1 = villagelist1 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>5 and village.VillageId<=10):
            villagelist2 = villagelist2 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>10 and village.VillageId<=15):
            villagelist3 = villagelist3 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>15 and village.VillageId<=20):
            villagelist4 = villagelist4 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>20):
            villagelist5 = villagelist5 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
    context = {
        "villagelist1" : villagelist1,
        "villagelist2" : villagelist2,
        "villagelist3" : villagelist3,
        "villagelist4" : villagelist4,
        "villagelist5" : villagelist5
    }
    return render(request, 'User/Forms/cast_certificate_form.html',context=context)

def land_owner_certificate_form(request):
    villages = Village.objects.all()
    villagelist1 = ""
    villagelist2 = ""
    villagelist3 = ""
    villagelist4 = ""
    villagelist5 = ""
    for village in villages:
        if(village.VillageId<=5):
            villagelist1 = villagelist1 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>5 and village.VillageId<=10):
            villagelist2 = villagelist2 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
        if(village.VillageId>10 and village.VillageId<=15):
            villagelist3 = villagelist3 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>15 and village.VillageId<=20):
            villagelist4 = villagelist4 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"    
        if(village.VillageId>20):
            villagelist5 = villagelist5 + "<option value=\"" + str(village.village_name) + "\">" + village.village_name + "</option>"
    context = {
        "villagelist1" : villagelist1,
        "villagelist2" : villagelist2,
        "villagelist3" : villagelist3,
        "villagelist4" : villagelist4,
        "villagelist5" : villagelist5
    }
    return render(request, 'User/Forms/land_ownership_form.html',context=context)

@login_required
def document_records(request):
    model1_queryset = IncomeCertificate.objects.filter(username=request.user.username)
    model2_queryset = BirthCertificate.objects.filter(username=request.user.username)
    model3_queryset = CharacterCertificate.objects.filter(username=request.user.username)
    model4_queryset = DeathCertificate.objects.filter(username=request.user.username)
    model5_queryset = CastCertificate.objects.filter(username=request.user.username)
    model6_queryset = NonCreamyLayerCertificate.objects.filter(username=request.user.username)
    model7_queryset = LandOwnershipCertificate.objects.filter(username=request.user.username)
    combined_queryset = list(model1_queryset) + list(model2_queryset) + list(model3_queryset) + list(model4_queryset) + list(model5_queryset) + list(model6_queryset) + list(model7_queryset)
    combined_queryset = sorted(combined_queryset, key=lambda obj: obj.application_date)
    p = Paginator(combined_queryset, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'User/document_records.html',context=context)

@csrf_exempt
def handleformsubmission(request):
    if request.method == 'POST':
        if request.POST.get('form_type') == 'birth_certificate_form':
           file = request.FILES['photo']
           formdata = BirthCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.father_name = request.POST.get('father_name')
           formdata.mother_name = request.POST.get('mother_name')
           formdata.address = request.POST.get('address')
           formdata.gender = request.POST.get('gender')
           formdata.birthdate = request.POST.get('birth_date')
           formdata.birth_place = request.POST.get('birth_place')
           formdata.weight = request.POST.get('weight')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.user_villageId = request.user.profile.village_id
           formdata.photo.save(file.name, file)
           formdata.save()

        if request.POST.get('form_type') == 'cast_certificate_form':
           photo = request.FILES['photo']
           own_lc = request.FILES['Own_LC']
           family_lc = request.FILES['Family_LC']
           electricity_bill = request.FILES['Electricity_bill']
           formdata = CastCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.parent_name = request.POST.get('father_mother_name')
           formdata.gender = request.POST.get('gender')
           formdata.religion = request.POST.get('religion')
           formdata.cast = request.POST.get('cast')
           formdata.subcast = request.POST.get('sub_cast')
           formdata.district = request.POST.get('district')
           formdata.taluka = request.POST.get('taluka')
           formdata.village = request.POST.get('village')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           formdata.user_villageId = request.user.profile.village_id
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.photo.save(photo.name, photo)
           formdata.leaving_certificate.save(own_lc.name, own_lc)
           formdata.family_lc_certificate.save(family_lc.name, family_lc)
           formdata.electricity_bill.save(electricity_bill.name, electricity_bill)
           formdata.save()

        if request.POST.get('form_type') == 'character_certificate_form':
           file = request.FILES['photo']
           formdata = CharacterCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.gender = request.POST.get('gender')
           formdata.parent_name = request.POST.get('father_mother_name')
           formdata.years = request.POST.get('years')
           formdata.religion = request.POST.get('cast')
           formdata.district = request.POST.get('district')
           formdata.taluka = request.POST.get('taluka')
           formdata.village = request.POST.get('village')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           formdata.user_villageId = request.user.profile.village_id
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.photo.save(file.name, file)
           formdata.save()

        if request.POST.get('form_type') == 'death_certificate_form':
           file = request.FILES['id_proof']
           formdata = DeathCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.gender = request.POST.get('gender')
           formdata.father_name = request.POST.get('father_name')
           formdata.mother_name = request.POST.get('mother_name')
           formdata.village = request.POST.get('village')
           formdata.taluka = request.POST.get('taluka')
           formdata.district = request.POST.get('district')
           formdata.address_of_deceased = request.POST.get('address')
           formdata.place_of_death = request.POST.get('place_of_death')
           formdata.remarks = request.POST.get('remarks')
           formdata.deathdate = request.POST.get('DOD')
           formdata.registrationdate = request.POST.get('registration_date')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           formdata.user_villageId = request.user.profile.village_id
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.id_proof.save(file.name, file)
           formdata.save()

        if request.POST.get('form_type') == 'income_certificate_form':
           photo = request.FILES['photo']
           ration_card = request.FILES['ration_card']
           electricity_bill = request.FILES['electricity_bill']
           adhar_card = request.FILES['adhar_card']
           formdata = IncomeCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.gender = request.POST.get('gender')
           formdata.parent_name = request.POST.get('father_mother_name')
           formdata.applicant_income = request.POST.get('applicant_income')
           formdata.parent_income = request.POST.get('parent_income')
           formdata.other_income = request.POST.get('other_income')
           formdata.rupee_in_words = request.POST.get('rupee_in_words')
           formdata.district = request.POST.get('district')
           formdata.taluka = request.POST.get('taluka')
           formdata.village = request.POST.get('village')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           formdata.user_villageId = request.user.profile.village_id
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.photo.save(photo.name, photo)
           formdata.ration_card.save(ration_card.name, ration_card)
           formdata.electricity_bill.save(electricity_bill.name, electricity_bill)
           formdata.adhar_card.save(adhar_card.name, adhar_card)
           formdata.save()

        if request.POST.get('form_type') == 'land_ownership_form':
           photo = request.FILES['photo']
           st_certificate = request.FILES['st_certificate']
           land_posession_certi = request.FILES['land_posession_certi']
           formdata = LandOwnershipCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.gender = request.POST.get('gender')
           formdata.district = request.POST.get('district')
           formdata.taluka = request.POST.get('taluka')
           formdata.village = request.POST.get('village')
           formdata.voter_id_no = request.POST.get('voter_id_no')
           formdata.land_description = request.POST.get('land_description')
           formdata.land_use = request.POST.get('land_use')
           formdata.parent_name = request.POST.get('parent_name')
           formdata.age = request.POST.get('age')
           formdata.acres = request.POST.get('acres')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           formdata.user_villageId = request.user.profile.village_id
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.st_certificate.save(st_certificate.name, st_certificate)
           formdata.land_posession_certi.save(land_posession_certi.name, land_posession_certi)
           formdata.save()

        if request.POST.get('form_type') == 'ncl_certificate_form':
           print('Village id is: '+ str(request.user.profile.village_id))
           photo = request.FILES['photo']
           leaving_certificate = request.FILES['LC']
           income_certificate = request.FILES['income_certificate']
           cast_certificate = request.FILES['cast_certificate']
           ration_card = request.FILES['ration_card']
           electricity_bill = request.FILES['electricity_bill']
           formdata = NonCreamyLayerCertificate()
           formdata.username = request.user.username
           formdata.fullname = request.POST.get('fullname')
           formdata.parent_name = request.POST.get('father_mother_name')
           formdata.gender = request.POST.get('gender')
           formdata.religion = request.POST.get('religion')
           formdata.cast = request.POST.get('cast')
           formdata.subcast = request.POST.get('sub_cast')
           formdata.district = request.POST.get('district')
           formdata.taluka = request.POST.get('taluka')
           formdata.village = request.POST.get('village')
           formdata.form_status = "Pending"
           formdata.application_date = datetime.datetime.now()
           formdata.user_villageId = int(request.user.profile.village_id)
           village = Village.objects.get(VillageId=request.user.profile.village_id)
           formdata.talati_id = village.talati_id
           formdata.photo.save(photo.name, photo)
           formdata.leaving_certificate.save(leaving_certificate.name, leaving_certificate)
           formdata.income_certificate.save(income_certificate.name, income_certificate)
           formdata.cast_certificate.save(cast_certificate.name, cast_certificate)
           formdata.ration_card.save(ration_card.name, ration_card)
           formdata.electricity_bill.save(electricity_bill.name, electricity_bill)
           formdata.save()
    messages.add_message(request, messages.SUCCESS, "Form Submitted Successfully, Your Physical Copy will be available at your Village Office after 5 working days From 10:00 AM to 05:00 PM.")
    return redirect('/newdocumentrequest')
    # return HttpResponse("Form Submitted Successfully, Your Physical Copy will be available at your Village Office.<br>Date: <br>Time: ")

def userprofile(request):
    village = Village.objects.get(VillageId=request.user.profile.village_id)
    context = {
        'village_name': village.village_name
    }
    return render(request, 'User/user_profile.html',context=context)

def edituserprofile(request):
    village = Village.objects.filter().values()
    context = {
       'villages' : village,
    }
    return render(request, 'User/edit_user_profile.html',context=context)

@csrf_exempt
def handle_edit_user_profile(request):
    if request.method == 'POST':
       user = User.objects.get(username=request.user.username)
       user.first_name = request.POST.get('firstname')
       user.last_name = request.POST.get('lastname')
       user.profile.gender = request.POST.get('gender')
       user.profile.mobile_number = request.POST.get('mobilenumber')
       user.profile.address = request.POST.get('address')
       user.profile.village_id = request.POST.get('village_id')
       user.save()
    return redirect('/userprofile')

class MyPDFView(View):
    def get(self, request, form_id, document_type):
        villages = Village.objects.all()

        if(document_type=="income"):
            income_template='Talati/Certificate_Templates/income_template.html'
            incomecertificate = IncomeCertificate.objects.filter(form_id=form_id).first()    
            data = {
            'rdata' : incomecertificate,
            'inward_id': incomecertificate.inward_id,
            'name': incomecertificate.fullname,
            'father_name': incomecertificate.parent_name,
            'gender': incomecertificate.gender,
            'village': incomecertificate.village,
            'taluka': incomecertificate.taluka,
            'district': incomecertificate.district,
            'rupee_words': incomecertificate.applicant_income,
            'own_income': incomecertificate.applicant_income,
            'parent_income': incomecertificate.parent_income,
            'other_income': incomecertificate.other_income,
            'total_income': incomecertificate.applicant_income,
            'villages': villages,
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            'userphoto' : incomecertificate.photo.path
            }
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable-local-file-access': 'true',
                                                        'margin-top': 10,
                                                        "zoom":1,
                                                        'javascript-delay':0,
                                                        "no-stop-slow-scripts":True,},
                                                        )
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)

            new_dir_path = getpath('userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"income",new_dir_path+ '/incomecertificates/'+ incomecertificate.inward_id + '.pdf',request.user.profile.signature.path)

            return FileResponse(open(new_dir_path+ '/incomecertificates/'+ incomecertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/income_table')
            
            
        elif (document_type=="birth"):
            income_template='Talati/Certificate_Templates/birth_template.html'
            birthcertificate = BirthCertificate.objects.filter(form_id=form_id).first()
            # print(getpath('images/barcode.svg'))
            data = {
            'rdata':birthcertificate,
            'name': birthcertificate.fullname,
            'gender': birthcertificate.gender,
            'dob': birthcertificate.birthdate,
            'birth_place': birthcertificate.birth_place,
            'mother_name': birthcertificate.mother_name,
            'father_name': birthcertificate.father_name,
            'address': birthcertificate.address,
            'inward_id': birthcertificate.inward_id,
            'today_date': datetime.datetime.now(),
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            'userphoto' : birthcertificate.photo.path
            } 
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable-local-file-access': 'true',
                                                        'margin-top': 10,
                                                        "zoom":1,
                                                        "viewport-size" :"1366 x 200",
                                                        'javascript-delay':0,
                                                        'footer-center' :'[page]/[topage]',
                                                        "no-stop-slow-scripts":True,
                                                        "disable-smart-shrinking":True},
                                                        )
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)
            
            new_dir_path = getpath('/userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"birth",new_dir_path+ '/birthcertificates/'+ birthcertificate.inward_id + '.pdf',request.user.profile.signature.path)
            
            return FileResponse(open(new_dir_path+ '/birthcertificates/'+ birthcertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/birth_table')
        
        elif (document_type=="cast"):
            income_template='Talati/Certificate_Templates/cast_template.html'
            castcertificate = CastCertificate.objects.filter(form_id=form_id).first()    #temporary
            data = {
            'rdata' : castcertificate,
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            'userphoto' : castcertificate.photo.path
            }
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable_local_file_access': True,
                                                        'margin-top': 10,
                                                        "zoom":1,
                                                        'javascript-delay':0,
                                                        "no-stop-slow-scripts":True,},
                                                        )
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)
            
            new_dir_path = getpath('/userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"cast",new_dir_path + '/castcertificates/' + castcertificate.inward_id + '.pdf',request.user.profile.signature.path)

            return FileResponse(open(new_dir_path + '/castcertificates/' + castcertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/cast_table')
        
        elif (document_type=="character"):
            income_template='Talati/Certificate_Templates/character_template.html'
            charactercertificate = CharacterCertificate.objects.filter(form_id=form_id).first()
            talati = User.objects.get(id=charactercertificate.talati_id)
            talati_name = talati.first_name + " " + talati.last_name
            data = {
            'rdata': charactercertificate,
            'talati_name': talati_name,
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            'userphoto' : castcertificate.photo.path
            } 
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable-local-file-access':'true',
                                                        'margin-top': '10',
                                                        "zoom":'1',
                                                        "viewport-size" :"1366 x 200",
                                                        'javascript-delay':'0',
                                                        'footer-center' :'[page]/[topage]',
                                                        "no-stop-slow-scripts":'true',
                                                        "disable-smart-shrinking":'true'},
                                                        )
            
            print("Received File Response:")
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)
            
            print("WRITING File Response:")
            new_dir_path = getpath('/userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"character",new_dir_path + '/charactercertificates/' + charactercertificate.inward_id + '.pdf',request.user.profile.signature.path)
            return FileResponse(open(new_dir_path+ '/charactercertificates/'+ charactercertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/character_table')
        
        elif (document_type=="death"):
            income_template='Talati/Certificate_Templates/death_template.html'
            deathcertificate = DeathCertificate.objects.filter(form_id=form_id).first()    #temporary
            data = {
            'rdata': deathcertificate,
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            # 'userphoto' : deathdertificate.photo.path
            } 
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable_local_file_access': True,
                                                        'margin-top': 10,
                                                        "zoom":1,
                                                        'javascript-delay':0,
                                                        "no-stop-slow-scripts":True,
                                                        },
                                                        )
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)
            
            new_dir_path = getpath('/userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"death",new_dir_path+ '/deathcertificates/'+ deathcertificate.inward_id + '.pdf',request.user.profile.signature.path)

            return FileResponse(open(new_dir_path+ '/deathcertificates/'+ deathcertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/death_table')
        
        elif (document_type=="land"):
            income_template='Talati/Certificate_Templates/land_template.html'
            landcertificate = LandOwnershipCertificate.objects.filter(form_id=form_id).first()    #temporary
            data = {
            'rdata' : landcertificate,
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            # 'userphoto' : landcertificate.photo.path
            } 
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable_local_file_access': True,
                                                        'margin-top': 10,
                                                        "zoom":1,
                                                        "viewport-size" :"1366 x 200",
                                                        'javascript-delay':0,
                                                        'footer-center' :'[page]/[topage]',
                                                        "no-stop-slow-scripts":True,
                                                        "disable-smart-shrinking":True},
                                                        )
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)
            
            new_dir_path = getpath('/userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"land",new_dir_path+ '/landcertificates/'+ landcertificate.inward_id + '.pdf',request.user.profile.signature.path)

            return FileResponse(open(new_dir_path+ '/landcertificates/'+ landcertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/death_table')
        
        elif (document_type=="ncl"):
            income_template='Talati/Certificate_Templates/cryamy_template.html'
            nclertificate = NonCreamyLayerCertificate.objects.filter().first()    #temporary
            data = {
            'rdata': nclertificate,
            'imglink': getpath('images/nationalsymbol.png'),
            'barcodelink': getpath('images/barcode.svg'),
            # 'fontlink' : getpath('fonts/NotoSansGujarati-Regular.ttf'),
            'userphoto' : nclertificate.photo.path
            }
            response = PDFTemplateResponse(request=request,
                                        template=income_template,
                                        filename="output.pdf",
                                        context= data,
                                        show_content_in_browser=False,
                                        cmd_options={'title': 'Certificate',
                                                        'enable_local_file_access': True,
                                                        'margin-top': 10,
                                                        "zoom":1,
                                                        "viewport-size" :"1366 x 200",
                                                        'javascript-delay':0,
                                                        'footer-center' :'[page]/[topage]',
                                                        "no-stop-slow-scripts":True,
                                                        "disable-smart-shrinking":True},
                                                        )
            with open(getpath('pdfsignatures/income_certificate_unsigned.pdf'), 'wb') as pdf_file:
                pdf_file.write(response.rendered_content)
            
            new_dir_path = getpath('/userdocuments')
            sign_pdf(getpath('/pdfsignatures/income_certificate_unsigned.pdf'),"ncl",new_dir_path+ '/nclertificates/'+ nclertificate.inward_id + '.pdf',request.user.profile.signature.path)
            
            return FileResponse(open(new_dir_path+ '/nclertificates/'+ nclertificate.inward_id + '.pdf', 'rb'), content_type='application/pdf')
            # return redirect('/cryamy_table')
        
def view_pdf(request,document_type,inward_id):
    if document_type == "income":
        folder_name = "incomecertificates"
    elif document_type == "birth":
        folder_name = "birthcertificates"
    elif document_type == "cast":
        folder_name = "castcertificates"
    elif document_type == "character":
        folder_name = "charactercertificates"
    elif document_type == "death":
        folder_name = "deathcertificates"
    elif document_type == "land":
        folder_name = "landcertificates"
    elif document_type == "ncl":
        folder_name = "nclcertificates"
    print("printing data:")
    print(getpath('userdocuments/'+ folder_name + '/' + str(inward_id) +'.pdf'))
    return FileResponse(open(getpath('userdocuments/'+ folder_name + '/' + str(inward_id) +'.pdf'), 'rb'), content_type='application/pdf')

def talati_doc_request(request):
    birth = BirthCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    death = DeathCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    cast = CastCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    income = IncomeCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    land = LandOwnershipCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    nonCreamy = NonCreamyLayerCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()
    character = CharacterCertificate.objects.filter(form_status="Pending",talati_id=request.user.id).count()

    context = {
        'Birth_Certificate' : birth,
        'cast' : cast,
        'Death_Certificate' : death,
        'Income_Certificate' : income,
        'Land_Ownership_Certificate' : land,
        'NonCreamy_Certificate' : nonCreamy,
        'character_Certificate' : character,
    }
    return render(request, 'Talati/talati_doc_request.html', context=context)
    # template = loader.get_template(''Talati/talati_doc_request.html)


# --------------------------------------------------------------------------------------------------------------------------------------------------#
# Document Requests Approval By Talati
def birth_table(request):
    birth = BirthCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/birth_table.html', { 'birth':birth })

def death_table(request):
    death = DeathCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/death_table.html', { 'death':death })

def cast_table(request):
    cast = CastCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/cast_table.html', { 'cast':cast })

def income_table(request):
    income = IncomeCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/income_table.html', { 'income':income })

def land_table(request):
    land = LandOwnershipCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/land_table.html', { 'land':land })

def cryamy_table(request):
    cryamy = NonCreamyLayerCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/cryamy_table.html', { 'cryamy':cryamy })

def character_table(request):
    character = CharacterCertificate.objects.filter(form_status="Pending",talati_id=request.user.id)
    return render(request, 'Talati/Doc_Tables/character_table.html', { 'character':character })

def user_birth_request(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(BirthCertificate, username=username,inward_id=request.POST.get('inward_id'))
        photo = req_info.photo.url
    return render(request, 'Talati/Doc_Tables/user_birth_request.html', {'req_info':req_info,'photo_path':photo})

def user_death_req(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(DeathCertificate, username=username, inward_id=request.POST.get('inward_id'))
        id_proof = req_info.id_proof.url
    return render(request, 'Talati/Doc_Tables/user_death_req.html', {'req_info':req_info,'id_proof':id_proof})

def user_income_req(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(IncomeCertificate, username=username, inward_id=request.POST.get('inward_id'))
        photo = req_info.photo.url
        ration = req_info.ration_card.url
        electricity = req_info.electricity_bill.url
        adhar = req_info.adhar_card.url
    return render(request, 'Talati/Doc_Tables/user_income_req.html', {'req_info':req_info,'photo_path':photo,'ration_path':ration,'electricity_path':electricity,'adhar_path':adhar})

def user_cast_req(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(CastCertificate, username=username, inward_id=request.POST.get('inward_id'))
        photo = req_info.photo.url
        leaving_certificate = req_info.leaving_certificate.url
        family_lc_certificate = req_info.family_lc_certificate.url
        electricity_bill = req_info.electricity_bill.url
    return render(request, 'Talati/Doc_Tables/user_cast_req.html', {'req_info':req_info,'photo_path':photo,'leaving_certificate':leaving_certificate,'family_lc_certificate':family_lc_certificate,'electricity_bill':electricity_bill})

def user_cryamy_req(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(NonCreamyLayerCertificate, username=username, inward_id=request.POST.get('inward_id'))
        photo = req_info.photo.url
        leaving_certificate = req_info.leaving_certificate.url
        income_certificate = req_info.income_certificate.url
        cast_certificate = req_info.cast_certificate.url
        ration_card = req_info.ration_card.url
        electricity_bill = req_info.electricity_bill.url
    return render(request, 'Talati/Doc_Tables/user_cryamy_req.html', {'req_info':req_info,'photo_path':photo,'leaving_certificate':leaving_certificate,'income_certificate':income_certificate,'cast_certificate':cast_certificate,'electricity_bill':ration_card,'ration_card':electricity_bill})

def user_character_req(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(CharacterCertificate, username=username, inward_id=request.POST.get('inward_id'))
        photo = req_info.photo.url
    return render(request, 'Talati/Doc_Tables/user_character_req.html', {'req_info':req_info,'photo_path':photo})

def user_land_req(request):
    if request.method == 'POST':
        username = request.POST.get('user_profile')
        req_info = get_object_or_404(LandOwnershipCertificate, username=username, inward_id=request.POST.get('inward_id'))
        photo = req_info.photo.url
        st_certificate = req_info.st_certificate.url
        land_posession_certi = req_info.land_posession_certi.url
    return render(request, 'Talati/Doc_Tables/user_land_req.html', {'req_info':req_info,'photo_path':photo,'st_certificate':st_certificate,'land_posession_certi':land_posession_certi})

def approve_request(request):
    if request.method == 'POST':
        inward_id = request.POST.get('user_doc')
        if inward_id[:5] == "17024":    
            req_info = get_object_or_404(BirthCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/birth/' + str(req_info.form_id))

        elif inward_id[:5] == "21028":    
            req_info = get_object_or_404(IncomeCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/income/' + str(req_info.form_id))

        elif inward_id[:5] == "18025":
            req_info = get_object_or_404(CastCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/cast/' + str(req_info.form_id))

        elif inward_id[:5] == "23030":
            req_info = get_object_or_404(NonCreamyLayerCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/ncl/' + str(req_info.form_id))

        elif inward_id[:5] == "20027":    
            req_info = get_object_or_404(DeathCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/death/' + str(req_info.form_id))

        elif inward_id[:5] == "22029":    
            req_info = get_object_or_404(LandOwnershipCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/land/' + str(req_info.form_id))
        
        elif inward_id[:5] == "19026":    
            req_info = get_object_or_404(CharacterCertificate, inward_id=inward_id)
            req_info.form_status = 'Approved'
            req_info.approval_date = datetime.datetime.now()
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been approved by officer, Please Login to your account and Access Your Document. Thank You."
            # send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('/pdf/character/' + str(req_info.form_id))

def reject_request(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        inward_no = request.POST.get('user_doc')
        if inward_no[:5] == "17024":
            req_info = get_object_or_404(BirthCertificate, inward_id=inward_no)
            req_info.form_status = 'Rejected because of ' + ' ' + reason
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been rejected by officer, Please Login to your account and Review the information provided. Thank You."
            send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('birth_table')
            
        elif inward_no[:5] == "21028":
            req_info = get_object_or_404(IncomeCertificate, inward_id=inward_no)
            req_info.form_status = 'Rejected because of ' + ' ' + reason
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been rejected by officer, Please Login to your account and Review the information provided. Thank You."
            send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('income_table')
            
        elif inward_no[:5] == "18025":    
            req_info = get_object_or_404(CastCertificate, inward_id=inward_no)
            req_info.form_status = 'Rejected because of ' + ' ' + reason
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been rejected by officer, Please Login to your account and Review the information provided. Thank You."
            send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('cast_table')
            
        elif inward_no[:5] == "23030":    
            req_info = get_object_or_404(NonCreamyLayerCertificate, inward_id=inward_no)
            req_info.form_status = 'Rejected because of ' + ' ' + reason
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been rejected by officer, Please Login to your account and Review the information provided. Thank You."
            send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('cryamy_table')
            
        elif inward_no[:5] == "20027":    
            req_info = get_object_or_404(DeathCertificate, inward_id=inward_no)
            req_info.form_status = 'Rejected because of ' + ' ' + reason
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been rejected by officer, Please Login to your account and Review the information provided. Thank You."
            send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('death_table')
            
        elif inward_no[:5] == "22029":    
            req_info = get_object_or_404(LandOwnershipCertificate, inward_id=inward_no)
            req_info.form_status = 'Rejected because of ' + ' ' + reason
            req_info.save()
            message = "Dear sir, " + "\n     " + "This is to inform you that your document request for " + str(req_info.__class__.__name__) + " has been rejected by officer, Please Login to your account and Review the information provided. Thank You."
            send_mail("From Village Helpdesk - Complaint Section",message,settings.EMAIL_HOST_USER,[req_info.username])
            return redirect('land_table')

# --------------------------------------------------------------------------------------------------------------------------------------------------#
def cast_template(request):
    return render(request, 'Talati/Certificate_Templates/cast_template.html')

def talatiprofile(request):
    user_profile = Profile.objects.get(user=request.user)
    villages = Village.objects.filter(talati_id=request.user.id)
    signature_url = user_profile.signature.url if user_profile.signature else None
    signature_url = signature_url[16:]
    context = {
        'villages': villages,
        'signature_url': signature_url,
    }
    return render(request, 'Talati/talati_profile.html', context=context)

def edittalatiprofile(request):
    villages = Village.objects.filter().values()
    context = {
       'villages' : villages,
    }
    return render(request, 'Talati/edit_talati_profile.html',context=context)


@csrf_exempt
def handle_edit_talati_profile(request):
    if request.method == 'POST':
       user = User.objects.get(username=request.user.username)
       user.first_name = request.POST.get('firstname')
       user.last_name = request.POST.get('lastname')
       user.profile.gender = request.POST.get('gender')
       user.profile.mobile_number = request.POST.get('mobilenumber')
       user.profile.address = request.POST.get('address')
       user.profile.village_id = request.POST.get('village_id')
       signature_file = request.FILES.get('signature')
       if signature_file:
        user.profile.signature.save(signature_file.name, signature_file)
        # user.profile.signature = SimpleUploadedFile(signature_file.name, signature_file.read())
       user.save()
    return redirect('/talatiprofile')

def collectorprofile(request):
    village = Village.objects.filter(VillageId=request.user.id).first()
    context = {
        'village_name' : village.village_name,
    }
    return render(request, 'Collector/collector_profile.html', context=context)

def editcollectorprofile(request):
    village = Village.objects.filter(VillageId=request.user.id).first()
    context = {
        'village_name' : village.village_name,
    }
    return render(request, 'Collector/edit_collector_profile.html',context=context)


@csrf_exempt
def handle_edit_collector_profile(request):
    if request.method == 'POST':
       user = User.objects.get(username=request.user.username)
       user.first_name = request.POST.get('firstname')
       user.last_name = request.POST.get('lastname')
       user.profile.gender = request.POST.get('gender')
       user.profile.mobile_number = request.POST.get('mobilenumber')
       user.profile.address = request.POST.get('address')
       user.save()
    return redirect('/collectorprofile')