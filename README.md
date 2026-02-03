# Tamunjya.com – Nepal Bhasa Literary Event Website

**Tamunjya.com** is a production-ready website built using **Django** and **Wagtail CMS** for managing and publishing content related to the annual *Nepal Bhasa Sahitya Tamunjya* (Nepal Bhasa Literary Festival).

The project focuses on a CMS-driven architecture that allows non-technical editors to manage yearly events, organizers, winners, media, news, and venue information efficiently.

🔗 **Live Website:** https://tamunjya.com

---

## Tech Stack

- **Backend:** Django
- **CMS:** Wagtail
- **Database:** PostgreSQL / SQLite (development)
- **Frontend:** HTML, Bootstrap 5, CSS, JavaScript
- **Media:** Wagtail Images & Collections
- **API Integration:** YouTube Data API v3
- **Caching:** Django Cache Framework

---

## Key Features

- **Year-based event pages** with easy switching between different years
- **Organizer & member management** using Wagtail Inline Panels
- **Literary & cultural winner sections** with nested category-based data
- **Photo albums** powered by Wagtail image collections
- **YouTube playlist integration** with API response caching
- **News module** with “View More” functionality
- **Venue section** with Google Maps embed and external links
- **Dynamic footer content** editable from the CMS

---

## Wagtail CMS Highlights

- Custom `Page` models with strict parent–child hierarchy
- Extensive use of:
  - `Orderable`
  - `ParentalKey`
  - `InlinePanel`
  - `TabbedInterface`
- Editor-friendly admin UI for content teams
- Clean separation of content management and frontend rendering

---

## Purpose of the Project

This project demonstrates real-world usage of **Django + Wagtail** for building a scalable, content-managed website with complex data relationships, media handling, and third-party API integration.

---

## Setup Instructions
- git clone https://github.com/Jenbati/Tamunjya-Wagtail.git
- cd Tamunjya-Wagtail
- python -m venv venv
- source venv/bin/activate  # Windows: venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver


## Author

**Jen Bati**  
