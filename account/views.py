from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from account.forms import LoginForm, RetailerRegisterForm, RetailerRegistrationCodeForm, FacebookRegisterForm, EditAccountForm
from retailer.models import RegistrationCode
import settings
from utility.facebook_functions import *

@csrf_exempt
def register(request, template_name='account/register.html'):
    if request.method == 'POST':
        facebook_data = fb_request_decode(request.POST.get('signed_request'), settings.FACEBOOK_APP_SECRET)

        form = FacebookRegisterForm(facebook_data['fb_data']['registration'])

        if form.is_valid():
            user = form.save()
            if facebook_data['auth']:
                user.facebook_uid = facebook_data['fb_data']['user_id']
                user.save()

            credentials = authenticate(username=user.username, password=facebook_data['fb_data']['registration']['password'])
            if credentials is not None:
                login(request, credentials)
                return HttpResponseRedirect('/')
    else:
        form = FacebookRegisterForm()

    variables = RequestContext(request, {
         'form':form
     })

    return render_to_response(template_name, variables)

def register_retailer(request, template_name='account/retailer/register_retailer.html'):
    if request.method == 'POST':
        form = RetailerRegisterForm(request.POST)

        registration_code = RegistrationCode.objects.get(pk=request.POST['registration_code'])
        retailer = registration_code.retailer

        if form.is_valid():
            retailer_account = form.save()
            retailer_account.retailer = retailer
            retailer_account.save()

            credentials = authenticate(username=request.POST['email'], password=request.POST['password'])
            if credentials is not None:
                login(request, credentials)
                return HttpResponseRedirect('/')

        else:
            variables = RequestContext(request, {
                'form':form,
                'registration_code':registration_code.code,
                'retailer':retailer
            })

            return render_to_response(template_name, variables)

    else:
        if 'registration_code' in request.GET:
            code_form = RetailerRegistrationCodeForm(request.GET)
            if code_form.is_valid():
                reg_code = code_form.cleaned_data['registration_code']
                retailer = reg_code.retailer

                variables = RequestContext(request, {
                    'form':code_form,
                    'retailer':retailer
                })

                return render_to_response(template_name, variables)
            else:
                return HttpResponseRedirect('/retailer/code')
        else:
            return HttpResponseRedirect('/retailer/code')


def registration_code(request):
    if 'registration_code' in request.GET:
        code_form = RetailerRegistrationCodeForm(request.GET)
        if code_form.is_valid():
            reg_code = code_form.cleaned_data['registration_code']
            retailer = reg_code.retailer
            reg_form = RetailerRegisterForm()

            variables = RequestContext(request, {
                'form':reg_form,
                'retailer':retailer,
                'registration_code':reg_code.code
            })

            return render_to_response('account/retailer/register_retailer.html', variables)

    else:
        code_form = RetailerRegistrationCodeForm()

    variables = RequestContext(request, {
        'form':code_form
    })

    return render_to_response('account/registration_code.html', variables)


def login_view(request, template_name='account/retailer/login.html'):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(username=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

    variables = RequestContext(request, {
        'form':form,
    })

    return render_to_response(template_name, variables)

def logoutUser(request, template_name='account/logout.html'):
    logout(request)
    return HttpResponseRedirect('/login')

def vault(request, template_name='account/customer/vault.html'):
    user = request.user
    retailers = dict()

    visited_retailers = user.visited_retailers.all()

    for retailer in visited_retailers:
        num_punches = user.punches.filter(retailer=retailer).count()
        earned_rewards = [earned_reward.reward for earned_reward in user.earned_rewards.filter(reward__retailer=retailer)]
        rewards = retailer.rewards.filter(active=True)
        rewards = sorted(rewards, key=lambda reward: reward.punches)
        levels = [reward.punches-1 for reward in rewards]
        retailers[retailer] = {'punches':num_punches,
                               'max':retailer.max_level,
                               'levels':levels,
                               'earned_rewards': earned_rewards
                                }

    user_updates = user.updates.all()[0:10]
    retailer_updates = list()

    for retailer in user.subscribed_retailers.all():
        retailer_updates.extend(retailer.updates.filter()[0:3])

    updates = retailer_updates
    updates.extend(user_updates)

    updates = sorted(updates, key= lambda update: update.date, reverse=True)
    num_punches = len(user.updates.filter(Q(action='punch') | Q(action='fb_punch')))
    if not num_punches:
        num_punches = 0

    variables = RequestContext(request,{
        'retailers':retailers,
        'updates':updates,
        'num_retailers':len(retailers),
        'num_punches':num_punches,
    })

    return render_to_response(template_name, variables)

def edit_account(request):
    user = request.user

    if user.type == 'user':
        return edit_user_account(request)
    elif user.type == 'retailer':
        return edit_retailer_account(request)

def edit_user_account(request, template_name='account/customer/edit_account.html'):
    user = request.user

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=user, initial={'zip':user.zip.code,})
        if form.is_valid():
            user = form.save()

    else:
        form = EditAccountForm(instance=user, initial={'zip':user.zip.code})

    vars = RequestContext(request, {
        'form':form
    })

    return render_to_response(template_name, vars)

def edit_retailer_account(request, template_name='account/retailer/edit_account.html'):
    pass




