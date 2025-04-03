from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from users.forms import SignupForm, UserLoginForm

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print("\n\nform:", form, "\n\n")
        print("\n\nform.is_valid():", form.is_valid(), "\n\n")
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect("applications:home")
    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('applications:home')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('users:login')
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("users:login")

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Update user fields
        user.iin = request.POST.get('iin')
        # user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        # Save the user
        user.save()
        
        # Add success message
        messages.success(request, 'Profile updated successfully!')
        
        return redirect('users:profile')
    
    # If not POST, redirect to profile page
    return redirect('profile')

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted.")
        return redirect("applications:home")
    # return render(request, "delete_account.html")

def profile_view(request):
    return render(request, "users/profile.html")