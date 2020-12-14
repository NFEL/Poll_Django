from django.contrib import admin
from .models import UserVote,Question,Choice

class QuestionChoice(admin.TabularInline):
    model = Choice

class UserVotesTab(admin.TabularInline):
    model = UserVote

class QuestionInline(admin.ModelAdmin):
    inlines = [QuestionChoice]

class ChoiceInline(admin.ModelAdmin):
    inlines = [UserVotesTab]

admin.site.register(Question,QuestionInline)
admin.site.register(Choice,ChoiceInline)
