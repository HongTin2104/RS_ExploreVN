# Vietnam Travel Recommendation System

## Overview

The Vietnam Travel Recommendation System is a web application built using Streamlit that assists users in discovering suitable travel destinations in Vietnam based on their interests. By entering keywords related to their preferences, users receive personalized recommendations along with relevant information such as weather conditions and images of the locations.

## Features

- **Keyword-Based Recommendations:** Users can input three keywords to receive tailored travel destination suggestions.
- **Weather Information:** The application fetches real-time weather data for the recommended locations.
- **Image Display:** Each recommended location is accompanied by an image for better visualization.
- **Vietnamese Language Support:** The application includes Vietnamese translations for weather descriptions.

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Manipulation:** Pandas
- **Natural Language Processing:** Underthesea (for Vietnamese word tokenization)
- **Machine Learning:** Scikit-learn (for TF-IDF and cosine similarity)
- **API Requests:** Requests (for fetching weather data)
- **Translation:** Google Translate API (for translating weather descriptions)

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/HongTin2104/VietNam-Travel-Recommendation-System.git
   cd VietNam-Travel-Recommendation-System

2. Install the required packages:
    ```bash
    pip install -r requirements.txt

3. Obtain an API key from OpenWeatherMap and save it in a file named api_key in the root directory.

4. Prepare your data:
- Ensure you have an Excel data file named data.xlsx in the root directory, containing a column named "Mô tả" for descriptions of the travel destinations.


## Usage

1. Run the application:
    ```bash
    streamlit run app.py

2. Open your web browser and navigate to http://localhost:8501 to access the application.

3. Enter three keywords related to your interests (e.g., beach, mountain, culture) and click "Submit" to receive recommendations.

## Example

https://github.com/user-attachments/assets/b5e01e5b-427d-41b4-80dd-8d96100608df



