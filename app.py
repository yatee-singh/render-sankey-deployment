## Main code containing backend(fetching data from API) and frontend(hiding,highlighting, grouping features)

##ERRORS
#  Doesnt display a message when no data is getting fetched(no data fits required filters)

## Can't make nested groups, fix by changing logic of grouping
##Debugs needed- display message when server has no data, fix flexbox of frontend
from dash import Dash, html, dcc, callback, Output, Input,ctx
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime,timedelta,timezone
from dash_extensions import EventListener
import requests 
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
import pytz
from dash import dcc,html,dash_table
from dash.dependencies import Input, Output
from dash_extensions.enrich import DashProxy, html, Input, Output, State
from dash_extensions import EventListener

app =Dash(__name__)
color_code2="#4f0099"
color_code1="#e6ccff"
red="rgb(255, 153, 153)"
dark_red='rgb(255, 133, 102)'
purple='rgb(230, 179, 255)'
dark_purple='rgb(230, 153, 255)'
base_url="http://10.1.19.105:5000/energygrid2?"
base_url2="http://10.1.19.105:5000/tempgrid2?"
lab=[]
src=[]
tar=[]
val=[]
hid=[]
ist_timezone = pytz.timezone("Asia/Kolkata")

branches=[] # will store the selected brnaches
groups={} #will store groups for un-grouping
nowStart=datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

def make_req_url(t1,t2):
    url=base_url+'where={"$and":[{"_created":{"$gte":"'+t1+'"}},{"_created":{"$lt":"'+t2+'"}}]}&max_results=1440'
    return url

def make_req_url_temp(t1,t2):
    url=base_url2+'where={"$and":[{"_created":{"$gte":"'+t1+'"}},{"_created":{"$lt":"'+t2+'"}}]}&max_results=1440'
    return url


now=datetime.now(timezone.utc)
ist_now=datetime.now(ist_timezone)
t1=now-timedelta(minutes=5)
ist1=ist_now-timedelta(minutes=5)
t2=now
t11=(t1-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT')
t21=(t2-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT')
url=make_req_url(t11,t21)
print(url)

#fetching data and making lab,sec,tar,val
r = requests.get(url) 
data={}


if r.status_code == 200:
    data = r.json()
else:
    print("Failed to fetch data from the API. Status code:", r.status_code)

#last_heard
print(data)

def update_last_heard():
    table_rows = []
    contents_string=""
    devices=[]
    t1=(datetime.now()-timedelta(days=90)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    t2=(datetime.now()).strftime('%a, %d %b %Y %H:%M:%S GMT')
    url=base_url+'where={"$and":[{"_created":{"$gte":"'+t1+'"}},{"_created":{"$lt":"'+t2+'"}}]}&max_results=1440'
    r_two_months=requests.get(url)

    if(r_two_months.status_code==200):
        res=r_two_months.json()
        df=pd.DataFrame.from_dict(pd.json_normalize(res['_items']), orient='columns')
        devices=list(df.Device_ID.unique())

    print(devices)
    def make_req_url(dev_id):
        url=base_url+'where={"Device_ID":"'+dev_id+'"}&sort=[("_created", -1)]&max_results=1'
        return url
    data={'date':[],'id':[]}

    for dev_id in devices:
        url=make_req_url(dev_id)
        r = requests.get(url) 
        data['id'].append(dev_id)
    # print(url)
        if r.status_code == 200:
            res=r.json()
            df = pd.DataFrame.from_dict(pd.json_normalize(res['_items']), orient='columns')
        # data[dev_id]=df['_created'].to_string()
            #print(df['_created'])
            date=datetime.strptime(df['Time_Stamp'].to_string()[5:15] + ' '+df['Time_Stamp'].to_string()[16:24] , "%Y-%m-%d %H:%M:%S")
            ist_date=date.astimezone(ist_timezone)
            print(ist_date)
            data['date'].append(ist_date)
        
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)

    df2=pd.DataFrame(data)
 
    df_sorted = df2.sort_values(by='date', ascending=False)
    print(df2['date'])
    df_sorted['date'] = df_sorted['date'].dt.strftime("%B %d, %Y %I:%M %p %Z")
    print(df_sorted['date'])
    
    # # Define function to convert date to UTC
    # def convert_to_utc(date):
    #     return date.astimezone(pytz.utc)

    # # Apply the function to each date in the DataFrame
    # df_sorted['date_utc'] = df_sorted['date'].apply(lambda x: convert_to_utc(x))
    
  
    return df_sorted

df_sorted=update_last_heard()

table =dash_table.DataTable(df_sorted.to_dict('records'), [{"name": i, "id": i} for i in df_sorted.columns],style_cell={'textAlign': 'center'})

# ans=update_last_heard()
# print(ans)

if(data['_items']!=[]):
    df = pd.DataFrame.from_dict(pd.json_normalize(data['_items']), orient='columns')
    lab=list(df.Device_ID.unique())
    print("lables are",lab)
    lab.insert(0,"MAIN_SUPPLY")


    #cretes power consumed column
    # df['power']=abs(df['Real_power'])
    df['power'] = pd.to_numeric(df['Real_power'], errors='coerce')
    df['power'].fillna(0, inplace=True)
    #finds avg power consumption
    averaged_columns=df.groupby(['Device_ID'])[df.select_dtypes(include='number').columns].mean()
    print(url)
    print(averaged_columns)

    #loads data for sankey diagram creation
    for r in averaged_columns.iterrows():
        src.append(0)
        temp=r[0]
        tar.append(lab.index(r[0]))
        val.append(r[1]['power'])


link_color = [color_code1]* len(src)# color of the links
node_colors = [color_code2]*len(lab)

fig = go.Figure(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=lab,
            color=node_colors
        ),
        link=dict(
            source=src,
            target=tar,
            value=val,
            color=link_color
        )
    ))

event = {"event": "click", "props": ["shiftKey"]}  #defining which prop of the event 'click' is needed 

#div for operation selection
branch_selection2 = dcc.Dropdown(
    id='branch-dropdown2',
    options=[
        {'label': 'Highlighting', 'value': 'Highlighting'},
        {'label': 'Hiding', 'value': 'Hiding'},
        {'label': 'Grouping', 'value': 'Grouping'},
        {'label': 'Un-grouping', 'value': 'Un-grouping'},
        {'label': 'Un-highlight', 'value': 'Un-highlight'},
        {'label': 'Un-hide', 'value': 'Un-hide'}
    ],
    value=''  # Default selection
)




app.layout = html.Div([
#      html.Div([
#     ,
#     # html.Div('Second div', style={'width': '50%', 'display': 'inline-block'})
# ],style={'width':'100%','padding-top':'8vh'}),
    html.Div([
        html.Div([
    html.H1('SANKEY DASHBOARD', style={'font-size': '50px'})
]), html.Hr(style={'height': '2px', 'border-width': '0', 'background-color': 'black', 'margin-top': '15px', 'margin-bottom': '15px'}),
        html.Div([
          
            html.Div(html.Button('◄', id='left-button', n_clicks=0, style={'background-color': dark_purple, 'border': 'none', 'color': 'white', 'padding': '10px 20px', 'text-align': 'center', 'font-size': '16px', 'margin': '4px 2px', 'cursor': 'pointer', 'border-radius': '12px', 'width': 'auto'}), style={'width':'10%'}),
            html.Div([
        EventListener(
        html.Div([
             dcc.Graph(figure=fig,id='sankey-diagram'),
        ]),
        events=[event], logging=True, id="el", style={'flex': '1','width':'100%'}
    ),
         dcc.Interval(
            id='interval-component',
            interval=1*60*1000, # in milliseconds
            
        ),
            html.Div(id='output-interval',children=ist1.strftime("%B %d, %Y %I:%M %p %Z"))
            , html.Hr(style={'height': '1px', 'border-width': '0', 'background-color': 'black', 'margin-top': '15px', 'margin-bottom': '15px','margin-top':'2vh'}),
           html.Div(dcc.Dropdown(
    id='branch-dropdown2',
    options=[
        {'label': 'Highlighting', 'value': 'Highlighting'},
        {'label': 'Hiding', 'value': 'Hiding'},
        {'label': 'Grouping', 'value': 'Grouping'},
        {'label': 'Un-grouping', 'value': 'Un-grouping'},
        {'label': 'Un-highlight', 'value': 'Un-highlight'},
        {'label': 'Un-hide', 'value': 'Un-hide'}
    ],
    value='' # Default selection
), style={ 'flex':'1','width':'20%','padding-left':'0px','margin-left':'0'})],style={'width':'80%','display':'flex','alignItems':'center','flex-direction':'column','padding':'0px','margin':'0'}),
            html.Div(html.Button('►', id='right-button', n_clicks=0,disabled='true', style={'background-color': dark_purple, 'border': 'none', 'color': 'white', 'padding': '10px 20px', 'text-align': 'center', 'font-size': '16px', 'margin': '4px 2px', 'cursor': 'pointer', 'border-radius': '12px', 'width': 'auto'}), style={'flex': '1'}),
        ], style={'padding-top':'0vw','display': 'flex', 'alignItems': 'center', 'justifyContent': 'center','width':'100%'}),
        html.Div([
    html.H6('Last Heard From Sensors:', style={'font-size': '30px'})
], style={'width':'100%'}),
      html.Div([
    html.Div( id="last-heard",children=table)
],style={'width':'50%', 'margin':'auto','textAlign': 'center','margin-bottom':'5vh'})
        
    ], style={'textAlign': 'center','width':'100%'}),
    
], style={'textAlign': 'center','width':'100%'})


# if __name__ == '__main__':
#     app.run_server(debug=True)




@dash.callback(
    Output('sankey-diagram', 'figure'),
    Output('branch-dropdown2','value'),
    Output('output-interval', 'children'),
    Output('right-button','disabled'),
    Input('interval-component', 'n_intervals'),
    Input('right-button', 'n_clicks'),
    Input('left-button', 'n_clicks'),
    Input('sankey-diagram', 'clickData'),
    Input('branch-dropdown2', 'value'),
    State("el", "event"),
       prevent_initial_call=True
    )


def update_sankey_diagram(n,n_inc,n_dec,branch1,operation,e):

    url=''
    global t1,t2,ist1
   
    global link_color
    global node_colors
    global lab
    global tar,val,src
    disabled=n_inc>=n_dec
    lc1=link_color.copy()
    now=datetime.now(timezone.utc)
    ist_now=datetime.now(ist_timezone)
    t1,t2,ist1
    if "right-button" == ctx.triggered_id or "left-button" == ctx.triggered_id or branch1==[]:
       
        if(n_inc<=n_dec):
        
            t1=now-timedelta(minutes=5*(abs(n_inc-n_dec)+1))
            ist1=ist_now-timedelta(minutes=5*(abs(n_inc-n_dec)+1))
            t2=now-timedelta(minutes=5*(abs(n_inc-n_dec)))
            
        else:
           
            t1=now-timedelta(minutes=5)
            ist1=ist_now-timedelta(minutes=5)
            t2=now
        
        url=make_req_url((t1-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'),(t2-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        print("URLLLLLLLLL IUSSSSSSSS",url)

        #fetching data and making lab,sec,tar,val
        r = requests.get(url) 
        global data
        print(url)
        if r.status_code == 200:
            data = r.json()
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)
        
        src=[]
        tar=[]
        val=[]
        if data['_items']!=[]:
            df = pd.DataFrame.from_dict(pd.json_normalize(data['_items']), orient='columns')
            lab=list(df.Device_ID.unique())
            lab.insert(0,"MAIN_SUPPLY")


            #cretes power consumed column
            df['power'] = pd.to_numeric(df['Real_power'], errors='coerce')
            df['power'].fillna(0, inplace=True)

            #finds avg power consumption
            averaged_columns=df.groupby(['Device_ID'])[df.select_dtypes(include='number').columns].mean()
            print(averaged_columns)

            #loads data for sankey diagram creation
        
        
            print(averaged_columns)
            for r in averaged_columns.iterrows():
                
                src.append(0)
                tar.append(lab.index(r[0]))
                val.append(r[1]['power'])

        print(len(src))
        link_color = [color_code1]*len(src)# color of the links
        node_colors = [color_code2]*len(lab)

        updated_fig =go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=lab,
                color=node_colors
            ),
            link=dict(
                source=src,
                target=tar,
                value=val,
                color=link_color
            )
        ))

        return [updated_fig, "",ist1.strftime("%B %d, %Y %I:%M %p %Z"),disabled]

    elif (branch1):
    
        branch=branch1['points'][0]['index'] 
        print(lab)
        print(tar)
        
        #print("branch : ",branch1['points'][0]['index'])
        #print("branch : ",operation)
    
        global branches

        #checks if shift key if pressed or not
        if e !=None:
            shift=e['shiftKey']
            #print("shift : ",shift)
            if(shift==True):
                # lc1[branch]='rgba(31,119,180,0.8)'
                if(branch not in branches):
                    branches.append(branch)
                    for a in branches:
                        if(lc1[a]==red):
                            lc1[a]=dark_red
                        else:
                            lc1[a]=dark_purple
            if(shift==False):
                branches=[branch]
                if(branch!=None):
                    if(lc1[branch]==red):
                    
                        lc1[branch]=dark_red
                    else : 
                        lc1[branch]=dark_purple
            


    
        if(operation=='Highlighting'):
        #inc opacity and change color of link for highlighting
                for a in branches:
                    link_color[a]=red
                    lc1[a]=red
                if(branches!=[]):
                    branches.clear()
            
            
        
    
        if(operation=='Hiding'):
        # make opacity 0 for hiding
                for a in branches:
                    link_color[a]='rgba(31,119,180,0.0)'
                    lc1[a]='rgba(31,119,180,0.0)'
                    #node_colors[a+1]='rgba(31,119,180,0.0)'
                if(branches!=[]):
                    branches.clear()
                    
                    
                    
                if(branches!=[]):
                    branches.clear()
            
        
        if(operation=='Un-highlight'): 
                for a in branches:
                    lc1[a]=purple 
                    link_color[a]=purple
                if(branches!=[]):
                    branches.clear()
        
        
        if(operation=='Un-hide'):
        #    lc1[branch]='#6E0CED'
            length = len(tar)
            for i in range(length):
                if(link_color[i]=='rgba(31,119,180,0.0)'):
                    lc1[i]=color_code1
                    link_color[i]=color_code1
            if(branches!=[]):
                    branches.clear()

        if(operation=="Grouping"):
            new_name=""
            global groups
            targets=[]
            branches.sort()

            #stores the name and index of nodes to be grouped
            for a in branches:
                new_name+=lab[tar[a]]+' '
                targets.append(tar[a])

            lab.append(new_name)
            node_colors.append(color_code2)
            groups.update({new_name:targets}) #adds group to dict to un-group later

            new_ind=len(lab)-1
            lent=len(src)
            #replaces all the selected nodes with group
            for i in range(lent):
                if src[i] in targets:
                    src[i]=new_ind
                if tar[i] in targets:
                    tar[i]=new_ind 
            
            if(branches!=[]):
                    branches.clear()
            
        if (operation=="Un-grouping"):
            
            grp_name=lab[tar[branches[0]]]#gets group name
            print(grp_name)
            targets=groups[grp_name]#extracts the original nodes of the group
            print(targets)
            length=len(src)
            k=0

            #replaces the group with original nodes
            for i in range(length):
                if lab[src[i]] ==grp_name:
                    if(k<len(targets)):
                        src[i]=targets[k]
                        #print(src[i],targets[k])
                        k+=1
                if lab[tar[i]] ==grp_name:
                    if(k<len(targets)):
                        tar[i]=targets[k]
                        #print(tar[i],targets[k])
                        k+=1
            if(branches!=[]):
                    branches.clear()
            

            
        
        updated_fig =go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=lab,
                color=node_colors
            ),
            link=dict(
                source=src,
                target=tar,
                value=val,
                color=lc1
            )
        ))

        return [updated_fig, "",ist1.strftime("%B %d, %Y %I:%M %p %Z"),disabled]
    else:
        t1=t1+n*timedelta(minutes=1)
        ist1=ist1+n*timedelta(minutes=1)
        t2=t2+n*timedelta(minutes=1)
        url=make_req_url((t1-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'),(t2-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        url2=make_req_url_temp((t1-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'),(t2-timedelta(minutes=5)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        print("URLLLLLLLLL IUSSSSSSSS",url)



        #fetching data and making lab,sec,tar,val
        r = requests.get(url) 
        r2=requests.get(url2)
       
       
        if r.status_code == 200:
            data = r.json()
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)

        if r2.status_code == 200:
            temp_data = r2.json()
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)
        
        src=[]
        tar=[]
        val=[]
   
        if data['_items']!=[]:
            df = pd.DataFrame.from_dict(pd.json_normalize(data['_items']), orient='columns')
            df2 = pd.DataFrame.from_dict(pd.json_normalize(temp_data['_items']), orient='columns')
            lab=list(df.Device_ID.unique())
            lab.insert(0,"MAIN_SUPPLY")
          
            #cretes power consumed column
            df['power'] = pd.to_numeric(df['Real_power'], errors='coerce')
            df['power'].fillna(0, inplace=True)

            #finds avg power consumption
            averaged_columns=df.groupby(['Device_ID'])[df.select_dtypes(include='number').columns].mean()
           
            #loads data for sankey diagram creation
        
        
            for r in averaged_columns.iterrows():
                
                src.append(0)
                tar.append(lab.index(r[0]))
                val.append(r[1]['power'])

      
        link_color = [color_code1]*len(src)# color of the links
        node_colors = [color_code2]*len(lab)

        updated_fig =go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=lab,
                color=node_colors
            ),
            link=dict(
                source=src,
                target=tar,
                value=val,
                color=link_color
            )
        ))
        print("why is this getting executed")
        return [updated_fig, "",ist1.strftime("%B %d, %Y %I:%M %p %Z"),disabled]
       





# @dash.callback(
   
#     Output('last-heard', 'children'),
   
#        prevent_initial_call=True
#     )


        

app.run_server(host="0.0.0.0", port="1000")


if __name__ == '__main__':
    app.run()
