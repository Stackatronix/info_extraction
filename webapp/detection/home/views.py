from django.shortcuts import render,redirect
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
from django.urls import path
import os
from home import textfns, face_identify, detecting_images

import json
import spacy
from home import face_identify

from transformers import pipeline # type: ignore
from spacy_entity_linker import EntityLinker #type: ignore
import stanza # type: ignore


# stanza.download('en')
# Load NLP model
nlp = spacy.load("en_core_web_sm")
# ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
# nlpStanza = stanza.Pipeline('en', processors='tokenize,ner')
# nlpStanza = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse,ner')
imgs= {}
excel = {}

entities = {}
import spacy

# Load the spaCy model (Make sure you have the model installed, e.g., `en_core_web_sm`)
nlp = spacy.load('en_core_web_sm')

def extract_named_entities(text):
    doc = nlp(text)
    current_person = None
    
    # Loop through the sentences (using 'sents' instead of 'sentences')
    for sent in doc.sents:
        for ent in sent.ents:
            # If the entity is a person, set it as the current person
            if ent.label_ == "PERSON":
                current_person = ent.text
                if current_person not in entities:
                    entities[current_person] = {}
            # Assign attributes like dates, locations, or any additional details
            elif current_person:
                if ent.label_ in ["DATE", "TIME", "GPE", "QUANTITY"]:
                    entities[current_person][ent.label_] = entities[current_person].get(ent.label_, []) + [ent.text]

        # Check sentences manually for explicit attributes like Height or Gender
        if current_person:
            sentence_text = sent.text.lower()
            if "height" in sentence_text:
                entities[current_person]["Height"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
            if "weight" in sentence_text:
                entities[current_person]["Weight"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
            if "gender" in sentence_text:
                entities[current_person]["Gender"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
            if "alias" in sentence_text:
                entities[current_person]["Alias"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text

    return entities



# def summarize_text(text):
#     """Generate a summary of the text."""
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
#     return summary[0]["summary_text"]


def home(request):
    mydata=MyFileUpload.objects.all()
    myform=MyFileForm()

    if mydata!='':
        context={'form':myform,'mydata':mydata}
        return render(request,'index.html',context)
    else:    
        context={'form':myform}
        return render(request,'index.html',context)
    

# functions for each file type
def process_text_file(file_path):
    text  = textfns.extract_text_from_txt(file_path)
    extract_named_entities(text)
    print(f"Processing text file: {file_path}")

def process_pdf_file(file_path):
    text = textfns.extract_text_from_pdf(file_path)
    extract_named_entities(text)
    print(f"Processing text file: {file_path}")

def process_doc_file(file_path):
    text  = textfns.extract_text_from_docx(file_path)
    extract_named_entities(text)
    print(f"Processing doc file: {file_path}")





def process_image_file(file_path):
    x = detecting_images.detect_objects_in_photo(file_path)
    print(x)
    if x == file_path:
        if 'img' in imgs:
            imgs['img'].append(x)
        else:
            imgs['img'] = [x]
    else:
        print(face_identify.face_idf(file_path))
    
    print(f"Processing image file: {file_path}")

def process_excel_file(file_path):
    text=textfns.extract_text_from_excel(file_path)
    if 'excel info' in excel:
        excel['excel info'].append(text)
    else:
        excel['excel info'] = [text]
    print(f"Processing doc file: {file_path}")

def process_unknown_file(file_path):
    print(f"Unknown file type: {file_path}")

# Map extensions to functions
file_handlers = {
    ".txt": process_text_file,
    ".pdf": process_pdf_file,
    ".jpeg": process_image_file,
    ".jpg": process_image_file,
    ".png": process_image_file,
    ".docx": process_doc_file,
    ".xlsx":process_excel_file,
}

# Get file paths from the folder
def get_file_paths(folder_path):
    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file))
    ]

# Process files by their extensions
def process_files_in_folder(folder_path):
    file_paths = get_file_paths(folder_path)
    print(file_paths)
    for file_path in file_paths:
        extension = os.path.splitext(file_path)[1].lower()  # Get file extension in lowercase
        handler = file_handlers.get(extension, process_unknown_file)  # Get corresponding function
        handler(file_path) 

def success(request):
    folder_path = "media/"
    process_files_in_folder(folder_path)
    
    response = render(request, 'success.html',{'imgs':imgs, 'entities':entities, 'excel':excel})
    imgs.clear()
    entities.clear()
    return response


def uploadfile(request):
    if request.method=="POST":    
        myform=MyFileForm(request.POST,request.FILES)               
        if myform.is_valid():  
            for MyFile in request.FILES.getlist('file'):                        
                exists=MyFileUpload.objects.filter(my_file=MyFile).exists()
                if exists:
                    data=1
                else:
                    data=0
                    MyFileUpload.objects.create(my_file=MyFile).save()  
            if data==1:                
                messages.error(request,'The file already exists...!!!')
            else:
                messages.success(request,"File uploaded successfully.")
            return redirect('home')

def deletefile(request,id):
    mydata=MyFileUpload.objects.get(id=id)    
    mydata.delete()    
    os.remove(mydata.my_file.path)
    messages.success(request,'File deleted successfully.')  
    return redirect('home')

def delete_all(request):
    if request.method=="POST":
        my_id=request.POST.getlist('id[]')
        for id in my_id:
            data = MyFileUpload.objects.get(id=id)
            data.delete()
            os.remove(data.my_file.path)
        messages.success(request,'File deleted successfully.')  
        return redirect('home')   

# with open("static\JSON\data.json", "w") as f:
#     json.dump(data, f)