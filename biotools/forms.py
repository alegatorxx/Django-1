from django import forms

class SeqContentForm(forms.Form):
    sequence = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Plain sequence (accept FASTA)',
                   'class': 'form-control'}
        ), 
        min_length=5, 
        required=True,
        error_messages={'required': 'Wpisz sekwencję!'}
        )
    word_size = forms.IntegerField(initial=1, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))

    def clean_sequence(self):
        sequence = self.cleaned_data['sequence']
        if sequence.startswith('>'):
            sequence = sequence[sequence.index('\n'): ]
        return sequence.upper()

    def clean(self):
        sequence = self.cleaned_data['sequence']
        word_size = self.cleaned_data['word_size']
        if sequence and word_size:
            if len(sequence) < word_size:
                raise forms.ValidationError('Sequence cannot be shorter than word size.')



class RevCompForm(forms.Form):
    CHOICES = (('RevComp', 'RevComp'), ('Reverse', 'Reverse'), ('Complement', 'Complement'),)
    choice = forms.ChoiceField(choices=CHOICES)
    sequence = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Plain sequence (accept FASTA)',
                   'class': 'form-control'}
        ), 
        min_length=5, 
        required=True,
        error_messages={'required': 'Wpisz sekwencję!'}
        )

    def clean_sequence(self):
        sequence = self.cleaned_data['sequence']
        if sequence.startswith('>'):
            sequence = sequence[sequence.index('\n'): ]
        return sequence.upper()


class DNAgenerateForm(forms.Form):
    a_prob = forms.FloatField(initial=0.25, required=True, 
        label='A probability', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'}))
    c_prob = forms.FloatField(initial=0.25, required=True, 
        label='C probability',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'}))
    g_prob = forms.FloatField(initial=0.25, required=True, 
        label='G probability',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'}))
    t_prob = forms.FloatField(initial=0.25, required=True, 
        label='T probability', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'}))
    seq_len = forms.IntegerField(initial=20, required=True, 
        label='Sequence length', max_value = 1000, min_value = 20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'step': 'any'}))

    def clean(self):
        a_prob = self.cleaned_data['a_prob']
        c_prob = self.cleaned_data['c_prob']
        g_prob = self.cleaned_data['g_prob']
        t_prob = self.cleaned_data['t_prob']
        seq_len = self.cleaned_data['seq_len']

        if (a_prob + c_prob + g_prob + t_prob) != 1:
            raise forms.ValidationError('Sum of probabilities should be equal 1.')

        if seq_len > 1000 or seq_len < 20:
            raise forms.ValidationError('Seq len out of the range(20, 1000).')