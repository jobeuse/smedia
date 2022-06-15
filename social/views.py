from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.views.generic import DeleteView, UpdateView


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm
        context = {
            'post_list': posts,
            'form': form,

        }
        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

        posts = Post.objects.all().order_by('-created_on')
        form = PostForm
        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'social/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        form = CommentForm()
        context = {
            'post': post,
            'form': form,
            'comments': comments
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        formComment = CommentForm(request.POST)
        if formComment.is_valid():
            newComment = formComment.save(commit=False)
            newComment.author = request.user
            newComment.post = post
            newComment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'comments': comments,
            'form': form
        }

        return render(request, 'social/post_detail.html', context)


class PostEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social\post_edit.html'

    def get_success_url(self):
        return self.request.path
        # primary lkey
        pk = self.kwargs['pk']

        # url to return to
        return reverse_lazy('post-view', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'social\post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'social\comment_delete.html'

    def get_success_url(self):
        # primary lkey
        pk = self.kwargs['post_pk']
        # url to return to
        return reverse_lazy('post-view', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
