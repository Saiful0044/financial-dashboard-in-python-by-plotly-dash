import dash
from dash import dcc,callback
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


# external css
external_stylesheets= [
      {
            "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
            "rel":"stylesheet",
            "integrity" : "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" ,
            "crossorigin": "anonymous"
      }]


# Dataset load
data = pd.read_csv('dataset/financial_data.csv')

# filter code start
data['pct_accounts_receivable'] = (data['accounts receivable'].pct_change()) * 100
data['pct_accounts_receivable'] = data['pct_accounts_receivable'].fillna(0)

data['pct_accounts_payable'] = (data['accounts payable'].pct_change()) * 100
data['pct_accounts_payable'] = data['pct_accounts_payable'].fillna(0)

data['pct_income'] = (data['income'].pct_change()) * 100
data['pct_income'] = data['pct_income'].fillna(0)

data['expenses'] = data['cost of goods sold'] + data['total operating expenses']
data['pct_expenses'] = (data['expenses'].pct_change()) * 100
data['pct_expenses'] = data['pct_expenses'].fillna(0)

data['gross profit'] = data['income'] - data['cost of goods sold']
data['pct_gross_profit'] = (data['gross profit'].pct_change()) * 100
data['pct_gross_profit'] = data['pct_gross_profit'].fillna(0)

data['pct_total_operating_expenses'] = (data['total operating expenses'].pct_change()) * 100
data['pct_total_operating_expenses'] = data['pct_total_operating_expenses'].fillna(0)

data['operating profit (EBIT)'] = data['gross profit'] - data['total operating expenses']
data['pct_operating_profit_(EBIT)'] = (data['operating profit (EBIT)'].pct_change()) * 100
data['pct_operating_profit_(EBIT)'] = data['pct_operating_profit_(EBIT)'].fillna(0)

data['pct_taxes'] = (data['Taxes'].pct_change()) * 100
data['pct_taxes'] = data['pct_taxes'].fillna(0)

data['pct_quick_ratio'] = (data['quick ratio'].pct_change()) * 100
data['pct_quick_ratio'] = data['pct_quick_ratio'].fillna(0)

data['pct_current_ratio'] = (data['current ratio'].pct_change()) * 100
data['pct_current_ratio'] = data['pct_current_ratio'].fillna(0)

data['pct_cash_at_eom'] = (data['cash at eom'].pct_change()) * 100
data['pct_cash_at_eom'] = data['pct_cash_at_eom'].fillna(0)

data['net profit'] = data['operating profit (EBIT)'] - data['Taxes']
data['pct_net_profit'] = (data['net profit'].pct_change()) * 100
data['pct_net_profit'] = data['pct_net_profit'].fillna(0)

data['net profit margin %'] = (data['net profit'] / data['income']) * 100
data['pct_net_profit_margin_%'] = (data['net profit margin %'].pct_change()) * 100
data['pct_net_profit_margin_%'] = data['pct_net_profit_margin_%'].fillna(0)

data['income budget %'] = (data['income'] / data['income budget']) * 100
data['pct_income_budget_%'] = (data['income budget %'].pct_change()) * 100
data['pct_income_budget_%'] = data['pct_income_budget_%'].fillna(0)

data['expense budget %'] = (data['expenses'] / data['expense budget']) * 100
data['pct_expense_budget_%'] = (data['expense budget %'].pct_change()) * 100
data['pct_expense_budget_%'] = data['pct_expense_budget_%'].fillna(0)

data['pct_cost_of_goods_sold'] = (data['cost of goods sold'].pct_change()) * 100
data['pct_cost_of_goods_sold'] = data['pct_cost_of_goods_sold'].fillna(0)

# Filter code end

# Initialization app
app = dash.Dash(__name__,external_stylesheets=external_stylesheets,meta_tags=[{'name':'viewport','content':'width=device-width'}])

app.layout = html.Div([
      dbc.Row([
            dbc.Col(html.Div(html.Img(src=app.get_asset_url('statistics.png'),id='statistics-image',
                              style={
                                    'height':'60px',
                                    'width':'auto',
                                    'margin-bottom':'25px',
                                    'display':'inline-block'
                              })), width=3),

            dbc.Col(html.Div( html.H3('Financial Dashboard',style={'color': '#D35940','display':'inline-block'} )), width=3),

            dbc.Col(html.Div(html.H6('Select Month Name: ',style={'color': '#D35940','display':'inline-block','text-align-last': 'end'} )), width=3),

            dbc.Col(html.Div(dcc.Dropdown(
                              id='select_month',
                              multi=False,
                              clearable=True,
                              value = 'Mar',
                              options= [{'label': i, 'value': i} for i in (data['months'].unique())]
                        )), width=3),
      ], justify="center",className='my-custom-row'),  # Centers the row content

      html.Br(),
      dbc.Row([
            dbc.Col([
                  # first row start
                  dbc.Row([
                        dbc.Col([
                              dbc.Row([
                                    html.Div([
                                          html.Div([
                                                html.P('Accounts Receivable'),
                                                html.Div(
                                                      id = 'accounts_receivable_value',
                                                      ),
                                                html.P('vs previous month')
                                          ],className='card-body',style={'text-align': 'center'})
                                    ],className='card')
                              ],justify="center"),

                              html.Br(),

                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Accounts Payable'),
                                                html.Div(id = 'accounts_payable_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ],justify="center")

                        ],width=3), # Left side card end

                        # 1st circle start
                        dbc.Col([
                              html.Div([
                                    dcc.Graph(id = 'pie_chart1',
                                          config = {'displayModeBar': False},
                                          style={'margin-left':'-3px','margin-top':'130px'}
                                    ),
                              ])
                        ],width=3), # 1st circle end


                        # Right side card start
                        dbc.Col([
                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Income'),
                                                html.Div(id = 'income_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ]),


                              html.Br(),

                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Expenses'),
                                                html.Div(id = 'expenses_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ])
                        ],width=3), # Right side card end


                        # 2nd right circle start
                        dbc.Col([
                              html.Div([
                                    dcc.Graph(id = 'pie_chart2',
                                          config = {'displayModeBar': False},
                                          style={'margin-left':'-3px','margin-top':'130px'}
                                    ),
                              ])
                        ],width=3), # 2nd right circle end



                  ]), # first row end

                  html.Br(),

                  # 2nd row start 
                  dbc.Row([
                        dbc.Col([
                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Quick Ratio'),
                                                html.Div(id = 'quick_ratio_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ]),

                              html.Br(),

                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Current Ratio'),
                                                html.Div(id = 'current_ratio_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ])

                        ],width=3), # Left side card end

                        # 1st circle start
                        dbc.Col([
                              html.Div([
                                    dcc.Graph(id = 'pie_chart3',
                                          config = {'displayModeBar': False},
                                          style={'margin-left':'-3px','margin-top':'130px'}
                                    ),
                              ])
                        ],width=3), # 1st circle end


                        # Right side card start
                        dbc.Col([
                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Net Profit'),
                                                html.Div(id = 'net_profit_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ]),


                              html.Br(),

                              dbc.Row([
                                    dbc.Card([
                                          dbc.CardBody([
                                                html.P('Cash at EOM'),
                                                html.Div(id = 'cash_at_eom_value'),
                                                html.P('vs previous month')
                                          ])
                                    ])
                              ])
                        ],width=3), # Right side card end


                        # 2nd right circle start
                        dbc.Col([
                              html.Div([
                                    dcc.Graph(id = 'pie_chart4',
                                          config = {'displayModeBar': False},
                                          style={'margin-left':'-3px','margin-top':'130px'}
                                    ),
                              ])
                        ],width=3), # 2nd right circle end
                  ]),# 2nd row end

            ],width=8), 
            # Left Graph end


            # Right side Graph
            dbc.Col([
                  dbc.Row([
                  html.Div([
                        html.Div([
                              dcc.Graph(
                              id='line_chart',
                              config= {'displayModeBar': False}
                              )
                        ],className='card-body')
                  ],className='card',style={'height':'300px'})
                  ]),

                  dbc.Row([
                  html.Div([
                        html.Div([
                              dcc.Graph(
                                    id = 'bar_chart',
                                    config={'displayModeBar': False},
                                    style={}
                              )
                        ],className='card-body')
                  ],className='card',style={'height':'260px'})
                  ]),

                  dbc.Row([
                  html.Div([
                        html.Div([
                              dcc.Graph(
                                    id = 'combination_chart',
                                    config = {'displayModeBar':False},
                                    style={}
                              )
                        ],className='card-body')
                  ],className='card', style={'height':'300px'})
                  ])
            ],width=4)
      ])


],className='container')

# accounts_receivable_value
@app.callback(
      Output('accounts_receivable_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            accounts_receivable = filter_month['accounts receivable'].iloc[0]
            pct_accounts_receivable = filter_month['pct_accounts_receivable'].iloc[0]

            if pct_accounts_receivable > 0:
                  return [
                        html.H4('${0:,.0f}'.format(accounts_receivable)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_accounts_receivable,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_accounts_receivable < 0:
                  return [
                        html.H4('${0:,.0f}'.format(accounts_receivable)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_accounts_receivable,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_accounts_receivable == 0:
                  return [
                        html.H4('${0:,.0f}'.format(accounts_receivable)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_accounts_receivable,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## accounts_receivable_value end


# accounts_payable_value
@app.callback(
      Output('accounts_payable_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            accounts_payable = filter_month['accounts payable'].iloc[0]
            pct_accounts_payable = filter_month['pct_accounts_payable'].iloc[0]

            if pct_accounts_payable > 0:
                  return [
                        html.H4('${0:,.0f}'.format(accounts_payable)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_accounts_payable,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_accounts_payable < 0:
                  return [
                        html.H4('${0:,.0f}'.format(accounts_payable)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_accounts_payable,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_accounts_payable == 0:
                  return [
                        html.H4('${0:,.0f}'.format(accounts_payable)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_accounts_payable,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## accounts_payable_value end
            
# income_value
@app.callback(
      Output('income_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            income = filter_month['income'].iloc[0]
            pct_income = filter_month['pct_income'].iloc[0]

            if pct_income > 0:
                  return [
                        html.H4('${0:,.0f}'.format(income)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_income,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_income < 0:
                  return [
                        html.H4('${0:,.0f}'.format(income)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_income,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_income == 0:
                  return [
                        html.H4('${0:,.0f}'.format(income)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_income,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## income_value end

# expenses_value
@app.callback(
      Output('expenses_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            expenses = filter_month['expenses'].iloc[0]
            pct_expenses = filter_month['pct_expenses'].iloc[0]

            if pct_expenses > 0:
                  return [
                        html.H4('${0:,.0f}'.format(expenses)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_expenses,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_expenses < 0:
                  return [
                        html.H4('${0:,.0f}'.format(expenses)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_expenses,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_expenses == 0:
                  return [
                        html.H4('${0:,.0f}'.format(expenses)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_expenses,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## expenses_value end
            

# quick_ratio_value
@app.callback(
      Output('quick_ratio_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            quick_ratio = filter_month['quick ratio'].iloc[0]
            pct_quick_ratio = filter_month['pct_quick_ratio'].iloc[0]

            if pct_quick_ratio > 0:
                  return [
                        html.H4('${0:,.0f}'.format(quick_ratio)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_quick_ratio,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_quick_ratio < 0:
                  return [
                        html.H4('${0:,.0f}'.format(quick_ratio)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_quick_ratio,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_quick_ratio == 0:
                  return [
                        html.H4('${0:,.0f}'.format(quick_ratio)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_quick_ratio,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## quick_ratio_value end
        

## current_ratio_value

@app.callback(
      Output('current_ratio_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            current_ratio = filter_month['current ratio'].iloc[0]
            pct_current_ratio = filter_month['pct_current_ratio'].iloc[0]

            if pct_current_ratio > 0:
                  return [
                        html.H4('${0:,.0f}'.format(current_ratio)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_current_ratio,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_current_ratio < 0:
                  return [
                        html.H4('${0:,.0f}'.format(current_ratio)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_current_ratio,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_current_ratio == 0:
                  return [
                        html.H4('${0:,.0f}'.format(current_ratio)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_current_ratio,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## current_ratio_value end
            

## net_profit_value
@app.callback(
      Output('net_profit_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            net_profit = filter_month['net profit'].iloc[0]
            pct_net_profit = filter_month['pct_net_profit'].iloc[0]

            if pct_net_profit > 0:
                  return [
                        html.H4('${0:,.0f}'.format(net_profit)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_net_profit,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_net_profit < 0:
                  return [
                        html.H4('${0:,.0f}'.format(net_profit)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_net_profit,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_net_profit == 0:
                  return [
                        html.H4('${0:,.0f}'.format(net_profit)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_net_profit,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## net_profit_value end
            

## cash_at_eom_value
@app.callback(
      Output('cash_at_eom_value','children'),
      [Input('select_month', 'value')]
)

def update_indacator(select_month):
      if select_month is None:
            raise PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            cash_at_eom = filter_month['cash at eom'].iloc[0]
            pct_cash_at_eom = filter_month['pct_cash_at_eom'].iloc[0]

            if pct_cash_at_eom > 0:
                  return [
                        html.H4('${0:,.0f}'.format(cash_at_eom)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_cash_at_eom,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            
            elif pct_cash_at_eom < 0:
                  return [
                        html.H4('${0:,.0f}'.format(cash_at_eom)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_cash_at_eom,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'decreasing': {'color': 'red'}
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ]
            elif pct_cash_at_eom == 0:
                  return [
                        html.H4('${0:,.0f}'.format(cash_at_eom)),
                        #html.P('{0:,.1f}%'.format(pct_accounts_receivable)),
                        dcc.Graph(
                              figure={
                                    'data': [go.Indicator(
                                                mode ='delta',
                                                value= pct_cash_at_eom,
                                                delta = {
                                                      'reference':0,
                                                      'position':'right',
                                                      'valueformat': ',.1f',
                                                      'relative': False,
                                                      'font': {'size':15},
                                                      'increasing': {'color': 'green'}, 
                                                },
                                                number={'valueformat':',',
                                                      'font':{'size':15},
                                                },
                                                domain={'y':[0,1],'x':[0,1]}
                                          )],
                                    'layout': go.Layout(
                                                title= {
                                                      'y': 1,
                                                      'x':0.5,
                                                      'xanchor': 'center',
                                                      'yanchor':'top'
                                                },
                                                font=dict(color='orange'),
                                                #paper_bgcolor='#1f2c56',
                                                #plot_bgcolor='#1f2c56',
                                                height=30,
                                                width=150,
                                                margin=dict(l=20, r=20, t=20, b=20)

                                          )
                              },
                              config={'displayModeBar':False}
                                    
                        )
                  ] ## cash_at_eom_value end

## Circle chart1

@app.callback(
            Output('pie_chart1','figure'),
            [Input('select_month','value')]
)
def update_chart(select_month):
      if select_month is None:
            return PreventUpdate
      else:
            filter_month = data[data['months']==select_month]
            net_profit_margin_percentage = abs(filter_month['net profit margin %'].iloc[0])
            remaining_percentage_profit = 100 - net_profit_margin_percentage

            colors = ['#B258D3', '#82FFFF']
      return {
            "data" : [
                  go.Pie(
                        labels=['',''],
                        values= [net_profit_margin_percentage,remaining_percentage_profit],
                        marker=dict(
                              colors = colors,
                              line = dict(color = '#DEB340',width=2)
                        ),
                        hoverinfo='skip',
                        textposition="inside",
                        textfont=dict(size=12, color="black"),
                        hole= 0.6,
                        rotation=90
                  )
            ],

            'layout' : go.Layout(
                        plot_bgcolor = 'rgba(0,0,0,0)',
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        height=175,
                        width=175,
                        margin= dict(t=0,b=0,r=0,l=0),
                        showlegend=False,
                          
                  )
                        
      }



## Circle chart2

@app.callback(
            Output('pie_chart2','figure'),
            [Input('select_month','value')]
)
def update_chart(select_month):
      if select_month is None:
            return PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            income_budget_percentage = filter_month['income budget %'].iloc[0]
            remaining_income_budget_percentage = 100 - abs(filter_month['income budget %'].iloc[0])
            colors = ['#63A0CC', '#82FFFF']

      return {
            "data" : [
                  go.Pie(
                        labels=['',''],
                        values= [income_budget_percentage,remaining_income_budget_percentage],
                        marker=dict(
                              colors = colors,
                              line = dict(color = '#DEB340',width=2)
                        ),
                        hoverinfo='skip',
                        textposition="inside",
                        textfont=dict(size=12, color="black"),
                        hole= 0.6,
                        rotation=90
                  )
            ],

            'layout' : go.Layout(
                        plot_bgcolor = 'rgba(0,0,0,0)',
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        height=175,
                        width=175,
                        margin= dict(t=0,b=0,r=0,l=0),
                        showlegend=False,
                          
                  )
                        
      }

## Circle chart3

@app.callback(
            Output('pie_chart3','figure'),
            [Input('select_month','value')]
)
def update_chart(select_month):
      if select_month is None:
            return PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            net_profit_margin_percentage = filter_month['net profit margin %'].iloc[0]
            pct_net_profit_margin_percentage = filter_month['pct_net_profit_margin_%'].iloc[0]
            net_profit_margin_percentage_target = float(10.0)
            net_profit_margin_vs_target_margin = abs(net_profit_margin_percentage - net_profit_margin_percentage_target)
            remaining_net_profit_margin_vs_target_margin = 100 - abs(net_profit_margin_vs_target_margin)

            colors = ['#8AC4A7', '#82FFFF']

      return {
            "data" : [
                  go.Pie(
                        labels=['',''],
                        values= [net_profit_margin_vs_target_margin,remaining_net_profit_margin_vs_target_margin],
                        marker=dict(
                              colors = colors,
                              line = dict(color = '#DEB340',width=2)
                        ),
                        hoverinfo='skip',
                        textposition="inside",
                        textfont=dict(size=12, color="black"),
                        hole= 0.6,
                        rotation=90
                  )
            ],

            'layout' : go.Layout(
                        plot_bgcolor = 'rgba(0,0,0,0)',
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        height=175,
                        width=175,
                        margin= dict(t=0,b=0,r=0,l=0),
                        showlegend=False,
                          
                  )
                        
      }


## Circle chart4

@app.callback(
            Output('pie_chart4','figure'),
            [Input('select_month','value')]
)
def update_chart(select_month):
      if select_month is None:
            return PreventUpdate
      else:
            filter_month = data[data['months'] == select_month]
            expense_budget_percentage = filter_month['expense budget %'].iloc[0]
            remaining_expense_budget_percentage = 100 - abs(filter_month['expense budget %'].iloc[0])

            colors = ['#B258D3', '#82FFFF']
      return {
            "data" : [
                  go.Pie(
                        labels=['',''],
                        values= [expense_budget_percentage,remaining_expense_budget_percentage],
                        marker=dict(
                              colors = colors,
                              line = dict(color = '#DEB340',width=2)
                        ),
                        hoverinfo='skip',
                        textposition="inside",
                        textfont=dict(size=12, color="black"),
                        hole= 0.6,
                        rotation=90
                  )
            ],

            'layout' : go.Layout(
                        plot_bgcolor = 'rgba(0,0,0,0)',
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        height=175,
                        width=175,
                        margin= dict(t=0,b=0,r=0,l=0),
                        showlegend=False,
                          
                  )
                        
      }


## buttom line_chart
@app.callback(
    Output('line_chart','figure'),
    [Input('select_month', 'value')]
)
def update_gragh(select_month):
      net_profit = data['net profit']
      months = data['months']
      text_color = np.where(net_profit > 0, 'black','#FF3399')

      return {
           'data': [
                  go.Scatter(
                        x = months,
                        y = net_profit,
                        text = net_profit,
                        texttemplate = '$' + '%{text:, .0f}',
                        textposition = 'top center',
                        textfont = dict(
                              family = 'Calibri',
                              size = 14,
                              color = text_color
                        ),
                        mode = 'markers+lines+text',
                        line = dict(
                              shape = "spline",
                              smoothing = 1.3,
                              width = 3,
                              color = '#B258D3'
                        ),
                        marker = dict(
                              size = 10,
                              symbol = 'circle',
                              color = '#FFFFFF',
                              line = dict(color = '#00B0F0', width = 2)
                        ),
                        hoverinfo = 'text',
                        hovertext = 
                              '<b>Month</b>: ' + months.astype(str) + '<br>'+
                              '<b>Net Profit</b>: $' + [f'{x:,.0f}' for x in net_profit]
                  )
           ],

           'layout': go.Layout(
                        plot_bgcolor = 'rgba(0,0,0,0)',
                        paper_bgcolor = 'rgba(0,0,0,0)',
                        title = dict(
                              text = 'New Profit',
                              y = 0.95,
                              x = 0.5,
                              xanchor = 'center',
                              yanchor = 'top'
                        ),
                        titlefont = dict(
                              color = '#404040',
                              size = 16,
                              family = 'Calibri'
                        ),
                        margin = dict(r = 20, t = 20, b = 40, l = 70),
                        height=280,
                        xaxis = dict(
                              title = '<b></b>',
                              visible = True,
                              color = 'white',
                              showline = False,
                              showgrid = False,
                              showticklabels = True,
                              linecolor = 'white',
                              linewidth = 1,
                              ticks = 'outside',
                              tickfont = dict(
                                    family = 'Arial',
                                    size = 12,
                                    color = '#404040'
                              )
                        ),
                        yaxis = dict(
                              title = '<b></b>',
                              tickprefix ='$',
                              tickformat = ',.0f',
                              visible = True,
                              color = 'white',
                              showline = False,
                              showgrid = False,
                              showticklabels = True,
                              linecolor = 'white',
                              linewidth = 1,
                              ticks = 'outside',
                              tickfont = dict(
                                    family = 'Calibri',
                                    size = 15,
                                    color = '#404040'
                              )
                        )
                  )
      } ## buttom line_chart end

## bar_chart start
@app.callback(
      Output('bar_chart','figure'),
      [Input('select_month','value')]
)

def update_graph(select_month):
      filter_month = data[data['months']==select_month]
      income = filter_month['income'].iloc[0]
      cost_of_goods_sold = filter_month['cost of goods sold'].iloc[0]
      gross_profit = filter_month['gross profit'].iloc[0]
      total_operating_expenses = filter_month['total operating expenses'].iloc[0]
      operating_profit_EBIT = filter_month['operating profit (EBIT)'].iloc[0]
      taxes = filter_month['Taxes'].iloc[0]
      net_profit = filter_month['net profit'].iloc[0]
      object_data = [['income', income], ['cost of goods sold', cost_of_goods_sold],['gross profit', gross_profit], 
                  ['total operating expenses', total_operating_expenses],['operating profit ebit', operating_profit_EBIT], ['taxes', taxes],['net profit', net_profit]]
      
      temp_df = pd.DataFrame(object_data, columns = ['Text', 'Value'])
      bar_color = np.where(temp_df['Value'] > 0, '#B258D3', '#FF3399')

      return {
            'data': [go.Bar(
                  x =  temp_df['Text'],
                  y = temp_df['Value'],
                  # text = df['Value'],
                  # texttemplate = '%{text:,.0f}',
                  # textposition = "none",
                  # textfont = dict(
                  #     family = "Calibri",
                  #     size = 14,
                  #     color = bar_color1,
                              # ),
                  marker = dict(color = bar_color),
                  width = 0.5,
                  orientation = 'v',
                  hoverinfo = 'text',
                  hovertext =
                        '' + temp_df['Text'].astype(str) + '<br>' +
                        '$' + [f'{x:,.0f}' for x in temp_df['Value']] + '<br>'
                  )],

            'layout': go.Layout(

                  plot_bgcolor = 'rgba(0,0,0,0)',
                  paper_bgcolor = 'rgba(0,0,0,0)',
                  title = {'text': 'Income Statement',
                        'y': 0.97,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                  titlefont = {'color': '#404040',
                        'size': 16,
                        'family': 'Calibri', },
                  margin = dict(r = 20, t = 20, b = 20, l = 70),
                  height=250,
                  xaxis = dict(title = '<b></b>',
                        visible = True,
                        color = 'white',
                        showline = False,
                        showgrid = False,
                        showticklabels = False,
                        linecolor = 'white',
                        linewidth = 0,
                        ticks = 'outside',
                        tickfont = dict(
                              family = 'Arial',
                              size = 12,
                              color = 'white')
                        ),

                  yaxis = dict(title = '<b></b>',
                        tickprefix = '$',
                        tickformat = ',.0f',
                        visible = True,
                        color = 'white',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'white',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                              family = 'Calibri',
                              size = 15,
                              color = '#404040')
                        ),
                  )
            
      }

## combination_chart
@app.callback(
      Output('combination_chart', 'figure'),
      [Input('select_month','value')]
)       

def update_graph(select_month):
      income = data['income']
      expenses = data['expenses']
      months = data['months']

      return {
            'data': [
                  go.Scatter(
                        x = months,
                        y = income,
                        mode = 'lines',
                        line = dict(
                              shape = 'spline',
                              smoothing = 1.3,
                              width = 3,
                              color = '#D35940'
                        ),
                        hoverinfo='text',
                        hovertext = 
                              '<b>Month</b>: ' + months.astype(str) + '<br>' +
                              '<b>Income</b>: $' + [f'{x:,.0f}' for x in income] + '<br>'
                  ),

                  go.Bar(
                        x = months,
                        y = expenses,
                        marker= dict(color='#63A0CC'),
                        width= 0.5,
                        hoverinfo= 'text',
                        hovertext = 
                              '<b>Month</b>: ' + months.astype(str) + '<br>' +
                              '<b>Expenses</b>: $' + [f'{x:,.0f}' for x in expenses] + '<br>'
                  )
            ],
            'layout' : go.Layout(
                  plot_bgcolor = 'rgba(0,0,0,0)',
                  paper_bgcolor = 'rgba(0,0,0,0)',
                  title = {'text': 'Income and Expenses',
                        'y': 0.97,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                  titlefont = {'color': '#404040',
                        'size': 16,
                        'family': 'Calibri', },
                  margin = dict(r = 30, t = 20, b = 40, l = 60),
                  height=280,
                  showlegend=False,
                  xaxis = dict(title = '<b></b>',
                        visible = True,
                        color = 'white',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'white',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                              family = 'Arial',
                              size = 12,
                              color = '#404040')
                        ),

                  yaxis = dict(title = '<b></b>',
                        tickprefix = '$',
                        tickformat = ',.0f',
                        visible = True,
                        color = 'white',
                        showline = False,
                        showgrid = False,
                        showticklabels = True,
                        linecolor = 'white',
                        linewidth = 1,
                        ticks = 'outside',
                        tickfont = dict(
                              family = 'Calibri',
                              size = 15,
                              color = '#404040')
                        ),
                  )
      }


if __name__ == "__main__":
    app.run_server(debug=True)