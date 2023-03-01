import pandas as pd
import matplotlib.pyplot as plt


def plotspend(df):
    # group by Month, Year, Date
    df_group_mo_yr = df.groupby(["YearMonth"])["Amount"].sum()
    # convert columns to df
    df_group_mo_yr = pd.DataFrame({'YearMonth':df_group_mo_yr.index, '[($)]':df_group_mo_yr.values})

    print(df_group_mo_yr)
    df_group_mo_yr.plot.bar("YearMonth",'[($)]', rot=-70)
    plt.xlabel('Month')
    plt.ylabel('Take my Money!')
    plt.title('Spend Tracker')
    # plt.yticks([])
    plt.yticks(range(1000,int(max(df_group_mo_yr['[($)]'])+1000), 750))
    plt.show()


# df = pd.read_csv("./spendcsv_2022-12-07 21:25.csv")
# plotspend(df)