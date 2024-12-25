from django.shortcuts import render,redirect
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
from django.urls import path
import os
from home import textfns, face_identify, detecting_images

import json
import spacy

from transformers import pipeline # type: ignore
from spacy_entity_linker import EntityLinker #type: ignore
import stanza # type: ignore


# stanza.download('en')
# Load NLP model
nlp = spacy.load("en_core_web_sm")
# ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
# nlpStanza = stanza.Pipeline('en', processors='tokenize,ner')
# nlpStanza = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse,ner')

data= {}
file_context= {}
file_info={}

def extract_named_entities(text):
    # nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        
        entities.append({"text": ent.text, "label": ent.label_})
    return entities






    # doc = nlpStanza(text)
    # print(doc)
    # entities = {}
    # current_person = None

    # for sentence in doc.sentences:
    #     for ent in sentence.ents:
    #         # If the entity is a person, set it as the current person
    #         if ent.type == "PERSON":
    #             current_person = ent.text
    #             if current_person not in entities:
    #                 entities[current_person] = {}
    #         # Assign attributes like dates, locations, or any additional details
    #         elif current_person:
    #             if ent.type in ["DATE", "TIME", "GPE", "QUANTITY"]:
    #                 entities[current_person][ent.type] = entities[current_person].get(ent.type, []) + [ent.text]

    #     # Check sentences manually for explicit attributes like Height or Gender
    #     if current_person:
    #         sentence_text = sentence.text.lower()
    #         if "height" in sentence_text:
    #             entities[current_person]["Height"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
    #         if "weight" in sentence_text:
    #             entities[current_person]["Weight"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
    #         if "gender" in sentence_text:
    #             entities[current_person]["Gender"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
    #         if "alias" in sentence_text:
    #             entities[current_person]["Alias"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text

    # print(entities)
    # return entities


# def summarize_text(text):
#     """Generate a summary of the text."""
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
#     return summary[0]["summary_text"]

def extract_and_summarize_pdf(pdf_path):
    text = textfns.extract_text_from_pdf(pdf_path)
    entities = extract_named_entities(text)
    # summary = summarize_text(text)
    if "pdf" in file_context:
        file_context["pdf"].extend([entities])
    else:
        file_context["pdf"] = [entities]
    # return {
    #     "summary": summary,
    #     "entities": entities
    # }


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
    print(f"Processing text file: {file_path}")

def process_pdf_file(file_path):
    extract_and_summarize_pdf(file_path)
    print("processed")

def process_doc_file(file_path):
    print(f"Processing doc file: {file_path}")

def process_image_file(file_path):
    x = detecting_images.detect_objects_and_plot(file_path)
    # print(x)
    print(f"Processing image file: {file_path}")

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
    folder_path = "upload/"
    res = process_files_in_folder(folder_path)

    print(res)
    return render(request, 'success.html',file_context)


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