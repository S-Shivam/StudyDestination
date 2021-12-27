from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
import logging
from .models import Country, University
from .forms import CountryForm, UniversityForm, UserForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'study/user_login.html')
    else:
        return render(request, 'study/index.html',
                      {'countries': Country.objects.filter(user=request.user), 'user': request.user})


class indexClass(View):
    model = Country


def delete_country(request, country_id):
    c = get_object_or_404(Country, pk=country_id)
    c.delete()
    return render(request, 'study/index.html',
                  {'countries': Country.objects.filter(user=request.user), 'user': request.user})


def delete_univ(request, university_id):
    u = get_object_or_404(University, pk=university_id)
    u.delete()
    return render(request, 'study/all_university.html', {'university': University.objects.all()})


def search(request):
    q = request.GET.get('query')
    if q:
        country = Country.objects.all()
        univs = University.objects.all()
        country_searched = country.filter(name__icontains=q)
        univ_searched = univs.filter(university_name__icontains=q)
        if not country_searched:
            if not univ_searched:
                context = {
                    'error_message': 'No such Country and University found'
                }
                return render(request, 'study/search.html', context)
            else:
                context = {
                    'univs': univ_searched,
                    'error_message': 'No such Country found'
                }
                return render(request, 'study/search.html', context)
        elif not univ_searched:
            context = {
                'countries': country_searched,
                'error_message': 'No such University found'
            }
            return render(request, 'study/search.html', context)

        return render(request, 'study/search.html', {'univs': univ_searched, 'countries': country_searched})
    else:
        return render(request, 'study/index.html',
                      {'countries': Country.objects.filter(user=request.user), 'user': request.user})


def detail(request, country_id):
    if not request.user.is_authenticated:
        return render(request, 'study/user_login.html')
    else:
        c = get_object_or_404(Country, pk=country_id)
        univs = c.university_set.all().order_by('rank')
        return render(request, 'study/detail.html', {'univs': univs, 'country': c})


def favorite(request, country_id):
    c = get_object_or_404(Country, pk=country_id)
    univs = c.university_set.all().order_by('rank')
    try:
        univ_selected = c.university_set.get(pk=request.POST['university'])
    except (KeyError, University.DoesNotExist):
        return render(request, 'study/detail.html', {
            'univs': c.university_set.all(),
            'country': c,
            'error_message': 'No University selected'
        })
    else:
        univ_selected.favorite = True
        univ_selected.save()
        return render(request, 'study/detail.html', {'univs': univs, 'country': c})


def add_country(request):
    if not request.user.is_authenticated:
        return render(request, 'study/user_login.html')
    else:
        form = CountryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            country = Country.objects.all()
            for c in country:
                if c.name == form.cleaned_data.get('name'):
                    context = {'form': form, 'error_message': 'Country already present'}
                    return render(request, 'study/add-country.html', context)

            c = form.save(commit=False)
            c.user = request.user
            c.save()
            return render(request, 'study/detail.html', {'univs': c.university_set.all().order_by('rank'), 'country': c})
        return render(request, 'study/add-country.html', {'form': form})


def edit_country(request, country_id):
    country_edited = get_object_or_404(Country, id=country_id)
    form = CountryForm(request.POST or None, request.FILES or None, instance=country_edited)
    if request.method == 'POST':
        if form.is_valid():
            c = form.save()
            u = c.university_set.all().order_by('rank')
            return render(request, 'study/detail.html', {'univs': u, 'country': c})

    return render(request, 'study/add-country.html', {'form': form})


def add_university(request, country_id):
    form = UniversityForm(request.POST or None, request.FILES or None)
    country = get_object_or_404(Country, pk=country_id)
    if form.is_valid():
        all_univs = country.university_set.all()
        for univ in all_univs:
            if univ.university_name == form.cleaned_data.get('university_name'):
                context = {
                    'form': form,
                    'error_message': 'University already present',
                    'country': country
                }
                return render(request, 'study/add-university.html', context)

        u = form.save(commit=False)
        u.country = country
        u.save()
        return render(request, 'study/univ_details.html', {'univs': u})
    return render(request, 'study/add-university.html', {'form': form, 'country': country})


def univ_details(request, university_id):
    if not request.user.is_authenticated:
        return render(request, 'study/user_login.html')
    else:
        univs = get_object_or_404(University, pk=university_id)
        return render(request, 'study/univ_details.html', {'univs': univs})


def all_university(request):
    if not request.user.is_authenticated:
        return render(request, 'study/user_login.html')
    else:
        return render(request, 'study/all_university.html', {'university': University.objects.all()})


def shortlists(request):
    return render(request, 'study/shortlists.html', {'university': University.objects.all()})


def edit_university(request, university_id):
    university_edited = University.objects.get(id=university_id)
    form = UniversityForm(request.POST or None, request.FILES or None, instance=university_edited)
    country = get_object_or_404(Country, pk=university_edited.country.id)
    if request.method == 'POST':
        if form.is_valid():
            u = form.save(commit=False)
            u.country = country
            u.save()
            return render(request, 'study/univ_details.html', {'univs': u})
    return render(request, 'study/add-university.html', {'form': form, 'country': country})


def register(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            u = form.save(commit=False)
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            u.set_password(pwd)
            u.save()
            user = authenticate(username=uname, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'study/index.html',
                                  {'countries': Country.objects.filter(user=user), 'user': user})

    return render(request, 'study/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=uname, password=pwd)

        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'study/index.html',
                              {'countries': Country.objects.filter(user=user), 'user': user})
            else:
                return render(request, 'study/user_login.html', {'error_message': 'User is de-activated'})
        else:
            return render(request, 'study/user_login.html', {'error_message': 'Invalid login'})
    return render(request, 'study/user_login.html')


def user_logout(request):
    logout(request)
    return render(request, 'study/user_login.html')


def test1(request):
    return render(request, 'study/test.html')


############################
# BELOW ARE THE CLASS BASED VIEWS
#############################

class CountryList(generic.ListView):
    template_name = 'study/index.html'
    context_object_name = 'countries'

    def get_queryset(self):
        return Country.objects.all()


class CountryDetail(generic.DetailView):
    model = Country
    template_name = 'study/detail.html'


class CountryCreate(generic.CreateView):
    model = Country
    fields = ['name', 'language', 'currency', 'country_pic']


class CountryEdit(generic.UpdateView):
    model = Country
    fields = ['name', 'language', 'currency', 'country_pic']
    success_url = 'study:detail'


class CountryDelete(generic.DeleteView):
    model = Country
    success_url = 'study:index'

