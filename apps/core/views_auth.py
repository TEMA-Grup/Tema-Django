from django.contrib.auth.views import LogoutView
class LogoutViewAllowGet(LogoutView):
    http_method_names = ["get", "post", "head", "options"]