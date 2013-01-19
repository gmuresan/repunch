from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^new', 'retailer.views.new_retailer'),
    url(r'^edit/(?P<id>\d+)/$', 'retailer.views.edit_retailer'),
    url(r'^add-reward/$', 'retailer.views.add_reward_level', name="add_reward"),
    url(r'^add-code/(?P<id>\d+)/$', 'retailer.views.add_code'),
    url(r'^participating-retailers/$', 'retailer.views.find_retailers'),
    url(r'^search/$', 'retailer.views.search', name='retailer_search'),
    url(r'^retailer/home/$', 'retailer.views.home'),
    url(r'^retailer/manage/$', 'retailer.views.manage_deals', name='manage_deals'),
    url(r'^retailer/data/$', 'retailer.views.view_data', name="view_data"),
    url(r'^retailer/reward/edit/(?P<reward_id>\d+)/$', 'retailer.views.edit_reward', name="edit_reward"),
    url(r'^retailer/reward/delete/(?P<reward_id>\d+)/$', 'retailer.views.remove_level', name="delete_reward"),
    url(r'^retailer/info/(?P<retailer_id>\d+)/$', 'retailer.views.retailer_info', name="retailer_info"),
    url(r'^retailer/employees/manage/$', 'retailer.views.manage_employees', name='manage_employees'),
    url(r'^retailer/employees/new/$', 'retailer.views.add_employee', name='add_employee'),
    url(r'^retailer/edit/$', 'retailer.views.edit_retailer_info', name='edit_retailer_info'),


)
