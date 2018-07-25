import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify

from django.views import View
from rest_framework import status, mixins, generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashcodrf.forms import PersonalInfo, PasswordChange, NewUser, NewClient, NewStaff, NewBranch, BranchStaff, \
    NewRoutePlan

# Current logged user
from dashcodrf.models import Client, Branch, BranchUser, RoutePlan, RoutePlanLog, Account

# Random key
from dashcodrf.serializers import LoginSerializer, ClientSerializer, RoutePlanSerializer, RoutePlanLogSerializer


def random_code(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def session_user(request):
    return request.user


@method_decorator(login_required, name='get')
class Index(View):
    template_name = 'base.html'

    context = {'index_active': True}

    def get(self, request):
        return render(request, self.template_name, self.context)


# Staff
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class Users(View):
    template_name = 'users/users.html'

    context = {'users_active': True,
               'user_form': NewStaff()}

    def get(self, request):
        self.context['users'] = User.objects.filter(is_staff=True)
        return render(request, self.template_name, self.context)

    def post(self, request):
        user_form = NewStaff(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password('caritas123')
            user.is_staff = True
            user.is_active = True
            user.save()

            messages.success(request, 'User created successfully')
            return redirect('users')
        else:
            self.context['user_form'] = user_form
            messages.error(request, user_form.errors)
            return render(request, self.template_name, self.context)


# Branches
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class Branches(View):
    template_name = 'branch/branches.html'

    context = {'branches_active': True,
               'branch_form': NewBranch()}

    def get(self, request):
        self.context['branches'] = Branch.objects.all()
        return render(request, self.template_name, self.context)

    def post(self, request):
        branch_form = NewBranch(request.POST)
        if branch_form.is_valid():
            branch = branch_form.save(commit=False)
            branch.created_by = session_user(request)
            branch.slug = slugify(random_code(5))
            branch.save()

            messages.success(request, 'Branch created successfully')
            return redirect('branches')
        else:
            self.context['branch_form'] = branch_form
            messages.error(request, branch_form.errors)
            return render(request, self.template_name, self.context)


# Branch detail
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class BranchDetail(View):
    template_name = 'branch/detail.html'

    context = {'branches_active': True,
               'users': User.objects.filter(is_active=True, is_staff=True),
               'branch_staff_form': BranchStaff()}

    def get(self, request, *args, **kwargs):
        branch = get_object_or_404(Branch, slug=kwargs['slug'])
        self.context['branch'] = branch
        self.context['branch_users'] = BranchUser.objects.filter(branch=branch, status=True)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        branch = get_object_or_404(Branch, slug=kwargs['slug'])
        branch_form = BranchStaff(request.POST)
        if branch_form.is_valid():
            user = get_object_or_404(User, id=request.POST.get('branch_user'))
            user_exists = BranchUser.objects.filter(user=user, status=True)
            if user_exists.count() is 0:
                branch_user = BranchUser()
                branch_user.branch = branch
                branch_user.user = user
                branch_user.created_by = session_user(request)
                branch_user.slug = slugify(random_code(5))
                branch_user.save()
                messages.success(request, 'Staff assigned successfully.')
            else:
                messages.error(request, 'This user is already assigned to one of the branches.')
            return redirect('edit_branch', slug=branch.slug)
        else:
            self.context['branch_form'] = branch_form
            messages.error(request, branch_form.errors)
            return render(request, self.template_name, self.context)


# Branch member delete
@method_decorator(login_required, name='get')
class BranchMemberDelete(View):
    context = {'branches_active': True,
               'users': User.objects.filter(is_active=True, is_staff=True),
               'branch_staff_form': BranchStaff()}

    def get(self, request, *args, **kwargs):
        branch = get_object_or_404(Branch, slug=kwargs['slug'])

        user = get_object_or_404(User, id=kwargs['user'])
        print(branch)
        user_exists = BranchUser.objects.filter(user=user, status=True)
        if user_exists.count() > 0:
            branch_user = get_object_or_404(BranchUser, user=user, status=True)
            if branch_user.delete():
                messages.success(request, 'Staff deleted successfully.')
            else:
                messages.error(request, 'Staff not removed. Try again.')
        else:
            messages.error(request, 'This user is not assigned to this branch.')

        return redirect('edit_branch', branch.slug)


# Clients
@method_decorator(login_required, name='get')
class Clients(View):
    template_name = 'clients/clients.html'

    context = {'clients_active': True,
               'client_form': NewClient()}

    def get(self, request):
        self.context['clients'] = Client.objects.all()
        return render(request, self.template_name, self.context)

    def post(self, request):
        client_form = NewClient(request.POST)
        if client_form.is_valid():

            client = client_form.save(commit=False)
            client.created_by = session_user(request)
            client.slug = slugify(random_code(5))
            client.save()

            messages.success(request, 'Client created successfully')
            return redirect('client')
        else:
            self.context['client_form'] = client_form
            messages.error(request, client_form.errors)
            return render(request, self.template_name, self.context)


# Plans
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class RoutePlans(View):
    template_name = 'plans/plans.html'

    context = {'plans_active': True,
               'plan_form': NewRoutePlan()}

    def get(self, request):
        self.context['plans'] = RoutePlan.objects.filter(status=True)
        self.context['users'] = User.objects.filter(is_staff=True, is_active=True)
        return render(request, self.template_name, self.context)

    def post(self, request):
        plan_form = NewRoutePlan(request.POST)
        if plan_form.is_valid():

            user = get_object_or_404(User, id=request.POST.get('plan_user'))

            plan = plan_form.save(commit=False)
            plan.user = user
            plan.created_by = session_user(request)
            plan_form.slug = slugify(random_code(5))
            plan.save()

            messages.success(request, 'Route plan created successfully')
            return redirect('plans')
        else:
            self.context['plan_form'] = plan_form
            messages.error(request, plan_form.errors)
            return render(request, self.template_name, self.context)


# Settings
# 1. Render
# 2. Update info
# 3. Update password
# 4. Delete account
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class Settings(View):
    template_name = 'settings/settings.html'

    context = {
        'settings_active': True
    }

    def get(self, request):
        self.context['password_form'] = PasswordChange(instance=session_user(request))
        self.context['personal_form'] = PersonalInfo(instance=session_user(request))
        return render(request, self.template_name, self.context)

    # Update personal info
    def post(self, request):
        personal_form = PersonalInfo(request.POST, instance=session_user(request))
        if personal_form.is_valid():
            personal_form.save()
            messages.success(request, 'Personal information updated')
            return redirect('settings')
        else:
            self.context['personal_form'] = personal_form
            messages.error(request, personal_form.errors)
            return render(request, self.template_name, self.context)


# REST-API
# From here write the REST-API Functions
class ApiLogin(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiClientList(APIView):
    """
    List all client, or create a new client.
    """

    def get(self, request, format=None):
        snippets = Client.objects.all()
        serializer = ClientSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['slug'] = slugify(random_code(5))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class ApiClientSearch(APIView):
    """
    List all client, or create a new client.
    """

    def get(self, request, format=None):
        q = request.GET.get('search_text')
        clients = Client.objects.filter(phone_number=q)
        serializer = ClientSerializer(clients, many=True)

        return Response(serializer.data)


class ApiRoutePlans(APIView):
    """
    List all route plans
    """

    def get(self, request):
        route_plans = RoutePlan.objects.filter(status=True)
        serializer = RoutePlanSerializer(route_plans, many=True)

        return Response(serializer.data)


class ApiUserRoutePlans(APIView):
    """
    List all route plans
    """

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['user'])
        route_plans = RoutePlan.objects.filter(status=True, user=user.id)
        serializer = RoutePlanSerializer(route_plans, many=True)

        return Response(serializer.data)


class ApiPlanDetail(APIView):
    """
    Retrieve, update or delete a plan instance.
    """

    def get_object(self, slug):
        try:
            return RoutePlan.objects.get(slug=slug)
        except RoutePlan.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        plan = self.get_object(slug)
        plan.status = False
        plan.save()

        route_plans = RoutePlan.objects.filter(status=True, user=plan.user)
        serializer = RoutePlanSerializer(route_plans, many=True)
        return Response(serializer.data)


class ApiUserRoutePlanLog(APIView):
    """
    List all route plans
    """

    def post(self, request, format=None):
        # serializer = RoutePlanLogSerializer(data=request.data)

        print("Started")
        new_log = RoutePlanLog()

        client = get_object_or_404(Client, slug=request.data['client'])
        print(client)

        user = get_object_or_404(User, username=request.data['user'])
        print(user)

        branch_selected = get_object_or_404(Branch, name=request.data['branch'])
        print(branch_selected)

        branch_user = get_object_or_404(BranchUser, user=user.id)
        print(branch_user.branch)

        if request.data['action'] == "Account":
            new_log.branch = branch_selected
            account = Account()
            account.branch = branch_selected
            account.client = client
            account.account_number = random_code(10)
            account.slug = slugify(random_code(5))
            account.created_by = user
            account.save()
        else:
            new_log.branch = branch_user.branch

        new_log.client = client
        new_log.location_lat = request.data['location_lat']
        new_log.location_lon = request.data['location_lon']
        new_log.user = branch_user.user
        new_log.action = request.data['action']
        new_log.summary = request.data['summary']
        new_log.slug = slugify(random_code(5))
        new_log.save()
        log_new = get_object_or_404(RoutePlanLog, id=new_log.id)
        return Response(request.data, status=status.HTTP_201_CREATED)


# Reports
@method_decorator(login_required, name='get')
class Reports(View):
    template_name = 'reports/reports.html'

    context = {'reports_active': True}

    def get(self, request):
        self.context['logs'] = RoutePlanLog.objects.all()
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='get')
class ReportsJSON(View):

    def get(self, request):
        logs = RoutePlanLog.objects.all()
        data = serializers.serialize('json', logs)
        return HttpResponse(data, content_type="application/json")


class BranchesJSON(View):

    def get(self, request):
        branch = Branch.objects.filter(status=True)
        data = serializers.serialize('json', branch)
        return HttpResponse(data, content_type="application/json")


@method_decorator(login_required, name='get')
class Accounts(View):
    template_name = 'accounts/accounts.html'

    context = {'accounts_active': True}

    def get(self, request):
        self.context['accounts'] = Account.objects.all()
        return render(request, self.template_name, self.context)
