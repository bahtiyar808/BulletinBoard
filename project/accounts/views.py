from .models import User
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import CreateView, UpdateView
# from .forms import SignUpForm

from django.shortcuts import redirect, render




# class SignUp(CreateView):
#     model = User
#     form_class = SignUpForm
#     success_url = 'registration/login'
#     template_name = 'registration/signup.html'


class CustomConfirmEmailView(UpdateView):
    model = User
    context_object_name = 'confirm'

    def post(self, request, *args, **kwargs):
        if 'confirmation_code' in request.POST:
            user = User.objects.filter(code=request.POST['confirmation_code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'account/invalid_code.html')
        return redirect('/accounts/login')
