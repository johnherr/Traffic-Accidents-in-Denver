import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns
import calendar as cal

#plt.style.use('ggplot')

def filename(str_in):
    name = str_in.lower().replace(' ','_')
    return name
    
def plot_over_time(df, time_col, ax, title, interval):
    '''
        Prints a timeline of accident data
        
        ARGS:
            df - pandas df
            time_col - column with time data
            ax - axis to plot on
            title - plot title
            interval - Datetime interval for plotting data  
                E.g., 'Y','Q','M','D'
        
        Return:
            ax - axis with plot
    '''
    ax.plot(df.groupby(pd.Grouper(key=time_col, freq=interval))
            .size(), '*-', linewidth=2)
    ax.set_title(title)
    ax.set_ylabel('# of Collisions')
    name=filename(title)
    save_location='images/'+ name +'_' + interval + '.png'
    plt.savefig(save_location)
    return ax

def plot_months(df, ax, title = 'Accidents per Day'):
    '''
        Prints a barchart of accidents per day in each month of the year
        
        ARGS:
            df - pandas df
            ax - axis to plot on

        Return:
            ax - axis with plot
    '''    
    df['year_mon'] = df['DATE'].apply(lambda x: (int(x.year), int(x.month)))
    df['weight'] = df['year_mon'].apply(lambda x: 1/cal.monthlen(x[0],x[1])/5)
    per_day = df.groupby(['month'])['weight'].sum()
    per_day

    sns.barplot(x = per_day.index, y = per_day, ax= ax)
    ax.set_ylim(65, 90)
    ax.set_title('Accidents by Month (Data averaged over 5 years)')
    ax.set_ylabel(title)
    name=filename(title)
    save_location='images/' + name + '.png'
    plt.savefig(save_location)
    return ax
    

def hist_categorical_factors(df,ax, col = 'TU1_DRIVER_HUMANCONTRIBFACTOR', vals = ['NO APPARENT','NOT RECORDED'], title = 'Human Contributing Factors'):
    '''
        Prints a histograms for categorical values
        
        ARGS:
            df - pandas df
            ax - axis to plot on
            col - the column with categorical data
            vals - values we do not want to consider
            title = plot title
        
        Return:
            ax - axis with plot
    '''
    df[col].replace('  ', value='NOT RECORDED', inplace=True)

    for val in vals:
        df[col] = df[col][df[col] != val]
    
    ordering = df.groupby(df[col]).size().sort_values(ascending=False).index
    sns.countplot(y=col, data=df, order=ordering, ax= ax)
    ax.set_title(title)
    ax.set_ylabel(None)
    #ax.text(5000, 14, "* Some accident reports did not record a human contributing factor", horizontalalignment='left', size='medium', color='black', weight='semibold')
    name=filename(title)
    save_location='images/'+name + '_bar_plot.png'
    plt.savefig(save_location, bbox_inches="tight")
    return ax


def plot_human_factors_and_time(df,ax, col = 'TU1_DRIVER_HUMANCONTRIBFACTOR', vals = ['NO APPARENT','NOT RECORDED', 'UNDER INVESTIGATION'], title = 'Human Contributing Factors'):
    '''
        Prints a violin plot for categorical values
        
        ARGS:
            df - pandas df
            ax - axis to plot on
            col - the column with categorical data
            vals - values we do not want to consider
            title = plot title
        
        Return:
            ax - axis with plot
    '''
    df[col].replace('  ', value='NOT RECORDED', inplace=True)

    for val in vals:
        df[col] = df[col][df[col] != val]
    
    ordering = df.groupby(df[col]).size().sort_values(ascending=False).index
    

    #Violin plot
    sns.violinplot(y=col, x="hour", data=df, ax=ax, bw=.1, order=ordering)
#     sns.catplot(y=col, x="hour", kind="violin", inner=None, data=df, ax = ax, pallete = "GnBu_d", order = ordering)
    ax.set_title(title)
    ax.set_ylabel(None)
    ax.set_xlabel('Hour of day')
    name=filename(title)
    save_location='images/'+name + '_violin_plot.png'
    plt.savefig(save_location, bbox_inches="tight")
    return ax


def joint_plot(df, x = 'w_day' , y = 'hour', title = 'joint_plot', ylabel = 'Hour', xlabel = 'Weekday'):
#     time_range_filter = df['DATE'] > '2018-01-01'
#     df2018 = df[time_range_filter].sample(100)
    ax = sns.set(style="ticks")
    x = df[x]
    y = df[y]
    a = sns.jointplot(x, y, kind="kde", color="g", xlim=(-.5,6.5), ylim=(0,24))
    # JointGrid has a convenience function
    a.set_axis_labels('Day of Week (Sunday-Saturday)', 'Hour of Day', fontsize=16)
    # labels appear outside of plot area, so auto-adjust
    plt.tight_layout()
    
    
    name=filename(title)
    save_location='images/'+name + '_joint_plot.png'
    plt.savefig(save_location)
    return ax

def swarm_plot(df, start ='2017-01-01', num = 7, title = 'Top Accident Locations'):
    """
    Creates a time-series swarm plot for locations with most accidents
    ARGS
        df- pd.dataFrame
        start - startdate (e.g., '2017-01-01')
        num = number of locations to plot"""
    time_range_filter = df['DATE'] > '2017-01-01'
    df2018 = df[time_range_filter]
    top_locations_list = list(df2018.groupby(['INCIDENT_ADDRESS']).size().sort_values(ascending = False)[:num].index)
    top_locations_list
    top_locations_df = df2018[df2018['INCIDENT_ADDRESS'].isin(top_locations_list)][['INCIDENT_ADDRESS','DATE']].sort_values('DATE')
    top_locations_df.head()
    fig5, ax5 = plt.subplots(1, 1, figsize=(10, 5))
    ax5 = sns.swarmplot(y='INCIDENT_ADDRESS', x='DATE', data = top_locations_df, order= top_locations_list)
    ax5.set_title(title)
    ax5.set_ylabel(None)
    ax5.set_xlabel('Location')
    name=filename(title)
    save_location='images/'+name + '_swarm_plot.png'
    plt.savefig(save_location, bbox_inches="tight")


    
if __name__ == '__main__':
    df = pd.read_pickle('data/pickled_df')
    
#     #Plot accidents over time
#     fig, ax = plt.subplots(1, 1, figsize=(10, 5))
#     plot_over_time(df, 'DATE', ax, 'ACCIDENTS OVER TIME', 'Q')
    
#     #Plot seasonal variation
#     fig4, ax4 = plt.subplots(1, 1, figsize=(10, 5))
#     plot_months(df, ax4)
    
#     #Take a look at Human contributing factors
#     fig2, ax2 = plt.subplots(1, 1, figsize=(10, 5))
#     hist_categorical_factors(df, ax2, col = 'TU1_DRIVER_HUMANCONTRIBFACTOR', vals = ['NO APPARENT','NOT RECORDED'])
#     fig3, ax3 = plt.subplots(1, 1, figsize=(10, 10))
#     plot_human_factors_and_time(df, ax3)

#     #Take a look at road condition
#     fig5, ax5 = plt.subplots(1, 1, figsize=(10, 5))
#     hist_categorical_factors(df, ax5, col = 'ROAD_CONDITION', vals = ['DRY'], title = 'Road Condition')
    
#     #Take a look at light conditions
#     fig5, ax5 = plt.subplots(1, 1, figsize=(10, 5))
#     hist_categorical_factors(df, ax5, col = 'LIGHT_CONDITION', vals=['UNDER INVESTIGATION'], title = 'Light Condition')
    
#     #Take a look at road location
#     fig5, ax5 = plt.subplots(1, 1, figsize=(10, 5))
#     hist_categorical_factors(df, ax5, col = 'ROAD_LOCATION', vals=['UNDER INVESTIGATION'], title = 'Road Location')
    
#     #Take a look at driver action
#     fig5, ax5 = plt.subplots(1, 1, figsize=(10, 5))
#     hist_categorical_factors(df, ax5, col = 'TU1_DRIVER_ACTION',vals=['UNDER INVESTIGATION'], title = 'Driver Action')
    
#     #Take a look at time vs weekday
#     joint_plot(df, title = 'When Accidents occur', xlabel='Weekday', ylabel='Hour of day')
                             
                 
    #SwarmPlot
    swarm_plot(df)