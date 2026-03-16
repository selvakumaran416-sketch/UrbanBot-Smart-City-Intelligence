import streamlit as st
from PIL import Image

def main():
    # Page config
    st.set_page_config(
        page_title="Selvakumaran MUTHUSAMY | Portfolio",
        page_icon="👩‍💻",
        layout="wide"
    )

    # Load profile image
    profile_image = Image.open("C:/Users/Selva.M/Downloads/data_science/final_project/data/SELVA (2).jpg")

    # ================= HEADER SECTION =================
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(profile_image, width=220)

    with col2:
        st.markdown("<h1>Selvakumaran M</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h4>Data Science Aspirant | B.VOC(SD & SA)</h4>",
            unsafe_allow_html=True
         )
        st.write(
            """
    Graduate in Software Developement & System Administractor with strong academic score
    and a purposeful transition into the IT and Data Science domain.
    """)

    st.divider()

    # ================= PROFESSIONAL SUMMARY =================
    st.subheader("Professional Summary")

    st.write(
        """
    With a strong motivation to **restart and redefine my professional career**, I chose
    **Data Science at HCL–GUVI** as a strategic transition into the IT industry. I am currently
    building skills in Python, data analysis, and problem-solving, with a long-term goal of
    contributing to data-driven solutions in a professional environment.
    """
    )

    # ================= CAREER TIMELINE =================
    st.subheader("Career Timeline")

    st.markdown(
      """
    **🎓 Education**
    - B.VOC - Software Developement & System Administractor

    **📚 Upskilling & Transition**
    - Python - SYSTECH  
    - Sql - SYSTECH
    - Django - SYSTECH  
    - Data Science Program – HCL GUVI
    """
    )

    # ================= SKILLS =================
    st.subheader("Skills")

    col1, col2, = st.columns(2)

    with col1:
        st.markdown(
            """
    **Technical**
    - Python 
    - Sql
    - Computer Networks
    - Django
    """
        )

    with col2:
        st.markdown(
            """
    **Soft Skills**
    - Clear Communication
    - Good Listener
    - Quick Learner
    - Organized Thinking
    """
        )

    # ================= INTERESTS =================
    st.subheader("Interests & Strengths")

    st.write(
        """
    - Reading books and continuous self-learning   
    - Explaining complex concepts in a simple and structured way  
    """
    )

    # ================= CAREER OBJECTIVE =================
    st.subheader("Career Objective")

    st.write(
        """
    To secure a role in the **IT / Data Science domain** where I can effectively combine my
    **academic discipline, analytical thinking, and continuous learning mindset**
    to grow professionally and contribute meaningfully to organizational goals.
    """
    )

    # ================= FOOTER =================
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: grey;'>© Selvakumaran Muthusamy | Developer Portfolio Page</p>",
        unsafe_allow_html=True
    )
if __name__ == "__main__":
    main()
    