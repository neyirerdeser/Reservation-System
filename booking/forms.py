from django import forms

class NumberOfPeopleForm(forms.form):
    number = forms.IntegerField()

    def reserve_for_number(self):
        pass