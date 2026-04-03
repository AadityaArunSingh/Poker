import streamlit as st


def render_header():
    st.markdown('<div class="suit-row">♠ ♥ ♦ ♣</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">JUAARI DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Gambling addiction tracker</div>', unsafe_allow_html=True)
    st.markdown('<hr class="red-divider">', unsafe_allow_html=True)