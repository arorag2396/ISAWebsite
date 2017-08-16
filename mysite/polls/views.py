from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponse
from django.template import loader
# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Choice, Question, Person, totalNumberOfVotes
from django.core.mail import EmailMessage
from django.contrib.admin.views.decorators import staff_member_required
import datetime


from django.utils import timezone

class IndexView(generic.ListView):
	def get(self,request):
            now = datetime.datetime.now()
            electionEndDate = datetime.datetime(2017,7,31,16,0)
            if now > electionEndDate:
                return render(request, 'polls/results.html', {'text': "Sorry Time is up! Better luck next time!!"})
            a = request.GET.get('id')
            allObjects = Person.objects.all()
            for per in allObjects:
                if per.uniqueCode == a:
                    if(per.voted ==True):
                        return render(request , 'polls/results.html' , {'text' : "You have already voted"})
                    return render(request,'polls/index.html',{
                        'voter' : per,
                        'latest_question_list' : Question.objects.all()
                    })
            return render(request , 'polls/results.html' , {'text' : "This seems odd, the link is broken."})



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'




def vote(request,voter_id):
    person = Person.objects.get(uniqueCode=voter_id)
    if person.voted == True:
        return render(request , 'polls/results.html' , {'text' : "You have already voted"})
    else:
        for question in Question.objects.all():
            try:
                selected_choice = question.choice_set.get(pk=request.POST['choice' + str(question.id)])
            except (KeyError, Choice.DoesNotExist):
                return render(request, 'polls/index.html', {
					'voter' : person,
					'latest_question_list' : Question.objects.all()
				})
            else:
                selected_choice.votes += 1
                selected_choice.save()
				# Always return an HttpResponseRedirect after successfully dealing
				# with POST data. This prevents data from being posted twice if a
				# user hits the Back button.
                #
        person.votingCompleted()
        person.save()
        tempT = totalNumberOfVotes.objects.all()[0]
        tempT.number+=1
        tempT.save()
        email = EmailMessage(
		    'ISA-Elections',
		    'We have got your response,\n Thanks for voting!',
		    'isa.uofs@gmail.com',
		    [person.email],
		)
        email.send()
        return render(request , 'polls/results.html' , {'text' : "Thanks for voting in ISA Elections 2016-17"})






