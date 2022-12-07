import pandas as pd
import matplotlib.pyplot as plt


def plotspend(df):
    # group by Month, Year, Date
    df_group_mo_yr = df.groupby(["YearMonth"])["Amount"].sum()
    # convert columns to df
    df_group_mo_yr = pd.DataFrame({'YearMonth':df_group_mo_yr.index, 'Amount':df_group_mo_yr.values})

    print(df_group_mo_yr)
    df_group_mo_yr.plot.bar("YearMonth",'Amount', rot=0)
    plt.xlabel('Month')
    plt.ylabel('Amount Spent')
    plt.title('CC Spend past Year')
    plt.yticks(range(500,int(max(df_group_mo_yr['Amount'])+500), 500))
    plt.show()