from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts_app.forms import InviteUserForm
from accounts_app.models import UserInvitation


class InviteUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # This would be the view where the invited user can join.
        # Here we have to check if the provided token points to an invitation which is valid and not expired.
        ...

    def post(self, request, *args, **kwargs):
        form = InviteUserForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            # We could further improve this here to first check if an invitation for this email already exists and is not expired
            UserInvitation.objects.filter(email=email).delete()

            invitation = UserInvitation(email=email, invited_by=request.user)
            invitation.save()

            invitation.send_invitation_email()

            # Reset form to clear the input field
            form = InviteUserForm()
            return render(request, "accounts_app/invite_modal_content.html", {"invite_user_form": form, "invited": True, "invited_email": email})
        else:
            return render(request, "accounts_app/invite_modal_content.html", {"invite_user_form": form, "invited": False})