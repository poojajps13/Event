from django.contrib import admin
from django.urls import path, include
from events.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from account.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('superuser/',login_required(superuser),name='superuser'),
    path('superuserlogin/',login_required(add_user),name='add_user'),
    path('form/', add_event, name='form'),
    path('logout/', login_required(logout), name='logout'),
    path('login', Login.as_view(), name='login'),
    path('edit_user/<username>',login_required(edit_user),name='edit_user'),
    path('consolidated/<username>',login_required(consolidated),name='consolidated'),
    path('consolidatedview/',login_required(consolidatedview),name='consolidatedview'),
    path('deleteuser/<username>',login_required(del_user),name='deleteuser'),
    path('excellence_center/',excellence_center,name='excellence_center'),
    path('seminar/', seminar, name='seminar'),
    path('workshop/', workshop, name='workshop'),
    path('training/', training, name='training'),
    path('competition/', competition, name='competition'),
    path('guest_lecture/', guest_lecture, name='guest_lecture'),
    path('delete/workshop/<slug>',login_required(delete_workshop),name='delete_workshop'),
    path('delete/seminar/<slug>',login_required(delete_seminar),name='delete_seminar'),
    path('delete/training/<slug>',login_required(delete_training),name='delete_training'),
    path('delete/competition/<slug>',login_required(delete_competition),name='delete_competition'),
    path('delete/guest_lecture/<slug>',login_required(delete_guestlecture),name='delete_guestlecture'),
    path('update/workshop/<slug>',login_required(update_workshop),name='update_workshop'),
    path('update/seminar/<slug>',login_required(update_seminar),name='update_seminar'),
    path('update/training/<slug>',login_required(update_training),name='update_training'),
    path('update/competition/<slug>',login_required(update_competition),name='update_competition'),
    path('update/guest_lecture/<slug>',login_required(update_guestlecture),name='update_guestlecture'),
    path('registration/', include(('registration.urls', 'registration'), namespace='registration')),
    path('guest_lecture/registration/<slug>',guest_lecture_registration,name='guest_lecture_registration'),
    path('workshop/description/<slug>',workshop_description,name='workshop_description_with_slug'),
    path('seminar/description/<slug>',seminar_description,name='seminar_description_with_slug'),
    path('training/description/<slug>',training_description,name='training_description_with_slug'),
    path('competition/description/<slug>',competition_description,name='competition_description_with_slug'),
    path('guest_lecture/description/<slug>',guest_lecture_description,name='guest_lecture_description_with_slug'),
    path('workshop/<int:year>/<month>', workshop_search, name='workshop_search'),
    path('seminar/<int:year>/<month>', seminar_search, name='seminar_search'),
    path('training/<int:year>/<month>', training_search, name='training_search'),
    path('competition/<int:year>/<month>', competition_search, name='competition_search'),
    path('guest_lecture/<int:year>/<month>', guest_lecture_search, name='guest_lecture_search'),
    path('Centre_of_Excellence_for_Structural_Design_and_Analysis/',structural_design,name='structural_design'),
    path('Cisco_Networking_Academy/',cisco_networking_academy,name='cisco_networking_academy'),
    path('Texas_Instruments_Embedded_System_Lab/',texas,name='texas'),
    path('Centre_of_Excellence_for_SMC_India_PvtLtd./',smc_india,name='smc_india'),
    path('Industrial_Automation_Research_&_Training_Centre_(IARTC)/',automation_research,name='automation_research'),
    path('Centre_of_Excellence_VLSI_Design/',vlsi_design,name='vlsi_design'),
    path('Center_of_Excellence_for_Big_Data_Analytics/',big_data,name='big_data'),
    path('ABES_NI_Innovation_Centre/',innovation_centre,name='innovation_centre'),
    path('Centre_of_Excellence_for_Mobile_Application_Development/',mobile_application,name='mobile_application'),
    path('Center_for_Enterprise_Software_Development/',software_development,name='software_development'),
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)