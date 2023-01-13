from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NotesForm
from .models import Notes

class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'
    login_url = '/login'

class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm
    login_url = '/login'

class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm
    login_url = '/login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print("Obj:", self.object)
        self.object.user=self.request.user
        self.object.save()
        return HttpResponseRedirect(self.success_url)

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = "notes/notes_list.html"
    context_object_name = "notes"
    login_url = "/login"
    def get_queryset(self):
        return self.request.user.notes.all()

class ListDetailView(DetailView):
    model = Notes
    context_object_name = "note"
