import cv2
import face_recognition
import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Directory to store student data and photos
DATA_DIR = "students_data"
PHOTOS_DIR = os.path.join(DATA_DIR, "photos")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)

import streamlit as st

def main():
    st.title('Streamlit App')
    st.write("Attandance Tracking")
    if st.button("Return to Home Page"):
        st.markdown("<a href='http://localhost:5000'>Return to Main Page</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()


def save_student_data(data, photo):
    roll_number = data['Roll Number']
    photo_path = os.path.join(PHOTOS_DIR, f"{roll_number}.jpg")
    cv2.imwrite(photo_path, photo)
    data['Photo Path'] = photo_path
    data_path = os.path.join(DATA_DIR, f"{roll_number}.csv")
    data_df = pd.DataFrame([data])
    data_df.to_csv(data_path, index=False)

def load_student_data(roll_number):
    data_path = os.path.join(DATA_DIR, f"{roll_number}.csv")
    data_df = pd.read_csv(data_path)
    photo_path = data_df['Photo Path'].iloc[0]
    photo = cv2.imread(photo_path)
    return data_df.drop(columns=['Photo Path']), photo

def capture_photo(window_name):
    camera = cv2.VideoCapture(0)
    photo = None
    while True:
        _, frame = camera.read()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):  # Press 'c' to capture
            photo = frame
            break
    camera.release()
    cv2.destroyAllWindows()
    return photo

def register_student():
    st.title("Register Student")
    name = st.text_input("Name")
    branch = st.text_input("Branch")
    address = st.text_input("Address")
    roll_number = st.text_input("Roll Number")
    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email")

    if "photo" not in st.session_state:
        st.session_state.photo = None

    if st.button("Open Camera"):
        st.write("Camera is open. Press 'c' to capture the photo.")
        st.session_state.photo = capture_photo("Capture Registration Photo")

        if st.session_state.photo is not None:
            st.image(st.session_state.photo, channels="BGR", caption="Captured Photo")

    if st.button("Submit"):
        if name and branch and address and roll_number and phone_number and email and st.session_state.photo is not None:
            data = {
                "Name": name,
                "Branch": branch,
                "Address": address,
                "Roll Number": roll_number,
                "Phone Number": phone_number,
                "Email": email
            }
            save_student_data(data, st.session_state.photo)
            st.success("Student registered successfully!")
        else:
            st.error("Please fill all the details and capture the photo.")

def verify_student():
    st.title("Verify Student")
    roll_number = st.text_input("Enter Roll Number to Verify")

    if "verification_data" not in st.session_state:
        st.session_state.verification_data = None
        st.session_state.verification_photo = None

    if st.button("Open Camera for Verification"):
        st.write("Camera is open for verification. Press 'c' to capture the photo.")
        photo = capture_photo("Capture Verification Photo")

        if photo is not None and roll_number:
            data_df, saved_photo = load_student_data(roll_number)

            # Get face encodings for the captured photo and the saved photo
            face_encodings_photo = face_recognition.face_encodings(photo)
            face_encodings_saved_photo = face_recognition.face_encodings(saved_photo)

            if face_encodings_photo and face_encodings_saved_photo:
                # Compare the face encodings
                match = face_recognition.compare_faces(face_encodings_saved_photo, face_encodings_photo[0])

                if match[0]:
                    st.success("Face verified!")
                    st.write("Click below to view Student Information:")
                    st.session_state.verification_data = data_df
                    st.session_state.verification_photo = saved_photo
                    cols = st.columns([1,1])  # Adjust the ratio of the columns as needed

                    with cols[0]:
                        st.image(st.session_state.verification_photo, channels="BGR", caption="Student Photo")

                    with cols[1]:
                        # Transpose the DataFrame and reset the index
                        data_transposed = st.session_state.verification_data.T.reset_index()
                        data_transposed.columns = ['Attribute', 'Value']

                        # Use Pandas Styler to render the DataFrame
                        st.write(data_transposed.style.set_table_styles([
                            {'selector': 'th', 'props': [('font-size', '15pt'), ('text-align', 'center')]},
                            {'selector': 'td', 'props': [('font-size', '15pt'), ('text-align', 'left')]}
                        ]))
                else:
                    st.error("Face not verified. Please try again.")
            else:
                st.error("Face not detected. Please try again.")
        else:
            st.error("Please enter roll number and capture the photo.")
        if st.session_state.verification_data is not None:
            os.system("python proctoring.py")

    
        

# Main app
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Register Student", "Verify Student"])

if page == "Register Student":
    register_student()
elif page == "Verify Student":
    verify_student()
