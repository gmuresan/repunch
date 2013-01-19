from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    #(r'^mobile/register', 'mobile.views.register'),
    (r'^mobile/login', 'mobile.views.login'),
    (r'^mobile/confirm_fb_post', 'mobile.views.confirm_facebook_post'),
    (r'^mobile/newsfeed', 'mobile.views.user_newsfeed'),
    #(r'^mobile/reward', 'mobile.views.redeem_reward'),
    (r'^mobile/vault', 'mobile.views.get_vault'),
    (r'^mobile/reward_info', 'mobile.views.get_reward_info'),
    (r'^mobile/retailer_info', 'mobile.views.get_retailer_info'),
    (r'^mobile/search', 'mobile.views.search'),
    #(r'^mobile/gift', 'mobile.views.gift'),
    #(r'^mobile/user_search', 'mobile.views.user_search'),
    #(r'^mobile/admin/generate', 'mobile.views.generate_code'),
    (r'^mobile/admin/login', 'mobile.views.admin_login'),
    (r'^mobile/admin/punch', 'mobile.views.punch'),
    (r'^mobile/admin/reward', 'mobile.views.admin_accept_reward'),


)
