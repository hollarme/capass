import streamlit as st
import pandas as pd
import gridfs
# import json

from utils import get_data, get_all_data, put_data, init_connection, get_question


st.set_page_config(page_title="Project Assessor Tool", layout="wide") 

st.header("Score Sheet")


try:
    
    score_for = st.sidebar.radio(
    "",
    [":red[Defence Score Sheet]", ":blue[Supervisor Score Sheet]"],
    captions = ["Enter scores for student in your defence group", "Enter scores for students you supervised"])


    data = pd.DataFrame(get_all_data(st.session_state['map_collection']))

    if score_for == ":red[Defence Score Sheet]":

        opts = ["",'Mr. O. Olorunniwo', 'Dr. A. Aransiola', 'Dr. E. Obayiuwana', 'Prof. T. K. Yesufu', 'Dr. F. K. Ariyo', 'Dr. A. A. Ogunseye', 'Mr. Olayiwola Pipelolu', 'Dr. K. P. Ayodele', 'Dr. O. Ilori', 'Mr. E. Akinboboye', 'Dr. A. A. Olawole', 'Dr. A. A. Fisusi', 'Dr. A. M. Jubril']

        with st.status("", expanded=True) as status:
            with st.container(border=True):

                assessor = st.selectbox('Assessor', options=opts, index=0, key='asse')

                students_in_group = sorted(list(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna(how='all')._id))
                
                
                matric_number = st.selectbox(f'Students in group :red[{int(list(set(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna(how="all").Group))[0]) if assessor else ""}]', options=[""]+students_in_group)
                
                st.caption(f"Student Names: :orange[{get_data(matric_number, st.session_state['map_collection']).get('Names', '')}]")

#                 uid = f'{assessor}-{matric_number}'

#                 title = get_data(matric_number, st.session_state['map_collection']).get('Title', "")
#                 supervisor = get_data(matric_number, st.session_state['map_collection']).get('Supervisor', "")

#                 score_obj = get_data(uid, st.session_state['score_collection'])

#                 if not score_obj:
#                     score_data = pd.DataFrame({"Title":title, 'Design(5)': [0], 'Implementation(5)': [0], 'Understanding(5)': [0], 'Quality of Presentation(5)': [0],  'Answer to Questions(8)': [0], 'Appearance(2)': [0], "Quality of Report and Poster(10)": [0],})
#                 else:
#                     score_data = pd.DataFrame(score_obj.get('score')[0], index=[0])

#                     # score_data = {"Title":title, 'Design (8)': 0, 'Implementation (8)': 0, 'State of Project (5)': 0, 'Quality of Presentation (8)': 0, 'Understanding (10)': 0, 'Answer to Questions (10)': 0, 'Appearance (1)': 0}

#                 score = st.data_editor(
#                     score_data,
#                     use_container_width=True,
#                     # width=1200,
#                     column_config={
#                         "Title": st.column_config.TextColumn(required=True),
#                         "Design(5)":  st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
#                         "Implementation(5)":  st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
#                         "Understanding(5)": st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
#                         "Quality of Presentation(5)": st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
#                         "Answer to Questions(8)":st.column_config.NumberColumn(required=True, min_value=0, max_value=8, step=0.1),
#                         "Appearance(2)": st.column_config.NumberColumn(required=True, min_value=0, max_value=2, step=0.1),
#                         "Quality of Report and Poster(10)": st.column_config.NumberColumn(required=True, min_value=0, max_value=5, step=0.1),
#                     },
#                     hide_index=True,

#                     # key=matric_number,
#                     # on_change=update_product_table
#                     )

#                 feedback = st.text_area(f'Enter feedback for {matric_number}', value= score_obj['feedback'] if score_obj else "")

#                 comment = st.text_area(f'Enter comment for {supervisor}', value= score_obj['comment'] if score_obj else "")

#                 score_fc = {'score':score.to_dict('records'), 'feedback': feedback, 'comment': comment}

#                 if st.button('Save', type="primary"):
#                     put_data(uid, st.session_state['score_collection'], score_fc)
#                     status.update(label="upload complete!", state="complete")


#             with st.container(border=True):
#                 st.text_area(f'Questions for the title: :red[{title}]', get_question(st.session_state['question_collection'], title.strip()).get('questions', "") if title else "")

                prows = []
                if assessor:
                    for student in students_in_group:
                        prows.append(
                            {"Registration No.": student, 
                             "Names":get_data(student, st.session_state['map_collection']).get('Names', ""), 
                             "Title":get_data(student, st.session_state['map_collection']).get('Title', ""), 
                             'Design(5)': '', 'Implementation(5)': '', 'Understanding(5)': '', 
                             'Quality of Presentation(5)': '',  'Answer to Questions(8)': '', 
                             'Appearance(2)': '', "Quality of Report and Poster(10)": ''
                            }
                                    )

                dsc = pd.DataFrame(prows).to_csv(index=False).encode('utf-8') if prows else ""

                # st.sidebar.caption("Pick an assessor's name")
                st.download_button("Download defence score sheet", dsc, file_name="defence_score_sheet.csv", type="primary", disabled= False if assessor else True)

    elif score_for == ":blue[Supervisor Score Sheet]":

        with st.status("", expanded=True) as status:
            with st.container(border=True):

                opts = ["",'Mr. O. Olorunniwo', 'Dr. A. Aransiola', 'Dr. E. Obayiuwana', 'Prof. T. K. Yesufu', 'Dr. F. K. Ariyo', 'Dr. A. A. Ogunseye', 'Mr. Olayiwola Pipelolu', 'Dr. K. P. Ayodele', 'Dr. O. Ilori', 'Mr. E. Akinboboye', 'Dr. A. A. Olawole', 'Dr. A. A. Fisusi', 'Dr. A. M. Jubril']

                supervisor = st.selectbox('Supervisor', options=opts, index=0, key='super')

                # data.where(data.Supervisor.str.fullmatch(supervisor, case=False)).dropna(how='all')[['_id', 'Title']]

                students_with_supervisor = sorted(list(data.where(data.Supervisor.str.fullmatch(supervisor, case=False)).dropna(how='all')._id))

                matric_number = st.selectbox(f'Students supervised by :red[{supervisor if supervisor else ""}]', options=[""]+students_with_supervisor)
                
                st.caption(f"Student Names: :orange[{get_data(matric_number, st.session_state['map_collection']).get('Names', '')}]")

#                 uid = f'{supervisor}-{matric_number}'

#                 title = get_data(matric_number, st.session_state['map_collection']).get('Title', "")
#                 # supervisor = get_data(matric_number, st.session_state['map_collection']).get('Supervisor', "")

#                 super_score_obj = get_data(uid, st.session_state['super_score_collection'])

#                 if not super_score_obj:
#                     super_score_data = pd.DataFrame({"Title":title, "Interaction(20)": [0], 'Understanding(10)': [0], 'State of Project(10)': [0],  "Dedication(10)": [0], "Quality of Report(10)": [0],})
#                 else:
#                     super_score_data = pd.DataFrame(super_score_obj.get('score')[0], index=[0])

#                     # score_data = {"Title":title, 'Design (8)': 0, 'Implementation (8)': 0, 'State of Project (5)': 0, 'Quality of Presentation (8)': 0, 'Understanding (10)': 0, 'Answer to Questions (10)': 0, 'Appearance (1)': 0}

#                 super_score = st.data_editor(
#                     super_score_data,
#                     use_container_width=True,
#                     # width=1200,
#                     column_config={
#                         "Title": st.column_config.TextColumn(required=True),
#                         "Interaction(20)":  st.column_config.NumberColumn(required=True, min_value=0, max_value=20, step=0.1),
#                         "Understanding(10)": st.column_config.NumberColumn(required=True, min_value=0, max_value=10, step=0.1),
#                         "State of Project(10)": st.column_config.NumberColumn(required=True, min_value=0, max_value=10, step=0.1),
#                         "Dedication(10)":st.column_config.NumberColumn(required=True, min_value=0, max_value=10, step=0.1),
#                         "Quality of Report(10)": st.column_config.NumberColumn(required=True, min_value=0, max_value=10, step=0.1),
#                     },
#                     hide_index=True,

#                     # key=matric_number,
#                     # on_change=update_product_table
#                     )

#                 feedback = st.text_area(f'Enter feedback for {matric_number}', value= super_score_obj['feedback'] if super_score_obj else "")

#                 super_score_f = {'score':super_score.to_dict('records'), 'feedback': feedback}

#                 if st.button('Save', type="primary"):
#                     put_data(uid, st.session_state['super_score_collection'], super_score_f)
#                     status.update(label="upload complete!", state="complete")

                prows = []
                if supervisor:
                    for student in students_with_supervisor:
                        prows.append(
                            {"Registration No.": student, 
                             "Names":get_data(student, st.session_state['map_collection']).get('Names', ""), 
                             "Title":get_data(student, st.session_state['map_collection']).get('Title', ""), 
                             "Interaction(20)": '', 'Understanding(10)': '', 'State of Project(10)': '',  
                             "Dedication(10)": '', "Quality of Report(10)": ''
                            }
                                    )

                dsc = pd.DataFrame(prows).to_csv(index=False).encode('utf-8') if prows else ""

                # st.sidebar.caption("Pick a supervisor's name")
                st.download_button("Download supervisor score sheet", dsc, file_name='supervisor_score_sheet.csv', type="primary", disabled= False if supervisor else True)


except:
    st.switch_page('Information.py')




#Demonstration: a practical exhibition and explanation of how something works or is performed i.e. understanding of how something works

#Implementation:
# Attention to detail
# Communication
# Problem solving
# Innovation