from django.urls import path
from .views import Home, Signup, Login, Logout, QuestionDetail, Profile, QuestionList, SubmitVote


class QuestionListSubmitVote(SubmitVote):
    next_url = 'qusetion/list/'
# class QuestionDetailSubmitVote(SubmitVote):
#     next_url = 'question/'


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('singup/', Signup.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),
    path('<int:id>', SubmitVote.as_view(), name='submit-vote'),
    path('question/<int:pk>', QuestionDetail.as_view(), name='question-detail'),
    # path('question/<int:id>',
    #      SubmitVote.as_view(), name='question-detail-submit'),
    path('qusetion/list/', QuestionList.as_view(), name='question-list'),
    path('qusetion/list/<int:id>',
         QuestionListSubmitVote.as_view(), name='question-list-submit'),
    path('profile/', Profile.as_view(), name='profile'),
]
