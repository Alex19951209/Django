from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
	"""Головна сторінка "Журналу спостережень"."""
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	"""Відображає всі теми."""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""Show a single topic and all its entries."""
	topic = Topic.objects.get(id=topic_id)
	# Пересвідитись, що тема належить поточному користувачеві.
	check_topic_owner(topic, request.user)
	

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""Add a new topic."""
	if request.method != 'POST':
		# Жодних даних на відправлено; створити порожню форму.
		form = TopicForm()
	else:
		# Відправлений POST; обробити дані.
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('learning_logs:topics')

	# Показати порожню або недійсну форму.
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Add a new entry for a particular topic."""
	topic = Topic.objects.get(id=topic_id)
	if request.method != 'POST':
		# Жодних даних не надіслано; створити порожню форму.
		form = EntryForm()
	else:
		# Отримані дані у POST - запиті; обробити дані.
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic', topic_id=topic_id)

	# Показати порожню або недійсну форму.
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edit an eiting entry."""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	check_topic_owner(topic, request.user)
		
	if request.method !='POST':
		# Initial requet; pre-fill ith the current entry.
		form = EntryForm(instance=entry)
	else:
		# POST data submitted; process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic_id=topic.id)

	context = {'entry': entry, 'topic': topic, 'form':form}
	return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(topic, user):
	# Перевіряти чи дана тема належить дійсно до користувача."""
	if topic.owner != user:
		raise Http404