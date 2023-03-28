from django.urls import path
from . import views


urlpatterns=[path('',views.home, name='home'),
            path('register',views.register, name='register'),
            path('main',views.home, name='home'),
            path('rooms',views.rooms, name='rooms'),
            path('restaurant',views.restaurant, name='restaurant'),
            path('about',views.about, name='about'),
            path('contact',views.contact, name='contact'),
            path('booking/<int:pk>',views.booking, name='booking'),
            path('room_available/<str:type>',views.room_available, name='room_available'),
            path('user',views.user, name='user'),
            path('logout',views.log_out, name='logout'),
            path('bookings',views.booking_history, name='bookings'),
            path('profile',views.create_profile, name='profile'),  
               
        
]

