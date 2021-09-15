#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing required packages

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


#Importing required dataset

df = pd.read_csv(r'A:\DataScience Projects\HotelBooking/hotel_bookings.csv')


# In[3]:


df.head()


# In[4]:


df.shape


# ### Data cleaning

# In[5]:


#Checking for missing values

df.isnull().values.any()


# In[6]:


#In which column there missing values?
df.isnull().sum()


# In[7]:


#Filling the missing values with 0 

df.fillna(0,inplace = True)


# In[8]:


df.isnull().sum()


# In[9]:


df['meal'].value_counts()


# In[10]:


df['children'].unique()


# In[11]:


df['adults'].unique()


# In[12]:


df['babies'].unique()


# In[13]:


filter = (df['children']==0)&(df['babies']==0)&(df['adults']==0)     
filter


#Adults,babies & children cant be zero at the same time 


# In[14]:


data = df[~filter]


# In[15]:


data.head()


# ### Where do the guests come from and performing spatial analysis
# 

# In[16]:


resort = data[(data['hotel']=='Resort Hotel') & (data['is_canceled']==0)]
city = data[(data['hotel']=='City Hotel') & (data['is_canceled']==0)]


# In[17]:


resort.head()


# In[18]:


city.head()


# In[19]:


import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px


# In[20]:


labels = resort['country'].value_counts().index
values = resort['country'].value_counts()


# In[21]:


fig = go.Figure(data = [go.Pie(labels = labels, values = values,
                               hoverinfo= 'label+percent',
                               textinfo = 'value')])
fig.update_layout(autosize = False,height = 500,width = 500,margin = dict(l = 20,r = 20,t = 20,b = 20))
             


# In[22]:


country_wise=data[data['is_canceled']==0]['country'].value_counts().reset_index()


# In[23]:


country_wise.columns=['Country','No. of guests']


# In[24]:


country_wise.head()


# #### Spatial Analysis

# In[25]:


px.choropleth(country_wise,locations = country_wise['Country'],
              color = country_wise['No. of guests'],hover_name=country_wise['Country'],title ='Home country of guests' )


# Most guests are from European countries in which Portugal is at the top.

# ### Price variation across years.

# #### Lets see how  much do the guests pay per night.

# In[26]:


data.columns


# In[27]:


d2 = data[data['is_canceled']==0]


# In[28]:


plt.figure(figsize = (12,8))
sns.boxplot(x = 'reserved_room_type',y = 'adr',data = d2,hue = 'hotel')
plt.title('Price of rooms per night per person',fontsize = 18),
plt.xlabel('Price')
plt.ylabel('Price[in Euros]')
plt.show


# This figure shows the average price per room, depending on its type and the standard deviation. Note that due to data anonymization rooms with the same type letter may not necessarily be the same across hotels.
# 

# #### Price variation per night over years

# In[29]:


data_resort = resort[resort['is_canceled']==0]
data_city= city[city['is_canceled']==0]


# In[30]:


resort_hotel = data_resort.groupby('arrival_date_month')['adr'].mean().reset_index()
city_hotel = data_city.groupby('arrival_date_month')['adr'].mean().reset_index()


# In[31]:


finaldf = resort_hotel.merge(city_hotel,on = 'arrival_date_month')


# In[32]:


finaldf.columns = ['Month','Price for Resort','Price for City Hotel']


# In[33]:


finaldf


# In[34]:


import sort_dataframeby_monthorweek as sd            


# In[35]:


final = sd.Sort_Dataframeby_Month(finaldf,'Month')


# In[36]:


final


# In[37]:


px.line(final,x = 'Month',y = ['Price for Resort','Price for City Hotel'],
        title = 'Room price Variation per night per person over the years' )


# We can see that for both the hotels price is highest during summer.

# ### Distribution of nights spent at hotels [by Market segment and Hotel type]

# In[38]:


data.head()


# In[39]:


plt.figure(figsize = (10,8))
sns.boxplot(x = 'market_segment',y = 'stays_in_weekend_nights',data = data,hue = 'hotel')


# MOst of the groups are normally distributed, some of them have positive skewness.
# Most of the people do not prefer to stay more than a week in hotels

# ### What do the guests prefer?

# In[40]:


data['meal'].value_counts()


# In[41]:


px.pie(data,values =data['meal'].value_counts(),names = data['meal'].value_counts().index,
       hole = 0.5 )


# Above the donut pie graph shows the meal categories. 
# There is a big difference in the Bed&Breakfast category and the others.
# Almost 80% of bookings reserved for Bed&Breakfast.

# ### Analyse special request done by customers

# In[42]:


data.head()


# In[43]:


sns.countplot(x = 'total_of_special_requests',data = data,palette = 'magma')


# Around 55% of the bookings do not have any special requests.

# ### Pivot table of special requests and cancellation.

# In[44]:


data.columns


# In[45]:


pivot_t=data.groupby(['total_of_special_requests','is_canceled']).agg({'total_of_special_requests':'count'}).rename(columns={'total_of_special_requests':'Count'}).unstack()


# In[46]:


pivot_t


# In[47]:


pivot_t.plot(kind = 'barh')


# The above  graph is about the relationship between special requests and cancellation of booking.
# Nearly half bookings without any special requests have been cancelled 
# and another half of them have not been canceled.

# ### Analysing Most busy month [Guests are high in which month]

# In[48]:


busyr = data_resort['arrival_date_month'].value_counts().reset_index()
busyc = data_city['arrival_date_month'].value_counts().reset_index()


# In[49]:


busyr.columns = ['Month','No of Guests']
busyc.columns = ['Month','No of Guests']


# In[50]:


busyr.head()


# In[51]:


busyc.head()


# In[52]:


f2 = busyr.merge(busyc,on = 'Month')


# In[53]:


f2.head()


# In[54]:


f2.columns = ['Month','No of guests in resort','No. of guests in city hotel']


# In[55]:


f2.head()


# In[56]:


final = sd.Sort_Dataframeby_Month(df = f2,monthcolumnname = 'Month')


# In[57]:


final.head()


# In[58]:


px.line(data_frame = final,x = 'Month',y =['No of guests in resort','No. of guests in city hotel']
                                          ,title = 'Total Number of Guests per months')


# The City hotel has more guests during spring and autumn, when the prices are also highest.
# In July and August there are less visitors, although prices are lower.
# 
# Guest numbers for the Resort hotel go down slighty from June to September, which is also when the prices are highest.
# Both hotels have the fewest guests during the winter.

# #### How long do people stay at hotels?

# In[59]:


data.head()


# In[60]:


filter = data['is_canceled']==0
clean_data = data[filter]


# In[61]:


clean_data.head()


# In[62]:


import warnings
from warnings import filterwarnings
filterwarnings('ignore')


# In[63]:


clean_data['Total_Nights']=clean_data['stays_in_weekend_nights']+clean_data['stays_in_week_nights']


# In[64]:


clean_data.head()


# In[65]:


stays = clean_data.groupby(['Total_Nights','hotel']).agg('count').reset_index()


# In[66]:


stays = stays.iloc[:,0:3]


# In[67]:


stays.head()


# In[68]:


stays = stays.rename(columns={'is_canceled':'No of stays'})


# In[69]:


stays.head()


# In[70]:


plt.figure(figsize = (20,8))
sns.barplot(x = 'Total_Nights',y = 'No of stays',hue ='hotel'
            ,hue_order=['City Hotel','Resort Hotel'],data = stays)


# ##### Bookings my Market segment

# In[71]:


clean_data.columns


# In[72]:


clean_data['market_segment'].value_counts()


# In[73]:


px.pie(clean_data,values =clean_data['market_segment'].value_counts()
      ,names = clean_data['market_segment'].value_counts().index,title = 'Bookings per Market Segment')


# Online TA dominates in bookings per markert segment.
# 

# ### Price per night(adr) and person based on booking and room 

# In[74]:


clean_data.columns


# In[75]:


plt.figure(figsize = (20,10))
sns.barplot(x = 'market_segment',y = 'adr',hue = 'reserved_room_type',data = clean_data)


# ##### How many bookings were cancelled?

# In[76]:


cancelled = data[data['is_canceled']==1]


# In[77]:


cancelled.head()


# In[78]:


len(cancelled[cancelled['hotel']=='Resort Hotel'])  ##Bookings cancelled in Resort Hotel


# In[79]:


len(cancelled[cancelled['hotel']=='City Hotel'])    ##Bookings cancelled in City Hotel


# In[80]:


px.pie(values=[11120,33079],names = ['Resort Cancellations','City Hotel Cancellations'])


# ##### Which Month has the highest cancellations?

# In[81]:


cmonth=data.groupby(['arrival_date_month','hotel']).agg('count').reset_index()
cancelled=cmonth.iloc[:,0:3]


# In[82]:


cancelled=cancelled.rename(columns={'is_canceled':'no of cancellations'})
cancelled.head()


# In[83]:


c2=sd.Sort_Dataframeby_Month(cancelled,'arrival_date_month')
c2.head()


# In[84]:


plt.figure(figsize=(12, 8))
sns.barplot(x = "arrival_date_month", y = "no of cancellations" , hue="hotel",
            hue_order = ["City Hotel", "Resort Hotel"], data=c2)


# For City hotel the relative number of cancelations is around 40 % throughout the year.
# 
# For Resort hotel it is highest in the summer and lowest during the winter.

# In[ ]:





# In[ ]:





# In[ ]:




