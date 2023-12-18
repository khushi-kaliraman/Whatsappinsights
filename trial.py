import streamlit as st  # pip install streamlit

def form():
    st.header(":mailbox: Get In Touch With Me!")


    contact_form = """
    <form action="https://formsubmit.co/shreshthn13@gmail.com" method="POST">
         <input type="text" name="name" placeholder="Your name" required>
         <input type="email" name="email" placeholder="Your email" required>
         <textarea name="message" placeholder="Your message here"></textarea>
         <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)