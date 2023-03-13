from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import book
# Create your views here.
def home(request):
    bk = book.objects.all()
   
    return render(request, 'home.html', {'bk': bk})

def addEntry(request):
    bid = request.POST["BookID"]
    aid = request.POST["AuthorID"]
    bname = request.POST["BookName"]
    aname = request.POST["AuthorName"]
    sts = request.POST["Status"]
    newbookEntry = book(bookID = bid, authorID = aid, bookName = bname, authorName = aname, status = sts)
    newbookEntry.save()
    print(newbookEntry)
    return HttpResponseRedirect('/')

def deleteAll(request):
    bk1 = book.objects.all()
    bk1.delete()
    
    return HttpResponseRedirect('/')

def dictfetchall(cursor): 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

def getSearch(request):
    q= request.POST["query"]
    print(q)
    cursor = connection.cursor()
    cursor.execute(q)
    bk = book.objects.all()
    bk1 = dictfetchall(cursor)
    print(bk1)
    print(connection.queries)
    return render(request, 'home.html', {'bk1': bk1, "bk": bk})

