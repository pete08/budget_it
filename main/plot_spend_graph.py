import pandas as pd
import matplotlib.pyplot as plt


def plotspend(df):
    # group by Month, Year, Date
    df_group_mo_yr = df.groupby(["YearMonth"])["Amount"].sum()
    # convert columns to df
    df_group_mo_yr = pd.DataFrame({'YearMonth':df_group_mo_yr.index, '[($)]':df_group_mo_yr.values})

    lowest_idx = df_group_mo_yr['[($)]'].idxmin()
    df_group_mo_yr = df_group_mo_yr.drop(lowest_idx)

    # Calculate the average of all columns
    avg_spend = df_group_mo_yr['[($)]'].mean()

    print(df_group_mo_yr)
    ax = df_group_mo_yr.plot.bar("YearMonth",'[($)]', rot=-70, legend=False)
    
    
    #add labels on top of the bars, formatted as currency
    for container in ax.containers:
        ax.bar_label(container, fmt='$%d', padding=3)

        # Define the styling for the floating window box
    box_properties = dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5)
    
    # Add the textbox inside the plot window
    # transform=ax.transAxes uses relative coordinates (0 to 1) instead of data values
    ax.text(0.05, 0.95, f"Monthly Avg: ${avg_spend:,.2f}", 
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=box_properties)
    

    plt.xlabel('Month')
    plt.ylabel('Take my Money!')
    plt.title('Spend Tracker')
    # plt.yticks([])
    plt.yticks(range(1000,int(max(df_group_mo_yr['[($)]'])+1000), 750))
    plt.tight_layout() 
    plt.show()


# df = pd.read_csv("./spendcsv_2022-12-07 21:25.csv")
# plotspend(df)