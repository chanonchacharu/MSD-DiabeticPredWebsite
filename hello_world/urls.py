from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from hello_world.core import views as core_views
from data_sci import views as data_sci_views

urlpatterns = [
    path("", core_views.homepage), # default landing page
    path("home", core_views.homepage, name ='homepage'), # for redirect in html file
    path("admin/", admin.site.urls), # interact with admin page
    path("__reload__/", include("django_browser_reload.urls")),
    path("load_diabetic_data", data_sci_views.import_diabetic_data_csv), # )NOT CALL) Call this API once to avoid duplicate data
    path("visualize_pima_diabetic_kaggle", data_sci_views.visualize_pima_diabetic_kaggle_data, name='kaggle_data'), # show pima india dataset in tabular format
    path('scatter_plot/', data_sci_views.scatter_plot_view, name='scatter-plot'), # plot data in scatter plot
    path('scatter_plot_data/', data_sci_views.scatter_plot_data, name='scatter-plot-data'), # get data for scatter plot
    path("personal_health_list", data_sci_views.personal_health_data_list, name='personal_health_list'), # display person health record
    path('dashboard_v2', data_sci_views.personal_dashboard_v2, name='dashboard_prediction'), # personal dashboard
    path("add", data_sci_views.personal_health_data_add, name='add_data'), # add health record
    path("data_sci/edit/<id>", data_sci_views.personal_health_data_edit), # edit health record
    path("data_sci/delete/<id>", data_sci_views.personal_health_data_delete), # delete health record
    # path("dashboard", data_sci_views.personal_dashboard),
    path('distribution_count', data_sci_views.diabetic_distribution_data), # statistic + distribution of non-diabetic and diabetic instances in the dataset
    path('result_pima_indian_data', data_sci_views.delete_all_pima_indian_diabetic_records), # factory reset Kaggle data loaded into the dataset
    path('ht_average_record', data_sci_views.health_tracker_data), # summary average personal record at homepage (0 if no record)
    path('api/register/', data_sci_views.api_register), # Regsiter new account
    path("api/login/", data_sci_views.api_login), # Login into existing account
    path("account", data_sci_views.account_page, name='account'), # show account page for login and signup for new account
    path('login/', data_sci_views.login_view, name='login'),  # Login using existing account - precess login form
    path('logout/', data_sci_views.logout_view, name='logout'), # Logout from the current signed in account
    path('chatbot',core_views.chatbot, name='chatbot'), # Direct to chatbot 
    path('api/predict_diabetes/', data_sci_views.diabetic_prediction_api, name='diabetic_prediction_api'),
    path('jokes/',core_views.geek_jokes_api),
]
