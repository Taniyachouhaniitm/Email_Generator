import streamlit as st
import re
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def normalize_email(text: str) -> str:
    """
    Reduce excessive blank lines in generated email
    """
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)  
    return text


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(
        page_title="XYZ AI Referral Email Writer",
        layout="wide"
    )

    st.markdown(
        """
        <style>
            .hero {
                text-align: center;
                padding: 60px 20px 40px;
            }
            .hero h1 {
                font-size: 42px;
                font-weight: 700;
                color: #0f172a;
            }
            .hero p {
                font-size: 18px;
                color: #475569;
                margin-top: 10px;
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }
            .input-box textarea {
                font-size: 16px !important;
                border-radius: 10px;
            }
            .divider {
                margin: 60px 0 40px;
            }
            .section-title {
                text-align: center;
                font-size: 30px;
                font-weight: 600;
                color: #0f172a;
            }
            .section-subtitle {
                text-align: center;
                color: #64748b;
                margin-bottom: 30px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero">
            <h1>AI Talent Referral Email Writer</h1>
            <p>
                XYZ Solutions helps companies fill roles faster by connecting them with
                pre-vetted engineering talent from our internal portfolio.
                Generate professional referral emails tailored to open job roles.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    url_input = st.text_area(
        label="",
        height=90,
        placeholder="Paste the job posting URL to refer matching XYZ talent",
        value="https://careers.nike.com/software-engineer-iii-itc/job/R-76025"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        generate_btn = st.button("Generate Referral Email", use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">How XYZ Talent Referrals Work</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">'
        'Analyze open roles → Match internal talent portfolio → Generate professional referral outreach'
        '</div>',
        unsafe_allow_html=True
    )

    if generate_btn:
        with st.spinner("Analyzing job role and matching talent..."):
            try:
                loader = WebBaseLoader([url_input])
                raw_data = loader.load()

                if not raw_data:
                    st.error("Unable to load content from the provided URL.")
                    return

                data = clean_text(raw_data.pop().page_content)

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No relevant job roles detected. Try another URL.")
                    return

                for idx, job in enumerate(jobs, start=1):
                    st.markdown("---")
                    st.markdown(f"### Job Opportunity")

                    col_left, col_right = st.columns([1, 2])

                    with col_left:
                        st.markdown("**Required Skills**")
                        skills = job.get("skills", [])
                        st.write(", ".join(skills) if skills else "Not specified")

                    with col_right:
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links)

                        email = normalize_email(email)

                        st.markdown("**Generated Referral Email (XYZ Solutions)**")
                        st.code(email, language="text")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
