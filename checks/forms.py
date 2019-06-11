from django import forms

from .models import Check

# from django.forms import HiddenInput


class SubmitCheckForm(forms.ModelForm):

    class Meta:
        model = Check
        fields = ('title', 'reason')


class EditCheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('author', 'title', 'reason', 'init_date')

        # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        # title = models.CharField(max_length=200)
        # reason = models.TextField()
        # init_date = models.DateTimeField(default=timezone.now)
        # test_field = models.CharField(max_length=50, default="ttt")