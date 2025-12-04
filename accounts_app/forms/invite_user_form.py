from django import forms


class InviteUserForm(forms.Form):
    email = forms.EmailField(
        max_length=65,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-primary focus:ring-primary disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600',
            'placeholder': 'test@test.com',
            'id': 'invite-email'
        })
    )