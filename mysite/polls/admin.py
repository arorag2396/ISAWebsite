from django.contrib.admin import widgets
from django.contrib import admin

from .models import Choice, Question, Person, totalNumberOfVotes


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


def findWinner(modeladmin, request, queryset):
    for obj in queryset:
        obj.findWinner()
        obj.save()


findWinner.short_description = "Find out Winners"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'winner', )
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    actions = [findWinner]



def makeTrueForVote(modeladmin, request, queryset):
    for obj in queryset:
        obj.sendEmail()
        obj.save()

makeTrueForVote.short_description = "Send Email To All"

class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'currentCondition']
    ordering = ['name']
    actions = [makeTrueForVote]




    

admin.site.register(Question, QuestionAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(totalNumberOfVotes)