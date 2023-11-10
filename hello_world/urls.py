from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from hello_world.core import views as core_views
from data_sci import views as data_sci_views

urlpatterns = [
    path("", core_views.homepage),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("load_diabetic_data", data_sci_views.import_diabetic_data_csv), # Call this API once to avoid duplicate data
    path("visualize_pima_diabetic_kaggle", data_sci_views.visualize_pima_diabetic_kaggle_data),
    path("personal_health_list", data_sci_views.personal_health_data_list, name='personal_health_list'),
    path("add", data_sci_views.personal_health_data_add, name='add_data'),
    path("data_sci/edit/<id>", data_sci_views.personal_health_data_edit),
    path("data_sci/delete/<id>", data_sci_views.personal_health_data_delete),
    path("dashboard", data_sci_views.personal_dashboard),
    path('scatter_plot_data/', data_sci_views.scatter_plot_data, name='scatter-plot-data'),
    path('scatter_plot/', data_sci_views.scatter_plot_view, name='scatter-plot'),
    path('distribution_count', data_sci_views.diabetic_distribution_data),
    path('result_pima_indian_data', data_sci_views.delete_all_pima_indian_diabetic_records),
    path('ht_average_record', data_sci_views.health_tracker_data),
]
