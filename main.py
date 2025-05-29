import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def main() -> None:
    st.header('Compound Interest')

    cola, colb, colc, cold = st.columns(4)
    nyrs = cola.number_input('Number of Years', min_value=0, value=10, step=1)
    initial = colb.number_input('Initial Deposit', min_value=0, value=0, step=1_000)
    yearly_deposit = colc.number_input(
        'Yearly Deposit', min_value=0, value=120_000, step=1_000
    )
    interest_yield = cold.number_input(
        'Interest Yield [%]', min_value=0.0, value=10.0, step=0.1, format='%.2f'
    )

    interest_yield /= 100.0

    deposits = np.full(nyrs, yearly_deposit)
    deposits[0] += initial
    deposits_sum = deposits.cumsum()
    interests_mul = np.logspace(
        0, nyrs, nyrs, base=(1 + interest_yield), endpoint=False
    )
    interests = (interests_mul - 1) * deposits
    interests_sum = interests.cumsum()
    total = deposits_sum + interests_sum

    compound_interest_df = pd.DataFrame(
        {
            'Deposit': deposits,
            'Deposits Sum': deposits_sum,
            'Interest': interests,
            'Interests Sum': interests_sum,
            'Total': total,
        }
    )

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    datetimes = pd.period_range(today, periods=nyrs + 1, freq='Y').drop(today)
    datetimes = datetimes.astype(pd.StringDtype())
    compound_interest_df.insert(0, 'Datetime', datetimes)

    fig = px.bar(
        compound_interest_df,
        x='Datetime',
        y=['Deposits Sum', 'Interests Sum'],
    )
    fig.update_layout(xaxis_title='Datetime', yaxis_title='Total')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        (
            compound_interest_df.style.format(
                '{:,.0f}',
                subset=[
                    'Deposit',
                    'Deposits Sum',
                    'Interest',
                    'Interests Sum',
                    'Total',
                ],
            )
        ),
        hide_index=True,
    )
    st.write('*Note: Interest is added following year.*')


if __name__ == '__main__':
    main()
