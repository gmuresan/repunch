from account.models import *
from django.contrib.auth.backends import ModelBackend

class CustomerModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):

        try:
            user_account = UserAccount.objects.get(username=username)
            if user_account.check_password(password):
                return user_account
        except UserAccount.DoesNotExist:
            try:
                retailer = RetailerAccount.objects.get(username=username)
                if retailer.check_password(password):
                    return retailer
            except RetailerAccount.DoesNotExist:
                try:
                    user = User.objects.get(username=username)
                    if user.check_password(password):
                        return user
                except User.DoesNotExist:
                    return None

    def get_user(self, user_id):
        try:
            return UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            try:
                return RetailerAccount.objects.get(pk=user_id)
            except RetailerAccount.DoesNotExist:
                try:
                    return User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return None