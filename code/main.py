import pandas as pd
import plotly as pl
import os
import datetime
import math

import matplotlib.pyplot as plt
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors
import numpy as np
from numpy.random import seed
from numpy.random import rand
import scipy.stats as stats

def prepFolders():
	main_folders = ['figures']
	# Create main folders:
	for folder in main_folders:
		if not os.path.exists(folder):
			os.makedirs(folder)
	
## Please make sure both the .xlsx file and main.py are in the same folder
## Input: N/A
## Output: path of the current folder
def xlsx_folder():
	xlsx_folder = os.getcwd()
	return xlsx_folder

## Input: Path to the main folder where all files reside
## Output: Full path to the .xlsx file in the given folder.(Finds by extension)
def find_xlsx_file(path):
	for file in os.listdir(str(path)):
		if file.endswith(".xlsx"):
			xlsx_path = os.path.join(str(path), file)
	return xlsx_path

## Returns the unique options in a given column of a dataframe
## type(df)= dataFrame type(column)=string
def get_column_options(df_x,column):
    df_x = df_x.drop_duplicates(column)
    options = [item for item in df_x[column]]
    return options

def filterByColumnsValue(df,column,filterValue):
	return df[df[column].isin(filterValue)]

def saveFigControlVsVariantUserCountPerDay(df,first_groupby,second_groupby,x_axis,figTitle='FigTitle'):
    df_vc_byFirstBySecondGroup = df.groupby([first_groupby,second_groupby], as_index=False).agg({'Visitors_Control':sum})
    df_vv_byFirstBySecondGroup = df.groupby([first_groupby,second_groupby], as_index=False).agg({'Visitors_Variant':sum})
    
    fig,ax =  plt.subplots(2,1,sharex=True)
    fig.suptitle(figTitle)
    uniq_metrics = get_column_options(df_x=df,column=second_groupby)
    for metric in uniq_metrics:
        df_vc_single_metric = filterByColumnsValue(df=df_vc_byFirstBySecondGroup,column=second_groupby,filterValue=[metric])
        ax[0].plot(x_axis,df_vc_single_metric['Visitors_Control'],label=metric)
        ax[0].set_title('Visitor Control')
        ax[0].legend()

        df_vv_single_metric = filterByColumnsValue(df=df_vv_byFirstBySecondGroup,column=second_groupby,filterValue=[metric])
        ax[1].plot(x_axis,df_vv_single_metric['Visitors_Variant'],label=metric)
        ax[1].set_title('Visitor Variant')
        ax[1].legend()
        for a in ax.flat:
            a.set(xlabel='Dates', ylabel='User Count')
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for a in ax.flat:
            a.label_outer()
    title = figTitle + '.png'
    fig.savefig(os.path.join(os.path.join(os.getcwd(),'figures'),title))

def determine_metricName(metric,second_groupby):
    metricName = metric
    
    if metric == 0 and second_groupby == 'Land':
            metricName = 'Didn\'t Land'
    elif metric == 1 and second_groupby == 'Land':
        metricName = 'Landed'
    
    if metric == 0 and second_groupby == 'Bounce':
        metricName = 'Didn\'t Bounce'
    elif metric == 1 and second_groupby == 'Bounce':
        metricName = 'Bounced'

    if metric == 0 and second_groupby == 'Purchase':
        metricName = 'Didn\'t Purchase'
    elif metric == 1 and second_groupby == 'Purchase':
        metricName = 'Purchased'
    return metricName

def saveSingFigControlVsVariantUserCountPerDay(df,first_groupby,second_groupby,x_axis,figTitle='FigTitle'):
    
    df_vc_byFirstBySecondGroup = df.groupby([first_groupby,second_groupby], as_index=False).agg({'Visitors_Control':sum})
    df_vv_byFirstBySecondGroup = df.groupby([first_groupby,second_groupby], as_index=False).agg({'Visitors_Variant':sum})

    print('df_vc_byFirstBySecondGroup = ',df_vc_byFirstBySecondGroup)
    print('df_vv_byFirstBySecondGroup = ',df_vv_byFirstBySecondGroup)
    t,p = stats.ttest_ind(df_vc_byFirstBySecondGroup['Visitors_Control'],df_vv_byFirstBySecondGroup['Visitors_Variant'])
    
    print('second_groupby = ',second_groupby)
    fig,ax =  plt.subplots(1,1,sharex=True)
    fig.suptitle(figTitle)
    uniq_metrics = get_column_options(df_x=df,column=second_groupby)
    print('uniq_metrics = ',uniq_metrics)
    

    for metric in uniq_metrics:
        print('metric = ',metric)
        df_vc_single_metric = filterByColumnsValue(df=df_vc_byFirstBySecondGroup,column=second_groupby,filterValue=[metric])
        metricName = determine_metricName(metric,second_groupby)
        print('metricName = ',metricName)
        print('Control = ')
        print(df_vc_single_metric['Visitors_Control'])
        
        ax.plot(x_axis,df_vc_single_metric['Visitors_Control'],label=str(metricName)+' (control)')
        ax.set_title(second_groupby)
        

        df_vv_single_metric = filterByColumnsValue(df=df_vv_byFirstBySecondGroup,column=second_groupby,filterValue=[metric])
        print('Variant = ')
        print(df_vv_single_metric['Visitors_Variant'])

        ax.plot(x_axis,df_vv_single_metric['Visitors_Variant'],label=str(metricName)+' (variant)')
        ax.legend()
    
    title = figTitle + '.png'
    fig.savefig(os.path.join(os.path.join(os.getcwd(),'figures'),title))
    return p


if __name__ == '__main__':
	
    # Create folder name: folder to save figures
    prepFolders()

    ## xlsx Reading into Pandas DataFrame ##
    main_folder = xlsx_folder()
    xlsx_path = find_xlsx_file(os.path.join(main_folder,'Product_Case_Data'))
    df = pd.read_excel(io=xlsx_path)

    print(df.head())
    print('info = ',df.info())
    print('describe = ',df.describe())
    print('channel = ',df.Channel.unique())
    print('ut = ',df['User Type'].unique())
    print('l = ',df['Land'].unique())
    print('b = ',df.Bounce.unique())
    print('Purchase = ',df.Purchase.unique())
    print('Visitors_Control = ',df.Visitors_Control.unique())
    print('Visitors_Variant = ',df.Visitors_Variant.unique())

    #######################################################################
    #######################################################################
    ######################### FIRST QUESTION ##############################
    #######################################################################
    #######################################################################

    ##################### CONVERSTION RATE CALCULATION ####################
    #######################################################################
    
    ## Find How Many People Visit per Visitor Control & per Visitor Variant
    vc_total_count = df['Visitors_Control'].sum()
    vv_total_count = df['Visitors_Variant'].sum()

    ## Calculate Total Number of People Who Made a Purchase per Visitor Control & per Visitor Variant
    # 1. Find DataFrame with All Users That Made a Purchase
    df_purchased = df[df['Purchase'] == 1]
    # 2. Sum the Visitor Control & Visitor Variant Users to Get the Total
    vc_purchased_count = df_purchased['Visitors_Control'].sum()
    vv_purchased_count = df_purchased['Visitors_Variant'].sum()
    print(f'vc_purchased_count = {vc_purchased_count}')
    print(f'vv_purchased_count = {vv_purchased_count}')
    t_conversionRate,p_conversionRate = stats.ttest_ind(df_purchased['Visitors_Control'],df_purchased['Visitors_Variant'])
    
    ## Calculate Conversion Rate
    vc_convRate = vc_purchased_count/vc_total_count*100
    vv_convRate = vv_purchased_count/vv_total_count*100
    print(f'vc_convRate = {vc_convRate:.2f}%')
    print(f'vv_convRate = {vv_convRate:.2f}%')


    ####################### BOUNCE RATE CALCULATION #######################
    #######################################################################
    ## V𝑖𝑠𝑖𝑡𝑜𝑟𝑠 𝑡h𝑎𝑡 𝑏𝑜𝑢𝑛𝑐𝑒 𝑓𝑟𝑜𝑚 𝑡h𝑒 h𝑜𝑚𝑒 𝑝𝑎𝑔𝑒 
    df_bounced = df[df['Bounce'] == 1]
    vc_bounced_count = df_bounced['Visitors_Control'].sum()
    vv_bounced_count = df_bounced['Visitors_Variant'].sum()
    print(f'vc_bounced_count = {vc_bounced_count}')
    print(f'vv_bounced_count = {vv_bounced_count}')

    ## T𝑜𝑡𝑎𝑙 𝑣𝑖𝑠𝑖𝑡𝑜𝑟𝑠 𝑡h𝑎𝑡 𝑙𝑎𝑛𝑑 𝑜𝑛 𝑡h𝑒 h𝑜𝑚𝑒 𝑝𝑎𝑔𝑒
    df_landed = df[df['Land'] == 1]
    vc_landed_count = df_landed['Visitors_Control'].sum()
    vv_landed_count = df_landed['Visitors_Variant'].sum()
    print(f'vc_landed_count = {vc_landed_count}')
    print(f'vv_landed_count = {vv_landed_count}')
    t_bounceRate,p_bounceRate = stats.ttest_ind(df_landed['Visitors_Control'],df_landed['Visitors_Variant'])

    ## Calculate Bounce Rate:
    vc_bounceRate = vc_bounced_count/vc_landed_count*100
    vv_bounceRate = vv_bounced_count/vv_landed_count*100
    print(f'vc_bounceRate = {vc_bounceRate:.2f}%')
    print(f'vv_bounceRate = {vv_bounceRate:.2f}%')
    print(f'Control has {vv_bounceRate-vc_bounceRate:.2f}% less bounce compared to variant')

    ########################### END OF Q2 ##############################
    ####################################################################

    #### PERFORMANCE OF THE CHANNEL IN CONTROL AND VARIANT #########
    uniq_dates = get_column_options(df_x=df,column='Date')
    # print('dates = ',uniq_dates)

    p1 = saveSingFigControlVsVariantUserCountPerDay(df=df,first_groupby='Date',second_groupby='Channel',x_axis=uniq_dates,figTitle='Channel Performance')    
    p2 = saveSingFigControlVsVariantUserCountPerDay(df=df,first_groupby='Date',second_groupby='User Type',x_axis=uniq_dates,figTitle='User Type Performance')
    p3 = saveSingFigControlVsVariantUserCountPerDay(df=df,first_groupby='Date',second_groupby='Land',x_axis=uniq_dates,figTitle='Land Performance')
    p4 = saveSingFigControlVsVariantUserCountPerDay(df=df,first_groupby='Date',second_groupby='Bounce',x_axis=uniq_dates,figTitle='Bounce Performance')
    p5 = saveSingFigControlVsVariantUserCountPerDay(df=df,first_groupby='Date',second_groupby='Purchase',x_axis=uniq_dates,figTitle='Purchase Performance')


    #### Q4: SUPPLIMENTARY ####
    p_values_metrics = [p1,p2,p3,p4,p5]
    print('Looking at p-values to see if there was any significant difference between the control and variant group')
    print(f'p-values for each metric = {p_values_metrics}')
    print(f'p_conversionRate = ',p_conversionRate)
    print(f'p_bounceRate = ',p_bounceRate)
    print(f'All the p values are greater than 0.05 so we can conclude that experiment didn\'t have a significant impact:\'( ')
    
    df_conv_channel_vc = df.groupby(['Date','Channel','Purchase'], as_index=False).agg({'Visitors_Control':sum})
    df_conv_channel_vv = df.groupby(['Date','Channel','Purchase'], as_index=False).agg({'Visitors_Variant':sum})

    # df_conv_channel_vc = df.groupby(['Date','Channel','Purchase']).agg({'Visitors_Control':sum})
    # df_conv_channel_vv = df.groupby(['Date','Channel','Purchase']).agg({'Visitors_Variant':sum})

    print('df_conv_channel_vc =',df_conv_channel_vc)
    print('df_conv_channel_vv =',df_conv_channel_vv.head(20))
    
    ######################################################################
    #### Q4: WHAT'S THE CONV RATE PER CHANNEL PER CONTROL AND VARIANT ####
    ######################################################################

    # Get Total Number of People per Channel for Control&Variant 
    totControl_people_per_channel = df.groupby(['Channel']).agg({'Visitors_Control':sum}).to_dict()
    totVariant_people_per_channel = df.groupby(['Channel']).agg({'Visitors_Variant':sum}).to_dict()
    print('totControl_people_per_channel = ',totControl_people_per_channel)
    print('totVariant_people_per_channel = ',totVariant_people_per_channel)

    # Get the number of people who purchased and didn't purchase per channel for both Control&Variant
    df_vc_channel = df.groupby(['Channel','Purchase'], as_index=False).agg({'Visitors_Control':sum})
    df_vv_channel = df.groupby(['Channel','Purchase'], as_index=False).agg({'Visitors_Variant':sum})

    print('df_vc_channel = ',df_vc_channel)
    print('df_vv_channel = ',df_vv_channel)


    uniq_channels = get_column_options(df_x=df,column='Channel')
    vc_purchased_per_channel = {}
    vv_purchased_per_channel = {}
    for channel in uniq_channels:
        df_1 = filterByColumnsValue(df=df_vc_channel,column='Channel',filterValue=[channel])
        df_2 = filterByColumnsValue(df=df_1,column='Purchase',filterValue=[1])

        df_3 = filterByColumnsValue(df=df_vv_channel,column='Channel',filterValue=[channel])
        df_4 = filterByColumnsValue(df=df_3,column='Purchase',filterValue=[1])

        vc_purchased_per_channel[channel] = int(df_2['Visitors_Control'])
        vv_purchased_per_channel[channel] = int(df_4['Visitors_Variant'])
    
    print('vc_purchased_per_channel = ',vc_purchased_per_channel)
    print('vv_purchased_per_channel = ',vv_purchased_per_channel)


    print('a=',vc_purchased_per_channel.values())
    print('totControl_people_per_channel = ',totControl_people_per_channel['Visitors_Control'].values())

    vc_conv_rate_per_channel = [i / j for i, j in zip(list(vc_purchased_per_channel.values()), list(totControl_people_per_channel['Visitors_Control'].values()))]
    vc_conv_rate_per_channel = [i * 100 for i in vc_conv_rate_per_channel]
    
    vv_conv_rate_per_channel = [i / j for i, j in zip(list(vv_purchased_per_channel.values()), list(totVariant_people_per_channel['Visitors_Variant'].values()))]
    vv_conv_rate_per_channel = [i * 100 for i in vv_conv_rate_per_channel]

    vc_conv_rate_dict = {}
    vv_conv_rate_dict = {}
    i=0
    for channel in uniq_channels:
        vc_conv_rate_dict[channel] = vc_conv_rate_per_channel[i]
        vv_conv_rate_dict[channel] = vv_conv_rate_per_channel[i]
        i = i + 1
    print('vc_conv_rate_dict = ',vc_conv_rate_dict)
    print('vv_conv_rate_dict = ',vv_conv_rate_dict)
    print('Look values above..')
    print(f'1 part of the q4 is that there is not much of a difference between variant and control per channel...')

    #### Q4 CONTINUED #### : BOUNCE RATE PER CHANNEL

    bounced_count_perChannel_vc = df_bounced.groupby(['Channel'],as_index=False).agg({'Visitors_Control':sum})
    bounced_count_perChannel_vv = df_bounced.groupby(['Channel'],as_index=False).agg({'Visitors_Variant':sum})
    print('bounced_count_perChannel_vc = ',bounced_count_perChannel_vc)
    print('bounced_count_perChannel_vv = ',bounced_count_perChannel_vv)
    tot_landed_count_perChannel_vc = df_landed.groupby(['Channel'],as_index=False).agg({'Visitors_Control':sum})
    tot_landed_count_perChannel_vv = df_landed.groupby(['Channel'],as_index=False).agg({'Visitors_Variant':sum})
    print('landed_count_perChannel_vc = ',tot_landed_count_perChannel_vc)
    print('landed_count_perChannel_vv = ',tot_landed_count_perChannel_vv)
    bounced_count_perChannel_vc['Control_Bounce_Rates'] = bounced_count_perChannel_vc['Visitors_Control']/tot_landed_count_perChannel_vc['Visitors_Control']*100
    bounced_count_perChannel_vv['Variant_Bounce_Rates'] = bounced_count_perChannel_vv['Visitors_Variant']/tot_landed_count_perChannel_vv['Visitors_Variant']*100
    print('bounced_count_perChannel_vc = ',bounced_count_perChannel_vc)
    print('bounced_count_perChannel_vv = ',bounced_count_perChannel_vv)

    ################# END OF BOUNCE RATE PER CHANNEL #############

    ############# Purchased per Channel and per User Type #############
    ###################################################################
    df_purchased_per_ch_per_uType = df_purchased.groupby(['Channel','User Type'],as_index=False).agg({'Visitors_Control':sum,'Visitors_Variant':sum})
    print('df_purchased_per_ch_per_uType = ')
    print(df_purchased_per_ch_per_uType)
    


    
    
    
    
    

        


    
    

    

    
    


    