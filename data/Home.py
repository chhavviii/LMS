# import streamlit as st
# import os

# def load_home_tab(df):
#     st.title("Course Recommendation App")
#     # Inject CSS for styling without background image
#     st.markdown(
#         f"""
#         <style>
#         .main > div {{
#             background-color: rgba(255, 255, 255, 0.85);
#             padding: 2rem;
#             border-radius: 10px;
#             margin-top: 1rem;
#             box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

    
#     st.markdown("### 🔍 Preview of Available Courses")
#     st.dataframe(df[['course_title', 'subject', 'level', 'price', 'num_subscribers']].head(10))


import streamlit as st
import os
import base64
import pandas as pd  # Assuming you're passing a DataFrame to this function

def load_home_tab(df):
    st.title("Course Recommendation App")

    # Image paths (make sure these images exist in the 'image' folder)
    image_folder = os.path.join(os.path.dirname(__file__), 'image')
    image_files = ['Business_Finance.gif', 'Graphic_Design.gif', 'Musical_Instruments.gif', 'Web_Dev.gif']
    image_titles = ['Business Finance', 'Graphic Design', 'Musical Instruments', 'Web Development']
    image_paths = [os.path.join(image_folder, file) for file in image_files]

    # Create a 4-column layout to simulate a carousel
    st.markdown("### Course Highlights")
    cols = st.columns(4)
    for i, col in enumerate(cols):
        try:
            base64_gif = image_to_base64(image_paths[i])
            gif_html = f'''
                <style>
                    .hover-img {{
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        border-radius: 10px;
                    }}
                    .hover-img:hover {{
                        transform: scale(1.1);
                        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                    }}
                    .image-caption {{
                        text-align: center;
                        font-size: 16px;
                        margin-top: 8px;
                        font-weight: 500;
                    }}
                </style>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="data:image/gif;base64,{base64_gif}" class="hover-img" style="height: 180px; width: auto;" />
                    <div class="image-caption">{image_titles[i]}</div>
                </div>
            '''
            col.markdown(gif_html, unsafe_allow_html=True)
        except Exception as e:
            col.warning(f"Image not found or failed to load: {image_files[i]}")

    # Styling for the content area
    st.markdown(
        """
        <style>
        .main > div {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
            margin-top: 1rem;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display a preview of courses
    st.markdown("### 🔍 Preview of Available Courses")
    st.dataframe(df[['course_title', 'subject', 'level', 'price', 'num_subscribers']].head(10))


# Convert image to base64 (works with GIFs)
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
