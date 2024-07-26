**Project Description:**

This project involves developing a pipeline to parse and organize various types of documents within an archive. The documents are consolidated into single files in a random order and may include:

Scanned Documents

Scanned Images

Programmatically Generated PDFs


**Summary**

The aim is to develop a pipeline to effectively parse and organize different types of documents (both scanned and programmatically generated) that are randomly consolidated into single files. 
This solution will handle various document types and structures, facilitating efficient data extraction and organization.

**Tasks:**

1. A function that takes a PDF file path as input and returns a dictionary of which page has to be rotated by which angle to be upright (OCR-parsable)

2. A function that classifies document pages into 3 categories:

   . Machine-readable PDF / searchable PDF
   
   . Image-based PDF which may be OCR’d
   
   . Image-based PDF which may not be OCR`d
