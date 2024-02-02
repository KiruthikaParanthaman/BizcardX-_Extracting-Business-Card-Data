# BizcardX-_Extracting-Business-Card-Data
Bizcardx Application is an Business Card Reader which extracts text details from the visiting card image like Name,Designation,Company name, Address,phone number, Mail address and Website address.

**Problem Statement:**
1. upload an image of a business card and extract relevant information from it using easyOCR.
2. Extracted information should include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state,
   and pin code.
3. Allow users to save the extracted information into a database along with the uploaded business card image
4. Allow the user to Read the data, Update the data and Allow the user to delete the data

**Tools Used:**
Python - pandas, cv2, easyocr, re(regex) , Sqlalchemy, Pathlib , Numpy, Mysql database,  Streamlit

**End Product :**
![app_scrnshot](https://github.com/KiruthikaParanthaman/BizcardX-_Extracting-Business-Card-Data/assets/141828622/0cf3205c-bba0-475a-aaf2-457275871e23)

**Home Menu**
In the home menu users will be able to upload images.After image upload, extracted details will be dispalyed on the right side of screen along with processed image with bounding box around text and original image below it in left side of the screen. The users will also be able to modify the details if any and click save to save the extacted details along with image path in Mysqldb

**Modify Menu**
In the modify screen, list of saved cardholders name will be displayed. Users can select one and click Edit. On clicking edit button, the details to be edited along with visiting card image will be displayed from database and modification if any can be undertaken. After editing, users should click save button at the end to update the changes

**Delete Button**
In the delete screen, list of saved cardholders name will be displayed. Users can select cardholder name to permananently delete the records.

**Challenges**
1. Storing uploaded business card image in Mysql :
   **Approach :** Uploaded image was read using cv2 and then pathlib library was used to write the uploaded file in designated directory in local hard disk. The uploaded image path is then appended in Mysql database for future retrieval/display

2. Classifying extracted texts in required category:
   **Approach :** For categories with pattern like Pincode, Phone number, web address and email address regex was used to match patterns. The vertical bounding box parameter y_ths in easyocr is used to extract name and Designation.

