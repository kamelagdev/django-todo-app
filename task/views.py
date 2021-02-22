from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Q


# Create your views here.
def index(request):
    tasks = Task.objects.all().order_by('-created_at')
    type_q = request.GET.get('type')
    title = request.GET.get('title')
    if type_q != 'none' and type_q is not None:
        tasks = tasks.filter(Q(is_completed=type_q))
    if title != '' and title is not None:
        tasks = tasks.filter(title__icontains=title)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm()

    context = {'tasks': tasks, 'form': form}
    return render(request, 'task/index.html', context)


def task_update(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm(instance=task)
    context = {'form': form}
    return render(request, 'task/task_update.html', context)


def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    context = {'task': task}
    return render(request, 'task/task_confirm_delete.html', context)
