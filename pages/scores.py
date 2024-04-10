import streamlit as st
import pandas as pd
import gridfs
# import json

from utils import get_data, get_all_data, put_data, init_connection, get_question


st.set_page_config(page_title="Project Assessor Tool", layout="wide") 

st.header("Score Sheet")

try:

    with st.container(border=True):

        data = pd.DataFrame(get_all_data(st.session_state['map_collection']))

        opts = ["",'Mr. Olorunniwo', 'Mr. Aransiola', 'Dr. Obayiuwana', 'Dr. Yesufu', 'Dr. Ariyo', 'Dr. Ogunseye', 'Mr. Olayiwola', 'Dr. Ayodele', 'Dr. Ilori', 'Mr. Akinboboye', 'Dr. Olawole', 'Dr. Babalola', 'Dr. Ogunba', 'Dr. Fisusi', 'Dr. Jubril']

        assessor = st.selectbox('Assessor', options=opts, index=0, key='asse')

        matric_number = st.selectbox(f'Students in group :red[{int(list(set(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna().Group))[0]) if assessor else ""}]', options=[""]+list(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna()._id))

        uid = f'{assessor}-{matric_number}'

        title = get_data(matric_number, st.session_state['map_collection']).get('Title', "")
        supervisor = get_data(matric_number, st.session_state['map_collection']).get('Supervisor', "")

        score_obj = get_data(uid, st.session_state['score_collection'])

        if not score_obj:
            score_data = pd.DataFrame({"Title":title, 'Design(5)': [0], 'Implementation(5)': [0], 'Understanding(5)': [0], 'Quality of Presentation(5)': [0],  'Answer to Questions(8)': [0], 'Appearance(2)': [0], "Quality of Report and Poster(10)": [0],})
        else:
            score_data = pd.DataFrame(score_obj.get('score')[0], index=[0])

            # score_data = {"Title":title, 'Design (8)': 0, 'Implementation (8)': 0, 'State of Project (5)': 0, 'Quality of Presentation (8)': 0, 'Understanding (10)': 0, 'Answer to Questions (10)': 0, 'Appearance (1)': 0}

        score = st.data_editor(
            score_data,
            use_container_width=True,
            # width=1200,
            column_config={
                "Title": st.column_config.TextColumn(required=True),
                "Design(5)":  st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
                "Implementation(5)":  st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
                "Understanding(5)": st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
                "Quality of Presentation(5)": st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
                "Answer to Questions(8)":st.column_config.NumberColumn(required=True, min_value=0, max_value=8, step=0.1),
                "Appearance(2)": st.column_config.NumberColumn(required=True, min_value=0, max_value=2, step=0.1),
                "Quality of Report and Poster(10)": st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
            },
            hide_index=True,

            # key=matric_number,
            # on_change=update_product_table
            )

        feedback = st.text_area(f'Enter feedback for {matric_number}', value= score_obj['feedback'] if score_obj else "")

        comment = st.text_area(f'Enter comment for {supervisor}', value= score_obj['comment'] if score_obj else "")

        score_fc = {'score':score.to_dict('records'), 'feedback': feedback, 'comment': comment}

        if st.button('Save', type="primary"):
            put_data(uid, st.session_state['score_collection'], score_fc)

    title

    with st.container(border=True):
        st.text_area(f'Questions for the title: :red[{title}]', get_question(st.session_state['question_collection'], title).get('questions', "") if title else "")
        # st.text_area(f'Questions for the title: :red[{title}]', st.session_state['db'][st.session_state['question_collection']].find_one({'title':title.strip()}).get('questions', "") if title else "")

except:
    st.switch_page('information.py')

#Demonstration: a practical exhibition and explanation of how something works or is performed i.e. understanding of how something works

#Implementation:
# Attention to detail
# Communication
# Problem solving
# Innovation