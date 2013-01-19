import datetime
from operator import attrgetter
from django.contrib.auth import authenticate
import json
from django.contrib.gis.geos.point import Point
from django.contrib.gis.measure import D
from django.db.models.query_utils import Q
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from account.models import RetailerAccount, Employee, Log, UserUpdate, PendingFacebookPost
from mobile.forms import *
from punchcode.models import  Code, Punch

@csrf_exempt
def login(request):
    if request.method == 'POST':
        response = dict()
        response['success'] = False
        access_token = request.POST['access_token']
        if 'expires' in request.POST and request.POST['expires'] is not None and request.POST['expires'] != '':
            expires = int(request.POST['expires'])
        else:
            expires = 1000

        user = authenticate(access_token=access_token, expires=expires)

        if user is None:
            response['error'] = 'User is not registered'
        else:
            response['success'] = True
            response['first_name'] = user.first_name
            response['last_name'] = user.last_name
            if user.zip is None:
                zip_code = 0
            else:
                zip_code = user.zip.code
            response['zip'] = zip_code
            response['user_id'] = user.id
            response['gender'] = user.gender

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        form = MobileAccessTokenForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def register(request):
    if request.method == 'POST':

        response = dict()

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            if request.POST['fb_uid']:
                user.facebook_uid = request.POST['fb_uid']
                user.save()

            response['success'] = True
        else:
            response['success'] = False
            response['error'] = form.errors[0]

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        form = RegisterForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def get_reward_info(request):
    if request.method == 'POST':
        response = dict()

        reward_id = int(request.POST['reward_id'])
        response['success'] = False

        try:
            reward = Reward.objects.get(pk=reward_id)
            response['success'] = True
            response['reward_text'] = reward.text
            response['punches'] = reward.punches
            response['retailer_id'] = reward.retailer.pk
            response['active'] = reward.active
            response['shareable'] = reward.shareable

        except Reward.DoesNotExist:
            response['success'] = False
            response['error'] = 'No Reward Found'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileRewardInfoForm(request.POST)

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def get_retailer_info(request):
    if request.method == 'POST':
        response = dict()

        retailer_id = int(request.POST['retailer_id'])

        try:
            retailer = Retailer.objects.get(pk=retailer_id)

            response['address'] = retailer.address
            response['city'] = retailer.city.name
            response['zip'] = retailer.zip.code
            response['lat'] = retailer.lat
            response['lng'] = retailer.lng
            response['name'] = retailer.name
            response['category'] = retailer.category
            response['description'] = retailer.description
            response['hours'] = retailer.hours
            response['phone'] = retailer.phone
            response['main_image'] = retailer.main_image.url
        except Retailer.DoesNotExist:
            response['error'] = 'Retailer does not exist'
            response['success'] = False

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileRetailerInfoForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def get_vault(request):
    if request.method == 'POST':

        response = dict()
        access_token = request.POST['access_token']
        if 'expires' in request.POST and request.POST['expires'] is not None and request.POST['expires'] != '':
            expires = int(request.POST['expires'])
        else:
            expires = 1000

        try:
            user = authenticate(access_token=access_token, expires=expires)

            punches = user.punches.all()
            vault = list()

            visited_retailers = user.visited_retailers.all()

            for retailer in visited_retailers:
                num_punches = user.punches.filter(retailer=retailer).count()
                earned_rewards = user.earned_rewards.filter(reward__retailer=retailer)
                earned_reward_list = list()
                for earned_reward in earned_rewards:
                    current_earned_reward = dict()
                    current_earned_reward['earned_reward_id'] = earned_reward.pk
                    current_earned_reward['reward_id'] = earned_reward.reward.pk
                    current_earned_reward['punches'] = earned_reward.reward.punches
                    current_earned_reward['text'] = earned_reward.reward.text
                    earned_reward_list.append(current_earned_reward)

                active_rewards = sorted(retailer.rewards.filter(active=True), key=attrgetter('punches'))
                reward_levels = list()
                for reward in active_rewards:
                    reward_levels.append(reward.punches)

                if active_rewards:
                    next_reward_id = active_rewards[0].id
                    for reward in active_rewards:
                        next_reward_id = reward.id
                        if num_punches < reward.punches:
                            break
                else:
                    next_reward_id = 1

                vault.append(dict( {'retailer_name':retailer.name,
                                   'retailer_id':retailer.pk,
                                   'punches':num_punches,
                                   'levels':reward_levels,
                                   'earned_rewards': earned_reward_list,
                                   'next_reward_id':next_reward_id,
                                   'main_image': retailer.main_image.url,
                                    } ))

            response['vault'] = vault
            response['success'] = True

        except UserAccount.DoesNotExist:
            response['success'] = False
            response['error'] = 'Invalid User ID'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileAccessTokenForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

# Logic for actually executing the punch
# Used by the admin punch call, and confirm_facebook_post consumer call
def execute_punch(user, retailer):
    response = dict()
    response['success'] = False

    # Record a punch for this user
    punch = Punch(retailer=retailer)
    punch.save()
    user.punches.add(punch)

    all_punches_at_retailer = user.punches.filter(retailer=retailer)
    num_punches = len(all_punches_at_retailer)

    rewards = retailer.rewards.all()

     # Check if a user has any updates related to this retailer
    # Option for facebook post first time user was punched
    response['facebook_post'] = (user.updates.filter(retailer=retailer).exists() is not True)
    response['reward'] = False

    # Check if a user needs to be given a reward based on number of punches
    for reward in rewards:
        if num_punches == reward.punches:
            earned_reward = EarnedReward()
            earned_reward.reward = reward
            earned_reward.save()
            user.earned_rewards.add(earned_reward)
            response['facebook_post'] = True

            reward_info = dict()
            reward_info['reward_text'] = reward.text
            reward_info['punches'] = reward.punches
            reward_info['retailer_id'] = reward.retailer.pk
            reward_info['active'] = reward.active
            reward_info['shareable'] = reward.shareable
            response['reward'] = reward_info
            break

    if response['reward']:
        reward_update = UserUpdate(action='earn', retailer=retailer, reward=earned_reward.reward, user=user)
        reward_update.save()

    # If the user has earned all the rewards, delete the punches
    if num_punches >= retailer.max_level:
        all_punches_at_retailer.delete()

    # Record that the user has a pending facebook post if applicable
    if response['facebook_post']:
        try:
            pending_facebook_post = user.pending_facebook_posts.get(retailer=retailer)
        except PendingFacebookPost.DoesNotExist:
            pending_facebook_post = PendingFacebookPost(retailer=retailer)
            pending_facebook_post.save()
            user.pending_facebook_posts.add(pending_facebook_post)

    if num_punches <= 2:
        if not user.subscribed_retailers.filter(pk=retailer.pk).exists():
            user.subscribed_retailers.add(retailer)

        if not user.visited_retailers.filter(pk=retailer.pk).exists():
            user.visited_retailers.add(retailer)

    response['success'] = True

    return response

@csrf_exempt
def punch(request):
    if request.method == 'POST':
        response = dict()

        access_token = request.POST['access_token']
        if 'expires' in request.POST and request.POST['expires'] is not None and request.POST['expires'] != '':
            expires = int(request.POST['expires'])
        else:
            expires = 1000
        employee_username = request.POST['employee_username']
        retailer_id = int(request.POST['retailer_id'])
        retailer_password = request.POST['retailer_password']

        try:
            user = authenticate(access_token=access_token, expires=expires)
            retailer = Retailer.objects.get(pk=retailer_id)
            # Check that the retailer admin password is correct
            if retailer.admin_password != retailer_password:
                response['success'] = False
                response['error'] = 'Incorrect Password'
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')

            response = execute_punch(user=user, retailer=retailer)

            # Log the punch in the user's updates
            punch_update = UserUpdate(action='punch', retailer=retailer, user=user)
            punch_update.save()

        except UserAccount.DoesNotExist:
            response['success'] = False
            response['error'] = "User does not exist"
        except Retailer.DoesNotExist:
            response['success'] = False
            response['error'] = 'Retailer does not exist'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        form = MobileCodeForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

# Used to confirm that a user successfully posted to facebook following a first
@csrf_exempt
def confirm_facebook_post(request):
    if request.method == 'POST':
        response = dict()
        response['success'] = False

        access_token = request.POST['access_token']
        if 'expires' in request.POST and request.POST['expires'] is not None and request.POST['expires'] != '':
            expires = int(request.POST['expires'])
        else:
            expires = 1000
        retailer_id = int(request.POST['retailer_id'])

        try:
            user = authenticate(access_token=access_token, expires=expires)
            retailer = Retailer.objects.get(pk=retailer_id)

            pending_facebook_post = user.pending_facebook_posts.get(retailer=retailer)

            response = execute_punch(user=user, retailer=retailer)

            # Log the punch in the user's updates
            punch_update = UserUpdate(action='fb_punch', retailer=retailer, user=user)
            punch_update.save()

            retailer.num_facebook_posts += 1
            retailer.save()

            # Delete the pending facebook post if the user does not have another pending facebook post
            if not response['facebook_post']:
                pending_facebook_post.delete()
            else:
                pending_facebook_post.save()

        except UserAccount.DoesNotExist:
            response['error'] = 'User does not exist'
        except Retailer.DoesNotExist:
            response['error'] = 'Retailer does not exist'
        except PendingFacebookPost.DoesNotExist:
            response['error'] = 'User cannot post to facebook at this time'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        form = MobileConfirmFBPostForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)


@csrf_exempt
def user_newsfeed(request):
    if request.method == 'POST':
        response = dict()
        response['success'] = False
        user_id = int(request.POST['user_id'])

        try:
            user = UserAccount.objects.get(pk=user_id)

            user_updates = user.updates.all()[0:20]
            retailer_updates = list()
            for retailer in user.subscribed_retailers.all():
                retailer_updates.extend(retailer.updates.all()[0:3])

            updates = retailer_updates
            updates.extend(user_updates)

            updates = sorted(updates, key= lambda update: update.date, reverse=True)

            response['news'] = list()
            for update in updates:
                current_update = dict()
                current_update['date'] = update.date.strftime('%m-%d-%y %H:%M:%S %z')
                current_update['text'] = unicode(update)
                current_update['type'] = update.action
                if update.retailer is not None:
                    current_update['retailer_id'] = update.retailer.id
                response['news'].append(current_update)

            response['success'] = True

        except UserAccount.DoesNotExist:
            response['error'] = 'User does not exist'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileUserIDForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)


@csrf_exempt
def search(request):
    if request.method == 'POST':
        #form = MobileSearchForm(request.POST)

        response = dict()
        response['retailers'] = list()

        method = request.POST['method']

        if 'distance' in request.POST and request.POST['distance'] is not None and request.POST['distance'] != '':
            distance = request.POST['distance']
        else:
            distance = 5

        retailers = list()
        if method == 'address':
            address = request.POST['address']
            location = geocode(address)
            lat = location['lat']
            lng = location['lng']
            point = Point(float(lng), float(lat))
            retailers = Retailer.objects.filter(point__distance_lte=(point, D(mi=int(distance))))

        elif method == 'coordinates':
            lat = request.POST['lat']
            lng = request.POST['lng']
            point = Point(float(lng), float(lat))
            retailers = Retailer.objects.filter(point__distance_lte=(point, D(mi=int(distance))))
        elif method == 'zip':
            code = request.POST['address']
            zip,created = Zip.objects.get_or_create(code=code)
            point = Point(float(zip.lng), float(zip.lat))
            distance = int(distance)+2
            retailers = Retailer.objects.filter(Q(zip=zip) | Q(point__distance_lte=(point, D(mi=int(distance)))))

        for retailer in retailers:
            retailer_dict = dict()
            retailer_dict['retailer_id'] = retailer.pk
            retailer_dict['name'] = retailer.name
            retailer_dict['zip'] = retailer.zip.code
            retailer_dict['address'] = retailer.address
            retailer_dict['lat'] = retailer.lat
            retailer_dict['lng'] = retailer.lng
            retailer_dict['description'] = retailer.description
            retailer_dict['hours'] = retailer.hours
            retailer_dict['city'] = retailer.city.name
            #retailer_dict['distance'] = retailer.distance(point).distance
            response['retailers'].append(retailer_dict)

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileSearchForm()

        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def user_search(request):
    if request.method == 'POST':
        response = list()

        search = request.POST['search']

        users = UserAccount.objects.filter(Q(first_name__in=[search,]) | Q(last_name__in=[search,]) | Q(email__in=[search,]))

        for user in users:
            user_dict = dict()
            user_dict['first_name'] = user.first_name
            user_dict['last_name'] = user.last_name
            user_dict['email'] = user.email
            user_dict['zip'] = user.zip.code
            user_dict['city'] = user.zip.city_set.first().name
            user_dict['state'] = user.zip.city_set.first().state.name
            user_dict['id'] = user.pk
            response.append(user_dict)

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        form = MobileUserSearchForm()
        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)

# OBSOLETE
@csrf_exempt
def redeem_reward(request):
    if request.method == 'POST':
        response = dict()
        form = MobileRedeemRewardForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user_id']
            earned_reward = form.cleaned_data['earned_reward_id']
            password = form.cleaned_data['password']

            if earned_reward.redeemed:
                response['error'] = 'Reward Already Redeemed'
                response['success'] = False
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')

            if user.check_password(password):
                if earned_reward.useraccount_set.all()[0].user.pk == user.pk:
                    response["success"] = True
                    response["reward_text"] = earned_reward.reward.text

                    barcode_text = dict()
                    barcode_text["erid"] = str(earned_reward.id)
                    barcode_text["uid"] = str(user.id)
                    barcode_text["dt"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                    response['barcode_text'] = mobile_encrypt(json.dumps(barcode_text))

                    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

                else:
                    response['success'] = False
                    response['error'] = 'User has not earned this reward'
            else:
                response['success'] = False
                response['error'] = 'Incorrect Password'
        else:
            response['success'] = False
            response['error'] = form.errors

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileRedeemRewardForm()
        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)



@csrf_exempt
def gift(request):
    if request.method == 'POST':
        response = dict()
        gifter_id = request.POST['gifter_id']
        gifter_password = request.POST['password']
        giftee_id = request.POST['giftee_id']
        reward_id = request.POST['reward_id']

        gifter = UserAccount.objects.get(pk=gifter_id)
        if gifter.check_password(gifter_password):
            giftee = UserAccount.objects.get(pk=giftee_id)

            reward = Reward.objects.get(pk=reward_id)
            if reward in gifter.rewards:
                gifter.rewards.remove(reward)
                giftee.rewards.add(reward)
                if reward in giftee.rewards:
                    response['success'] = True
            else:
                response['success'] = False
                response['error'] = 'User does not own reward'

        else:
            response['success'] = False
            response['error'] = 'Invalid Password'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        variables = RequestContext(request, {})
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        response = dict()
        form = MobileAdminLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            retailer_id = form.cleaned_data['retailer_id']
            password = form.cleaned_data['password']
        else:
            response['success'] = False
            response['error'] = 'Invalid form values'
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')

        try:
            retailer = Retailer.objects.get(pk=retailer_id)
            if retailer.admin_password == password:
                employee_account = retailer.employees.get(username=username)
                response['success'] = True
                response['employee_first_name'] = employee_account.first_name
                response['employee_last_name'] = employee_account.last_name

                retailer_info = dict()
                retailer_info['name'] = retailer.name
                retailer_info['address'] = retailer.address
                retailer_info['city'] = retailer.city.name
                retailer_info['zip'] = retailer.zip.code
                retailer_info['lat'] = retailer.lat
                retailer_info['lng'] = retailer.lng
                retailer_info['category'] = retailer.category
                retailer_info['description'] = retailer.description
                retailer_info['hours'] = retailer.hours
                response['retailer_info'] = retailer_info

                return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        except Employee.DoesNotExist:
            response['success'] = False
            response['error'] = 'Employee does not exist.'
        except Retailer.DoesNotExist:
            response['success'] = False
            response['error'] = 'Retailer does not exist'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileAdminLoginForm()
        variables = RequestContext(request, {
            'form':form
        })
        return render_to_response('mobile/test.html', variables)

@csrf_exempt
def generate_code(request):
    if request.method == 'POST':
        response = dict()
        retailer_id = request.POST['retailer_id']
        retailer_password = request.POST['password']
        employee_id = request.POST['employee_id']

        try:
            retailer_account = RetailerAccount.objects.get(retailerId=retailer_id)
            if retailer_account.user.check_password(retailer_password):
                retailer = retailer_account.retailer
                employee = Employee.objects.get(employeeId=employee_id, retailer=retailer)

                code = Code()
                code.used = False
                code.retailer = retailer

                code.code = hash(str(retailer.name)+str(datetime.datetime.now()))
                while int(code.code) < 0:
                    code.code = hash(str(retailer.name) + str(datetime.datetime.now()))

                code.save()

                log = Log()
                log.employee = employee
                log.code = code
                log.date = datetime.datetime.now()
                log.action = 'generated'

                response['success'] = True
                response['code'] = code.code
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')
            else:
                response['success'] = False
                response['error'] = 'Incorrect Password'

        except Employee.DoesNotExist:
            response['success'] = False
            response['error'] = 'Employee ID is incorrect'
        except RetailerAccount.DoesNotExist:
            response['success'] = False
            response['error'] = 'Retailer ID is incorrect'

        return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def admin_accept_reward(request):
    if request.method == 'POST':
        try:
            response = dict()
            response['success'] = False

            access_token = request.POST['access_token']
            if 'expires' in request.POST and request.POST['expires'] is not None and request.POST['expires'] != '':
                expires = int(request.POST['expires'])
            else:
                expires = 1000

            earned_reward_id = int(request.POST['earned_reward_id'])
            retailer_id = int(request.POST['retailer_id'])
            retailer_password = request.POST['retailer_password']
            employee_username = request.POST['employee_username']

            user = authenticate(access_token=access_token, expires=expires)
            earned_reward = user.earned_rewards.get(pk=earned_reward_id)
            if earned_reward.redeemed:
                response['error'] = 'Reward was Already Redeemed'
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')

            retailer = Retailer.objects.get(pk=retailer_id)
            if retailer.admin_password != retailer_password:
                response['error'] = 'Incorrect Password'
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')

            if earned_reward.reward.retailer != retailer:
                response['error'] = 'Reward is not valid at this retailer'
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')

            employee = retailer.employees.get(username=employee_username)

            user_update_punch = UserUpdate(action='redeem', retailer=retailer, reward=earned_reward.reward, user=user)
            user_update_punch.save()

            earned_reward.redeemed = True
            earned_reward.save()

            response['success'] = True
            response['reward_text'] = earned_reward.reward.text


        except UserAccount.DoesNotExist:
            response['error'] = 'Invalid Barcode'
        except Retailer.DoesNotExist:
            response['error'] = 'Retailer Does Not Exist'
        except Employee.DoesNotExist:
            response['error'] = 'Employee Does Not Exist'
        except EarnedReward.DoesNotExist:
            response['error'] = 'Earned Reward Does Not Exist'


        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    else:
        form = MobileAdminRedeemRewardForm()
        variables = RequestContext(request, {'form':form})
        return render_to_response('mobile/test.html', variables)


