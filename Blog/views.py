from django.shortcuts import render
from Blog.models import Posteo, Comentario
from Blog.forms import FormComentario

def blog_index(request):
    # Todos los posts ordenados por el campo created on de forma descenddiente
    posteos = Posteo.objects.all().order_by('-created_on')

    context = {
        'posteos': posteos,
    }

    return render(request, 'index.html', context)

def blog_detail(request,pk):
    # Un post en específico
    posteo = Posteo.objects.get(pk=pk)

    formulario = FormComentario()
    if request.method == 'POST':
        # Se quiere guardar un comentario en este post
        formulario = FormComentario(request.POST)

        if formulario.is_valid():
            comentario = Comentario(
                autor = formulario.cleaned_data['autor'],
                body = formulario.cleaned_data['body'],
                posteo = posteo
            )
            # Guardaddo el comentario
            comentario.save()

            # Limpiamos los campos del formulario
            formulario = FormComentario()
    
    # Filtrado de los comentario perteneciente a este post para mostrarlo en el template
    comentarios = Comentario.objects.filter(posteo=posteo)

    context = {
        'posteo': posteo,
        'comentarios': comentarios,
        'formulario': formulario
    }

    return render(request, 'detail.html', context)