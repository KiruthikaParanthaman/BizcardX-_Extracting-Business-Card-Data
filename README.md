# BizcardX-_Extracting-Business-Card-Data
Bizcardx Application is an Business Card Reader which extracts text details from the visiting card image like Name,Designation,Company name, Address,phone number, Mail address and Website address.

**Problem Statement:**
1. upload an image of a business card and extract relevant information from it using easyOCR.
2. Extracted information should include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state,
   and pin code.
3. Allow users to save the extracted information into a database along with the uploaded business card image
4. Allow the user to Read the data, Update the data and Allow the user to delete the data

**Tools Used:**
Python - pandas, cv2, easyocr, Sqlalchemy, Pathlib , Numpy, Mysql database,  Streamlit

**End Product :**
![app_scrnshot](https://github.com/KiruthikaParanthaman/BizcardX-_Extracting-Business-Card-Data/assets/141828622/0cf3205c-bba0-475a-aaf2-457275871e23)

**Home Menu**
In the home menu users will be able to upload images.After image upload, extracted details will be dispalyed on the right side of screen along with processed image with bounding box around text and original image below it in left side of the screen. The users will also be able to modify the details if any and click save to save the extacted details along with image path in Mysqldb

**

