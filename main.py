import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

def main():
    st.header('Compound Interest')
    nyrs = st.number_input('Number of Years', min_value=0, value=10, step=1)
    initial = st.number_input('Initial', min_value=0, value=0, step=1)
    yearly_deposit = st.number_input('Yearly Deposit', min_value=0, value=120_000, step=1)
    interest_yield = st.number_input('Interest Yield [%]', min_value=0., value=10., step=0.1)

    interest_yield /= 100.

    # yr 0
    deposit = initial + yearly_deposit
    interest = deposit * interest_yield
    value = deposit + interest

    data = [{
        'deposit': deposit,
        'interest': interest,
        'value': value

    }]

    for yr in range(2, nyrs+1):
        deposit = yearly_deposit
        interest = interest_yield * value
        value += deposit + interest
        data.append({
            'deposit': deposit,
            'interest': interest,
            'value': value
        })

    df = pd.DataFrame(data)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    datetimes = pd.period_range(today, periods=nyrs+1, freq='Y').drop(today)
    datetimes = datetimes.astype(pd.StringDtype())
    df.insert(0, 'datetime', datetimes)

    st.dataframe(df.style.format('{:,.0f}', subset=['deposit', 'value', 'interest']), hide_index=True)

    fig = px.bar(
        df,
        x='datetime',
        y=['deposit', 'interest'],
    )
    fig.update_layout(xaxis_title='Datetime', yaxis_title='Value')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
