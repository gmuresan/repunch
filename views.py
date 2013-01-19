from operator import attrgetter
import pdb
import datetime
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from account.forms import CodeForm, UserRegisterForm
from account.models import UserUpdate
from punchcode.models import Punch, Code, EarnedReward
from retailer.forms import RetailerContactForm

def index(request, template_name='index.html'):

    if request.user.is_authenticated():

        if hasattr(request.user, 'retailer'):
            return HttpResponseRedirect('/retailer/home/')
        elif request.user.is_superuser:
            logout(request)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/vault/')

        user = request.user
        user_updates = user.updates.all()[0:10]
        retailer_updates = list()

        for retailer in user.subscribed_retailers.all():
            retailer_updates.extend(retailer.updates.filter()[0:3])

        updates = retailer_updates
        updates.extend(user_updates)

        updates = sorted(updates, key= lambda update: update.date, reverse=True)

        variables = RequestContext(request, {
            'updates':updates,

        })
    else:
        variables = RequestContext(request, {})

    
    return render_to_response(template_name, variables)

def retailers(request, template='info/retailers.html'):
    if request.method == 'POST':

        contact_form = RetailerContactForm(request.POST)

    else:

        contact_form = RetailerContactForm()

    variables = RequestContext(request, {
        'form': contact_form
    })

    return render_to_response(template, variables)

def contact(request, template_name='info/contact.html'):

    variables = RequestContext(request, {

    })

    return render_to_response(template_name, variables)