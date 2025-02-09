import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from dash import html
import plotly_express as px
#from dash_bootstrap_templates import load_figure_template

# loads the "sketchy" template and sets it as the default
#load_figure_template("plotly_dark")  # serve per avere lo sfondo nero anche nei grafici, tolta perche da problemi nella legenda del pie chart

# lettura del file
df = pd.read_csv('ds531_classi_reddito_complessivo.csv', sep=';', header = 0,  names= ['Anno','Classi_di_reddito_complessivo','Frequenza_persone_fisiche','Ammontare_totale'])
df['Reddito_medio']= df['Ammontare_totale']/df['Frequenza_persone_fisiche']
df['Reddito_medio']= round(df['Ammontare_totale']/df['Frequenza_persone_fisiche'],0)

# creo colonna con valore dell'ammontare del reddito standardizzato al 2008, calcolato per ogni classe di reddito ((ammontare anno specifico - ammontare 2008)/ ammontare 2008)*100 
df_ammontare_2008 = df[['Anno','Classi_di_reddito_complessivo','Ammontare_totale']].query('Anno == 2008')
df['Ammontare_rapporto_index_2008'] = df['Ammontare_totale'].div(df['Classi_di_reddito_complessivo'].map(df_ammontare_2008.set_index('Classi_di_reddito_complessivo')['Ammontare_totale']))
df['Ammontare_rapporto_index_2008'] = (df['Ammontare_rapporto_index_2008'] -1)*100
df['Ammontare_rapporto_index_2008'] = round(df['Ammontare_rapporto_index_2008'],2)

# creo colonna con valore della freq persone fisiche standardizzato al 2008, calcolato per ogni classe di reddito ((freq anno specifico - freq 2008)/ freq 2008)*100 
df_frequenza_2008 = df[['Anno','Classi_di_reddito_complessivo','Frequenza_persone_fisiche']].query('Anno == 2008')
df['Frequenza_persone_index_2008'] = df['Frequenza_persone_fisiche'].div(df['Classi_di_reddito_complessivo'].map(df_frequenza_2008.set_index('Classi_di_reddito_complessivo')['Frequenza_persone_fisiche']))
df['Frequenza_persone_index_2008'] = (df['Frequenza_persone_index_2008'] -1)*100
df['Frequenza_persone_index_2008'] = round(df['Frequenza_persone_index_2008'],2)


# creo colonna con valore del reddito_medio standardizzato al 2008, calcolato per ogni classe di reddito ((reddito_medio anno specifico - reddito_medio 2008)/ freq 2008)*100 
df_reddito_medio_2008 = df[['Anno','Classi_di_reddito_complessivo','Reddito_medio']].query('Anno == 2008')
df['Reddito_medio_index_2008'] = df['Reddito_medio'].div(df['Classi_di_reddito_complessivo'].map(df_reddito_medio_2008.set_index('Classi_di_reddito_complessivo')['Reddito_medio']))
df['Reddito_medio_index_2008'] = (df['Reddito_medio_index_2008'] -1)*100
df['Reddito_medio_index_2008'] = round(df['Reddito_medio_index_2008'],2)


#################################
### SEZIONE AMMONTARE REDDITO####
#################################
# grafici dinamici
#elementi grafico dinamico 1
graph_1 = dcc.Graph(id='graf_bar_amm')
radio_1 = dcc.RadioItems(id='radio_1_amm', options=df['Classi_di_reddito_complessivo'].unique(), value='da 10.000 a 15.000')
#elementi grafico dinamico 2
graph_2 = dcc.Graph(id='graf_bar_amm_2')
radio_2 = dcc.RadioItems(id='radio_2_amm', options=df['Classi_di_reddito_complessivo'].unique(), value='da 10.000 a 15.000')
# grafici statici
grafico_1 = px.line(df, x='Anno', y='Ammontare_totale', color='Classi_di_reddito_complessivo',
                    title='Andamento dell\' ammontare del reddito complessivo per classe di reddito',
                    color_discrete_sequence= px.colors.qualitative.D3
                    )    #D3 serve per avere colori legenda non riprodotti ogni 5 items

grafico_2 = px.bar(df, x='Anno', y='Ammontare_totale', color='Classi_di_reddito_complessivo',
                    title='Confronto ammontare del reddito complessivo per classe di reddito',barmode='group',
                    color_discrete_sequence= px.colors.qualitative.D3,) 



# Creo tabella pivot dell'ammmontare totale
tabella_pivot_amm = pd.pivot_table(
    data=df,
    index= 'Anno',
    columns='Classi_di_reddito_complessivo',
    values='Ammontare_totale'
).reset_index()

# Creo tabella pivot dell'ammmontare totale standardizzato al 2008
tabella_pivot_amm_std = pd.pivot_table(
    data=df,
    index= 'Anno',
    columns='Classi_di_reddito_complessivo',
    values='Ammontare_rapporto_index_2008'
).reset_index()


#################################
### SEZIONE FREQUENZA####
#################################

# grafici dinamici
#elementi grafico dinamico 1
graph_1_p = dcc.Graph(id='graf_bar_freq')
radio_1_p = dcc.RadioItems(id='radio_1_freq', options=df['Classi_di_reddito_complessivo'].unique(), value='da 10.000 a 15.000')
#elementi grafico dinamico 2
graph_2_p = dcc.Graph(id='graf_bar_freq_2')
radio_2_p = dcc.RadioItems(id='radio_2_freq', options=df['Classi_di_reddito_complessivo'].unique(), value='da 10.000 a 15.000')
#elementi grafico dinamico 3   pie
graph_3_p = dcc.Graph(id='graf_pie_freq')
radio_3_p = dcc.RadioItems(id='radio_3_freq', options=df['Anno'].unique(), value= 2022)
# grafici statici
grafico_1_p = px.line(df, x='Anno', y='Frequenza_persone_fisiche', color='Classi_di_reddito_complessivo',
                    title='Andamento del numero di persone appartenenti a una classe di reddito',
                    color_discrete_sequence= px.colors.qualitative.D3,)    #D3 serve per avere colori legenda non riprodotti ogni 5 items

grafico_2_p = px.bar(df, x='Anno', y='Frequenza_persone_fisiche', color='Classi_di_reddito_complessivo',
                    title='Confronto del numero di persone appartenenti a una classe di reddito',barmode='group',
                    color_discrete_sequence= px.colors.qualitative.D3,) 


# Creo tabella pivot della frequenza persone fisiche
tabella_pivot_freq = pd.pivot_table(
    data=df,
    index= 'Anno',
    columns='Classi_di_reddito_complessivo',
    values='Frequenza_persone_fisiche'
).reset_index()

# Creo tabella pivot della frequenza persone fisiche standardizzato al 2008
tabella_pivot_freq_std = pd.pivot_table(
    data=df,
    index= 'Anno',
    columns='Classi_di_reddito_complessivo',
    values='Frequenza_persone_index_2008'
).reset_index()


#################################
### SEZIONE REDDITO ANNUO MEDIO####
#################################
# grafici dinamici
#elementi grafico dinamico 1
graph_1_rm = dcc.Graph(id='graf_bar_rm')
radio_1_rm = dcc.RadioItems(id='radio_1_rm', options=df['Classi_di_reddito_complessivo'].unique(), value='da 10.000 a 15.000')
#elementi grafico dinamico 2
graph_2_rm = dcc.Graph(id='graf_bar_rm_2')
radio_2_rm = dcc.RadioItems(id='radio_2_rm', options=df['Classi_di_reddito_complessivo'].unique(), value='da 10.000 a 15.000')

# grafici statici
grafico_1_rm = px.line(df, x='Anno', y='Reddito_medio', color='Classi_di_reddito_complessivo',
                    title='Andamento dell\' ammontare del reddito medio per classe di reddito',
                    color_discrete_sequence= px.colors.qualitative.D3,)    #D3 serve per avere colori legenda non riprodotti ogni 5 items

grafico_2_rm = px.bar(df, x='Anno', y='Reddito_medio', color='Classi_di_reddito_complessivo',
                    title='Confronto dell\' ammontare del reddito medio per classe di reddito',barmode='group',
                    color_discrete_sequence= px.colors.qualitative.D3,) 

# Creo tabella pivot del reddito medio
tabella_pivot_rm = pd.pivot_table(
    data=df,
    index= 'Anno',
    columns='Classi_di_reddito_complessivo',
    values='Reddito_medio'
).reset_index()

# Creo tabella pivot del reddito medio standardizzato al 2008
tabella_pivot_rm_std = pd.pivot_table(
    data=df,
    index= 'Anno',
    columns='Classi_di_reddito_complessivo',
    values='Reddito_medio_index_2008'
).reset_index()


# Creo l'app dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server
# App Layout frontend
app.layout = dbc.Container([
    html.H1('REDDITO CITTA\' DI MILANO',style={'textAlign': 'center'}),
    html.Br(),
    html.H5('dati presi a questo link https://dati.comune.milano.it/dataset/ds531_distribuzione-del-reddito-complessivo-delle-persone-fisiche-2008-avanti'),
    html.Br(),
    html.H2('SEZIONE: ANALISI AMMONTARE DEL REDDITO TOTALE'),
    dbc.Row(dcc.Graph(figure=grafico_1),
            ),
     html.Br(),
    dbc.Row(dcc.Graph(figure=grafico_2),
            ),
    html.Br(),
    html.H4('Ammontare del reddito complessivo'),
    html.Br(), 
    dbc.Row([
        dbc.Col([ radio_1
            
        ], width=3),
        
        dbc.Col([ graph_1
            
        ], width=9),
    ]),
    html.Br(),
    html.H4('Dati del dataset relativi all\' ammontare del reddito complessivo'),
    html.Br(),
    dbc.Table.from_dataframe(tabella_pivot_amm, style={'textAlign' : 'center'}, 
                             #??????? format = {locale ={'grouping' : [3]}
                                                 ),  # to do la visualizzazione deve essere arrotondata.
    html.Br(),
    html.H4('Dati variazione percentuale ammontare del reddito complessivo rispetto al dato del 2008'),
    html.Br(),
    dbc.Table.from_dataframe(tabella_pivot_amm_std, style={'textAlign' : 'center'}),  
    html.Br(),
    html.H4('Variazione percentuale ammontare del reddito complessivo rispetto al dato del 2008'),
    html.Br(),
       dbc.Row([
        dbc.Col([ radio_2
            
        ], width=3),
        
        dbc.Col([ graph_2
            
        ], width=9),
    ]),
    html.Br(),
    html.H2('ANALISI DELLA FREQUENZA PERSONE FISICHE'),
    html.Br(),
    dbc.Row(dcc.Graph(figure=grafico_1_p),
            ),
     html.Br(),
    dbc.Row(dcc.Graph(figure=grafico_2_p),
            ),
    html.Br(),
    html.H4('Numero di persone appartenenti a una classe di reddito'),
    html.Br(),
    dbc.Row([
        dbc.Col([ radio_1_p
            
        ], width=3),
        
        dbc.Col([ graph_1_p
            
        ], width=9),
    ]),
    html.Br(),    
    html.H4('Dati del dataset relativi al numero di persone appartenenti a una classe di reddito'),
    html.Br(),
    dbc.Table.from_dataframe(tabella_pivot_freq, style={'textAlign' : 'center'}, 
                             #??????? format = {locale ={'grouping' : [3]}
                                                 ),  # to do la visualizzazione deve essere arrotondata.
    html.Br(),
    html.H4('Dati variazione percentuale ammontare del numero di persone appartenenti a una classe di reddito rispetto al dato del 2008'),
    html.Br(),
    dbc.Table.from_dataframe(tabella_pivot_freq_std, style={'textAlign' : 'center'}),  
    html.Br(),
    html.H4('Variazione percentuale del numero di persone appartenenti a una classe di reddito rispetto al dato del 2008'),
    html.Br(),
       dbc.Row([
        dbc.Col([ radio_2_p
            
        ], width=3),
        
        dbc.Col([ graph_2_p
            
        ], width=9),
                ]),
    html.Br(),
    html.H4('Percentuale del numero di persone appartenenti a una classe di reddito'),
    html.Br(),     
     dbc.Row([
        dbc.Col([ radio_3_p
            
        ], width=3),
        
        dbc.Col([ graph_3_p
            
        ], width=9),    
    html.Br(),      
            ]),
html.Br(),    
html.H2('SEZIONE: ANALISI AMMONTARE DEL REDDITO MEDIO'),
html.Br(),    
dbc.Row(dcc.Graph(figure=grafico_1_rm),
            ),
     html.Br(),
    dbc.Row(dcc.Graph(figure=grafico_2_rm),
            ),
html.Br(),
html.H4('Ammontare del reddito medio'),
html.Br(), 
html.Br(),
    dbc.Row([
        dbc.Col([ radio_1_rm
            
        ], width=3),
        
        dbc.Col([ graph_1_rm
            
        ], width=9),
    ]),
    html.Br(),    
    html.H4('Dati calcolati dal dataset relativi all\' ammontare del reddito medio per classe di reddito'),
    html.Br(),        
    dbc.Table.from_dataframe(tabella_pivot_rm, style={'textAlign' : 'center'}, 
                             #??????? format = {locale ={'grouping' : [3]}
                                                 ),  # to do la visualizzazione deve essere arrotondata.
    html.Br(),
    html.H4('Dati variazione percentuale ammontare del reddito medio rispetto al dato del 2008'),
    html.Br(),
    dbc.Table.from_dataframe(tabella_pivot_rm_std, style={'textAlign' : 'center'}),  
    html.Br(),
    html.H4('Variazione percentuale dell\' ammontare del reddito medio rispetto al dato del 2008'),
    html.Br(),
       dbc.Row([
        dbc.Col([ radio_2_rm
            
        ], width=3),
        
        dbc.Col([ graph_2_rm
            
        ], width=9),
                ]),
    html.Br(),         
        
        
])


# Callback
# grafico 1
@callback(
    Output(component_id='graf_bar_amm', component_property='figure'),
    Input(component_id='radio_1_amm', component_property='value')
)
def update_grafico(selected_class):
    filtered_df = df[df['Classi_di_reddito_complessivo'] == selected_class]
    fig = px.bar(filtered_df, x='Anno', y='Ammontare_totale',
                 text=['{:.3}B'.format(x / 1000000000) for x in filtered_df['Ammontare_totale']],
                                  )
    fig.update_traces(textposition= "outside")
    return fig

# grafico 2
@callback(
    Output(component_id='graf_bar_amm_2', component_property='figure'),
    Input(component_id='radio_2_amm', component_property='value')
)
def update_grafico(selected_class):
    filtered_df = df[df['Classi_di_reddito_complessivo'] == selected_class]
    fig = px.bar(filtered_df, x='Anno', y='Ammontare_rapporto_index_2008',
                 text=['{:.2f}%'.format(x) for x in filtered_df['Ammontare_rapporto_index_2008']],
                                  )
    fig.update_traces(textposition= "outside")
    return fig

# grafico 1 frequenza
@callback(
    Output(component_id='graf_bar_freq', component_property='figure'),
    Input(component_id='radio_1_freq', component_property='value')
)
def update_grafico(selected_class):
    filtered_df = df[df['Classi_di_reddito_complessivo'] == selected_class]
    fig = px.bar(filtered_df, x='Anno', y='Frequenza_persone_fisiche',
                 text=['{:}'.format(x) for x in filtered_df['Frequenza_persone_fisiche']],
                                  )
    fig.update_traces(textposition= "outside")
    return fig

# grafico 2 freq
@callback(
    Output(component_id='graf_bar_freq_2', component_property='figure'),
    Input(component_id='radio_2_freq', component_property='value')
)
def update_grafico(selected_class):
    filtered_df = df[df['Classi_di_reddito_complessivo'] == selected_class]
    fig = px.bar(filtered_df, x='Anno', y='Frequenza_persone_index_2008',
                 text=['{:.2f}%'.format(x) for x in filtered_df['Frequenza_persone_index_2008']],
                                  )
    fig.update_traces(textposition= "outside")
    return fig

# grafico 3 freq   pie
@callback(
    Output(component_id='graf_pie_freq', component_property='figure'),
    Input(component_id='radio_3_freq', component_property='value')
)
def update_grafico(selected_year):
    filtered_df = df[df['Anno'] == selected_year]
    fig = px.pie(filtered_df, names='Classi_di_reddito_complessivo', values='Frequenza_persone_fisiche', title= '', hole=.3, 
                 color = { label: color_1  for label, color_1 in zip(df['Classi_di_reddito_complessivo'].unique(), px.colors.qualitative.Light24)}
                               #color = { label: color  for label, color in zip(df['Classi_di_reddito_complessivo'].unique(), colormaps['Dark2'].colors)} 
                               ) # vedere colore legenda ,,,metterne più di 7 color_discrete_sequence=px.colors.qualitative.G10
    fig.update_traces(textposition= "outside", marker=dict(line=dict(color='#000000', width=2)),)
    return fig

# grafico 1 reddito medio
@callback(
    Output(component_id='graf_bar_rm', component_property='figure'),
    Input(component_id='radio_1_rm', component_property='value')
)
def update_grafico(selected_class):
    filtered_df = df[df['Classi_di_reddito_complessivo'] == selected_class]
    fig = px.bar(filtered_df, x='Anno', y='Reddito_medio',
                 text=['{:}'.format(x) for x in filtered_df['Reddito_medio']],
                                  )
    fig.update_traces(textposition= "outside")
    return fig

# grafico 2 reddito medio
@callback(
    Output(component_id='graf_bar_rm_2', component_property='figure'),
    Input(component_id='radio_2_rm', component_property='value')
)
def update_grafico(selected_class):
    filtered_df = df[df['Classi_di_reddito_complessivo'] == selected_class]
    fig = px.bar(filtered_df, x='Anno', y='Reddito_medio_index_2008',
                 text=['{:.2f}%'.format(x) for x in filtered_df['Reddito_medio_index_2008']],
                                  )
    fig.update_traces(textposition= "outside")
    return fig



# Run the App 
if __name__ == '__main__':
    app.run_server(debug = False)   # False per andare in deploy