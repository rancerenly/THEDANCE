import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from main.forms import SignUpForm, PayForm
from .models import Payment, TeacherProfile, Schedule, Style


def profile(request):
    try:
        if request.user.profile is not None:
            print('user-client')
            is_client = True
            styles = request.user.profile.style_set.all()
    except:
        print('user-teacher')
        is_client = False
        styles = request.user.teacher_profile.style_set.all()
    return render(request, 'main/profile.html', {'styles': styles,
                                                 'is_client': is_client})


def timetable(request):
    schedules = Schedule.objects.all()

    def get_weekday():
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        day_number = datetime.date.today().weekday()
        return days[day_number]

    today = get_weekday()
    return render(request, 'main/timetable.html', {'schedules': schedules,
                                                   'today': today})


def index(request):
    teachers = TeacherProfile.objects.all()
    return render(request, 'main/index.html', {'teachers': teachers})


def pay_for_style(request):
    template = "main/pay.html"

    def calculate_payment(style, count_of_lessons):
        return style.price * count_of_lessons

    def dif_cost(user_cost, total_payment):
        return total_payment - user_cost

    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            cost = Decimal(form.cleaned_data['cost'])
            sum_payment = calculate_payment(form.cleaned_data['lessons'],
                                            form.cleaned_data['count_of_lessons'])
            if cost < sum_payment:
                dif_cost = dif_cost(cost, sum_payment)
                return render(request, template, {
                    'form': form,
                    'error_message': f'Введенный платеж меньше положенного платежа на {dif_cost}\n'
                                     f'Необходимо заплатить {sum_payment}'
                })
            elif cost > sum_payment:
                dif_cost = dif_cost(sum_payment, cost)
                return render(request, template, {
                    'form': form,
                    'error_message': f'Введенный платеж больше положенного платежа на {dif_cost}\n'
                                     f'Необходимо заплатить {sum_payment}'})
            else:
                pay = Payment(client=request.user,
                              cost=sum_payment,
                              payment_date=datetime.date.today())
                pay.save()

            return HttpResponseRedirect('profile')
    else:
        form = PayForm()

    return render(request, template, {'form': form})


def signup(request):
    # if this is a POST request we need to process the form data
    template = 'main/register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Юзернейм уже существует!.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Пароли не совпадают.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                )
                user.set_password(form.cleaned_data['password'])
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone']
                user.profile.passport = form.cleaned_data['passport']
                user.save()

                # Login the user
                login(request, user)

                # redirect to accounts page:
                return HttpResponseRedirect('home')

    # No post data availabe, let's just show the page.
    else:
        form = SignUpForm()

    return render(request, template, {'form': form})


def home(request):
    print(request.COOKIES)
    print(request.user)
    return render(request, 'main/index.html', dict(user=request.user))


"""

REQUEST                    -> REQUEST-> REQUEST.user -> REQUEST      ->               -> del REQUEST

пользователь послал запрос -> (сервер -> MIDDLEWARE    -> бизнес логика -> MIDDLEWARE -> ответ)
        БРАУЗЕР                ПРИЛОЖЕНИЕ

middleware = [AuthMiddleware]


"""


class IndexFromView(TemplateView):
    template_name = 'main/index.html'


class CustomLoginView(LoginView):
    template_name = 'main/login.html'


class CustomLoginOutView(LogoutView):
    pass
