from duckduckgo_image_search import DuckDuckGoImageSearch
from fastduck import FastDuck


ducksearch = DuckDuckGoImageSearch()

us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
    "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
    "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

ducksearch = DuckDuckGoImageSearch(
    input_terms_or_urls=[], max_images=10, safesearch="off")

for state in us_states:
    search_term = f"{state} drivers license"
    try:
        ducksearch.download_images_for_term(search_term)
    except Exception as e:
        print(f"Error processing images for {state}: {e}")

# Verify and clean up the downloaded images
ducksearch.verify_and_clean()

# state_license_images = {}

# for state in us_states:
#     search_term = state + " drivers license"
#     ducksearch = DuckDuckGoImageSearch(
#         input_terms_or_urls=[search_term], max_images=10)
#     images = ducksearch.image_search(search_term, safesearch="off")
#     state_license_images[state] = images
