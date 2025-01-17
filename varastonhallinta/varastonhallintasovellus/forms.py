import datetime

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Henkilo, Tuote, Varastotapahtuma


class RekisteroityminenForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Salasana'
        self.fields['password2'].label = 'Salasana uudelleen'

        self.fields['password1'].help_text = 'Anna salasana joka sisältää ainakin 8 merkkiä'
        self.fields['password2'].help_text = 'Syötä sama salasana tarkistuksen vuoksi uudelleen'

    class Meta:
        model = Henkilo
        fields = ("username", "email", "first_name", "last_name", "vastuuopettaja", "password1", "password2")

        labels = {
            "username"          : "Anna käyttäjätunnus",
            "email"             : "Anna sähköpostiosoite",
            "first_name"        : "Anna etunimi",
            "last_name"         : "Anna sukunimi",
            "vastuuopettaja"    : "Vastuuopettaja",
        }

        help_texts = {
            "username"          : "Anna käyttäjätunnus, esim. oppilaan opiskelijanumero",
            "email"             : "Anna koulun tarjoama sähköpostiosoite",
            "vastuuopettaja"    : "Jos luot käyttäjää oppilaalle, valitse hänen vastuuopettajansa"
        }


class MuokkaaKayttajaaForm(UserChangeForm):
    password = None

    class Meta:
        model = Henkilo
        fields = ("username", "email", "first_name", "last_name")


class TuoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('kayttajan_rooli')
        super(TuoteForm, self).__init__(*args, **kwargs)
        self.fields['hankintapaiva'].required = False

        if self.user == 'varastonhoitaja':
            for kentta in ['hankintapaikka', 'hankintapaiva', 'hankintahinta', 'laskun_numero', 'kustannuspaikka', 'takuuaika']:
                del self.fields[kentta]

    class Meta():
        model = Tuote
        fields = '__all__'
        widgets = {
            'hankintapaiva' : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'takuuaika'     : forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

        labels = {
            "viivakoodi"        : "Lisää tuotteen viivakoodi",
            "nimike"            : "Lisää tuotteen nimi",
            "valmistaja"        : "Lisää tuotteen valmistaja",
            "kappalemaara"      : "Lisää tuotteiden kappalemäärä",
            "tuotekuva"         : "Anna tuotteelle kuva",
            "tuoteryhma"        : "Valitse tuoteryhmä johon tuote kuuluu",
            "hankintapaikka"    : "Mistä tuote on ostettu?",
            "hankintapaiva"     : "Lisää päivä jona tuote on ostettu",
            "hankintahinta"     : "Tuotteen hankintahinta",
            "laskun_numero"     : "Laskun numero",
            "kustannuspaikka"   : "Mille osastolle tuote on ostettu",
            "takuuaika"         : "Jos tuotteella on takuu, mihin asti se on voimassa",
        }

        error_messages = {
            "nimike": {
                "required"      : "Sinun on annettava tuotteelle nimi.",
                "max_length"    : "Tuotteen nimen on oltava maksimissaan 100 merkkiä."
            },
            "valmistaja": {
                "max_length"    : "Valmistajan nimen on oltava maksimissaan 100 merkkiä."
            },
            "hankintapaikka": {
                "max_length"    : "Hankintapaikan nimen on oltava maksimissaan 100 merkkiä."
            },
            "tuoteryhma": {
                "required"      : "Sinun on lisättävä tuotteen tuoteryhmä johon tuote kuuluu."
            }
        }

    def clean_hankintapaiva(self):
        hankintapaiva = self.cleaned_data['hankintapaiva']
        if hankintapaiva > datetime.date.today():
            raise forms.ValidationError('Hankintapäivä ei voi olla tulevaisuudessa!')
        return hankintapaiva


class LainaaTuoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LainaaTuoteForm, self).__init__(*args, **kwargs)

        self.fields['asiakas'].required = True
        self.fields['palautuspaiva'].required = True

        self.fields['tuote'].disabled = True
        self.fields['arkistotunnus'].disabled = True

        self.piilota_label = ('tyyppi', 'varastonhoitaja', 'varasto',)
        for field in self.piilota_label:
            self.fields[field].label = ''

    class Meta:
        model = Varastotapahtuma
        fields = '__all__'
        widgets = {
            'tyyppi': forms.HiddenInput(),
            'varastonhoitaja': forms.HiddenInput(),
            'varasto': forms.HiddenInput(),
            'palautuspaiva' : forms.DateInput(format=('%Y-%m-%d'), attrs={'type' : 'date'}),
        }

    def clean_maara(self):
        maara = self.cleaned_data['maara']
        if maara <= 0:
            raise forms.ValidationError('Tämän arvon on oltava vähintään 1!')
        return maara


class PalautaTuoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PalautaTuoteForm, self).__init__(*args, **kwargs)

        self.fields['tuote'].disabled = True
        self.fields['arkistotunnus'].disabled = True

        self.piilota_label = ('tyyppi', 'varastonhoitaja', 'varasto', 'palautuspaiva',)
        for field in self.piilota_label:
            self.fields[field].label = ''

    class Meta:
        model = Varastotapahtuma
        fields = '__all__'
        widgets = {
            'tyyppi': forms.HiddenInput(),
            'varastonhoitaja': forms.HiddenInput(),
            'varasto': forms.HiddenInput(),
            'palautuspaiva' : forms.HiddenInput(),
        }
