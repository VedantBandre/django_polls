from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# Create your views here.

class IndexView(generic.ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_question_list"

	def get_queryset(self):
		# Returns last 5 published questions(futureproof)
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = "polls/detail.html"

	def get_queryset(self):
		# Excludes any unpublished questions
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Question
	template_name = "polls/results.html"


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST["choice"])
	except (KeyError, Choice.DoesNotExist):
		# Display the voting form again
		return render(request, 
			"polls/detail.html", 
			{
				"question": question,
				"error_message": "You did not select a choice.",
			}
		)
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing with POST data
		# This prevents data being posted twice if user clicks the back button
	return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


