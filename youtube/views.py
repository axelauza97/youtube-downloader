# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import urllib.request
import re
from pytube import YouTube

import threading
import os

import glob

from youtube.models import Genre, Video
import random

def thread_function(list,dictt,x,y):
    for id in list[x:y]:
        yt = YouTube('http://youtube.com/watch?v='+id)
        dictt[id]=yt.title

def thread_downloadVideo(id,genre):
    stream = os.popen("yt-dlp -S 'res:1080,acodec:mp3,vcodec:h263' -o './"+genre+"/%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt youtube.com/watch?v="+id)
    #output = stream.read()
    #print(output)

# Create your views here.
def index(request):
    if request.method == 'GET':
        context ={
            "data":"GET",
            "list":[]
        }
        return render(request, 'youtube/index.html',context)
    elif request.method == 'POST':
        name=request.POST["name"]
        #html = urllib.request.urlopen("https://www.youtube.com/results?search_query=mozart")
        name=name.replace(" ","")
        print(name)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+name)

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        #size_ids=len(video_ids)
        video_dic={}
        ids=[]
        #random.shuffle(video_ids)
        while(len(ids)!=20):
            key=video_ids.pop()
            if Video.objects.filter(key=key).exists():
                #print(key)                
                print("existe")
            else:
                ids.append(key)
                pass
        threads=list()
        dicts=[]
        for x in range(0,22,2):
            dictt={}
            thread=threading.Thread(target=thread_function, args=(ids,dictt,x,x+2))
            thread.start()
            threads.append(thread)
            dicts.append(dictt)
        
        for thread in threads:
            thread.join()

        for dictt in dicts:
            video_dic.update(dictt)
        

        #print(video_dic)
        context ={
            "data":"POST",
            "name":name,
            #"list":video_ids
            "dict":video_dic,
            #"list":['KZh60U1PqSE', 'U3AugwfuuB0', 'Nhea8S9L8_Q', 'QEPRUeLIq0o', 'cMtBOR_U-pI', 'rgLTWI9BObc', '65sL2OD0ml0', 'pM2S99_JQvU', '8XSw1Q6jBoI', '8TOcvnWODXE', '1iqgSpk-uKQ', '0nWKrvNjdtQ', 'Jd86fMKwtGg', 'qlGjKd4t0ms', 'A9KpY4Kbzbw', 'cZxJvh-k4S0', 'LYftF8LmZnI', 'NU8hWO8YuxQ', 'ki2Kj4fz8TI', 'C8FQ4wQXyaE', 'kanyeO5uoNo', 'QEPRUeLIq0o', 'QEPRUeLIq0o', 'cMtBOR_U-pI', 'vYxKhC1kGpE', 'AaJ09SPAym8', 'KktT_jxfR8s', 'aovqSlz3qKc', 'zPHG4zyryII', 'KZh60U1PqSE', 'KZh60U1PqSE', 'U3AugwfuuB0', 'oz3Pa6-47vI', 'KZh60U1PqSE', 'KZh60U1PqSE', 'Nhea8S9L8_Q', 'U3AugwfuuB0', 'NYI1DsY6_Ho', 'dYOT3YB-v7M', 'cMtBOR_U-pI', '8XSw1Q6jBoI', '1MibkygUPLU', 'ETq0pxEiLFE', '1iqgSpk-uKQ'],
            #"list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        return render(request, 'youtube/index.html',context)

def download(request):
    print(request)
    if request.method == 'GET':
        return render(request, 'youtube/list.html')

    elif request.method == 'POST':      
        key=request.POST["key"]
        genre=request.POST["genre"]

        genreObject=Genre.objects.get(name=genre)                
        video = Video.objects.create(key=key,genre=genreObject)
        video.save()
       
        #stream = os.popen("yt-dlp -S 'res:1080,acodec:mp3,vcodec:h263' -o '%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt "+key)
        thread=threading.Thread(target=thread_downloadVideo, args=(key,genre))
        thread.start()
        ##yt-dlp -S 'res:720,acodec:mp3,vcodec:h263' -o '%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt --concurrent-fragments 5 oDRp1DPhPLI
        return render(request, 'youtube/list.html',)

def playlist(request):
    if request.method == 'GET':
        print(glob.glob("*.mp4")) 

        return render(request, 'youtube/playlist.html')

    elif request.method == 'POST':   
        url=request.POST["url"]
        genre=request.POST["genre"]
        print(url)
        print(url.split("&list=")[1])
        thread=threading.Thread(target=thread_downloadVideo, args=(url.split("&list=")[1],genre))
        thread.start()
        return render(request, 'youtube/playlist.html',)

def downloads(request):
    if request.method == 'GET':
        
        if request.GET.get("genre","") !="":
            genre=request.GET["genre"]    
            context ={
                "genre":genre,
                "list":[w.replace(genre+"/", '') for w in glob.glob(genre+"/"+"/*.mp4")] ,
            }
        else:        
            context ={
                "genre":"pop",
            "list":[w.replace("pop/", '') for w in glob.glob("pop/*.mp4")] ,
            }

        return render(request, 'youtube/downloads.html',context)
'''    
def save(request):
    if request.method == 'GET':
        file1 = open('ids.txt', 'r')
        lines = file1.readlines()
        
        # Strips the newline character
        for line in lines:
            key =line.split("youtube ")[1]
            print(key)
            genre=Genre.objects.get(name="pop")
            print(genre)
            
            video = Video.objects.create(key=key,genre=genre)
            video.save()
        return render(request, 'youtube/index.html')
'''