import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils import get_data, get_all_data, put_data, init_connection, img_to_html


st.set_page_config(page_title="Project Assessor Tool", layout="wide") 

if 'client' not in st.session_state:
    st.session_state['client'] = init_connection()
    
if 'db' not in st.session_state:
    st.session_state['db'] = st.session_state['client'].capstoneDB

# if 'collection' not in st.session_state:
#     st.session_state['collection'] = 'title_information_form'
    
if 'map_collection' not in st.session_state:
    st.session_state['map_collection'] = 'mapper'#'student_staff_map'

if 'score_collection' not in st.session_state:
    st.session_state['score_collection'] = 'score'#'student_staff_map'
    
if 'question_collection' not in st.session_state:
    st.session_state['question_collection'] = 'question'#'student_staff_map'
    
if 'super_score_collection' not in st.session_state:
    st.session_state['super_score_collection'] = 'supervisorScore'#'student_staff_map'
    

arr = []

for x in get_all_data(st.session_state['map_collection']):
    arr.append(x.get('Readiness', 0))

fig, ax = plt.subplots(figsize=(5, 3))
ax.hist(arr, bins=11, align='mid')

# readiness = st.pyplot(fig)

st.header("Information Board")

tab1, tab2 = st.tabs(["Information", "Distribution Table"])


with tab1:
    with st.container(border=True):

        st.markdown("""
        ## Information for the staff Members:

        - You could download the report and the posters for each student you are required to assess by :red[Thursday $11^{th}$ of April 2024]
        - You could download the files using the "file download" menu: just filter the list of students with assessor's name
        - You could prepare a question pool for each student using the "question pool" menu
        - Scores and feedbacks could either be uploaded or recorded directly on the app
            - You will (at the minimum) need to score the qualities of the posters and reports before the presentation using this app
        - Each poster presentation transaction between an assessor and the student should not take more than 10 mins: 5 minutes for the presentation and 5 for question and answers
        - Note that you can download and use the score sheets from the scores menu instead of filling scores online

        ## Information to the Students:

        - Please be aware that :red[EEE501 defense] for the 2022/2023 academic session will take place on :red[Tuesday $16^{th}$ and Wednesday $17^{th}$] of the month of April 2024
        - It shall take the form of a poster presentation (see the poster template below) where the assessors and passerbys will have the chance to interact with the presenters
        - You will also need to write a concise report (3 to 5 pages) on your work (see the report link below)
        - Both the report and the poster are to be submitted with file upload menu, on or before :red[midnight Thursday $11^{th}$ of April 2024].
        - You can download the files using the file download menu on the top left: just filter the list of students with assessor's name
        - Each poster presentation transaction between an assessor and the student should not take more than 10 mins: 5 minutes for the presentation and 5 for question and answers
        - You are required to print the poster on an A1 paper

        ## Material Links:

        - This is the link to the poster template (look for the poster named :red[Kensington.pptx]): https://www.posterpresentations.com/free-poster-templates.html
        - This is the link to the report template: https://drive.google.com/file/d/1yLS-4gloZyNICn6eAJjDnM-AdGSjKSes/view?usp=sharing
        - You might need to compile the latex output with TexMaker (https://www.xm1math.net/texmaker/) or any other tool you are comfortable with
        - Download the score sheet from here:


        ## Presentation Tutorials: 

        - https://www.youtube.com/watch?v=vMSaFUrk-FA
        - https://www.youtube.com/watch?v=r0ezNEDWAiE

        ## Student readiness for project defence at a glance:

        """)

        st.markdown(img_to_html(fig), unsafe_allow_html=True)
        
with tab2:
    with st.container(border=True):
        st.dataframe(get_all_data(st.session_state['map_collection']), height=1000)
        
            


   