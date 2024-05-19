from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login, name='login'),
    path('inscrire/', views.inscrire, name='inscrire'),
    path('index/', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('index3/', views.index3, name='index3'),
    path('enquetes/', views.enquetes, name='enquetes'),    
    path('personne/', views.personne, name='personne'),
    path('ist/', views.ist, name='ist'),
    path('pratiques/', views.pratiques, name='pratiques'),   
    path('grossesse/', views.grossesse, name='grossesse'), 
    path('violence/', views.violence, name='violence'),
    path('sr/', views.sr, name='sr'),  
    path('general/', views.general, name='general'),
    path('facteur/', views.facteur, name='facteur'),
    path('prenatal_maternel/', views.prenatal_maternel, name='prenatal_maternel'),  
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('enquete_soumis/', views.enquete_soumis, name='enquete_soumis'),
    path('reset_password/', views.reset_password, name='reset_password'),
   
    #------------------------------------------------------------------------------------------------------------------------#

    path('projects/', views.projects, name='projects'),
    path('project_detail/', views.project_detail, name='project_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('profile/', views.profile, name='profile'),
    path('page_403/', views.page_403, name='page_403'),
    path('page_404/', views.page_404, name='page_404'),
    path('page_500/', views.page_500, name='page_500'),
    path('plain_page/', views.plain_page, name='plain_page'),
    path('pricing_tables/', views.pricing_tables, name='pricing_tables'),
    path('compte_active/', views.compte_active, name='compte_active'),
    path('compte_desactive/', views.compte_desactive, name='compte_desactive'),
    path('activer_compte/<str:cin>/', views.activer_compte, name='activer_compte'),
    path('desactiver_compte/<str:cin>/', views.desactiver_compte, name='desactiver_compte'),
    path('form_validation/', views.form_validation, name='form_validation'),
    path('form_wizard/', views.form_wizard, name='form_wizard'),
    path('form_upload/', views.form_upload, name='form_upload'),
    path('form_buttons/', views.form_buttons, name='form_buttons'),
    path('general_elements/', views.general_elements, name='general_elements'),
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




    
    path('personnes/', views.personne, name='personne'),
    path('Sr/', views.sr, name='sr'),
    path('IST/', views.ist, name='ist'),
    path('PrenatalMaternel/', views.prenatal_maternel, name='prenatal_maternel'),
    path('Violence/', views.violence, name='violence'),
    path('Grossesse/', views.grossesse, name='grossesse'),
    path('Pratique/', views.pratiques, name='pratiques'),
    path('Facteur/', views.facteur, name='facteur'),
    
]
