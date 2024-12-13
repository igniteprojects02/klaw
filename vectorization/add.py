
from .pdf_extract import extract_text_from_pdf  # to extract contents from pdf
from .chunks import create_chunks
from .create import access_collection
from datetime import datetime

import filetype

  
def add(dbname,file):



    # access a collection for storing your PDF data
    collection = access_collection(dbname)


    print(f"going to work on  database =  {dbname}")        
    print(f"going to work on  file =  {file}")            


    # extract data from pdf or txt file

    # Guess the file type using the filetype library
    kind = filetype.guess(file)
    
    
    # Check for PDF and text file types
    if kind.extension == 'pdf':
        print("file found to be pdf")

        text_data = extract_text_from_pdf(file)

        print("pdf data extracted")
    elif kind.mime == 'text/plain':
        print("file found to be txt")

        try:
            # Open the file in read mode
            with open(file, 'r') as files:
                # Read the contents of the file
                text_data = files.read()
        except FileNotFoundError:
            return "Error: The file was not found."
        except IOError:
            return "Error: An I/O error occurred."


        print("txt data extracted")
    
    else:
        print("No accepted file type")




    chunks = create_chunks(text_data) # created chunks of text data
    print("Created data chunks")





    # Get the current date and time
    now = datetime.now()

    # Format the date and time
    formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S")


    # Add extracted texts to the collection with unique IDs
    collection.add(                          # instructs ChromaDB to store new information 
        documents=chunks,             #  a list that contains the actual content you want to store.
        metadatas=[{"source": f"{dbname}"}]*len(chunks),  #  allows you to add extra information about each document being added
        ids=[f"{dbname}_{formatted_time}_{i}" for i in range(len(chunks))]  #assigns unique identifiers to each chunks of document being added.
    )
    print("Created the vectoriezed data successfully")
    return "Success"







