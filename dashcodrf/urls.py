from django.urls import path

from dashcodrf.views import Index, Settings, Clients, Users, Branches, BranchDetail, BranchMemberDelete, ApiLogin, \
    ApiClientList, ApiClientSearch, ApiRoutePlans, RoutePlans, ApiUserRoutePlans, ApiPlanDetail, ApiUserRoutePlanLog, \
    Reports, ReportsJSON, BranchesJSON, Accounts

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('clients/', Clients.as_view(), name='client'),
    path('settings/', Settings.as_view(), name='settings'),
    path('users/', Users.as_view(), name='users'),
    path('branches/', Branches.as_view(), name='branches'),
    path('branches/<slug>', BranchDetail.as_view(), name='edit_branch'),
    path('branches/<slug>/delete/<user>/', BranchMemberDelete.as_view(), name='delete_branch_staff'),
    path('route-plans/', RoutePlans.as_view(), name='plans'),
    path('reports/', Reports.as_view(), name='reports'),
    path('reports/json/', ReportsJSON.as_view(), name='reports_json'),
    path('clients/accounts/', Accounts.as_view(), name='clients_accounts'),

    # REST-API
    path('api-v1/login/', ApiLogin.as_view(), name='api_login'),
    path('api-v1/clients/', ApiClientList.as_view(), name='api_clients'),
    path('api-v1/clients/search/', ApiClientSearch.as_view(), name='api_client_search'),
    path('api-v1/route/plans/', ApiRoutePlans.as_view(), name='api_route_plans'),
    path('api-v1/route/<user>/plans/', ApiUserRoutePlans.as_view(), name='api_route_user_plans'),
    path('api-v1/route/plans/<slug>/', ApiPlanDetail.as_view(), name='api_route_plan_clear'),
    path('api-v1/facility/', ApiUserRoutePlanLog.as_view(), name='api_plan_log'),
    path('api-v1/branches/', BranchesJSON.as_view(), name='api_branches'),
]
