#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests


CLIENT_ID='290e7fe179ab41459e19b98510a0f9c5'
CLIENT_SECRET='f39df4cca1184723860fe2449b07bc86'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = f"Bearer {auth_response_data['access_token']}"
print(access_token)


# In[3]:


userid='cqjdjhde9cqbcm6gu0hd8evez'


# In[4]:




url = f"https://api.spotify.com/v1/users/{userid}/playlists?limit=50"

payload={}
headers = {
  'Authorization': access_token
}

response = requests.request("GET", url, headers=headers, data=payload)

#print(response.text)
playlistsdata=response.json()
playlistsdata


# In[5]:


plkeys=list(playlistsdata.keys())
i=0
while i<len(playlistsdata.keys()):
    print(playlistsdata[plkeys[i]])
    i=i+1 
    


# In[6]:


import pandas as pd
import numpy as np
#print(plkeys)
pldf=pd.DataFrame(playlistsdata['items'])
pldf.index+=1
pldfowners=[]
for i in range(len(pldf)):
    pldfowner=str(pldf['owner'][i+1]['display_name'])
    pldfowners.append(pldfowner)
#print(pldfowners)
pldf['Own']=pldfowners

pldffiltered=pldf.loc[(pldf['Own']=='Raghul')|(pldf['Own']=='radhavaghi')]
pldffiltered.reset_index=[x+1 for x in range(len(pldffiltered))]
pid=list(pldffiltered['id'])
#pid.reset_index=[x+1 for x in range(len(pid))]
pldffiltered[['id','name']]
#pldffiltered=pldffiltered.reset_index(drop=True)
pldffiltered.index=np.arange(1,len(pldffiltered)+1)
pldffiltered


# In[7]:


pldf['owner'][1]['display_name']
referencepid=pldffiltered[['id','name']]
referencepid


# In[8]:


sumlist,tracklist=[],[]
sum=0
for i in range(len(pldffiltered)):
    x=pldffiltered['tracks'][i+1]['total']
    sum=sum+x
    sumlist.append(sum)
    tracklist.append(x)
    print(x,sum)
noftracksdf=pd.DataFrame(columns=['Playlist ID','Playlist Name','No of tracks','Total tracks'])
referencepid=pldffiltered[['id','name']]

noftracksdf['Playlist ID']=referencepid['id']
noftracksdf['Playlist Name']=referencepid['name']
noftracksdf['No of tracks']=tracklist
noftracksdf['Total tracks']=sumlist
noftracksdf


# In[9]:


noftracksdf['No of tracks'].describe()


# In[29]:


import matplotlib.pyplot as plt
plt.pie(np.array(noftracksdf['No of tracks']),labels=list(noftracksdf['Playlist Name']),shadow=True,autopct='%.1f%%')
plt.rcParams["figure.figsize"] = [12, 5]
plt.rcParams["figure.autolayout"] = True
plt.legend()
plt.show()


# In[11]:


from collections import defaultdict

listraw=defaultdict(list)
listof=[]
for i in range(len(noftracksdf)):
    for j in range(0,noftracksdf['No of tracks'][i+1],50):
        url = f"https://api.spotify.com/v1/users/{userid}/playlists/{noftracksdf['Playlist ID'][i+1]}/tracks?limit=50&offset={j}"

        payload={}
        headers = {
          'Authorization': access_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        d1=response.json()
        #dd[noftracksdf['Playlist ID'][i+1]]=d1
        #listof.append(d1)
        #if noftracksdf['Playlist ID'][i+1] not in listraw:
            #listraw[noftracksdf['Playlist ID'][i+1]]=d1
        listraw[noftracksdf['Playlist ID'][i+1]].append(d1)
        #else:
            #listraw[noftracksdf['Playlist ID'][i+1]].append(d1)

    
    

    
        
        
            #listraw[noftracksdf['Playlist ID'][i+1]]=response.json()
        
    
    
    

listraw


# In[12]:


#referencepid=pldffiltered[['id','name']]

#referencepid.iloc[0]['id']
#listraw[referencepid.iloc[8]['id']]['total']
#print(dd)
#len(dd[noftracksdf.iloc[11]['Playlist ID']]['items'])
#listraw[noftracksdf.iloc[8]['Playlist ID']][3]['items'][2]
#listraw[noftracksdf.iloc[0]['Playlist ID']][0]['items'][0]['track')]


# In[13]:


listoftracks=[]

for i in range(len(noftracksdf)):
    for j in range(len(listraw[noftracksdf.iloc[i]['Playlist ID']])):
        for k in range(len(listraw[noftracksdf.iloc[i]['Playlist ID']][j]['items'])):
            trackdict=listraw[noftracksdf.iloc[i]['Playlist ID']][j]['items'][k]['track']
            if trackdict:
                listoftracks.append(trackdict)
          

            
listoftracksdf=pd.DataFrame(listoftracks)

listoftracksdf.index+=1
listoftracksdf.head()


# In[14]:


playlistbreakup=pd.Series(np.array(noftracksdf['No of tracks']),index=noftracksdf['Playlist Name'])
playlistbreakup
#len(noftracksdf['No of tracks'])


# In[15]:


listoftracksdf=listoftracksdf.assign(Playlist_Name=0)
k=0
for i in range(len(noftracksdf)):
    
    
    j=noftracksdf['No of tracks'][i+1]
    print(j,k)
    listoftracksdf['Playlist_Name'].loc[k:k+j]=noftracksdf['Playlist Name'][i+1]
    k=k+j
listoftracksdf
#for i in range(len(noftracksdf)):
#    listoftracksdf.loc[:noftracksdf['Playlist Name'][i+1]]


# In[16]:


listoftracksdf['album'][1]


# In[17]:


listoftracksdf[['id','name','Playlist_Name','popularity','duration_ms','album','artists']]


# In[18]:


listoftracksdf['artists'][1]


# In[19]:


artist,album=[],[]
for i in range(len(listoftracksdf)):
    album.append(listoftracksdf['album'][i+1]['name'])
    coartist=[]
    for j in range(len(listoftracksdf['artists'][i+1])):
        coartist.append(listoftracksdf['artists'][i+1][j]['name'])
            #print(coartist)
    artist.append(coartist)

listoftracksdf['artistsc']=artist
listoftracksdf['albumc']=album


# In[30]:


listoftracksdf2=listoftracksdf[['id','name','Playlist_Name','popularity','duration_ms','albumc']]
xyza=listoftracksdf2
xyza


# In[21]:


dictrepeat={}
x=listoftracksdf2[listoftracksdf2['name'].duplicated(keep=False)]
x=x.reset_index()
x.index+=1
x

for i in range(1,len(x)):
    for j in range(i+1,len(x)):
        a=x['name'][i]
        b=x['name'][j]
        
        if a==b:
            print(f'{a} {i} a')
            print(f'{b} {j}b')
            if a in dictrepeat:
                if x['Playlist_Name'][j] not in dictrepeat[a]:
                    dictrepeat[a].append(x['Playlist_Name'][j])
            else:
                dictrepeat[a]=[x['Playlist_Name'][i]]

                dictrepeat[a].append(x['Playlist_Name'][j])


# In[22]:


repeatsongs=list(dictrepeat.keys())
len(repeatsongs)
dictrepeat
repeatsongs


# In[23]:


nofpl=[]
for i in range(len(repeatsongs)):
    a=len(dictrepeat[repeatsongs[i]])
    nofpl.append(a)
    
hrepeat=[]    
for i in range(len(nofpl)):
    if nofpl[i]>2:
        print(repeatsongs[i],nofpl[i])
        xx=(repeatsongs[i],listoftracksdf2.loc[(listoftracksdf2['Playlist_Name']==dictrepeat[repeatsongs[i]][0])&(listoftracksdf2['name']==repeatsongs[i])]['albumc'].values[0])
        hrepeat.append(xx)
    elif nofpl[i]==2:
        if listoftracksdf2['popularity'].iloc[i]>70:
            print(repeatsongs[i],nofpl[i])
            xy=(repeatsongs[i],listoftracksdf2.loc[(listoftracksdf2['Playlist_Name']==dictrepeat[repeatsongs[i]][0])&(listoftracksdf2['name']==repeatsongs[i])]['albumc'].values[0])
            hrepeat.append(xy)
    

hrepeatdf=pd.DataFrame(hrepeat,columns=['Song','Album'])

hrepeatdf.index+=1
hrepeatdf


# In[24]:


hrepeatdf.to_excel(r'C:\Users\Raghul\Desktop\playlist.xlsx')


# In[25]:


x


# In[26]:


import seaborn as sns
sns.heatmap(x[['popularity','duration_ms']].corr(), cmap = "coolwarm")


# In[27]:


pd.DataFrame(repeatsongs)


# In[ ]:




