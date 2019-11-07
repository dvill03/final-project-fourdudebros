from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run', views.run, name='run'),
    path('reports', views.reports, name='reports'),
    path('analysis', views.analysis, name='analysis'),
    path('compare', views.compare, name='compare'),
    path('prepare', views.prepare, name='prepare'),
    path('setup', views.setup, name='setup'),
    path('help', views.help, name='help'),
    path('heatmap', views.heatmap, name='heatmap'),
]
