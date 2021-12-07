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

def thread_function(list,dictt,x,y):
    for id in list[x:y]:
        yt = YouTube('http://youtube.com/watch?v='+id)
        dictt[id]={yt.title}

def thread_downloadVideo(id):
    stream = os.popen("yt-dlp -S 'res:1080,acodec:mp3,vcodec:h263' -o '%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt "+id)
    output = stream.read()
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
        if(request.GET.get('download')):
            key=request.POST["key"]
            print(key)
            return render(request, 'youtube/index.html')

        name=request.POST["name"]
        #html = urllib.request.urlopen("https://www.youtube.com/results?search_query=mozart")
        name=name.replace(" ","")
        print(name)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+name)

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        size_ids=len(video_ids)
        video_dic={}
        if(size_ids>=20):
            threads=list()
            dicts=[]
            for x in range(0,20,2):
                dictt={}
                thread=threading.Thread(target=thread_function, args=(video_ids,dictt,x,x+2))
                thread.start()
                threads.append(thread)
                dicts.append(dictt)
            
            for thread in threads:
                thread.join()

            for dictt in dicts:
                video_dic.update(dictt)    
        else:
            for id in video_ids:
                yt = YouTube('http://youtube.com/watch?v='+id)
                video_dic[id]=yt.title
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
    if request.method == 'GET':
        return render(request, 'youtube/list.html')

    elif request.method == 'POST':      
        key=request.POST["key"]
        '''name=request.POST["name"]
        name_video=request.POST["name_video"]
        dict=request.POST["dict"]'''
       
        #stream = os.popen("yt-dlp -S 'res:1080,acodec:mp3,vcodec:h263' -o '%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt "+key)
        
        thread=threading.Thread(target=thread_downloadVideo, args=(key,))
        thread.start()
        context ={
        '''    "data":"POST",
            "key":key,
            "name":name,
            "dict":dict,
            "name_video":name_video,'''
        }

        ##yt-dlp -S 'res:720,acodec:mp3,vcodec:h263' -o '%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt --concurrent-fragments 5 oDRp1DPhPLI
        return render(request, 'youtube/list.html',)

def playlist(request):
    if request.method == 'GET':
        print(glob.glob("*.mp4")) 

        return render(request, 'youtube/playlist.html')

    elif request.method == 'POST':   
        url=request.POST["url"]
        print(url)
        print(url.split("&list=")[1])
        thread=threading.Thread(target=thread_downloadVideo, args=(url.split("&list=")[1],))
        thread.start()
        #https://www.youtube.com/watch?v=TUVcZfQe-Kw&list=PLNrotoZZ8BaoXT_LJuwEyESQlctWNDCwD
        ##yt-dlp -S 'res:720,acodec:mp3,vcodec:h263' -o '%(title)s' --remux-video mp4  --user-agent chrome --download-archive ids.txt --concurrent-fragments 5 oDRp1DPhPLI
        return render(request, 'youtube/playlist.html',)

def downloads(request):
    if request.method == 'GET':
        context ={
           "list":glob.glob("*.mp4") ,
        }

        return render(request, 'youtube/downloads.html',context)

   