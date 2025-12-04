from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts_app.forms import EditUserForm, InviteUserForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts_app/profile.html", {"form": EditUserForm(instance=request.user), "invite_user_form": InviteUserForm() })
    
    def post(self, request, *args, **kwargs):
        form = EditUserForm(request.POST, instance=request.user)
        invite_user_form = InviteUserForm()

        if form.is_valid():
            form.save()
            # Refresh the user object from the database to get updated data
            request.user.refresh_from_db()
            # Re-instantiate the form with updated user data to show new values in template
            form = EditUserForm(instance=request.user)

        return render(request, "accounts_app/profile.html", {"form": form, "invite_user_form": invite_user_form})