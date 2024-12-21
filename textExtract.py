import re
import spacy
from PyPDF2 import PdfReader
from transformers import pipeline
from spacy_entity_linker import EntityLinker
from transformers import pipeline
import stanza


# stanza.download('en')
# Load NLP model
nlp = spacy.load("en_core_web_sm")
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
# nlpStanza = stanza.Pipeline('en', processors='tokenize,ner')
nlpStanza = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma,depparse,ner')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    # print(text)
    return text

def extract_named_entities(text):
    """Extract named entities using SpaCy."""
    # doc = nlp(text)
    # entities = {"PERSON": [], "EVENT": [], "GPE": []}  # GPE: Geopolitical entity (places)
    # for ent in doc.ents:
    #     if ent.label_ in entities:
    #         entities[ent.label_].append(ent.text)
    # # Remove duplicates
    # for key in entities:
    #     entities[key] = list(set(entities[key]))
    # return entities

    # entities = ner_model(text)
    # for entity in entities:
    #     print(f"Entity: {entity['word']}, Label: {entity['entity']}, Score: {entity['score']}")
    # return entities

    # related_info = {}
    # current_person = None
    doc = nlpStanza(text)
    # return doc

    entities = {}
    current_person = None

    for sentence in doc.sentences:
        for ent in sentence.ents:
            # If the entity is a person, set it as the current person
            if ent.type == "PERSON":
                current_person = ent.text
                if current_person not in entities:
                    entities[current_person] = {}
            # Assign attributes like dates, locations, or any additional details
            elif current_person:
                if ent.type in ["DATE", "TIME", "GPE", "QUANTITY"]:
                    entities[current_person][ent.type] = entities[current_person].get(ent.type, []) + [ent.text]

        # Check sentences manually for explicit attributes like Height or Gender
        if current_person:
            sentence_text = sentence.text.lower()
            if "height" in sentence_text:
                entities[current_person]["Height"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
            if "weight" in sentence_text:
                entities[current_person]["Weight"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
            if "gender" in sentence_text:
                entities[current_person]["Gender"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text
            if "alias" in sentence_text:
                entities[current_person]["Alias"] = sentence_text.split(":")[1].strip() if ":" in sentence_text else sentence_text

    print('----------------------')
    print(entities)
    return entities


def summarize_text(text):
    """Generate a summary of the text."""
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]["summary_text"]

def extract_and_summarize(pdf_path):
    """Extract entities and summarize connections from a PDF."""
    text = extract_text_from_pdf(pdf_path)
    entities = extract_named_entities(text)
    summary = summarize_text(text)

    return {
        "summary": summary,
        "entities": entities
    }

# Example usage
if __name__ == "__main__":
    pdf_path = "D:\\kandupidtham\\ArjunProjectDefense\\textdata\\pdf\\biodata.pdf"  # Replace with your PDF file path
    result = extract_and_summarize(pdf_path)
    
    print("Extracted Entities:")
    # for entity_type, values in result["entities"].items():
    #     print(f"{entity_type}: {', '.join(values)}")
    persons = []
    locations = []
    Organization = []
    WORK_OF_ART = []
    # for ent in result["entities"].ents:
    #     if ent.type == 'PERSON':
    #         persons.append(ent.text)
    #     elif ent.type == 'GPE':
    #         locations.append(ent.text)
    #     elif ent.type == 'ORG':
    #         Organization.append(ent.text)
    #     elif ent.type == 'WORK_OF_ART':
    #         WORK_OF_ART.append(ent.text)
        
        # print(f"Entity: {ent.text}, Label: {ent.type}")
    
    print("\nSummary:")
    print(result["summary"])

    print('-------------------------------')
    print(persons)
    print(locations)
    print(Organization)
    print(WORK_OF_ART)
