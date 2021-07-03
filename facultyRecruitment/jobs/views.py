from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from userAccounts.decorators import allowed_users, admin_only
from .models import Jobs, Applicants, CollegeImages, Reminder
from django.contrib.auth.models import User
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
import threading
import zipfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import datetime
from itertools import chain
from random import shuffle

class EmailThreading(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently = False)

@admin_only
def addJob(request):
    if request.method == 'POST':
        job = Jobs()
        job.adminId = User.objects.get(id = request.user.id )
        job.collegeId = CollegeImages.objects.get(CollegeId = request.POST['college'])
        job.position = request.POST['position']
        job.location = request.POST['location']
        job.applyBy = request.POST['applyBy']
        job.description = request.POST['description']
        job.availablePositions = request.POST['openings']
        job.adminPhoneNumber = request.POST['number']
        job.adminEmail = request.POST['email']
        job.collegeWebsite = request.POST['website']
        job.save()
        return redirect('jobs')
    context = {
                'colleges':CollegeImages.objects.all()
                }
    return render(request,'jobs/addJobForm.html',context)

@login_required(login_url='login')
def applyJob(request,id):
    job = Jobs.objects.get(jobId = int(id))
    if request.method == 'POST':
        applicant = Applicants()
        applicant.userId = User.objects.get(id = request.user.id)
        applicant.jobId = Jobs.objects.get(jobId = int(id))
        applicant.name = request.POST['name']
        applicant.email = request.POST['email']
        applicant.phoneNumber = request.POST['phone']
        applicant.location = request.POST['location']
        applicant.resume = request.FILES['resume']
        applicant.linkedInProfileLink = request.POST['linkedInLink']
        applicant.portfolioLink = request.POST['personalPrtfolio']
        applicant.queAboutUs = request.POST['aboutYourself']
        applicant.save()
        return redirect('dashboard')
    return render(request,'jobs/jobApplyForm.html',{'job':job})

def showJobDetails(request,id):
    job = Jobs.objects.get(jobId = int(id))
    applicants = Applicants.objects.filter(jobId = int(id))
    alreadyApply = 'Yes'
    try:
        Applicants.objects.get(userId = int(request.user.id),jobId = int(id))
    except:
        alreadyApply = 'No'
    context = {
                'job' : job,
                'applicants' : applicants,
                'alreadyApply' : alreadyApply
              }
    return render(request, 'jobs/jobDetails.html',context)

@login_required(login_url='login')
def dashboard(request):
    applicant = Applicants.objects.filter(userId = request.user.id).select_related('jobId')
    print(applicant)
    return render(request, 'jobs/jobStatus.html',{'jobs':applicant})

def jobs(request):
    jobsPassed = Jobs.objects.filter(applyBy__lt = datetime.date.today())
    jobsRemains = Jobs.objects.filter(applyBy__gte = datetime.date.today())
    jobs = chain(jobsRemains,jobsPassed)
    context = {
                'jobs':jobs,
                'colleges':CollegeImages.objects.all()
                }
    return render(request,'jobs/jobs.html',context)

# def pagechanger(request,obj,size):
#     paginator = Paginator(obj,size)
#
#     try:
#         current_page = request.POST['page']
#         result = paginator.page(current_page)
#     except KeyError:
#         result = paginator.page(1)
#     except PageNotAnInteger:
#         result = paginator.page(1)
#     except EmptyPage:
#         print(paginator.num_pages)
#         result = paginator.page(paginator.num_pages)
#
#     return result

@admin_only
def updateStatus(request,applicatId,jobId,type):
    applicant = Applicants.objects.get(userId = User.objects.get(id = applicatId),jobId = Jobs.objects.get(jobId = jobId))
    status = 'Accepted' if type == 'accept' else 'Rejected'
    applicant.status = status
    applicant.save()
    template = get_template('jobs/statusConfirmation.html')
    if status == 'Accepted':
        html  = template.render({'applicant':applicant,'statusImage':'https://cdn3.iconfinder.com/data/icons/simple-web-navigation/165/tick-512.png'})
        toApplicantEmail = Applicants.objects.only('email').get(userId = User.objects.get(id = int(applicatId))).email
        message = EmailMessage('Application Status', html, 'tododjangowebapp@gmail.com', [toApplicantEmail])
        message.content_subtype = 'html'
        EmailThreading(message).start()
    return HttpResponse(status)

@admin_only
def updateJob(request,jobId):
    job = Jobs.objects.get(jobId = int(jobId))
    if request.method == 'POST':
        job.position = request.POST['position']
        job.location = request.POST['location']
        job.applyBy = request.POST['applyBy']
        job.description = request.POST['description']
        job.collegeId = CollegeImages.objects.get(CollegeId = request.POST['college'])
        job.availablePositions = request.POST['openings']
        job.adminPhoneNumber = request.POST['number']
        job.adminEmail = request.POST['email']
        job.collegeWebsite = request.POST['website']
        job.save()
        return redirect('jobs')
    context = {
                'job':job,
                'colleges':CollegeImages.objects.all()
    }
    return render(request,'jobs/addJobForm.html',context)

@admin_only
def deleteJob(request,jobId):
    job = Jobs.objects.get(jobId = int(jobId))
    job.delete()
    return HttpResponse('ok')

def view_404(request,exception):
    return render(request,'jobs/404.html')

@admin_only
def download(request,applicatId,jobId):
    applicant = Applicants.objects.get(userId = User.objects.get(id = applicatId),jobId = Jobs.objects.get(jobId = jobId))
    pdf = render_to_pdf('jobs/pdfDetail.html', {'applicant':applicant})
    files = []
    files.append((applicant.name + '_Details.pdf',pdf))
    print(applicant.resume.path)
    files.append((applicant.name + '_Resume.pdf',open(applicant.resume.path,'r').read()))
    zipfile = generate_zip(files)
    response = HttpResponse(zipfile, content_type = 'application/pdf')
    content = 'attachment; filename=' + applicant.name + '_' + applicant.jobId.position + '.zip'
    response['Content-Disposition'] = content
    return response

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return result.getvalue()
	return None

def generate_zip(files):
	mem_zip = BytesIO()
	with zipfile.ZipFile(mem_zip, mode = 'w', compression = zipfile.ZIP_DEFLATED) as zf:
		for f in files:
			zf.writestr(f[0],f[1])
	return mem_zip.getvalue()

def search(request):
    jobs = Jobs.objects.none()
    if request.method == 'POST':
        checkboxes = request.POST.getlist('checkbox')
        if not checkboxes:
            return redirect('jobs')
        else:
            for check in checkboxes:
                jobs = jobs | Jobs.objects.filter(collegeId = CollegeImages.objects.get(CollegeId = int(check)))
    context = {
                'jobs':jobs,
                'colleges':CollegeImages.objects.all(),
                'checklist':request.POST.getlist('checkbox')
                }
    return render(request,'jobs/jobs.html',context)

def reminder(request,applicatId,jobId):
    remind = Reminder()
    try:
        remind.userId = User.objects.get(id = int(applicatId))
        remind.jobId = Jobs.objects.get(jobId = int(jobId))
        remind.save()
    except:
        return HttpResponse('reminder already set by user')
    return HttpResponse('reminder set by user for current job. Thank you!')
