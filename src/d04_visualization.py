import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height + 1,
                '%.0f' % int(height),
                ha='center', va='bottom')

def createandsavebarplots(dfplotleft, dfplotright, bar_width=0.12, category='BOROUGH', subcategory='YEAR'):        
    fig, (ax1, ax2) = plt.subplots(1,2, 
                                   sharey=True,
                                   figsize=(18,10), 
                                   gridspec_kw={'hspace': 0, 'wspace': 0.1})
    
    xlabels = list(dfplotleft[category])
    xticks = range(len(xlabels))
    subcat = list(dfplotright[subcategory].unique())
    
    #LEFT PLOT
    #Remove frame
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels, rotation='vertical')
    ax1.set_title('Average Totals by {}'.format(category))
    #values
    counts = list(dfplotleft['TOTALS']/len(subcat))#for mean display
    #plot
    ax1.bar(x=xticks, height=counts, align='center', alpha=0.6)
    #autolabel(c_rects, ax1)

    #RIGHT PLOT
    index = np.arange(len(dfplotleft.index))
    xticks = index + len(xlabels)*bar_width / 2
    #Remove frame
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels, rotation='vertical')
    ax2.set_title('Totals by {} and {}'.format(category, subcategory))
    #values
    i = 0
    for el in subcat:
        counts = list(dfplotright[dfplotright[subcategory]==el]['TOTALS'])
        ax2.bar(index +i*bar_width, counts, bar_width,
                     label=str(el))
        i += 1
    
    
    ax2.legend(loc='lower left', bbox_to_anchor=(1, 0))
    #plt.tight_layout()
    plt.show()
    fig.savefig(r'..\data\04_output\TotalsBy{}and{}.png'.format(category, subcategory))

def createandsavehourplots(df):
    fig, (ax1,ax3) = plt.subplots(1,2,figsize=(18,10),gridspec_kw={'hspace': 0, 'wspace': 0.35})
    xlabels = list(df['HOUR'])
    xticks = np.arange(len(xlabels))-0.5 #-0.5 to draw the ticks in between of the bars
    
    color = 'tab:blue'
    #Remove frame
    #ax.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Total Crashs', color=color)
    ax1.set_title('Average Totals by HOUR')
    ax1.bar(x=xlabels, height=list(df['TOTAL CRASHS']), align='center', alpha=0.6, width=0.9, color=color)
    ax1.tick_params('y', labelcolor = color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    #Remove frame
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)

    color = 'tab:orange'
    ax2.set_ylabel('Danger Rate', color=color)  # we already handled the x-label with ax1
    ax2.plot(xlabels,df['DANGER RATE'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    #ax3 = ax1.twinx()   instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    #Remove frame
    #ax.spines['left'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.set_xticks(xticks)#-0.5 to draw the ticks in between of the bars
    ax3.set_xticklabels(xlabels)
    ax3.set_xlabel('Hour')
    ax3.set_ylabel('Total Crashs', color=color)
    ax3.set_title('Totals by HOUR')
    ax3.bar(x=xlabels, height=list(df['TOTAL CRASHS']), align='center', alpha=0.6, width=0.9, color=color)
    ax3.tick_params('y', labelcolor = color)

    ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis
    ax4.spines['top'].set_visible(False)
    ax4.spines['bottom'].set_visible(False)

    color = 'tab:red'
    ax4.set_ylabel('Death Rate', color=color)  # we already handled the x-label with ax1
    ax4.plot(xlabels, df['DEATH RATE'], color=color)
    ax4.tick_params(axis='y', labelcolor=color)

    #plt.tight_layout()
    plt.show()
    fig.savefig(r'..\data\04_output\TotalsByHour.png')

    
def drawplot(dataframe, xlabel, ylabel, ltitle, rtitle):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(18,10),gridspec_kw={'hspace': 0, 'wspace': 0.35})

    width = 0.2

    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.set_xlabel(xlabel)
    ax1.set_xticks(np.arange(len(dataframe.index))+width)
    ax1.set_xticklabels(list(dataframe[xlabel.upper()]))
    ax1.set_ylabel(ylabel)
    ax1.set_title(ltitle)
    ax1.bar(x=np.arange(len(dataframe[xlabel.upper()])), height=dataframe['NUMBER OF PEDESTRIANS INJURED'], width=width, color='blue', label='Pedestrians')
    ax1.bar(x=np.arange(len(dataframe[xlabel.upper()]))+width, height=dataframe['NUMBER OF CYCLIST INJURED'], width=width, color='red', label='Cyclists')
    ax1.bar(x=np.arange(len(dataframe[xlabel.upper()]))+2*width, height=dataframe['NUMBER OF MOTORIST INJURED'], width=width, color='green', label='Motorists')
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))

    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.set_xlabel(xlabel)
    ax2.set_xticks(np.arange(len(dataframe[xlabel.upper()]))+width)
    ax2.set_xticklabels(list(dataframe[xlabel.upper()]))
    ax2.set_ylabel(ylabel)
    ax2.set_title(rtitle)
    ax2.bar(x=np.arange(len(dataframe[xlabel.upper()])), height=dataframe['NUMBER OF PEDESTRIANS KILLED'], width=width, color='blue', label='Pedestrians')
    ax2.bar(x=np.arange(len(dataframe[xlabel.upper()]))+width, height=dataframe['NUMBER OF CYCLIST KILLED'], width=width, color='red', label='Cyclists')
    ax2.bar(x=np.arange(len(dataframe[xlabel.upper()]))+2*width, height=dataframe['NUMBER OF MOTORIST KILLED'], width=width, color='green', label='Motorists')

    #plt.tight_layout()
    plt.show()
    fig.savefig(r'..\data\04_output\InjuriesAndFatalitiesBy{}.png'.format(xlabel))    

    
def make_map(x, y, projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(13,13), subplot_kw=dict(projection=projection))
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

def drawheatmap(heatmap, figx, figy, extent, reader):
    fig, m = make_map(x=figx, y=figy)
    m.set_extent = extent
    m.set_title('NYC Vehicle Crashs Causing Motorist Injuries 2013-2019', weight='heavy')
    im = m.imshow(heatmap.T, extent=extent, origin='lower',transform=ccrs.PlateCarree(), cmap='coolwarm')
    for borough in reader.records():
        m.add_geometries(borough.geometry, ccrs.PlateCarree(),facecolor='grey', edgecolors='black', alpha=0.3)
        m.add_geometries(borough.geometry, ccrs.PlateCarree(),facecolor='None', edgecolors='black', alpha=1)
        x = borough.geometry.centroid.x        
        y = borough.geometry.centroid.y
        m.text(x, y, borough.attributes['boro_name'], color='black', size=13, ha='right', va='top', weight='heavy', transform=ccrs.PlateCarree())
    m.set_aspect(figx/figy)
    plt.show()
    fig.savefig(r'..\data\04_output\MapMotoristInjuries.png', transparent=True, bbox_inches='tight')

def drawgpsdata(df, figx, figy, extent, reader):
    request = cimgt.GoogleTiles()
    fig, m = make_map(figx, figy, projection=request.crs)
    m.set_title('NYC Vehicle Crashs 2013-2019', weight='heavy')
    m.set_extent(extent)
    for borough in reader.records():
        m.add_geometries(borough.geometry, ccrs.PlateCarree(),facecolor='grey', edgecolors='black', alpha=0.3)
        m.add_geometries(borough.geometry, ccrs.PlateCarree(),facecolor='None', edgecolors='black', alpha=1)
        x = borough.geometry.centroid.x        
        y = borough.geometry.centroid.y
        m.text(x, y, borough.attributes['boro_name'], color='black', size=13, ha='right', va='top', weight='heavy', transform=ccrs.PlateCarree())
    m.add_image(request, 11)
    m.scatter(list(df.LONGITUDE[df.SEVERITY==0]),list(df.LATITUDE[df.SEVERITY==0]), color='red', marker='o', s=0.001, alpha=1,transform=ccrs.PlateCarree())
    m.scatter(list(df.LONGITUDE[df.SEVERITY==1]),list(df.LATITUDE[df.SEVERITY==1]), color='red', marker='o', s=0.001, alpha=1,transform=ccrs.PlateCarree())
    m.scatter(list(df.LONGITUDE[df.SEVERITY==2]),list(df.LATITUDE[df.SEVERITY==2]), color='red', marker='o', s=0.001, alpha=1,transform=ccrs.PlateCarree())
    m.set_aspect(figy/figx)
    plt.show()
    fig.savefig(r'..\data\04_output\MapVehicleCrashs.png', transparent=True, bbox_inches='tight')

def drawfromdataframe(df,x, y, title):
    df = df.set_index(x)
    plot = df[y].sort_values(ascending=False).drop('None').head(5).sort_values(ascending=True).plot(kind='barh', title=title)
    plt.show()
    fig = plot.get_figure()
    fig.savefig(r'..\data\04_output\Top5_{}.png'.format(title.replace(" ","")), bbox_inches='tight')
    
def main():
    
    #read data
    df = pd.read_feather(r'..\data\02_intermediate\NYC_VehicleCollisions_cleaned.feather')
    dfborough = pd.read_feather(r'..\data\03_processed\NYC_proc_byborough.feather')
    dfyear = pd.read_feather(r'..\data\03_processed\NYC_proc_byyear.feather')
    dfboroughyear = pd.read_feather(r'..\data\03_processed\NYC_proc_byboroughyear.feather')
    dfhour = pd.read_feather(r'..\data\03_processed\NYC_proc_byhour.feather')
    dfmonth = pd.read_feather(r'..\data\03_processed\NYC_proc_bymonth.feather')
    dfweekday = pd.read_feather(r'..\data\03_processed\NYC_proc_byweekday.feather')
    dfcauses = pd.read_feather(r'..\data\03_processed\NYC_proc_bycauses.feather')
    
    #draw and save pictures
    createandsavebarplots(dfborough,dfboroughyear, category='BOROUGH', subcategory='YEAR')
    createandsavebarplots(dfyear,dfboroughyear, category='YEAR', subcategory='BOROUGH')
    createandsavehourplots(dfhour)
    drawplot(dfyear, 'Year', 'Totals', 'Total Injured', 'Total Killed')
    drawplot(dfmonth, 'Month', 'Totals', 'Total Injured', 'Total Killed')
    drawplot(dfweekday, 'Weekday', 'Totals', 'Total Injured', 'Total Killed')
    drawfromdataframe(dfcauses,'CONTRIBUTING FACTOR VEHICLE 1', 'NUMBER OF PERSONS KILLED', 'Total Fatality Causes')
    drawfromdataframe(dfcauses,'CONTRIBUTING FACTOR VEHICLE 1', 'NUMBER OF PEDESTRIANS KILLED', 'Pedestrian Fatality Causes')
    drawfromdataframe(dfcauses,'CONTRIBUTING FACTOR VEHICLE 1', 'NUMBER OF MOTORIST KILLED', 'Motorist Fatality Causes')
    drawfromdataframe(dfcauses,'CONTRIBUTING FACTOR VEHICLE 1', 'NUMBER OF CYCLIST KILLED', 'Cyclist Fatality Causes')
    
    #GPS Maps
    ##draw map
    reader = shpreader.Reader(r'..\data\01_raw\Borough Boundaries\geo_export_00e2b999-6122-421c-a134-a3aea95afdef.shp' )
    
    ##data & constants
    extent = [-74.3, -73.68,40.48, 40.92]
    step = 0.009#0.0015
    bins = [np.arange(extent[0], extent[1],step), np.arange(extent[2], extent[3],step)]
    df = df[(df.LONGITUDE > extent[0]) & (df.LONGITUDE < extent[1]) & (df.LATITUDE > extent[2]) & (df.LATITUDE < extent[3])]
    heatmap, xedges, yedges = np.histogram2d(list(df.LONGITUDE[df['NUMBER OF MOTORIST INJURED']>0]), list(df.LATITUDE[df['NUMBER OF MOTORIST INJURED']>0]), bins=bins, range=[[extent[0],extent[1]],[extent[2],extent[3]]])
    figx = len(xedges)
    figy = len(yedges)
    
    ##drawmaps
    drawheatmap(heatmap, figx, figy, extent, reader)
    drawgpsdata(df, figx, figy, extent, reader)
    
main()