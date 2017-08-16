import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from random import randrange
# Create your models here.

@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	winner = models.CharField(max_length=200,default="Needs to be decided")
	def __str__(self):
		return self.question_text
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)
	def findWinner(self):
		count = 0
		maxVoter = self.choice_set.all()[0]
		for obj in self.choice_set.all()[1:]:
			if obj.votes == maxVoter.votes:
				count = count + 1
			elif obj.votes > maxVoter.votes:
				maxVoter = obj
				count = 0
		if count > 0:
			self.winner = "Draw"
		else:
		 self.winner = maxVoter.choice_text



@python_2_unicode_compatible  # only if you need to support Python 2
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.choice_text
def random_string():
	import random
	return str(random.randint(10000000, 999999999))


class Person(models.Model):
	name = models.CharField(max_length=200)
	email = models. EmailField()
	uniqueCode = models.CharField(max_length=100,unique=True, default= random_string )
	voted = models.NullBooleanField()
	currentCondition = models.CharField(max_length=100,default='Not Touched')

	def __str__(self):
		return self.name

	def votingCompleted(self):
		self.voted = True
		self.currentCondition = 'Voted'


	def sendEmail(self):
		x = "http://isauofs.pythonanywhere.com/polls/?id=" + self.uniqueCode
		email = EmailMessage(
		    'ISA-Elections',
                             'Dear ' + self.name +',\nThis email contains a unique link to the 2016-17 ISA elections voting page. Do not share this link or email with anyone else. You can vote by clicking on the following link -\n %s\n\nThe link will be active till 4pm on Sunday, 31st July.\n\nWe ask the ballots to be filled out by checking the YES box for the candidate you wish to vote for, NO box for candidate you do not wish for, or ABSTAIN box to refrain from voting for that position.\n\nIf you are facing any technical difficulties, please email us at isa.uofs@gmail.com\n\nBest,\n2015-16 ISA Committee' %(x),
		    'isa.uofs@gmail.com',
		    [self.email],
		)
		email.send()
		self.currentCondition = 'Email Sent'

class totalNumberOfVotes(models.Model):
	number = models.IntegerField(default=0)
