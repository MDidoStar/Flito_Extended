# Importing libraries
import requests
import pandas as pd
import streamlit as st
from color import edit
st.set_page_config(page_title="FLITO: Currency", page_icon='logo.png', layout="wide")

edit()

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('countries.csv')
        df['Currency_Code'] = df['Currency_Code'].astype(str)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Country', 'City', 'Currency_Code'])

df = load_data()

def get_conversion_rates(base_currency):
    api_key = st.secrets["exchange_api_key"]
    request = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    response = requests.get(request)
    if response.status_code == 200:
        return response.json()
    return None

with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')
    st.divider()
    if st.button("← Back to FLITO", key="back_btn"):
        st.switch_page("E:\Coding Mohamed\Flito Extened\Flito-main\FLITO.py")

st.title("💱 Currency Converter")
st.write("Convert all currencies in real-time!")

if not df.empty:
    all_currencies = sorted(df['Currency_Code'].dropna().unique().tolist())
    common = ['USD', 'EUR', 'GBP']
    for c in common:
        if c not in all_currencies:
            all_currencies.append(c)
    all_currencies = sorted(list(set(all_currencies)))
else:
    all_currencies = ['USD', 'EUR']

col1, col2 = st.columns(2)
with col1:
    idx_usd = all_currencies.index('USD') if 'USD' in all_currencies else 0
    base_currency = st.selectbox('From currency', all_currencies, index=idx_usd, key='base_curr')
with col2:
    idx_eur = all_currencies.index('EUR') if 'EUR' in all_currencies else 0
    target_currency = st.selectbox('To currency', all_currencies, index=idx_eur, key='target_curr')

amount = st.number_input('Enter the amount:', min_value=0.01, value=1.0, step=0.01)

if st.button('Calculate Rate', key='currency_calc'):
    with st.spinner('Fetching exchange rates...'):
        result = get_conversion_rates(base_currency)
        if result and 'conversion_rates' in result:
            rates = result['conversion_rates']
            if target_currency in rates:
                exchange_rate = rates[target_currency]
                total = exchange_rate * amount
                st.success(f'{amount:,.2f} {base_currency} = {total:,.2f} {target_currency}')
                st.info(f'Exchange Rate: 1 {base_currency} = {exchange_rate:,.4f} {target_currency}')
            else:
                st.error(f'Currency {target_currency} not found in conversion rates.')
        else:
            st.error('Failed to fetch exchange rates. Please try again later.')

st.write('---')
st.caption('💱 Currency data from ExchangeRate-API')
