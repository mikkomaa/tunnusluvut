import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np

import fileutility

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Tunnusluvut'

# For Heroku
server = app.server

#######################################
# Global variables
#######################################

df, units = fileutility.prepare_data()
yhtiot = sorted(df['Yhtiö'].unique())
tunnusluvut = {
    'Sijoitukset': sorted((df.columns[[6, 7, 13, 14, 15, 16, 17, 18, 19]])),
    'Muut': sorted((df.columns[[4, 5, 8, 9, 10, 11, 12, 20, 21, 22, 23, 24, 25]]))
}
vuodet = sorted(df['Vuosi'].unique())

# Companies' own colors for Elo, Etera, Ilmarinen, Varma, and Veritas
colors = {
    'Alandia': '#b97454',
    'Elo': '#FFD200',
    'Etera': '#9ACD68',
    'Fennia': '#69BDD1',
    'Ilmarinen': '#003975',
    'Varma': '#D10168',
    'Veritas': '#00990F',
    'background': '#F9FBFD'
}

#######################################
# Modals
#######################################

tietoa_yhtioista = html.Div(children=[
    html.Section([
        html.H6('Sulautumiset'),
        html.P(['Nykyiset yhtiöt ovat Elo, Ilmarinen, Varma ja Veritas.',
                html.Br(),
                'Alandia sulautui Veritakseen 1.1.2019.',
                html.Br(),
                'Etera sulautui Ilmariseen 1.1.2018.',
                html.Br(),
                'Fennia sulautui Eloon 1.1.2014.'
                ])
    ]),
    html.Section([
        html.H6('Viralliset nimet'),
        html.P(['Försäkringsaktiebolaget Pensions-Alandia',
                html.Br(),
                'Keskinäinen Työeläkevakuutusyhtiö Elo',
                html.Br(),
                'Keskinäinen Eläkevakuutusyhtiö Etera',
                html.Br(),
                'Keskinäinen vakuutusyhtiö Eläke-Fennia',
                html.Br(),
                'Keskinäinen Eläkevakuutusyhtiö Ilmarinen',
                html.Br(),
                'Keskinäinen työeläkevakuutusyhtiö Varma',
                html.Br(),
                'Pensionsförsäkringsaktiebolaget Veritas'
                ]),
        html.P('''Elo toimi vuonna 2013 nimellä LähiTapiola Keskinäinen Eläkevakuutusyhtiö 
        ja sitä ennen nimellä Keskinäinen Eläkevakuutusyhtiö Tapiola.''')
    ])
])

tietoa_sivusta = html.Div(children=[
    html.P('''Sivulla voit luoda kaavioita työeläkevakuutusyhtiöiden tunnusluvuista. 
    Hiirellä tai kaavion painikkeilla voit esimerkiksi suurentaa tai vierittää kaavioita. 
    Osaa tunnusluvuista ei ole kaikilta vuosilta.'''),
    html.P(['Luvut ovat Finanssivalvonnan julkaisemista ',
            html.A('tilastoista', href='https://www.finanssivalvonta.fi/tilastot/vakuutus/elakevakuutus/'),
            ' ja yhtiöiden tilinpäätöksistä. Kunkin vuoden luvut ovat tilanne 31.12. ',
            'Lukujen pyöristystarkkuus vaihtelee.']),
    html.P(['Sivun lähdekoodi on ',
            html.A('GitHubissa', href='https://github.com/mikkomaa/tunnusluvut'),
            '.']),
    html.P('''Kysymyksiä ja kommentteja voit lähettää sähköpostilla mkkmatis at hotmail.com.''')
])

yhtio_info_button = dbc.Button('Tietoa yhtiöistä',
                               id='open-yhtio-modal',
                               outline=True,
                               style={
                                   'margin-top': 20,
                               })

sivu_info_button = dbc.Button('Tietoa sivusta',
                              id='open-sivu-modal',
                              outline=True,
                              style={
                                  'margin-top': 20,
                                  'margin-left': 20,
                              })

yhtio_modal = html.Div(
    [
        yhtio_info_button,
        dbc.Modal(
            [
                dbc.ModalHeader('Tietoa yhtiöistä'),
                dbc.ModalBody(
                    children=[
                        tietoa_yhtioista,
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button('Sulje',
                               id='close-yhtio-modal',
                               outline=True)
                ),
            ],
            id='yhtio-modal',
        ),
    ]
)

sivu_modal = html.Div(
    [
        sivu_info_button,
        dbc.Modal(
            [
                dbc.ModalHeader('Tietoa sivusta'),
                dbc.ModalBody(
                    children=[
                        tietoa_sivusta,
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button('Sulje',
                               id='close-sivu-modal',
                               outline=True)
                ),
            ],
            id='sivu-modal',
        ),
    ]
)

#######################################
# Options for the user
#######################################

yhtio_checklist = html.Div([
    html.H6('Yhtiöt'),
    dcc.Checklist(
        id='yhtio-checklist',
        options=[{'label': i, 'value': i} for i in yhtiot],
        value=['Elo', 'Ilmarinen', 'Varma', 'Veritas'],
        labelStyle={'display': 'inline-block', 'margin-right': 10},
        inputStyle={'margin-right': 2},
    ),
])

sijoitukset_dropdown = html.Div([
    html.H6('Sijoitusluvut'),
    dcc.Dropdown(
        id='sijoitukset-dropdown',
        options=[{'label': i, 'value': i} for i in tunnusluvut['Sijoitukset']],
        value=[tunnusluvut['Sijoitukset'][0]],
        placeholder='Valitse...',
        multi=True,
        style={'width': 450}
    )
])

muut_dropdown = html.Div([
    html.H6('Muut luvut'),
    dcc.Dropdown(
        id='muut-dropdown',
        options=[{'label': i, 'value': i} for i in tunnusluvut['Muut']],
        value=[tunnusluvut['Muut'][0]],
        placeholder='Valitse...',
        multi=True,
        style={'width': 450}
    )
])

vuosi_slider = html.Div([
    html.H6('Vuodet'),
    dcc.RangeSlider(
        id='vuosi-slider',
        min=vuodet[0],
        max=vuodet[-1],
        value=[vuodet[-5], vuodet[-1]],
        marks={str(year): str(year) for year in vuodet},
        step=None,
    )],
    style={'width': 450}
)

kaavio_radioitems = html.Div([
    html.H6('Kaavio'),
    dcc.RadioItems(
        id='kaavio-radioitems',
        className='radio-group',
        options=[{'label': 'Pylväs', 'value': 'bar'},
                 {'label': 'Viiva', 'value': 'line'}],
        value='bar',
        labelStyle={'display': 'inline-block', 'margin-right': 10},
        inputStyle={'margin-right': 2},
    )
])

#######################################
# Page layout
#######################################

app.layout = html.Div(
    html.Div([
        # Header
        html.Div([
            html.H2('Työeläkevakuutusyhtiöiden tunnusluvut',
                    style={'margin-left': 20},
                    ),
            html.Div([yhtio_modal],
                     style={'margin-left': 50},
                     ),
            html.Div([sivu_modal],
                     ),
        ], className='row'),

        # Options: yhtiöt, kaavio, vuodet
        html.Div([
            html.Div([yhtio_checklist],
                     style={'margin-left': 20}
                     ),
            html.Div([kaavio_radioitems],
                     style={'margin-left': 20}
                     ),
            html.Div([vuosi_slider],
                     style={'margin-left': 20}
                     )
        ], className='row'),

        # Options: sijoitusluvut, muut luvut
        html.Div([
            html.Div([sijoitukset_dropdown],
                     style={'margin-left': 20},
                     ),
            html.Div([muut_dropdown],
                     style={'margin-left': 20},
                     )
        ], className='row'),

        # Graphs, from create_graphs-method
        html.Div(id='container'),
    ])
)


#######################################
# Callbacks
#######################################

@app.callback(
    Output('container', 'children'),
    [Input('yhtio-checklist', 'value'),
     Input('sijoitukset-dropdown', 'value'),
     Input('muut-dropdown', 'value'),
     Input('vuosi-slider', 'value'),
     Input('kaavio-radioitems', 'value')]
)
def create_graphs(yhtiot, sijoitusluvut, muutluvut, vuodet, kaavio):
    """Create graphs to display"""
    yhtiot.sort()
    tunnusluvut = sorted(sijoitusluvut + muutluvut)
    vuodet = [i for i in range(vuodet[0], vuodet[1] + 1)]
    dff = df[df['Vuosi'].isin(vuodet)]

    graphs = []
    for t in tunnusluvut:
        graphs.append(dcc.Graph(
            id='graph-{}'.format(t),
            figure=create_figure(t, yhtiot, kaavio, dff),
        ))
    return html.Div(graphs,
                    className='row')


def create_figure(tunnusluku, yhtiot, kaavio, df):
    """Create a figure for a graph"""
    data = []
    for yhtio in yhtiot:
        dff = df[(df['Yhtiö'] == yhtio) & (df[tunnusluku] != np.nan)]
        if dff.empty:
            continue
        data.append({'x': dff['Vuosi'], 'y': dff[tunnusluku],
                     'type': kaavio, 'name': yhtio,
                     'marker': {'color': colors[yhtio]},
                     'hovertemplate': '%{y}',
                     'hoverlabel': {'bgcolor': 'white'},
                     }
                    )

    return {
        'data': data,
        'layout': dict(
            title=get_figure_title(tunnusluku),
            xaxis={
                'title': 'Vuosi',
                'dtick': 1
            },
            height=550,
            width=get_figure_width(yhtiot, kaavio, df),
            hovermode='closest',
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'])
    }


def get_figure_title(tunnusluku):
    """Return a figure title"""
    if units[tunnusluku] in ['euroa', 'kpl', '%']:
        return f'{tunnusluku} ({units[tunnusluku]})'
    return tunnusluku


def get_figure_width(yhtiot, kaavio, df):
    years = len(df['Vuosi'].unique())
    if kaavio == 'bar':
        width = max(550, 37 * years * len(yhtiot))
        return min(1200, width)
    return max(550, 75 * years)


# Modal callbacks
@app.callback(
    Output('sivu-modal', 'is_open'),
    [Input('open-sivu-modal', 'n_clicks'), Input('close-sivu-modal', 'n_clicks')],
    [State('sivu-modal', 'is_open')]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('yhtio-modal', 'is_open'),
    [Input('open-yhtio-modal', 'n_clicks'), Input('close-yhtio-modal', 'n_clicks')],
    [State('yhtio-modal', 'is_open')]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=False)  # Set debug=False for the production server
