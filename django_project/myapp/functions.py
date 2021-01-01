def handle_uploaded_file(f):
    with open('myapp/media/'+f.name, 'wb+') as destiantion:
        for chunk in f.chunks():
            destiantion.write(chunk)


