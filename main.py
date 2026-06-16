import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def main() -> None:
    st.header('Compound Interest')

    cols = st.columns(5)
    start_yr = cols[0].number_input('Start year', min_value=0, value=2023, step=1)
    end_yr = cols[1].number_input('End year', min_value=1, value=2053, step=1)
    initial = cols[2].number_input('Initial Deposit', min_value=0, value=0, step=1_000)
    yearly_deposit = cols[3].number_input(
        'Yearly Deposit', min_value=0, value=100_000, step=1_000
    )
    interest_yield = cols[4].number_input(
        'Interest Yield [%]', min_value=0.0, value=10.0, step=0.1, format='%.2f'
    )

    interest_yield /= 100.0

    nyrs = end_yr - start_yr
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

    start_dt = datetime.datetime.strptime(str(start_yr), '%Y')
    end_dt = datetime.datetime.strptime(str(end_yr), '%Y')
    datetimes = pd.date_range(start_dt, end_dt, freq='YE')
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
