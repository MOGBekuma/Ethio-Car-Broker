from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login, authenticate

from vehicle.forms import CarForm, ProfileForm
from vehicle.models import Car, ContactMessage
from vehicle.utils import login_or_register

# Home page
@login_or_register
def index(request, context):
    return render(request, "index.html", context)

@login_or_register
def contact_us(request, context):
   if request.method == "POST":
      # data from the form 
      # ***********************************
      name = request.POST.get('name')
      phone = request.POST.get('subject')
      email = request.POST.get('email')
      message = request.POST.get('message')
   # ***********************************
      contact = ContactMessage()
      print("######################################")
      print(contact)
      contact.name = name
      contact.email = email
      contact.phone = phone
      contact.msg = message
      contact.save()
      print(contact)

   return render(request, "contact_us.html", context)

@login_or_register
def CarList(request, context):
    car_list = Car.objects.all()

    if request.user.is_authenticated and request.user.userprofile.type == 'dealer':
        car_list = car_list.filter(owner=request.user)

    page = request.GET.get('page', 1)
    paginator = Paginator(car_list, 20)

    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        # if page has an invalid value default to page 1
        cars = paginator.page(1)
    except EmptyPage:
        # if this page is empty default to page 1
        cars = paginator.page(1)

    context['cars'] = cars

    return render(request, "vehicle/car_list.html", context)

@login_or_register
def CarDetails(request, context, *args, **kwargs):
    id = kwargs['id']
    car = Car.objects.get(id=id)
    context['car'] = car
    return render(request, "vehicle/car_details.html", context)

@method_decorator(login_required, name='dispatch')
class CreateCar(CreateView):
    model = Car
    fields = [
        'vehicleId',
        'make',
        'shortModel',
        'longModel',
        'trim',
        'derivative',
        'yearIntroduced',
        'yearDiscontinued',
        'currentlyAvailable',
        'model_pic'
    ]

    success_url = reverse_lazy('car_list')

    def get(self, request):
        if request.user.userprofile.type == 'client':
            return HttpResponseRedirect(reverse_lazy('car_list'))
        return super().get(request)

    def get_form_class(self):
        return CarForm

    def form_valid(self, form):
        car = form.save(False)
        car.owner = self.request.user
        car.save()
        return HttpResponseRedirect(self.success_url)

@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('profile'))
    else:
        form = ProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

@login_required
def logout(request):
    return render(request, "accounts/logout.html")
