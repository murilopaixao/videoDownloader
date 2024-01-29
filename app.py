import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
import banco


def download_video():
    url = entry_url.get()

    status_label.pack(pady=("10p", "5p"))
    progress_label.pack(pady=("10p", "5p"))
    progress_bar.pack(pady=("10p", "5p"))

    audio = opAudioVar.get()
    video = opVideoVar.get()

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)

        if video == "s":
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path="downloadsVideo")        

        status_label.configure(text="Downloaded Successfully", text_color="white", fg_color="Green")
    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")
    
    if audio == "s":
        streamAudio = yt.streams.get_by_itag(140)    
        streamAudio.download(output_path="downloadsAudio")

# call back function to update the progress
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    progress_label.configure(text= str(int(percentage_completed)) + " %")
    progress_label.update()
    progress_bar.set(float(percentage_completed / 100)) 

def popularTreeview():
    treeview.delete(*treeview.get_children())
    entradas=banco.selectAll()
    for x in entradas:
        treeview.insert("","end",values=(x["id"],x["titulo"],x["thumbnail"],x["url"]))

def pesquisar():
    url = entry_url.get()
    yt = YouTube(url)
    thumbnail = yt.thumbnail_url.split("?")[0]
    copyImage(thumbnail)
    #filtrarStreams(yt)
    if entry_url.get() != "":
        qtdRegistros = banco.selectOne(url)
        if len(qtdRegistros) != 0:
            print("Registro já consta na base!")
            messagebox.showinfo(title="Url Existente",message="Url já consta na base!")
        else:
            banco.insertOne(yt.title,thumbnail,url)
    popularTreeview()
    entry_url.delete(0,END)

def verificaBanco():
    messagebox.showinfo(title="Url Existente",message="Url já consta na base!")

def copyImage(url):
    global image3
    raw_data = urlopen(url).read()
    im = Image.open(BytesIO(raw_data))
    converted_image=im.resize((360,240), Image.Resampling.LANCZOS)
    image3 = ImageTk.PhotoImage(converted_image)

    logo_label["image"]=image3

def itemSelectTreeview(event):   
    itemSelect=treeview.selection()[0]
    valores=treeview.item(itemSelect,"values")
    copyImage(valores[2])
    entry_url.delete(0,END)
    entry_url.insert(END,valores[3])

def filtrarStreams(yt):
    print("High: " + str(yt.streams.get_highest_resolution()))
    #stream = yt.streams.filter(only_audio=True)
    stream = yt.streams.filter(file_extension='mp4')

    for x in stream:
        print(x)        
        
def clear():
    entry_url.delete(0,END)


# create a root windows
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# title of the window
root.title("YouTube Downloader!")

# set min and max width and the height
root.geometry("1250x520")
root.minsize(720, 520)
root.maxsize(1280, 720)

# create a frame to hold the content
left_frame = ctk.CTkFrame(root)
left_frame.pack(side=LEFT, fill=ctk.BOTH, expand=True, padx=5, pady=10)

pesquisa_frame = ctk.CTkFrame(root)
pesquisa_frame.pack(side=RIGHT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

left_frame_a = ctk.CTkFrame(left_frame, width=710, height=630)
left_frame_a.grid(column=0,row=0,padx=5,pady=50)

# create a label and the entry widget for the video url
url_label = ctk.CTkLabel(left_frame_a, text="Enter the youtube url here : ")
entry_url = ctk.CTkEntry(left_frame_a, width=400, height=40)
url_label.pack(pady=("10p", "5p"))
entry_url.pack(padx=40,pady=("10p", "5p"))

optionFrame = ctk.CTkFrame(left_frame_a)
optionFrame.pack(pady=("10p", "5p"))

opAudioVar=StringVar(value="s")
opVideoVar=StringVar(value="s")

opAudio=ctk.CTkCheckBox(optionFrame,text="Audio", variable=opAudioVar, onvalue="s", offvalue="n")
opAudio.pack(side=LEFT)
opVideo=ctk.CTkCheckBox(optionFrame,text="Video", variable=opVideoVar, onvalue="s", offvalue="n")
opVideo.pack(side=LEFT)


btn_frame = ctk.CTkFrame(left_frame_a)
btn_frame.pack(pady=("10p", "5p"))

# Criar botão pesquisar
pesquisar_button = ctk.CTkButton(btn_frame, text="Pesquisar", command=pesquisar)
pesquisar_button.grid(column=0,row=0,padx=5,pady=5)

# Botão Limpar
clear_button = ctk.CTkButton(btn_frame, text="Limpar", command=clear)
clear_button.grid(column=1,row=0,padx=5,pady=5)

# create a download button
download_button = ctk.CTkButton(btn_frame, text="Download", command=download_video)
download_button.grid(column=2,row=0,padx=5,pady=5)

# create a label and the progress bar to display the download progress
progress_label = ctk.CTkLabel(left_frame_a, text="0%")
#progress_label.pack(pady=("10p", "5p"))

progress_bar = ctk.CTkProgressBar(left_frame_a, width=400)
progress_bar.set(0)
#progress_bar.pack(pady=("10p", "5p"))

# create the status label
status_label = ctk.CTkLabel(left_frame_a, text="")
#status_label.pack(pady=("10p", "5p"))

###################### Detalhes ######################
detalhes_pesquisa_frame = ctk.CTkFrame(pesquisa_frame, width=710, height=230)
detalhes_pesquisa_frame.grid(column=0,row=0,padx=5,pady=5)
 
treeview=ttk.Treeview(detalhes_pesquisa_frame,columns=("id","titulo","thumbnail","url"), show="headings")
treeview.place(x=5,y=5,width=690,height=220)

treeview.column("id",minwidth=0,width=50)
treeview.column("titulo",minwidth=0,width=50)
treeview.column("thumbnail",minwidth=0,width=50)
treeview.column("url",minwidth=0,width=50)

treeview.heading("id",text="ID")
treeview.heading("titulo",text="Titulo")
treeview.heading("thumbnail",text="Thumbnail")
treeview.heading("url",text="Url")

barra = ttk.Scrollbar(detalhes_pesquisa_frame, orient="vertical", command=treeview.yview)
barra.place(x=695,y=5,height=220)
treeview.configure(yscrollcommand=barra.set)
popularTreeview()

treeview.bind("<ButtonRelease-1>", itemSelectTreeview)

itens_pesquisa_frame = ctk.CTkFrame(pesquisa_frame)
itens_pesquisa_frame.grid(column=0,row=1,padx=5)

imagem=PhotoImage(file="image.png")
logo_label=Label(itens_pesquisa_frame,image=imagem)
logo_label.pack(padx=30,pady=5)

# to start the app
root.mainloop()

