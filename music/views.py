from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views import generic
from django.views.generic import View
from .models import Album
from .forms import UserForm

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    #display blanck form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned(normalised) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns user objects if correct
            user = authenticate(username=username,password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return render(request, self.template_name, {'form':form})





















"""
from django.shortcuts import render,get_object_or_404
from .models import Album,Song

def index(request):
    all_albums = Album.objects.all()
    context = { 'all_albums': all_albums }
    #Shortcut using render
    return render(request, 'music/index.html', context)

def detail(request,album_id):
    #album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album,pk=album_id)
    return render(request, 'music/detail.html', {'album': album})

def favourite(request,album_id):
    album = get_object_or_404(Album,pk=album_id)
    #selected_song exists or not
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError,Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album': album,
            'error_message':"You did not select a valid song"
        })
    else:
        selected_song.is_favourite=True
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})
"""

"""
Index view...

---------Combining html and python---------
from django.http import HttpResponse

html=''
for album in all_albums:
    url='/music/' + str(album.id) + '/'
    html+='<a href="' + url + '">' + album.album_title + '</a><br/>'
return HttpResponse(html)

---------Keeping html seperate---------
from django.http import HttpResponse
from django.template import loader

template = loader.get_template('music/index.html')
return HttpResponse(template.render(context, request))
"""


"""
Detail view..

---------Try catch for 404-----------
from django.http import Http404

try:
    album = Album.objects.get(pk=album_id)
except Album.DoesNotExist:
    raise Http404("Album does not exist")
"""
