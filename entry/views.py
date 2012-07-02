from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from entry.models import Patient, Entry
from entry.forms import RegistrationForm, LoginForm, EntryForm
from urllib import urlencode
from urllib2 import urlopen

from tropo import Tropo, Session, Message
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
    try:
        t = Tropo()
                
        session = Session(request.body)
        if('parameters' in dir(session)):
            print('Found Params')
            json = t.say("Sending TEXT MSG")

        else :

            msg = request.POST.get('msg', '')
            s = Session(request.body)
            cell = s.fromaddress['id']

            # lookup patient with this cell #
            if cell[0]=='1':   # trim leading 1 in cell # if there
                cell = cell[1:]
            print('Cell #%s' % cell)
            p = Patient.objects.filter(cell=cell)   # all patients with this cell #
            if p.exists():                                    # if cell # found then create new entry
                if p.count()>1:
                    print('WARNING: Multiple patients with cell # %s' % cell)
                parent = p[0]  # assume first 
                entry = Entry(patient=parent, entry=msg)
                entry.save()
                if msg.find('CODE')>-1:
                    json = t.say("Congratulations " + parent.name + " your code qualified you for a prize!")            
                else:
                    json = t.say("Entry saved, thank you " + parent.name)
            else:                                               # if cell # NOT found then notify
                json = t.say("Could not find patient with cell # " + cell)

        json = t.RenderJson(json)

        return HttpResponse(json)
    except Exception, err:
        print('ERROR: %s\n' % str(err))



def HomePage(request):
    context = {}
    return render_to_response('index.html', context, context_instance=RequestContext(request))
    

def PatientRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['name'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            user.save()
            patient = Patient(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'], gender = form.cleaned_data['gender'], email = form.cleaned_data['email'], cell = form.cleaned_data['cell'])
            patient.save()

            # text patient if cell # provided
            if len(patient.cell)==10:
                t = Tropo()
                t.say("Thank you for registering " + patient.name)
                t.message("Thank you for registering.", to="+17813128445", network = "SMS")
                t.RenderJson()
                print "Registration confirmation sent"

            return HttpResponseRedirect('/profile/')

#                try:
#                    t.message("Thank you for registering.", {"to":"+17816408832", "network":"SMS"})
#                send_message("+17816408832", "Thank you for registering.")
#                except Exception, err:
#                    print('ERROR: %s\n' % str(err))

        else:   # form is not valid
#            print form.errors
            return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    
    else:
        ''' user is not submitting the form '''
        form = RegistrationForm()
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))

@login_required
def Profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    patient = request.user.get_profile
    context = {'patient': patient}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))


def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            print "authenticating user: %s" % name
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile/')
            else:
                
                return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
        
    else:
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')
        
def AddEntry(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = EntryForm(request.POST)
            if form.is_valid():
                parent = request.user.get_profile()
                entry = Entry(patient=parent, entry=form.cleaned_data['entry'], desc=form.cleaned_data['desc'])
                entry.save()
                if form.cleaned_data['entry'].find('CODE')>-1:
                    return HttpResponseRedirect('/code/')
                else:
                    return HttpResponseRedirect('/profile/')
            else:
                print form.errors
                return render_to_response('entry.html', {'form':form}, context_instance=RequestContext(request))
        else:
            ''' user is not submitting the form '''
            form = EntryForm()
            context = {'form': form}
            return render_to_response('entry.html', context, context_instance=RequestContext(request))
    else:
        pass


def send_message(cell, msg):
    base_url = 'http://api.tropo.com/1.0/sessions'
    token = '13bed2b0b149a5449342d27e3728470c308535c1c2033349cc1735d293bcd3dfbc64601eab5934e7c45c52f1'      
    action = 'create'
    number  = cell
    message = msg
        
    params = urlencode([('action', action), ('token', token), ('to_num', number), ('message', message), ('outgoing', True)])
    urlopen('%s?%s' % (base_url, params))

