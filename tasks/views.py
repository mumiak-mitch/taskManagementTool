from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Notification
from .forms import ProjectForm, TaskForm

def create_notification(message):
    Notification.objects.create(message=message)



def dashboard(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    total_notifications = Notification.objects.count()
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'total_notifications': total_notifications,
        'notifications': notifications,
    })



def project_list(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'project-list.html', {'projects': projects})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            create_notification(f"New project added: {project.name}")
            return redirect('project_list') 
    else:
        form = ProjectForm()
    return render(request, 'add-project.html', {'form': form})

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            create_notification(f"Project edited: {project.name}")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit-project.html', {'form': form})

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        create_notification(f"Project deleted: {project.name}")
        return redirect('project_list')
    return render(request, 'delete-project.html', {'project': project})



def task_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all().order_by('priority')
    return render(request, 'task-list.html', {'project': project, 'tasks': tasks})

def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            create_notification(f"New task added: {task.title} to project {project.name}")
            return redirect('task_list', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'add-task.html', {'form': form, 'project': project})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            create_notification(f"Task edited: {task.title}")
            return redirect('task_list', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit-task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        create_notification(f"Task deleted: {task.title}")
        return redirect('task_list', project_id=task.project.id)
    return render(request, 'delete-task.html', {'task': task})



def update_task_priority(request, task_id, priority):
    task = get_object_or_404(Task, id=task_id)
    if priority >= 0:
        task.priority = priority
        task.save()
        #Notification.objects.create(message=f"Task '{task.title}' priority updated to {priority}")
        create_notification(f"Task priority updated: {task.title} to {priority}")
    return redirect('task_list', project_id=task.project.id)

def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    return redirect('dashboard')
