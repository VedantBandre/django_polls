from django.contrib import admin

from .models import Choice, Question

# Register your models here.

class ChoiceInline(admin.TabularInline):
	# removes the need to admin.site.register(Choice)
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {"fields": ["question_text"]}),
		("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
	]
	
	# choices will be presented inline rather than stacked on top of each other
	inlines = [ChoiceInline]

	# select what is displayed in the list
	list_display = ["question_text", "pub_date", "was_published_recently"]
	
	# filter according to the pub_date
	list_filter = ["pub_date"] 
	
	# added search facility based on question_text
	search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)