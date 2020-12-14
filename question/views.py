from django.shortcuts import redirect, render, HttpResponse,get_object_or_404
from django.views.generic import ListView, DetailView,CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.db import IntegrityError

from .models import Question, Choice, UserVote
from .forms import LoginForm,QuestionForm,ChoiceForm
#ShowQuestions, Signup, Login, Logout, QuestionDetail, Profile, QuestionList


class QuestionList(ListView):
    model = Question
    context_object_name = 'questions'
  
    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context['Qadd'] = QuestionForm()
        context['Cadd'] = ChoiceForm()
        return context

    def post(self,request,*args, **kwargs):
        Cform = ChoiceForm(request.POST)
        Qform = QuestionForm(request.POST)
        if Cform.is_valid():
            print(Cform.save())
        if Qform.is_valid():
            Qform.save()

        return redirect('home')




class QuestionDetail(DetailView):
    model = Question

    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['Cadd'] = ChoiceForm(initial={'question':kwargs.get('object')})
        return context

    def post(self,request,*args, **kwargs):
        Cform = ChoiceForm(request.POST)
        if Cform.is_valid():
            print(Cform.save())

        return redirect('home')



class Signup(View):
    def get(self, request, *args, **kwargs):
        
        return render(request,'signup.html',{'form':UserCreationForm()})

    def post(self, request, *args, **kwargs):
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)
            print(username)
            print(request.POST)
            if user:
                login(request, user)
                return redirect('home')
            return redirect('login')
        
        messages.add_message(request, messages.INFO, 'Issue With Sign Up \n double check ....')

        return redirect('signup')

class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Issue With Sign Up \n double check ....')
            return redirect('home')
        else:
            return render(request,'login.html',{'form':LoginForm()})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successful ')

                return redirect('home')
                
        return redirect('login')    


class Logout(View):
    def get(self,requset):
        try:
            logout(requset)
            print(f'Success you are - > {requset.user}')
        except:
            return redirect('login')
        return redirect('home')


class Profile(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET request!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

class Home(ListView):
    model = Question
    context_object_name = 'question'
    template_name='index.html'
    queryset = Question.objects.all().order_by('-date')[:5]

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['Qadd'] = QuestionForm()
        context['Cadd'] = ChoiceForm()
        return context

    def post(self,request,*args, **kwargs):
        Qform = QuestionForm(request.POST)
        Cform = ChoiceForm(request.POST)

        if Qform.is_valid():
            question = Qform.save()

        if Cform.is_valid():
            print(Cform.save())

        return redirect('home')
            

class SubmitVote(View):
    next_url='home'
    def get(self,requst,*args, **kwargs):
        if requst.user.is_authenticated:
            # print(kwargs.get('pk'))
            choice_to_vote =get_object_or_404(Choice,c_name = kwargs.get('choice_name'))
            try:
                UserVote.objects.create(user_id=requst.user,
                                    vote=choice_to_vote,
                                    question = choice_to_vote.question)
            except IntegrityError as e:
                messages.add_message(requst, messages.INFO, 'U voted once in this question X-X')
                
            # choice_to_vote.votes_count += 1
            # choice_to_vote.save()
        return redirect(SubmitVote.next_url)
        
