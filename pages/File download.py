import streamlit as st
import pandas as pd
import gridfs
from gridfs import errors
import zipfile
import io

from utils import get_data, get_all_data, put_data, init_connection


st.set_page_config(page_title="Project Assessor Tool", layout="centered") 

st.header("Download Files")

# try:

fs_report = gridfs.GridFS(st.session_state['db'], 'report')

fs_poster = gridfs.GridFS(st.session_state['db'], 'poster')

col1, col2 = st.columns([0.8, 0.2])

with col2:
    zipit = st.checkbox(':green[Zip files]', help='All student files linked to the assessor/supervisor will be downloaded into a folder')
    st.caption('You need to pick an assessor/supervisor')

with col1: 
    staff_status = st.sidebar.radio(
    "",
    [":red[Assessor]", ":blue[Supervisor]"],
    captions = ["Download files for students in your defence group", "Download files for students you supervised"])

    data = pd.DataFrame(get_all_data(st.session_state['map_collection']))

    if staff_status == ":red[Assessor]":
        with st.status("", expanded=True) as status:
            with st.container(border=True):

                tot = data.shape[0]

                # (len(fs_report.list())/tot)*100

                st.progress(len(fs_report.list())/tot, text=f'{len(fs_report.list())} reports submitted out of {tot}')
                st.progress(len(fs_poster.list())/tot, text=f'{len(fs_poster.list())} posters submitted out of {tot}')

                opts = ["",'Mr. Olorunniwo', 'Mr. Aransiola', 'Dr. Obayiuwana', 'Dr. Yesufu', 'Dr. Ariyo', 'Dr. Ogunseye', 'Mr. Olayiwola', 'Dr. Ayodele', 'Dr. Ilori', 'Mr. Akinboboye', 'Dr. Olawole', 'Dr. Babalola', 'Dr. Ogunba', 'Dr. Fisusi', 'Dr. Jubril']

                assessor = st.selectbox('Assessor', options=opts, index=0, key='superd')

                id_list = sorted(list(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna(how='all')._id))

                matric_number = st.selectbox(f'Students in group :red[{int(list(set(data.where(data.Assessors.str.contains(assessor, regex=False, case=False)).dropna(how="all").Group))[0]) if assessor else ""}]', options=[""]+id_list, disabled=True if zipit else False)

                if zipit:
                    # try:
                    zip_buf = io.BytesIO()
                    if assessor:
                        with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as myzip:
                            for _id in id_list:
                                try:
                                    myzip.writestr(f'{_id.replace("/","_")}_poster.pdf', fs_poster.get(_id).read())
                                except errors.NoFile: 
                                    st.info(f'Student with matric number {_id} has not submitted his/her poster', icon="ℹ️")                            
                    zip_buf.seek(0)

                    if st.download_button(f'download poster.zip', zip_buf if assessor else "", mime='text/pdf', disabled=True if not assessor else False, use_container_width=True, file_name=f'{assessor}_students_poster.zip'):
                        status.update(label="done downloading files...", state="complete")
                    # except:
                    #     st.warning('The student you selected is yet to upload the requested file', icon="⚠️")

                    # try:
                    zip_bufr = io.BytesIO()
                    if assessor:
                        with zipfile.ZipFile(zip_bufr, 'w', zipfile.ZIP_DEFLATED) as myzip:
                            for _id in id_list:
                                try:
                                    myzip.writestr(f'{_id.replace("/","_")}_report.pdf', fs_report.get(_id).read())
                                except errors.NoFile: 
                                    st.info(f'Student with matric number {_id} has not submitted his/her report', icon="ℹ️")  
                    zip_bufr.seek(0)

                    if st.download_button(f'download report.zip', zip_bufr if assessor else "", mime='text/pdf', disabled=True if not assessor else False, use_container_width=True, file_name=f'{assessor}_students_report.zip'):
                        status.update(label="done downloading files...", state="complete")

                else:

                    try:
                        if st.download_button(f'download poster.pdf', fs_poster.get(matric_number).read() if matric_number else "", mime='text/pdf', disabled=True if not matric_number else False, use_container_width=True, file_name=f'{matric_number}_poster.pdf'):
                            status.update(label="done downloading files...", state="complete")
                    except:
                        st.warning('The student you selected is yet to upload the requested file', icon="⚠️")

                    try:
                        if st.download_button(f'download report.pdf', fs_report.get(matric_number).read() if matric_number else "", file_name=f'{matric_number}_report.pdf', mime='text/pdf', disabled=True if not matric_number else False, use_container_width=True):
                            status.update(label="done downloading files...", state="complete")
                    except:
                        st.warning('The student you selected is yet to upload the requested file', icon="⚠️")

    else:
        with st.status("", expanded=True) as status:
            with st.container(border=True):

                tot = data.shape[0]

                # (len(fs_report.list())/tot)*100

                st.progress(len(fs_report.list())/tot, text=f'{len(fs_report.list())} reports submitted out of {tot}')
                st.progress(len(fs_poster.list())/tot, text=f'{len(fs_poster.list())} posters submitted out of {tot}')

                opts = ["",'Mr. Olorunniwo', 'Dr. Aransiola', 'Dr. Obayiuwana', 'Dr. Yesufu', 'Dr. Ariyo', 'Dr. Ogunseye', 'Mr. Olayiwola', 'Dr. Ayodele', 'Dr. Ilori', 'Mr. Akinboboye', 'Dr. Olawole', 'Dr. Babalola', 'Dr. Ogunba', 'Dr. Fisusi', 'Dr. Jubril']

                supervisor = st.selectbox('Supervisor', options=opts, index=0, key='supero')

                id_list = sorted(list(data.where(data.Supervisor.str.contains(supervisor, regex=False, case=False)).dropna(how='all')._id))

                matric_number = st.selectbox(f'Students with :red[{supervisor}]', options=[""]+id_list, disabled=True if zipit else False)

                if zipit:
                    # try:
                    zip_buf = io.BytesIO()
                    if supervisor:
                        with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as myzip:
                            for _id in id_list:
                                try:
                                    myzip.writestr(f'{_id.replace("/","_")}_poster.pdf', fs_poster.get(_id).read())
                                except errors.NoFile: 
                                    st.info(f'Student with matric number {_id} has not submitted his/her report', icon="ℹ️")
                    zip_buf.seek(0)

                    if st.download_button(f'download poster.zip', zip_buf if supervisor else "", mime='text/pdf', disabled=True if not supervisor else False, use_container_width=True, file_name=f'{supervisor}_students_poster.zip'):
                        status.update(label="done downloading files...", state="complete")
                    # except:
                    #     st.warning('The student you selected is yet to upload the requested file', icon="⚠️")

                    # try:
                    zip_bufr = io.BytesIO()
                    if supervisor:
                        with zipfile.ZipFile(zip_bufr, 'w', zipfile.ZIP_DEFLATED) as myzip:
                            for _id in id_list:
                                myzip.writestr(f'{_id.replace("/","_")}_report.pdf', fs_report.get(_id).read())
                    zip_bufr.seek(0)

                    if st.download_button(f'download report.zip', zip_bufr if supervisor else "", mime='text/pdf', disabled=True if not supervisor else False, use_container_width=True, file_name=f'{supervisor}_students_report.zip'):
                        status.update(label="done downloading files...", state="complete")
                    # except:
                    #     st.warning('The student you selected is yet to upload the requested file', icon="⚠️")

                else:
                    try:
                        if st.download_button(f'download poster.pdf', fs_poster.get(matric_number).read() if matric_number else "", mime='text/pdf', disabled=True if not matric_number else False, use_container_width=True, file_name=f'{matric_number}_poster.pdf'):
                            status.update(label="done downloading files...", state="complete")
                    except:
                        st.warning('The student you selected is yet to upload the requested file', icon="⚠️")

                    try:
                        if st.download_button(f'download report.pdf', fs_report.get(matric_number).read() if matric_number else "", file_name=f'{matric_number}_report.pdf', mime='text/pdf', disabled=True if not matric_number else False, use_container_width=True):
                            status.update(label="done downloading files...", state="complete")
                    except:
                        st.warning('The student you selected is yet to upload the requested file', icon="⚠️")


# except:
#     st.switch_page("Information.py")