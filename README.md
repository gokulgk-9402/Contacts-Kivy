# ContaX App

This is an application that I created to get, post, put, delete data to the API I have created before ([Contact manager](https://github.com/gokulgk-9402/ContactManager)) The API uses django rest framework with Token Authorization. This application uses [kivymd](https://kivymd.readthedocs.io/en/latest/) which is a collection of Material Design compliant widgets for use with the popular cross-platform graphical framework, Kivy.

## Screens:
1) Login
2) Register
3) Contact-List
4) Contact-Details
5) Add Contact
6) Edit Contact

along with some dialog corresponding to different actions.
You can find the screenshots under the `sample` directory.

## Overview:
* As soon as you launch the app, you will be prompted to enter your login credentials (same as the one used in the [website](https://contaxmanagerapp.herokuapp.com/)). In case you don't have an account already, you can register for a new account by providing the required details.
* An API request is made to the API with the login credentials you entered here, if they are correct, the API returns your unique API token, which can be used to retrieve your contacts.
* I have used kivymd's list which works particularly well with scrollview, as I thought it was perfect for the list of contacts screen. I have used 2 line list item, first line - Contact Name, second line - Description.
* Once you click on a contact, the contact details screen opens up, you can either copy or edit contact details, or even delete the contact in this screen.
* In the contact list screen, there's an option to add a new contact.
* In each screen required dialogs are displayed accordingly (for example, confirm delete, invalid data for contact details, not filling both fields in login screen, etc.)
* Clicking on a field of the contact-details screen, copies the data of the field to your clipboard.
  
## Learnings:
* This project helped me in applying things I learnt in REST.
* I faced a number of problems (like which widget to use for what, positions, passing arguments to on_release functions, etc.) and those helped me learn a lot.

## Requirements:
* The requirements of this code can be found in the file `requirements.txt`.

## Shortcomings:
* I still haven't implemented change password function in the app, but it's there in the website.
* I am still not sure about adding a search field.