from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template import loader
# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question, Person, totalNumberOfVotes


class IndexView(generic.ListView):
	def get(self,request):
		a = request.GET.get('id')
		allObjects = Person.objects.all()
		for per in allObjects:
			if per.uniqueCode == a:
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
	if person.voted != True:
		for question in Question.objects.all():
			try:
				selected_choice = question.choice_set.get(pk=request.POST['choice' + str(question.id)])
			except (KeyError, Choice.DoesNotExist):
				# Redisplay the question voting form.
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
		person.voted = True
		person.save()
		tempT = totalNumberOfVotes.objects.all()[0]
		tempT.number+=1
		tempT.save()
		
		return render(request , 'polls/results.html' , {'text' : "Thanks for voting in ISA Elections 2016-17"})
	else:
		return render(request , 'polls/results.html' , {'text' : "You have already voted"})
	
		
	


