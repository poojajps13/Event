import json
import urllib.parse
import urllib.request
from datetime import date

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView

from event.models import EventRecord
from registration.models import RegistrationRecord
from student.forms import StudentForm
from student.models import StudentRecord
from .forms import SignupForm, LoginForm, ResetPasswordForm, EditUserForm, EmailForm
from .tokens import account_activation_token, password_reset_token


# Create your views here.
def is_block(request, user):
    if not user.is_active and user.last_login:
        return True
    return False


def logout(request):
    auth.logout(request)
    return redirect('home')


# noinspection PyBroadException
class Login(TemplateView):
    template = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        form1 = EmailForm()
        request.session['head_name'] = 'login'
        return render(request, self.template, {'form': form, 'form1': form1, 'site_key': settings.RECAPTCHA_SITE_KEY})

    def post(self, request):
        try:
            form = LoginForm(request.POST)
            form1 = EmailForm(request.POST)
            ''' Begin reCAPTCHA validation '''
            values = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': request.POST.get('recaptcha')
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(settings.RECAPTCHA_SITE_VERIFICATION_URL, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # print(result)
            ''' End reCAPTCHA validation '''

            # Login Form
            if result['success'] and result['action'] == 'login' and form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                u = User.objects.get(username=email.lower())
                if is_block(request, u):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                user = auth.authenticate(username=email.lower(), password=password)
                if user is not None:
                    auth.login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    return redirect("account:consolidated_view_all")
                elif not u.is_active:
                    messages.warning(request, 'Please confirm the activation link from your Email')
                else:
                    messages.error(request, "Your authentication information is incorrect. Please try again.")

            # Forget Password
            elif result['success'] and result['action'] == 'forgetPassword' and form1.is_valid():
                email = form1.cleaned_data['email1']
                user = User.objects.get(username=email.lower())
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                '''Begin Email Sending '''
                current_site = get_current_site(request)
                mail_subject = 'Password Reset link of your CBSE Account.'
                message = render_to_string('forget-password.txt', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                    'email': settings.CONTACT_EMAIL,
                    'number': settings.CONTACT_NUMBER
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()
                '''End Email sending'''

                messages.success(request, 'Password reset link has been sent to your registered E-mail Address')
                return redirect('home')
            else:
                messages.warning(request, 'Invalid Input or Invalid reCAPTCHA. Please try again')

        except ObjectDoesNotExist:
            messages.error(request, 'Invalid Inputs. Please try again')
        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('home')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
        form = LoginForm()
        form1 = EmailForm()
        return render(request, self.template, {'form': form, 'form1': form1, 'site_key': settings.RECAPTCHA_SITE_KEY})


# noinspection PyBroadException
class Signup(TemplateView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        request.session['head_name'] = 'signup'
        return render(request, self.template_name, {'form1': form, 'site_key': settings.RECAPTCHA_SITE_KEY})

    def post(self, request):
        try:
            ''' Begin reCAPTCHA validation '''
            values = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': request.POST.get('recaptcha')
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(settings.RECAPTCHA_SITE_VERIFICATION_URL, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # print(result)
            ''' End reCAPTCHA validation '''

            form = SignupForm(request.POST)
            if result['success'] and result['action'] == 'signup' and form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email'].lower()
                password = form.cleaned_data['password']
                try:
                    user = User.objects.get(username=email)
                    if is_block(request, user):
                        raise PermissionDenied('Your Account is blocked. Please Contact Us')
                    user.first_name = first_name
                    user.last_name = last_name
                    user.set_password(password)
                    user.save()
                except ObjectDoesNotExist:
                    user = User.objects.create(username=email, email=email, password=password, first_name=first_name,
                                               last_name=last_name, is_active=False)

                '''Begin Email Sending '''
                current_site = get_current_site(request)
                mail_subject = 'Action Required: Activate your CBSE account'
                message = render_to_string('acc_active_email.txt', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'email': settings.CONTACT_EMAIL,
                    'number': settings.CONTACT_NUMBER
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()
                '''End Email sending'''

                messages.success(request, 'Check your mail to complete registration')
                return redirect("account:login")
            else:
                messages.warning(request, 'Invalid Input or Invalid reCAPTCHA. Please try again')
            return render(request, self.template_name, {'form1': form, 'site_key': settings.RECAPTCHA_SITE_KEY})

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('home')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("account:signup")


# noinspection PyBroadException
class Activate(TemplateView):
    template_name = 'activate.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = StudentForm()
                return render(request, self.template_name, {'user': user, 'form': form})
            else:
                raise PermissionDenied('Activation link is invalid! Please SignUp Again or Contact Us')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('home')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("account:signup")

    def post(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = StudentForm(request.POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.user = user
                    temp.save()
                    user.is_active = True
                    user.save()
                    auth.login(request, user)
                    messages.success(request, 'Thank you for Registration')
                    return redirect("home")
                else:
                    messages.warning(request, 'Invalid Input')
                    return render(request, self.template_name, {'user': user, 'form': form})
            else:
                raise PermissionDenied('Activation link is invalid! Please SignUp Again or Contact Us')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('home')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("account:signup")


# noinspection PyBroadException
class ForgetPassword(TemplateView):
    template_name = 'reset-password.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if password_reset_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = ResetPasswordForm()
                return render(request, self.template_name, {'form': form})
            else:
                raise PermissionDenied('Invalid Password Reset link!')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('home')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("home")

    def post(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if password_reset_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Password Successfully Updated')
                    auth.login(request, user)
                    return redirect('home')
                messages.error(request, 'Invalid Password')
                return render(request, self.template_name, {'form': form})
            else:
                raise PermissionDenied('Invalid Password Reset link!')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('home')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("home")


# noinspection PyBroadException
# class ResetPassword(TemplateView):
#     template_name = 'reset-password.html'
#
#     def get(self, request, *args, **kwargs):
#         try:
#             user = User.objects.get(username=request.user)
#             if user.is_active:
#                 form = ResetPasswordForm()
#                 return render(request, self.template_name, {'form': form})
#         except Exception:
#             messages.error(request, 'User not Found')
#         return redirect('home')
#
#     def post(self, request):
#         try:
#             user = User.objects.get(username=request.user)
#             if user.is_active:
#                 form = ResetPasswordForm(request.POST)
#                 if form.is_valid():
#                     password = form.cleaned_data['password']
#                     user.set_password(password)
#                     user.save()
#                     messages.success(request, 'Password Updated')
#                     auth.login(request, user)
#                     return redirect('home')
#                 messages.error(request, 'Password Does not Match')
#                 return render(request, self.template_name, {'form': form})
#         except Exception:
#             messages.error(request, 'Invalid Link')
#         return redirect('home')

class ConsolidatedView(TemplateView):
    template_name = 'consolidated_view.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                if kwargs.get('c_o_e'):
                    event_list = EventRecord.objects.filter(c_o_e=kwargs['c_o_e']).order_by('-id')
                    print('aa')
                elif kwargs.get('username'):
                    user = User.objects.get(username=kwargs['username'])
                    event_list = EventRecord.objects.filter(user=user).order_by('-id')
                    print('bb')
                else:
                    event_list = EventRecord.objects.all().order_by('-id')
            elif request.user.is_staff:
                event_list = EventRecord.objects.filter(user=request.user).order_by('-id')
            else:
                student = StudentRecord.objects.get(user=request.user)
                event_list = RegistrationRecord.objects.filter(student=student)
            return render(request, self.template_name, {'event_list': event_list, 'now': date.today()})

        except ObjectDoesNotExist:
            messages.error(request, 'Record Not Found')
            return redirect('home')
        # except Exception as e:
        #     messages.error(request, (str(e) + '. Please Contact Us'))
        #     return redirect("home")


# noinspection PyBroadException
def superuser(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                form = SignupForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    User.objects.create_user(username=username.lower(), email=email.lower(), password=password,
                                             first_name=first_name, last_name=last_name, is_active=True, is_staff=True)
                    messages.success(request, 'User Created')
                else:
                    messages.error(request, 'Invalid Inputs')
            except Exception:
                messages.warning(request, 'User name and already exits')
        form = SignupForm()
        user = User.objects.filter(is_staff=True, is_superuser=False)
        return render(request, 'superuser.html', {'u': user, 'form': form})
    else:
        raise PermissionDenied


def edit_user(request, username):
    try:
        u = User.objects.get(username=username)
        if request.user.is_superuser:
            if request.method == "POST":
                form = EditUserForm(request.POST, instance=u)
                if form.is_valid():
                    u.first_name = form.cleaned_data['first_name']
                    u.last_name = form.cleaned_data['last_name']
                    u.email = form.cleaned_data['email']
                    new_password = form.cleaned_data['password']
                    u.set_password(new_password)
                    u.save(update_fields=['username', 'password', 'first_name', 'last_name', 'email'])
                    messages.success(request, 'Updated')
                else:
                    messages.info(request, 'Invalid Input')
            form = EditUserForm(instance=u)
            return render(request, 'edit_user.html', {'form': form})
        else:
            raise PermissionDenied
    except PermissionDenied:
        messages.error(request, 'Edit not allowed!!!')
    except ObjectDoesNotExist:
        messages.error(request, 'User does not exist !!!')
    return redirect('superuser')


def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        if not u.is_superuser and request.user.is_superuser:
            u.delete()
            messages.success(request, "The user is deleted")
        else:
            messages.warning(request, 'Invalid Response')
    except ObjectDoesNotExist:
        messages.error(request, "User does not exist")
        return render(request, 'superuser.html')
    except Exception as e:
        return render(request, 'superuser.html', {'err': e})
    return redirect('superuser')
