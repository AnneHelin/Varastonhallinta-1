from django.shortcuts import render, redirect

# Tarvittavat json-importit hakukentän toimimiseen
import json
from django.http import JsonResponse

# Djangon autentikaatiot sisään- ja uloskirjautumiseen
from django.contrib.auth import authenticate, login, logout
# MUUT KIRJAUTUMISEEN / ULOSKIRJAUTUMISEEN TARVITTAVAT ASETUKSET
# LÖYTYVÄT --> settings.py!

from django.contrib.auth.decorators import login_required

# "messages" avulla voimme näyttää kustomoituja viestejä käyttäjille
# + näyttää ne templeiteissä.
from django.contrib import messages

# Importit "testeille joiden käyttäjien on läpäistävä" jotta he pääsevät tietyille sivulle 
from django.contrib.auth.mixins import UserPassesTestMixin

# Importit class näkymän parametrille joka vaatii käyttäjää
# olemaan sisäänkirjautuneena nähdäkseen sivun
from django.contrib.auth.mixins import LoginRequiredMixin

# Importit class näkymä tyypeille
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView

# Models importit
from .models import Tuote

# Lomakkeen import --> "forms.py"
from .forms import TuoteForm


def kirjautuminen(request):
    """
    Funktio sisäänkirjautumista varten, sekä uudelleenohjaus etusivulle jos
    käyttäjä on jo kirjautunut tai uudelleenohjaus kirjautumissivulle jos
    käyttäjän antamat todentamistiedot ovat virheelliset.
    """
    if request.user.is_authenticated:
        return redirect('/')
    else:
        # Jos lomake lähetetään (submit) metodi on POST
        if request.method == 'POST':
            username = request.POST['käyttäjätunnus']
            password = request.POST['salasana']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                # Kirjautumistiedot ovat väärät, näytä viesti
                # ja uudelleenohjaa kirjautumissivulle.
                messages.success(request, ('Antamasi salasana tai käyttäjätunnus on väärä!'))
                return redirect('kirjautuminen')
        else:
            # Jos metodi on GET renderöidään kirjautumissivu
            return render(request, 'kirjautuminen.html')


def uloskirjautuminen(request):
    """
    Funktio uloskirjautumista varten, sekä viesti kirjautumislomakkeeseen
    että käyttäjä on nyt kirjautunut ulos
    """
    logout(request)
    messages.success(request, ('Olet nyt kirjautunut ulos.'))
    return redirect('kirjautuminen')


class JosEiOikeuttaUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Kun käyttäjällä ei ole oikeutta johonkin sivuun...
    1. Käyttäjällä ei ole oikeutta johonkin sivuun uudelleenohjaus --> 'kirjautuminen'
    2. tai jos käyttäjä on kirjautunut mutta ei oikeutta --> 'kirjautuminen' -> 'etusivu'
    """

    def handle_no_permission(self):
        return redirect('kirjautuminen')


class KaikkiKayttajatUserMixin(JosEiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet kaikille käyttäjätyypeille --> esim etusivua varten
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        sallitut_kayttajatyypit = ['oppilas', 'varastonhoitaja', 'opettaja', 'hallinto']

        if self.request.user.rooli in sallitut_kayttajatyypit:
            return True


class PaakayttajatUserMixin(JosEiOikeuttaUserMixin, UserPassesTestMixin):
    """
    Pääsyoikeidet kaikille pääkäyttäjäjille --> varastonhoitajat, opettajat, hallinto jne.
    --> Tätä classia käytetään parametrina tietyissä class näkymissä.
    """
    
    def test_func(self):
        sallitut_kayttajatyypit = ['varastonhoitaja', 'opettaja', 'hallinto']

        if self.request.user.rooli in sallitut_kayttajatyypit:
            return True


class EtusivuView(KaikkiKayttajatUserMixin, TemplateView):
    """
    Näkymä etusivulle johon pääse kaikki kirjautuneet käyttäjät joiden
    rooli on joko --> 'oppilas', 'varastonhoitaja', 'opettaja' tai 'hallinto'
    """
    template_name = 'etusivu.html'


@login_required
def lainaus(request):
    tuotteet = Tuote.objects.all()
    context = {'tuotteet':tuotteet,}
    return render(request, 'lainaus.html', context)


def tuotehaku(request):
    if request.method == 'POST':
        # Hakuun syötettävät asiat muutetaan python dictionaryksi
        haku_str = json.loads(request.body).get('hakuteksti')
        # Tallentaa tuotteet-muuttujaan haut, jotka vastaavat haun sisältöä
        tuotteet = Tuote.objects.filter(
            nimike__icontains=haku_str) | Tuote.objects.filter(
            viivakoodi__icontains=haku_str)
    data = tuotteet.values()
    # Palauttaa tulokset JSON-muodossa
    return JsonResponse(list(data), safe=False)



#@login_required
# def palautus(request):
#     return HttpResponse('palautussivu')


# HALLINTA NÄKYMÄ FUNKTIONA --> JOS CLASS VIEW EI TOIMI
# MUISTA VAIHTAA MYÖS URLS.PY:SSÄ!
# @login_required
# def hallinta(request):
#     return render(request, 'hallinta.html')


class HallintaView(PaakayttajatUserMixin, ListView):
    """
    Vain pääkäyttäjät (varastonhoitaja', 'opettaja', 'hallinto) pääsevät hallinta
    näkymään, jossa listataan kaikki tietokannassa olevat tuotteet ja joissa on linkit
    niiden poistamiseen ja muokkaamiseen + tiedot tuotteista
    --> (tiedon määrä riippuen käyttäjän roolista).
    """
    template_name = 'hallinta.html'
    model = Tuote
    context_object_name = "tuotteet"


class LisaaTuoteView(PaakayttajatUserMixin, CreateView):

    model = Tuote
    form_class = TuoteForm
    template_name = 'lisaa-tuote.html'
    success_url = '/lisaa-tuote/'

    def get_form_kwargs(self):
        kwargs = super(LisaaTuoteView, self).get_form_kwargs()
        kwargs['kayttajan_rooli'] = self.request.user.rooli
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Tuote on nyt lisätty! Lisätäänkö saman tien toinen?')
        return super().form_valid(form)


class MuokkaaTuotettaView(PaakayttajatUserMixin, UpdateView):
    model = Tuote
    form_class = TuoteForm
    template_name = 'muokkaa-tuotetta.html'
    success_url = '/hallinta/'

    def get_form_kwargs(self):
        kwargs = super(MuokkaaTuotettaView, self).get_form_kwargs()
        kwargs['kayttajan_rooli'] = self.request.user.rooli
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f'Tuotetta on nyt muokattu!')
        return super().form_valid(form)


class PoistaTuoteView(PaakayttajatUserMixin, DeleteView):
    model = Tuote
    template_name = 'poista-tuote.html'
    success_url = '/hallinta/'