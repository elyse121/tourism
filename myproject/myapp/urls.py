from django.urls import path
from . import views

urlpatterns = [
          path('hy/', views.hy, name='hy'),

      path('login/', views.login_view, name='login'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),

     path('hotels/', views.hotels_view, name='hotels'),
    path('transports/', views.transports_view, name='transports'),
    path('parks/', views.parks_view, name='parks'),
       
        path('logout/', views.logout_view, name='logout'),

        path('get-managers/', views.get_managers, name='get_managers'),

        path('login/', views.login_view, name='login'),

    
        path('get_booking_details/<int:booking_id>/', views.get_booking_details, name='get_booking_details'),

        path('get-park-details/<int:park_id>/', views.get_park_details, name='get_park_details'),

        path('park/', views.park, name='park'),

        path('dashboard/', views.dashboard, name='dashboard'),

        path('fetch-deals/', views.fetch_deals, name='fetch_deal'),

     path('fetch_places/<int:location_id>/', views.fetch_places, name='fetch_places'),
    path('fetch_hotels/<int:place_id>/', views.fetch_hotels, name='fetch_hotels'),
    path('deals/', views.fetch_deals, name='fetch_deals'),
    path('more/<int:park_id>/', views.more, name='more'),
    path('hello/', views.hello, name='hello'),

    path('fetch_deals/', views.fetch_deals, name='fetch_deals'),
        path('fetch/', views.fetch, name='fetch'),
        path('fetch_places/<int:location_id>/', views.fetch_places, name='fetch_places'),
path('fetch_hotels/<int:place_id>/', views.fetch_hotels, name='fetch_hotels'),
  path('fetch_deals/', views.fetch_deals, name='fetch_deals'),
    path('fetch-deals/', views.fetch_deals_view, name='fetch_deals_view'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/<int:location_id>/', views.places_in_location, name='places_in_location'),
    path('places/<int:place_id>/hotels/', views.hotels_near_place, name='hotels_near_place'),
    # Existing URLs
        


    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
      path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
     path('approve_booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
  # Add path for the booking page


    path('about/', views.about, name='about'),
    path('deals/', views.deals, name='deals'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
        path('register/', views.register, name='register'),

    path('submit-deal/', views.submit_deal, name='submit_deal'),
        path('register-manager/', views.register_manager, name='register_manager'),
         path('locations/', views.location_list, name='location_list'),
    path('locations/<int:location_id>/', views.places_in_location, name='places_in_location'),
    path('places/<int:place_id>/hotels/', views.hotels_near_place, name='hotels_near_place'),
    # Existing URLs

]
