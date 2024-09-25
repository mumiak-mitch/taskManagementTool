from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Notification
from .forms import ProjectForm, TaskForm

def create_notification(message):
    """
    Creates a new notification with the given message.
    """
    Notification.objects.create(message=message)

def dashboard(request):
    """
    Renders the dashboard page, displaying total counts for projects, tasks, and notifications.
    """
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
    """
    Renders a list of all projects.
    """
    projects = Project.objects.all().order_by('-id')
    return render(request, 'project-list.html', {'projects': projects})

def add_project(request):
    """
    Handles the addition of a new project.
    If the request is POST, validates the form and saves the new project.
    Otherwise, displays an empty form.
    """
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
    """
    Handles the editing of an existing project.
    If the request is POST, validates the form and updates the project.
    Otherwise, pre-fills the form with the current project data.
    """
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)  # Bind the form to the existing project instance
        if form.is_valid():
            form.save()  # Save the updated project
            create_notification(f"Project edited: {project.name}")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)  # Create a form pre-filled with the project data
    
    return render(request, 'edit-project.html', {'form': form})

def delete_project(request, project_id):
    """
    Handles the deletion of a project.
    If the request is POST, deletes the project.
    Otherwise, displays the confirmation page.
    """
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project.delete()  # Delete the project
        create_notification(f"Project deleted: {project.name}")
        return redirect('project_list')
    
    return render(request, 'delete-project.html', {'project': project})

def task_list(request, project_id):
    """
    Renders a list of tasks for a specific project.
    """
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all().order_by('priority')
    
    return render(request, 'task-list.html', {'project': project, 'tasks': tasks})

def add_task(request, project_id):
    """
    Handles the addition of a new task to a specific project.
    If the request is POST, validates the form and saves the new task.
    Otherwise, displays an empty form.
    """
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Do not save to the database yet
            task.project = project  # Associate the task with the project
            task.save()  # Save the task
            create_notification(f"New task added: {task.title} to project {project.name}")
            return redirect('task_list', project_id=project.id)
    else:
        form = TaskForm()
    
    return render(request, 'add-task.html', {'form': form, 'project': project})

def edit_task(request, task_id):
    """
    Handles the editing of an existing task.
    If the request is POST, validates the form and updates the task.
    Otherwise, pre-fills the form with the current task data.
    """
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # Bind the form to the existing task instance
        if form.is_valid():
            form.save()  # Save the updated task
            create_notification(f"Task edited: {task.title}")
            return redirect('task_list', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)  # Create a form pre-filled with the task data
    
    return render(request, 'edit-task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    """
    Handles the deletion of a task.
    If the request is POST, deletes the task.
    Otherwise, displays the confirmation page.
    """
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.delete()  # Delete the task
        create_notification(f"Task deleted: {task.title}")
        return redirect('task_list', project_id=task.project.id)
    
    return render(request, 'delete-task.html', {'task': task})

def update_task_priority(request, task_id, priority):
    """
    Updates the priority of a specific task.
    If the new priority is valid, saves the updated task.
    """
    task = get_object_or_404(Task, id=task_id)
    
    if priority >= 0:
        task.priority = priority
        task.save()
        create_notification(f"Task priority updated: {task.title} to {priority}")
    
    return redirect('task_list', project_id=task.project.id)

def mark_notification_read(request, notification_id):
    """
    Marks a specific notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    
    return redirect('dashboard')
