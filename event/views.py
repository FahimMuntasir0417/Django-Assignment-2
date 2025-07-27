from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, RSVP
from django.db.models import Q
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.contrib import messages
from datetime import date
from django.utils import timezone
from django.http import Http404
from .models import Event,  Category
from .forms import EventForm,  CategoryForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from users.views import is_admin



def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()


@user_passes_test(is_organizer)
def manager_dashboard(request):
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=timezone.now().date()).count()
    past_events_count = Event.objects.filter(date__lt=timezone.now().date()).count()
    total_participants = User.objects.count()

    counts = {
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'total_participants': total_participants,
    }

    event_filter_type = request.GET.get('type', 'all')

    filtered_events = Event.objects.select_related('category').annotate(participant_count=Count('participants'))

    if event_filter_type == 'upcoming':
        filtered_events = filtered_events.filter(date__gte=timezone.now().date())
    elif event_filter_type == 'past':
        filtered_events = filtered_events.filter(date__lt=timezone.now().date())

    filtered_events = filtered_events.order_by('date', 'time')

    context = {
        "filtered_events": filtered_events,
        "counts": counts,
        "current_filter_type": event_filter_type,
    }
    return render(request, "event/dashboard.html", context)

@user_passes_test(is_organizer)
def create_event(request):
    event_form = EventForm()

    if request.method == "POST":
        event_form = EventForm(request.POST,request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('event:event_list')

    context = {"form": event_form, "title": "Create New Event"}
    return render(request, "event/event_form.html", context)

@user_passes_test(is_organizer)
def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    event_form = EventForm(instance=event)

    if request.method == "POST":
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event:event_detail', pk=pk)

    context = {"form": event_form, "title": "Update Event"}
    return render(request, "event/event_form.html", context)


@user_passes_test(is_organizer)
def delete_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('event:event_list')
    return render(request, 'event/confirm_delete.html', {'object': event, 'type': 'Event'})

@user_passes_test(is_organizer)
def event_list(request):
    events = Event.objects.all().select_related('category').annotate(participant_count=Count('participants'))

    search_query = request.GET.get('q')
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category__id=category_id)

    events = events.order_by('date', 'time')
    categories = Category.objects.all().order_by('name')

    context = {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'event/event_list.html', context)

@user_passes_test(is_organizer)
def event_detail(request, pk):
    try:
        event = Event.objects.prefetch_related('participants').get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    return render(request, 'event/event_detail.html', {'event': event})



@user_passes_test(is_organizer)
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'event/category_list.html', {'categories': categories})


@user_passes_test(is_organizer)
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    events_in_category = Event.objects.filter(category=category).order_by('date', 'time')
    return render(request, 'event/category_detail.html', {'category': category, 'events_in_category': events_in_category})

@user_passes_test(is_organizer)
def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully")
            return redirect('event:category_list')
    return render(request, 'event/category_form.html', {'form': form, 'title': 'Create New Category'})


@user_passes_test(is_organizer)
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('event:category_detail', pk=pk)
    return render(request, 'event/category_form.html', {'form': form, 'title': 'Update Category'})


@user_passes_test(is_organizer)
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category Deleted Successfully')
        return redirect('event:category_list')
    return render(request, 'event/confirm_delete.html', {'object': category, 'type': 'Category'})

def view_categories_with_event_counts(request):
    categories = Category.objects.annotate(num_events=Count('event')).order_by('num_events')
    return render(request, "event/category_event_counts.html", {"categories": categories})


# Create your views here.

# def participant_dashboard(request):
#     # Get user's RSVP'd events
#     rsvp_events = Event.objects.filter(
#         participants=request.user
#     ).order_by('date', 'time')
    
#     # Get recommended events (events not RSVP'd yet)
#     recommended_events = Event.objects.filter(
#         is_upcoming=True
#     ).exclude(
#         participants=request.user
#     ).order_by('date', 'time')[:6]
    
#     context = {
#         'rsvp_events': rsvp_events,
#         'recommended_events': recommended_events,
#     }
#     return render(request, 'dashboard/participant.html', context)


@login_required
@user_passes_test(is_participant)
def participant_dashboard(request):
  
    rsvp_events = Event.objects.filter(
        participants=request.user
    ).order_by('date', 'time')
    
  
    recommended_events = Event.objects.filter(
        date__gte=timezone.now().date() 
    ).exclude(
        participants=request.user
    ).order_by('date', 'time')[:6]
    
    context = {
        'rsvp_events': rsvp_events,
        'recommended_events': recommended_events,
    }
    return render(request, 'dashboard/participant.html', context)

@login_required
@user_passes_test(is_participant)
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        if not event.participants.filter(id=request.user.id).exists():
            event.participants.add(request.user, through_defaults={'status': 'going'})
            messages.success(request, f'You have successfully RSVP\'d to {event.title}')
        else:
            messages.warning(request, 'You have already RSVP\'d to this event')
    
    return redirect('event:participant') 


@login_required
@user_passes_test(is_participant)
def cancel_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        if event.participants.filter(id=request.user.id).exists():
            event.participants.remove(request.user)
            messages.success(request, f'You have canceled your RSVP to {event.title}')
        else:
            messages.warning(request, 'You had not RSVP\'d to this event')
    
    return redirect('event:participant')

def home(request):
    return render(request, 'event/home.html')



@user_passes_test(is_participant)
def participant_catagory(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/participant_category.html', {'categories': categories})

@login_required
@user_passes_test(is_participant)
def participant_event(request):
    events = Event.objects.all()
    return render(request, 'dashboard/participant_event.html', {'events': events})

@login_required
def main_dashboard(request):
    if is_organizer(request.user):
        return redirect('event:dashboard')
    elif is_participant(request.user):
        return redirect('event:participant')
    elif is_admin(request.user):
        return redirect('users:admin-dashboard')
    else:
        messages.error(request, "You do not have access to this dashboard.")
        return redirect('event:home')