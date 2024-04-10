import streamlit as st
import pandas as pd
import gridfs
import json

from utils import get_data, get_all_data, put_data, init_connection

st.set_page_config(page_title="Project Assessor Tool", layout="wide") 

st.header("Question Pool")

try:
    with st.container(border=True):

        data = pd.DataFrame(get_all_data(st.session_state['map_collection']))

        opts = ["",'Mr. Olorunniwo', 'Mr. Aransiola', 'Dr. Obayiuwana', 'Dr. Yesufu', 'Dr. Ariyo', 'Dr. Ogunseye', 'Mr. Olayiwola', 'Dr. Ayodele', 'Dr. Ilori', 'Mr. Akinboboye', 'Dr. Olawole', 'Dr. Babalola', 'Dr. Ogunba', 'Dr. Fisusi', 'Dr. Jubril']

        assessor = st.selectbox('Assessor', options=opts, index=0, key='asse')

        matric_number = st.selectbox(f'Students in group :red[{int(list(set(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna().Group))[0]) if assessor else ""}]', options=[""]+list(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna()._id))

        uid = f'{assessor}-{matric_number}'

        title = get_data(matric_number, st.session_state['map_collection']).get('Title', "")

        st.markdown(f':red[Title: {title}]')

        question_obj = get_data(uid, st.session_state['question_collection'])

        questions = st.text_area(f'Generate questions here, after reading the report submitted by {matric_number}', value= question_obj['questions'] if question_obj else "")

        quest = {'questions': questions, 'title': title.strip()}

        if st.button('Save', type="primary"):
            put_data(uid, st.session_state['question_collection'], quest)
        
except:
    st.switch_page('information.py')