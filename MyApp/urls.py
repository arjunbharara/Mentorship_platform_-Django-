from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    		path('', views.index, name="index"),
			path("index.html", views.index	, name="index"),
			path('Login.html', views.Login, name="Login"), 
			path('StartupRegister.html', views.StartupRegister, name="StartupRegister"),
			path('LoginAction', views.LoginAction, name="LoginAction"),
			path('MentorRegister.html', views.MentorRegister, name="MentorRegister"), 	
			path('StartupRegisterAction', views.StartupRegisterAction, name="StartupRegisterAction"),
			path('MentorRegisterAction', views.MentorRegisterAction, name="MentorRegisterAction"),
			path('GroupForm.html', views.GroupForm, name="GroupForm"), 	
			path('FormGroup', views.FormGroup, name="FormGroup"),
			path('ViewQueries.html', views.ViewQueries, name="ViewQueries"), 	
			path('Suggestions', views.Suggestions, name="Suggestions"),
			path('SuggestionAction', views.SuggestionAction, name="SuggestionAction"),
			path('ViewMentorRatings.html', views.ViewMentorRatings, name="ViewMentorRatings"), 	
			path('Logout', views.Logout, name="Logout"), 
			path('ViewStartupGroup.html', views.ViewStartupGroup, name="ViewStartupGroup"), 	
			path('Subscribe', views.Subscribe, name="Subscribe"),
			path('PostQueries.html', views.PostQueries, name="PostQueries"), 
			path('PostQueriesAction', views.PostQueriesAction, name="PostQueriesAction"),
			path('ViewSuggestions.html', views.ViewSuggestions, name="ViewSuggestions"), 
			path('SuggestionView', views.SuggestionView, name="SuggestionView"),
			path('Rating', views.Rating, name="Rating"), 
			path('RatingAction', views.RatingAction, name="RatingAction"),
			path('ViewRatings.html', views.ViewRatings, name="ViewRatings"), 
			path('Filter',views.Filter, name="Filter"),
			path('ViewProfile', views.ViewProfile, name="ViewProfile"),
			path('ForgotPassword',views.ForgotPassword, name="ForgotPassword"),
			path('ForgotPasswordSubmit', views.ForgotPasswordSubmit, name="ForgotPasswordSubmit"),
			path('RequestMeeting',views.RequestMeeting, name="RequestMeeting")
]

urlpatterns += staticfiles_urlpatterns()