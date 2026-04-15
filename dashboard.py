import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table
import io

# Page Config
st.set_page_config(
    page_title="Enterprise AI Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Dark Mode
dark_mode = st.sidebar.toggle("🌙 Dark Mode", True)

# Login System
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and password == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid Login")

else:

    st.title("🚀 Enterprise AI Dashboard")

    page = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard","Analytics","AI Prediction","Reports"]
    )

    np.random.seed(42)

    months = ['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec']

    sales = np.random.randint(200,1000,12)
    profit = np.random.randint(50,300,12)
    customers = np.random.randint(100,700,12)
    orders = np.random.randint(100,500,12)

    df = pd.DataFrame({
        "Month":months,
        "Sales":sales,
        "Profit":profit,
        "Customers":customers,
        "Orders":orders
    })

# Dashboard
    if page == "Dashboard":

        st.subheader("📊 KPI")

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Sales", df["Sales"].sum())
        col2.metric("Profit", df["Profit"].sum())
        col3.metric("Customers", df["Customers"].sum())
        col4.metric("Orders", df["Orders"].sum())

        col1,col2 = st.columns(2)

        with col1:
            fig = px.line(df,x="Month",y="Sales",markers=True)
            st.plotly_chart(fig)

        with col2:
            fig = px.bar(df,x="Month",y="Profit")
            st.plotly_chart(fig)

# Analytics
    elif page == "Analytics":

        fig = px.scatter(
            df,
            x="Sales",
            y="Profit",
            size="Customers"
        )

        st.plotly_chart(fig)

        fig = px.box(df,y="Sales")
        st.plotly_chart(fig)

# AI Prediction
    elif page == "AI Prediction":

        prediction = np.append(
            df["Sales"],
            df["Sales"].rolling(3).mean().iloc[-1]
        )

        months2 = months + ["Next"]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=months2,
            y=prediction,
            mode="lines+markers"
        ))

        st.plotly_chart(fig)


# Reports + PDF Download
    elif page == "Reports":

        st.subheader("📄 Generate Report")

        st.dataframe(df)

        def create_pdf():

            buffer = io.BytesIO()

            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Enterprise Dashboard Report", styles['Heading1']))
            story.append(Spacer(1,12))

            table_data = [df.columns.tolist()] + df.values.tolist()

            table = Table(table_data)

            story.append(table)

            doc = SimpleDocTemplate(buffer, pagesize=letter)
            doc.build(story)

            buffer.seek(0)

            return buffer

        pdf = create_pdf()

        st.download_button(
            label="Download PDF Report",
            data=pdf,
            file_name="dashboard_report.pdf",
            mime="application/pdf"
        )


    st.sidebar.markdown("---")
    st.sidebar.write("Enterprise Dashboard v4.0")