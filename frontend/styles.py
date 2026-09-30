import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        .main {
            background: #f7f8fc;
        }

        .hero {
            padding: 30px;
            border-radius: 20px;
            background: linear-gradient(
                135deg,
                #111827,
                #312e81
            );
            color: white;
            margin-bottom: 25px;
        }

        .hero h1 {
            font-size: 42px;
            margin-bottom: 5px;
        }

        .hero p {
            font-size: 17px;
            color: #e5e7eb;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #e5e7eb;
            margin-bottom: 15px;
        }

        .day-card {
            background: white;
            padding: 22px;
            border-radius: 16px;
            border-left: 5px solid #4f46e5;
            margin: 15px 0;
            box-shadow: 0 3px 15px rgba(
                0,
                0,
                0,
                0.05
            );
        }

        .expense-card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            margin-bottom: 10px;
        }

        .trip-small {
            background: white;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            margin-bottom: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )