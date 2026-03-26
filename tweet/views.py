from django.shortcuts import render, redirect
from .models import Tweet, Profile
from .forms import TweetForm, UserRegisterForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create Tweet.
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

# Edit Tweet
@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

# Delete Tweet
@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html',{'form': form}) 


@login_required
def tweet_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.likes.filter(pk=request.user.id).exists():
        tweet.likes.remove(request.user) # Unlike
    else:
        tweet.likes.add(request.user) # Like
    return redirect('tweet_list')

# profile
@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    # This line prevents the 500 error by creating the profile if missing
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated, {request.user.username}!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})