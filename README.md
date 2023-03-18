# Data app for New York motor vehicle collisions


This project is a Streamlit web application that displays an interactive map of earthquake data using PyDeck, Pandas, and NumPy.

## Installation
To run this project locally, you need to follow these steps:

1. Clone this repository
2. Create a virtual environment
3. Install the required packages listed in requirements.txt
4. Run the app.py file using the command streamlit run app.py

## Technologies Used
### Streamlit
Streamlit is a Python library that allows you to create interactive web applications with just a few lines of code. It is built on top of Flask, and provides a simple way to create data-driven web applications.

In this project, Streamlit is used to create the user interface, load the earthquake data, and display the interactive map.

## PyDeck
PyDeck is a Python library for creating visualizations using the Deck.gl library. It allows you to create interactive maps, scatterplots, and other types of visualizations with just a few lines of code.

In this project, PyDeck is used to create the interactive map of earthquake data.

## Pandas
Pandas is a Python library for data manipulation and analysis. It provides data structures for efficiently storing and manipulating large datasets, as well as tools for data cleaning, transformation, and analysis.

In this project, Pandas is used to load the earthquake data, clean and transform it, and prepare it for visualization using PyDeck.

## NumPy
NumPy is a Python library for scientific computing. It provides tools for working with arrays and matrices, and for performing mathematical operations on them.

In this project, NumPy is used to calculate the magnitude and depth of each earthquake, which are used for visualization on the PyDeck map.

### Acknowledgements
This project was inspired by the Streamlit tutorial and the Deck.gl earthquake example. The earthquake data is sourced from the USGS Earthquake Catalog.
