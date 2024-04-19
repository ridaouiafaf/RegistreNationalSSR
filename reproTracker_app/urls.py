from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('index3/', views.index3, name='index3'),
    path('enquete/', views.enquetes, name='enquetes'),  
    path('personne/', views.personne, name='personne'),

    #------------------------------------------------------------------------------------------------------------------------#

    path('projects/', views.projects, name='projects'),
    path('project_detail/', views.project_detail, name='project_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('profile/', views.profile, name='profile'),
    path('page_403/', views.page_403, name='page_403'),
    path('page_404/', views.page_404, name='page_404'),
    path('page_500/', views.page_500, name='page_500'),
    path('plain_page/', views.plain_page, name='plain_page'),
    path('login/', views.login_page, name='login'),
    path('pricing_tables/', views.pricing_tables, name='pricing_tables'),
    path('form/', views.form, name='form'),
    path('advanced_components/', views.advanced_components, name='advanced_components'),
    path('form_validation/', views.form_validation, name='form_validation'),
    path('form_wizard/', views.form_wizard, name='form_wizard'),
    path('form_upload/', views.form_upload, name='form_upload'),
    path('form_buttons/', views.form_buttons, name='form_buttons'),
    path('media_gallery/', views.media_gallery, name='media_gallery'),
    path('typography/', views.typography, name='typography'),
    path('icons/', views.icons, name='icons'),
    path('glyphicons/', views.glyphicons, name='glyphicons'),
    path('widgets/', views.widgets, name='widgets'),
    path('invoice/', views.invoice, name='invoice'),
    path('inbox/', views.inbox, name='inbox'),
    path('calendar/', views.calendar, name='calendar'),
    path('tables/', views.tables, name='tables'),
    path('tables_dynamic/', views.tables_dynamic, name='tables_dynamic'),
    path('chartjs/', views.chartjs, name='chartjs'),
    path('chartjs2/', views.chartjs2, name='chartjs2'),
    path('morisjs/', views.morisjs, name='morisjs'),
    path('echarts/', views.echarts, name='echarts'),
    path('other_charts/', views.other_charts, name='other_charts'),
    path('fixed_sidebar/', views.fixed_sidebar, name='fixed_sidebar'),
    path('fixed_footer/', views.fixed_footer, name='fixed_footer'),
]