import streamlit as st


def render_header(month_active: bool) -> bool:
    """Render hero title, subtitle, month toggle. Returns updated month_active."""
    st.markdown('<div class="suit-row">♠ ♥ ♦ ♣</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">JUAARI DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Gambling addiction tracker</div>', unsafe_allow_html=True)

    # Centred toggle
    _, col_toggle, _ = st.columns([4, 1, 4])
    with col_toggle:
        toggled = st.toggle("This month only", value=month_active, key="month_toggle")
        if toggled != month_active:
            st.query_params["month_filter"] = "1" if toggled else "0"
            st.rerun()

    st.markdown('<hr class="red-divider">', unsafe_allow_html=True)
    return toggled
