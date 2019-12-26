from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from blog.models import Comment, Post
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Account have been successfully created')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


@login_required
def profile(request):
    last_comments = Comment.objects.filter(user=request.user).order_by('created')[:5]
    comment_user = Comment.objects.filter(user=request.user)
    favorite = Post.objects.filter(likes=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Profile was successfully updated.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'comment_user': comment_user,
        'last_comments': last_comments,
        'favorite': favorite,
    }
    return render(request, 'account/profile.html', context)

