import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import io, base64


# (kibtool) imachine@imachine:~$ mongosh "mongodb+srv://cluster0.lhxokzx.mongodb.net/" --apiVersion 1 --username bovenssolutions
# st.write(st.secrets["mongo"]["uri"])

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    # Create a new client and connect to the server
    return MongoClient(str(st.secrets["mongo"]["uri"]), server_api=ServerApi('1'))
    # return pymongo.MongoClient(**st.secrets["mongo"], authSource="admin")


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def get_data(uid, collection):
    db = st.session_state['db']
    collection = collection
    item = db[collection].find_one({'_id':uid})
    return item if item else {}

def get_all_data(collection):
    db = st.session_state['db']
    collection = collection
    
    items = db[collection].find({})#,{'_id':0})
    items = list(items)  # make hashable for st.cache_data
    return items if items else []


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def put_data(uid, collection, data):
    db = st.session_state['db']
    collection = collection
    db[collection].replace_one({'_id':uid},data,True)
    
def get_question(collection, query):
    db = st.session_state['db']
    collection = collection
    item = db[collection].find_one({'title':query})
    return item if item else {}


# img_to_bytes and img_to_html inspired from https://pmbaumgartner.github.io/streamlitopedia/sizing-and-images.html
def img_to_html(fig):
    picture = io.BytesIO()
    fig.savefig(picture, format='png')
    picture.seek(0)
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        base64.b64encode(picture.read()).decode()#img_to_bytes
    )
    return img_html


def send_email(recipient, score_sheet):
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from smtplib import SMTP
    import smtplib
    import sys
    

    recipients = [recipient] 
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = f"{course_name} Project Result"
    msg['From'] = 'eakinboboye@oauife.edu.ng'

    html = f"""\
            <html>
              <head></head>
              <body>
              <div>Please sir/ma, return grades for the students you supervised for "{course_name}".</div>
              <div>The table below contains the score sheet for your students. </div>
                {score_sheet.to_html(index=False)}
              <div>Thank you.</div>
              </body>
            </html>
    """
    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    try:
        # """Checking for connection errors"""

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('eakinboboye@oauife.edu.ng',st.secrets["oaumailpassword"])
        server.sendmail(msg['From'], emaillist , msg.as_string())
        server.close()

    except Exception as e:
        st.write(f"Error for connection: {e}")
        
name_email_map = {
'Mr. Olorunniwo': 'dareniwo@oauife.edu.ng',
'Mr. Aransiola': 'aaransiola@oauife.edu.ng',
'Dr. Obayiuwana': 'obayiuwanae@oauife.edu.ng',
'Dr. Yesufu': 'tyesufu@oauife.edu.ng',
'Dr. Ariyo': 'ariyofunso@oauife.edu.ng',
'Dr. Ogunseye': 'aaogunseye@oauife.edu.ng',
'Mr. Olayiwola': 'solayiwola@oauife.edu.ng',
'Dr. Mrs. Offiong': 'fboffiong@oauife.edu.ng',
'Dr. Ayodele': 'kayodele@oauife.edu.ng',
'Dr. Akinwale': 'olawale.akinwale@oauife.edu.ng',
'Dr. Ilori': 'sojilori@oauife.edu.ng',
'Mr. Akinboboye': 'eakinboboye@oauife.edu.ng',
'Dr. Olawole': 'alex_olawole@oauife.edu.ng',
'Dr. Babalola': 'babfisayo@oauife.edu.ng',
'Dr. Ogunba': 'kolaogunba@oauife.edu.ng',
'Dr. Fisusi': 'bimbofisusi@oauife.edu.ng',
'Dr. Jubril': 'ajubril@oauife.edu.ng'
}