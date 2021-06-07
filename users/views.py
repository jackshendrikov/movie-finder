from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import redirect, render
from django.views.generic import (ListView, DetailView,  UpdateView, DeleteView)

from .forms import ReviewForms
from .models import Review


@login_required
def fill_form(request):
    movie_selected = request.GET.get('movie', "notSelected")
    if movie_selected == "notSelected":
        messages.warning(request, f'URL Not Allowed. Select the movie first!')
        return redirect('../')

    if request.method == 'POST':
        form = ReviewForms(request.POST or None)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.movie = movie_selected
            messages.success(request, f'Added Review for {movie_selected}')
            form.save()
            return redirect('my-reviews')
    form = ReviewForms()
    params = {'form': form, 'movie': movie_selected}
    return render(request, 'form.html', params)


class PostListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews.html'
    context_object_name = 'reviewPosts'
    ordering = ['-timestamp']
    paginate_by = 4


class PostListViewUser(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'my-reviews.html'
    context_object_name = 'reviewPosts'


class PostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Review
    template_name = 'post-detail.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return True


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    context_object_name = 'reviews'
    fields = ['rating', 'review_description']
    template_name = 'form.html'
    success_url = "/reviews"

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.INFO, f'Your Review has been Updated!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'confirm-delete.html'
    success_message = f"Review has been Deleted Successfully"
    success_url = '/reviews'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)
