from datetime import  datetime
from operator import attrgetter
import pdb
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.gis.geos.factory import fromstr
from django.contrib.gis.geos.point import Point
from django.contrib.gis.measure import D
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect, HttpResponseNotFound
from account.forms import  NewEmployeeForm
from account.models import Employee, UserUpdate
from punchcode.models import Code, Reward, EarnedReward
from retailer.forms import NewRetailerForm, RewardForm, SearchForm, EditRetailerForm
from retailer.models import Retailer, RetailerUpdate
from tools import geocode

user_is_retailer = lambda user: hasattr(user, 'type') and user.type == 'retailer'

def retailer_info(request, retailer_id, template_name='retailer/info.html'):
    try:
        retailer = Retailer.objects.get(pk=retailer_id)
    except Retailer.DoesNotExist:
        return HttpResponseNotFound("No retailer with that ID exists")

    vars = RequestContext(request, {
        'retailer':retailer
    })

    return render_to_response(template_name, vars)

def new_retailer(request, template_name='admin/new_retailer.html'):
    if request.method == 'POST':
        form = NewRetailerForm(request.POST)

        if form.is_valid():
            retailer = form.save()
            return HttpResponseRedirect('/edit/'+str(retailer.id))
    else:
        form = NewRetailerForm()

    variables = RequestContext(request, {
         'form':form
     })
    return render_to_response(template_name, variables)

def edit_retailer(request, id, template_name="admin/edit_retailer.html"):
    retailer = Retailer.objects.get(pk=id)

    rewards = sorted(retailer.rewards.all(), key=attrgetter('punches'))
    codes = sorted(retailer.code_set.all(), key=attrgetter('used'))

    vars = RequestContext(request, {
         'retailer':retailer,
         'rewards':rewards,
         'codes':codes
    })
    return render_to_response(template_name, vars)

@login_required
@user_passes_test(user_is_retailer)
def edit_retailer_info(request, template_name='retailer/edit_info.html'):
    retailer = request.user.retailer

    if request.method == 'POST':
        form = EditRetailerForm(request.POST, request.FILES, instance=retailer, initial={'zip':retailer.zip.code, 'city':retailer.city.name})
        if form.is_valid():
            retailer = form.save()
            return HttpResponseRedirect('/')

    else:
        form = EditRetailerForm(instance=retailer, initial={'zip':retailer.zip.code, 'city':retailer.city.name})

    vars = RequestContext(request , {
        'form':form
    })

    return render_to_response(template_name, vars)


def add_reward_level(request, template_name='retailer/add_reward_level.html'):
    if request.method == 'POST':
        form = RewardForm(request.POST)

        if form.is_valid():
            reward = form.save(commit=False)
            retailer = request.user.retailer
            reward.retailer = retailer
            reward.save()
            retailer.rewards.add(reward)
            if reward.punches > retailer.max_level:
                retailer.max_level = reward.punches
                retailer.save()

            return HttpResponseRedirect('/retailer/manage/')
    else:
        form = RewardForm()

    variables = RequestContext(request, {
         'form':form
     })
    return render_to_response(template_name, variables)

def add_code(request, id):
    retailer = Retailer.objects.get(pk=id)
    code = Code()
    code.used = False
    code.retailer_id = id

    code.code = hash(str(retailer.name)+str(datetime.now()))
    while int(code.code) < 0:
        code.code = hash(str(retailer.name) + str(datetime.now()))

    code.save()

    return HttpResponseRedirect('/edit/'+id)


def find_retailers(request, template_name='retailer/find_retailers.html'):
    if request.user.is_authenticated() :
        zip = request.user.zip
        retailers = Retailer.objects.filter(zip=zip)
    else:
        retailers = Retailer.objects.filter(zip__code__in=[48104,])

    variables = RequestContext(request, {
        'retailers':retailers
    })

    return render_to_response(template_name, variables)

def search(request, template_name='retailer/search.html'):
    form = SearchForm()
    retailers = list()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            location = geocode(form.cleaned_data['address'])
            lat = location['lat']
            lng = location['lng']
            pnt = Point(float(lng), float(lat))
            retailers = Retailer.objects.filter(point__distance_lte=(pnt, D(mi=5)))
            #retailers = Retailer.objects.filter(zip__code=48104)
        else:
            form = SearchForm()

    variables = RequestContext(request, {
         'form':form,
         'retailers':retailers,
     })
    return render_to_response(template_name, variables)

@login_required
@user_passes_test(user_is_retailer)
def home(request, template_name='retailer/home.html'):

    retailer = request.user.retailer
    employees = retailer.employees.all()
    active_rewards = retailer.rewards.filter(active=True)

    num_punches = retailer.punch_set.all().count()

    rewards = retailer.rewards.all()
    num_rewards_redeemed = 0
    num_rewards_earned = 0
    for reward in rewards:
        earned_rewards = reward.earnedreward_set
        num_rewards_earned += earned_rewards.count()
        num_rewards_redeemed += earned_rewards.filter(redeemed=True).count()

    variables = RequestContext(request, {
        'retailer':retailer,
        'employees':employees,
        'rewards':active_rewards,
        'num_punches':num_punches,
        'num_rewards_earned':num_rewards_earned,
        'num_rewards_redeemed':num_rewards_redeemed,
        'num_facebook_posts':retailer.num_facebook_posts,
    })

    return render_to_response(template_name, variables)

@login_required
@user_passes_test(lambda user: hasattr(user, 'type') and user.type == 'retailer')
def manage_deals(request, template_name='retailer/manage_deals.html'):
    retailer_account = request.user
    retailer = retailer_account.retailer
    rewards = retailer.rewards
    active_rewards = rewards.filter(active=True)
    inactive_rewards = rewards.filter(active=False)

    sorted(inactive_rewards, key=lambda reward: reward.punches)
    sorted(active_rewards, key=lambda reward: reward.punches)

    variables = RequestContext(request, {
        'rewards':rewards.all(),
        'retailer':retailer,
        'active_rewards':active_rewards,
        'inactive_rewards':inactive_rewards,
    })

    return render_to_response(template_name, variables)

def sample_data(request, template_name='retailer/view_data.html'):

    vars = RequestContext(request, {

    })

    return render_to_response(template_name, vars)

@login_required
@user_passes_test(user_is_retailer)
def view_data(request, template_name='retailer/view_data.html'):

    user = request.user
    retailer = user.retailer
    num_punches = retailer.code_set.filter(used=True).count()

    rewards = retailer.rewards.all()
    num_rewards_redeemed = 0
    num_rewards_earned = 0
    for reward in rewards:
        earned_rewards = reward.earnedreward_set
        num_rewards_earned += earned_rewards.count()
        num_rewards_redeemed += earned_rewards.filter(redeemed=True).count()

    customers = retailer.users_visited


    variables = RequestContext(request, {
        'num_punches':num_punches,
        'num_rewards_earned':num_rewards_earned,
        'num_rewards_redeemed':num_rewards_redeemed,
        'num_facebook_posts':retailer.num_facebook_posts,
    })
    return render_to_response(template_name, variables)

@login_required
@user_passes_test(user_is_retailer)
def edit_reward(request, reward_id, template_name='retailer/edit_reward.html'):
    try:
        user = request.user
        retailer = user.retailer
        reward = Reward.objects.get(pk=reward_id)

        if reward not in retailer.rewards.all():
            return HttpResponseRedirect(reverse('manage_deals'))
    except Reward.DoesNotExist:
        return HttpResponseRedirect(reverse('manage_deals'))

    if request.method == 'POST':
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            reward = form.save()

            num_punches_for_reward = reward.punches
            subscribed_users = retailer.users_subscribed
            for user in subscribed_users.all():
                num_punches_at_retailer = user.punches.filter(retailer=retailer).count()
                if num_punches_at_retailer >= num_punches_for_reward:
                    earned_reward = EarnedReward(reward=reward)
                    earned_reward.save()
                    user.earned_rewards.add(earned_reward)

                    reward_update = UserUpdate(action='earn', retailer=retailer, reward=earned_reward.reward, user=user)
                    reward_update.save()


            return HttpResponseRedirect(reverse('manage_deals'))
        else:
            variables = RequestContext(request, {
                'form':form,
                'reward':reward
            })
            return render_to_response(template_name, variables)

    else:
        form = RewardForm(instance=reward)
        variables = RequestContext(request, {
            'form':form,
            'reward':reward
        })

        return render_to_response(template_name, variables)

@login_required
@user_passes_test(user_is_retailer)
def remove_level(request, reward_id):
    try:
        user = request.user
        retailer = user.retailer
        reward = Reward.objects.get(pk=reward_id)
    except Reward.DoesNotExist:
        return HttpResponseRedirect(reverse('manage_deals'))

    if reward in retailer.rewards.filter(active=True):
        reward.active = False
        reward.save()

    if reward.punches == retailer.max_level:
        levels = sorted([reward.punches for reward in retailer.rewards.filter(active=True)])
        retailer.max_level = levels[-1]
        retailer.save()

    return HttpResponseRedirect(reverse('manage_deals'))

@login_required
@user_passes_test(user_is_retailer)
def manage_employees(request, template_name='retailer/employee/manage_employees.html'):
    employees = request.user.retailer.employees

    vars = RequestContext(request, {
        'employees':employees.all(),
    })

    return render_to_response(template_name, vars)

@login_required
@user_passes_test(user_is_retailer)
def edit_employee(request, employee_id, template_name='retailer/employee/edit_employee'):
    employee = Employee.objects.get(pk=employee_id)
    if employee.retailer != request.user.retailer:
        return HttpResponseRedirect(reverse('manage_employee'))

@login_required
@user_passes_test(user_is_retailer)
def add_employee(request, template_name='retailer/employee/add_employee.html'):
    if request.method == 'POST':
        form = NewEmployeeForm(request.POST)

        if form.is_valid():
            employees = request.user.retailer.employees
            username_exists = employees.filter(username=form.cleaned_data['username'])
            if username_exists.exists():
                form._errors['username'].append('Username already exists')
            else:
                employee = Employee()
                employee.first_name = form.cleaned_data['first_name']
                employee.last_name = form.cleaned_data['last_name']
                employee.username = form.cleaned_data['username']
                employee.retailer = request.user.retailer
                employee.save()
                return HttpResponseRedirect(reverse('manage_employees'))

    else:
        form = NewEmployeeForm()


    vars = RequestContext(request, {
        'form':form
    })

    return render_to_response(template_name, vars)



