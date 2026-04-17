import streamlit as st


def edit():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

    /* ─── Base ─────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background-color: #0C1B2A;
        color: #FFFFFF;
    }
    header[data-testid="stHeader"] {
        background-color: #0C1B2A !important;
        color: #FFFFFF !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown,
    div[data-testid="stMarkdownContainer"] > p {
        color: #FFFFFF !important;
    }

    /* ─── Sidebar ───────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background-color: #0C1B2A;
        border-right: 1px solid #CDA555;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* ─── Text / Number / Textarea inputs ──────────────────── */
    div[data-baseweb="base-input"],
    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
        border-color: #CDA555 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-baseweb="base-input"]:hover,
    div[data-baseweb="base-input"]:focus,
    div[data-baseweb="base-input"]:focus-within,
    div[data-baseweb="base-input"][aria-invalid="true"],
    div[data-baseweb="input"]:hover,
    div[data-baseweb="input"]:focus,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="input"][aria-invalid="true"] {
        border-color: #CDA555 !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1F284A !important;
        color: #FFFFFF !important;
        caret-color: #FFFFFF !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    [data-testid="stNumberInput"] div,
    [data-testid="stNumberInput"] div:focus-within {
        border-color: #CDA555 !important;
        box-shadow: none !important;
    }
    [data-testid="stNumberInput"] button {
        background-color: #1F284A !important;
        color: #CDA555 !important;
        border: none !important;
    }

    /* ─── Select / Dropdown ─────────────────────────────────── */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div:focus-within {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
        border-color: #CDA555 !important;
        box-shadow: none !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[class*="placeholder"],
    div[data-baseweb="select"] div[class*="singleValue"] {
        color: #FFFFFF !important;
    }
    /* Dropdown menu list */
    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
    }
    li[role="option"],
    div[data-baseweb="menu-item"] {
        background-color: #1F284A !important;
        color: #FFFFFF !important;
    }
    li[role="option"]:hover,
    div[data-baseweb="menu-item"]:hover {
        background-color: #2A3660 !important;
        color: #CDA555 !important;
    }
    li[aria-selected="true"],
    div[aria-selected="true"] {
        background-color: #0C1B2A !important;
        color: #CDA555 !important;
    }

    /* ─── Multiselect ───────────────────────────────────────── */
    span[data-baseweb="tag"] {
        background-color: #CDA555 !important;
        color: #0C1B2A !important;
        border-radius: 4px !important;
    }
    span[data-baseweb="tag"] span { color: #0C1B2A !important; }
    span[data-baseweb="tag"] button { color: #0C1B2A !important; }

    /* ─── Slider ────────────────────────────────────────────── */
    div[data-testid="stSlider"] > div > div > div {
        background-color: #CDA555 !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #CDA555 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 6px rgba(205,165,85,0.5) !important;
    }
    /* Track fill */
    div[data-testid="stSlider"] > div > div > div > div {
        background-color: #CDA555 !important;
    }
    div[data-testid="stSlider"] p { color: #FFFFFF !important; }

    /* ─── Checkbox ──────────────────────────────────────────── */
    label[data-baseweb="checkbox"] span[data-baseweb="checkbox"] {
        background-color: #1F284A !important;
        border: 2px solid #CDA555 !important;
        border-color: #CDA555 !important;
    }
    label[data-baseweb="checkbox"] input:checked + span[data-baseweb="checkbox"] {
        background-color: #CDA555 !important;
        border-color: #CDA555 !important;
    }
    label[data-baseweb="checkbox"] span:last-child { color: #FFFFFF !important; }

    /* ─── Radio buttons ─────────────────────────────────────── */
    label[data-baseweb="radio"] > div:first-child {
        background-color: #1F284A !important;
        border: 2px solid #CDA555 !important;
    }
    label[data-baseweb="radio"] input:checked + div {
        background-color: #CDA555 !important;
        border-color: #CDA555 !important;
    }
    label[data-baseweb="radio"] span { color: #FFFFFF !important; }

    /* ─── Toggle / Switch ───────────────────────────────────── */
    label[data-baseweb="toggle"] div[data-baseweb="toggle"] {
        background-color: #1F284A !important;
        border: 2px solid #CDA555 !important;
    }
    input:checked ~ div[data-baseweb="toggle"] {
        background-color: #CDA555 !important;
        border-color: #CDA555 !important;
    }

    /* ─── Date / Time picker ────────────────────────────────── */
    div[data-baseweb="calendar"] {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
    }
    div[data-baseweb="calendar"] * { color: #FFFFFF !important; }
    div[data-baseweb="calendar"] button:hover { background-color: #CDA555 !important; color: #0C1B2A !important; }
    div[data-baseweb="calendar"] div[aria-selected="true"] {
        background-color: #CDA555 !important;
        color: #0C1B2A !important;
    }

    /* ─── Buttons ───────────────────────────────────────────── */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button,
    .stLinkButton > a,
    a[data-baseweb="link-button"] {
        background-color: #CDA555 !important;
        color: #0C1B2A !important;
        border: 1px solid #CDA555 !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        text-decoration: none !important;
        width: 100%;
    }
    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover,
    a[data-baseweb="link-button"]:hover {
        background-color: #1F284A !important;
        color: #FFFFFF !important;
        border: 1px solid #CDA555 !important;
        transform: scale(1.02);
    }

    /* ─── Tabs ──────────────────────────────────────────────── */
    div[data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #CDA555 !important;
        gap: 0.25rem;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #AAAAAA !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #CDA555 !important;
        border-bottom: 2px solid #CDA555 !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #CDA555 !important;
        background-color: rgba(205,165,85,0.08) !important;
    }
    div[data-baseweb="tab-panel"] {
        background-color: transparent !important;
        padding-top: 1rem !important;
    }

    /* ─── Expander ──────────────────────────────────────────── */
    details[data-testid="stExpander"] {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
        border-radius: 10px !important;
        overflow: hidden;
    }
    details[data-testid="stExpander"] summary {
        background-color: #1F284A !important;
        color: #CDA555 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
    }
    details[data-testid="stExpander"] summary:hover {
        background-color: #2A3660 !important;
    }
    details[data-testid="stExpander"] > div {
        background-color: #1F284A !important;
        padding: 0.5rem 1rem 1rem !important;
    }

    /* ─── Progress bar ──────────────────────────────────────── */
    div[data-testid="stProgress"] > div > div {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
        border-radius: 99px !important;
    }
    div[data-testid="stProgress"] > div > div > div {
        background-color: #CDA555 !important;
        border-radius: 99px !important;
    }

    /* ─── Spinner ───────────────────────────────────────────── */
    div[data-testid="stSpinner"] svg { color: #CDA555 !important; }

    /* ─── Metrics ───────────────────────────────────────────── */
    div[data-testid="stMetric"] {
        background-color: #1F284A;
        border: 1px solid #CDA555;
        border-radius: 12px;
        padding: 1rem 1.2rem;
    }
    div[data-testid="stMetric"] label {
        color: #AAAAAA !important;
        font-size: 0.8rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] { color: #CDA555 !important; font-size: 2rem !important; }
    div[data-testid="stMetricDelta"] svg { fill: currentColor !important; }
    div[data-testid="stMetricDelta"][data-direction="up"] { color: #4CAF82 !important; }
    div[data-testid="stMetricDelta"][data-direction="down"] { color: #E05A5A !important; }

    /* ─── Alerts / Info / Warning / Error / Success ─────────── */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left-width: 4px !important;
    }
    div[data-baseweb="notification"][kind="info"],
    div[data-testid="stAlert"][data-baseweb="notification"] {
        background-color: #1A2540 !important;
        border-left-color: #CDA555 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stNotification"][kind="success"] {
        background-color: #1A2D24 !important;
        border-left-color: #4CAF82 !important;
    }
    div[data-testid="stNotification"][kind="warning"] {
        background-color: #2D2418 !important;
        border-left-color: #CDA555 !important;
    }
    div[data-testid="stNotification"][kind="error"] {
        background-color: #2D1A1A !important;
        border-left-color: #E05A5A !important;
    }

    /* ─── File uploader ─────────────────────────────────────── */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #1F284A !important;
        border: 2px dashed #CDA555 !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stFileUploadDropzone"]:hover {
        background-color: #2A3660 !important;
    }
    section[data-testid="stFileUploadDropzone"] button {
        background-color: #CDA555 !important;
        color: #0C1B2A !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* ─── Data / Tables ─────────────────────────────────────── */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {
        border: 1px solid #CDA555 !important;
        border-radius: 10px !important;
        overflow: hidden;
    }
    thead tr th {
        background-color: #1F284A !important;
        color: #CDA555 !important;
        border-bottom: 1px solid #CDA555 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 1.5px !important;
        font-size: 0.95rem !important;
    }
    tbody tr td {
        background-color: #0C1B2A !important;
        color: #FFFFFF !important;
        border-color: #1F284A !important;
    }
    tbody tr:hover td {
        background-color: #1F284A !important;
    }

    /* ─── Code blocks ───────────────────────────────────────── */
    div[data-testid="stCodeBlock"] pre,
    .stCode pre {
        background-color: #0A1520 !important;
        border: 1px solid #CDA555 !important;
        border-radius: 8px !important;
        color: #CDA555 !important;
    }

    /* ─── Chat / Message ────────────────────────────────────── */
    div[data-testid="stChatMessage"] {
        background-color: #1F284A !important;
        border: 1px solid rgba(205,165,85,0.25) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stChatInputContainer"] {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
        border-radius: 10px !important;
    }

    /* ─── Star rating ───────────────────────────────────────── */
    [data-testid="stStarRating"] svg { fill: #CDA555 !important; }

    /* ─── Tooltip ───────────────────────────────────────────── */
    div[data-baseweb="tooltip"] {
        background-color: #1F284A !important;
        border: 1px solid #CDA555 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }

    /* ─── Scrollbar ─────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0C1B2A; }
    ::-webkit-scrollbar-thumb { background: #CDA555; border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: #e0bb77; }

    /* ─── Input / Select text always white ──────────────────── */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [class*="singleValue"],
    div[data-baseweb="select"] [class*="placeholder"],
    div[data-baseweb="input"] input,
    input[type="text"],
    input[type="number"],
    input[type="password"],
    textarea {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* Placeholder text — slightly dimmed but still visible */
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder,
    .stTextArea textarea::placeholder,
    textarea::placeholder,
    input::placeholder {
        color: #AAAAAA !important;
        -webkit-text-fill-color: #AAAAAA !important;
        opacity: 1 !important;
    }

    /* Fix autofill turning inputs dark with gray text */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active {
        -webkit-text-fill-color: #FFFFFF !important;
        -webkit-box-shadow: 0 0 0px 1000px #1F284A inset !important;
        transition: background-color 5000s ease-in-out 0s;
    }

    /* ─── Custom utility classes ────────────────────────────── */
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4rem;
        color: #CDA555 !important;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 0.2rem;
        line-height: 1;
    }
    .hero-subtitle {
        text-align: center;
        color: #AAAAAA !important;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .divider {
        border: none;
        border-top: 1px solid #CDA555;
        opacity: 0.4;
        margin: 1.5rem 0;
    }
    .section-label {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.1rem;
        color: #CDA555 !important;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .app-card {
        background: #1F284A;
        border: 1px solid #CDA555;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    .app-card:hover {
        border-color: #CDA555;
        box-shadow: 0 4px 20px rgba(205, 165, 85, 0.25);
    }
    .app-card-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.5rem;
        color: #CDA555 !important;
        letter-spacing: 1.5px;
        margin-bottom: 0.2rem;
    }
    .app-card-desc {
        color: #CCCCCC !important;
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)
