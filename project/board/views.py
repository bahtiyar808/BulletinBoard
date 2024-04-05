from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import OuterRef, Exists
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import ResponseFilter
from .models import Announcement, Response, News
from .forms import AnnouncementForm, ResponseForm, NewsForm


@login_required
@csrf_protect
def announcement_list(request):
    if request.method == 'POST':
        announcement_id = request.POST.get('announcement_id')
        announcement = Announcement.objects.get(id=announcement_id)
        action = request.POST.get('action')
        if action == 'respond':
            Response.objects.create(announcement=announcement, user=request.user)

    announcements_with_responses = Announcement.objects.annotate(
        user_responsed=Exists(
            Response.objects.filter(
                user=request.user,
                announcement=OuterRef('pk')
            )
        )
    ).order_by('-date_time')
    paginator = Paginator(announcements_with_responses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'all_announcements.html',
        {'announcements': announcements_with_responses, 'page_obj': page_obj},
    )


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcements'


class AnnouncementCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_announcement')
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AnnouncementEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'

    def test_func(self):
        announcement = self.get_object()
        return self.request.user == announcement.user


class AnnouncementDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcement_list')

    def test_func(self):
        announcement = self.get_object()
        return self.request.user == announcement.user


class CreateResponse(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        announcement_id = self.kwargs['pk']
        announcement = get_object_or_404(Announcement, pk=announcement_id)
        form.instance.announcement = announcement
        form.instance.user = self.request.user
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    ordering = '-date'
    template_name = 'response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        user = self.request.user
        queryset = Response.objects.filter(announcement__user=user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('response_list')


def accept_response(request, pk):
    response = Response.objects.get(pk=pk)
    response.accepted = True
    response.save()
    return redirect('response_list')


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_news')
    form_class = NewsForm
    model = News
    template_name = 'news_create.html'
    success_url = reverse_lazy('announcement_list')
