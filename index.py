# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 00:14:53 2018

@author: 柯西君_bingWong
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import requests
import json
from flask import send_from_directory
import os
import yaml

app = dash.Dash()
server = app.server # the Flask app
app.scripts.serve_locally=True


links_file = '_data/links.yml'
search_services_file = '_data/search_services.yml'

built_with_file = '_data/built_with.yml'
hosted_by_file = '_data/hosted_by.yml'
powered_by_file = '_data/powered_by.yml'
info_file = '_data/info.yml'

#read yaml file
def read_yaml(file):
    stream = open(file, "rb")
    return yaml.load(stream)  
    
#autocomplete suggestion from either google or baidu
def get_suggestion(search_engine,word):
    if search_engine=='baidu':
        url = 'http://suggestion.baidu.com/su?wd=%s&sugmode=3&json=1' % word
        response = requests.get(url, verify=False)  # API request
        cont = response.content  # retieve content
        res = cont[17: -2].decode('gbk')  # slice the content to get 'list' and return as unicode format
        res_json = json.loads(res)  # convert it into json format
        return res_json['s']  # return keywords list        
    
    elif search_engine=='google':
        url="http://suggestqueries.google.com/complete/search?client=firefox&q=%s" % word   
        response = requests.get(url)
        res_json = json.loads(response.content.decode('utf-8'))
        res_json  = res_json[1]
        return res_json
        
#######################################################################################
"""header"""
#######################################################################################
def header():
    search_options = []
    data_lists = read_yaml(search_services_file)
    for data in data_lists:
        search_options.append({'label':data['name'],'value':data['id']})
    
    
    return html.Div(className='ui vertical masthead center aligned segment', children=[
            html.Div(className='ui container', children=[
                html.Div(className='ui secondary  menu', children=[
                        html.A('首页', className="item active", href="/"),     
                        html.A('行业分类', className="item", href="/industry"), 
                        html.A('股东关联', className="item", href="/shareholders"),                                                                                                                                                                                                                                      
                        html.A('财务报表', className="item", href="/indicators"),
                        html.A('投资组合', className="item", href="/portfolio"),
                        html.A('风险价值', className="item", href="/var"),                      
                        html.A('技术分析', className="item", href="/tick"),            
                        html.Div(className='right menu',children=[
                                html.A('GitHub', className="ui item", href="https://github.com/fundviz",target="_blank" ),
                                        ])
                                ]),                               
                    ]),
                                                  
                                                                                                  
             html.Div(className='ui text container', children=[
                    html.H1('查企.Net',className='ui header'),
                    html.H2('Do whatever you want when you want to.'),
                    html.Form(id='submit-form',target='_blank',method='post',className='ui input focus',children=[
                                dcc.Input(id='searchInput',
                                          list='autoSuggestion',
                                          type='text',
                                          style={'padding': '0px'}
                                            ),
                                html.Div(children=[dcc.Dropdown(id='search-engine',
                                             options = search_options,
                                             value='wechat',
                                             searchable=False,
                                             clearable=False,
                                             )],style={'width': '20%',}),
                    html.Datalist(id="autoSuggestion")
                                                                                                                                                                          
            ],style={'width': '90%',})]       )])
#######################################################################################
"""footer"""
#######################################################################################
def footer():
    html_built_with = []
    html_hosted = []
    html_powered = []
    html_info = []
    built_lists = read_yaml(built_with_file)
    hosted_lists = read_yaml(hosted_by_file)
    powered_lists = read_yaml(powered_by_file)  
    info_lists = read_yaml(info_file)  

    for built_list in built_lists:
        html_built_with.append(html.A(built_list['name'], className="item", href=built_list['url'],target="_blank"))
    
    for hosted_list in hosted_lists:
        html_hosted.append(html.A(hosted_list['name'], className="item", href=hosted_list['url'],target="_blank"))

    for powered_list in powered_lists:
        html_powered.append(html.A(powered_list['name'], className="item", href=powered_list['url'],target="_blank"))

    for info_list in info_lists:
        html_info.append(html.H4(info_list['name'],className='ui inverted header'))
        html_info.append(html.Div(info_list['author']))
        html_info.append(html.Div(info_list['slogon']))

           
    return html.Div(className='ui inverted vertical footer segment', children=[
            html.Div(className='ui container', children=[
                html.Div(className='ui stackable inverted divided equal height stackable grid', children=[
                        html.Div(className="three wide column",children=[
                                html.H4('Built with',className='ui inverted header'),
                                html.Div(className='ui inverted link list',children=html_built_with)
                                ]),                          
                        html.Div(className="four wide column",children=[
                                html.H4('Designed & Inspired by',className='ui inverted header'),
                                html.Div(className='ui inverted link list',children=html_hosted)
                                ]),     
                        html.Div(className="three wide column",children=[
                                html.H4('Modified by',className='ui inverted header'),
                                html.Div(className='ui inverted link list',children=html_powered)
                                ]),  
                        html.Div(className="six wide column",children=html_info)
                        ]),      
                ]),                               
 
        ])

#######################################################################################
"""layout"""
#######################################################################################
def links_layout():
    html_layout = []
    data_lists = read_yaml(links_file)

    for data_list in data_lists:
        html_layout.append(html.Div(className="ui vertical stripe links segment",children=[
                        html.Div(className="ui equal width stackable internally celled grid",children=[
                                html.Div(className="center aligned row",children=[html.Div(className="links column",children=[html.Div(className="ui top attached label",children=[category['category']]),html.Div(className="ui labels",children=[html.A(className="ui {} label".format(x['style']), href=x['url'], rel="nofollow", target="_blank",**{'data-html':x['des'].replace(',','<br/>')},children=[html.I(className=x['icon']),x['name']]) for x in category['links'] ])]) for category in data_list['categories']]
                                )])]))
    return html.Div(children=[
            header(),
            html.Div(children=html_layout),
            footer()])

app.layout = links_layout
app.title = '查企.Net  - Mainly focus on stock analysis.'


@app.callback(
    Output('autoSuggestion', 'children'),
    [Input('searchInput', 'value')])
def auto_suggestion(search_keywords):
    print(search_keywords)
    if search_keywords:
        return [html.Option(value=sug) for sug in get_suggestion('baidu',search_keywords)]
    
@app.callback(
    Output('submit-form', 'action'),
    [Input('searchInput', 'value'),
     Input('search-engine', 'value')])
def search_output(search_keywords,search_engine):
    data = read_yaml(search_services_file)
    if search_keywords and search_engine:
        for myDict in data:
            if search_engine in myDict.values():
                try:
                    search_url = myDict['url']
                    search_suffix = myDict['suffix']
                except KeyError:
                    search_url = myDict['url']
                    search_suffix = ""
                print(search_url + search_keywords + search_suffix)
                return search_url + search_keywords + search_suffix
    



external_css = ['static/css/home.css',
                'https://cdn.bootcss.com/semantic-ui/2.3.1/semantic.min.css']
for css in external_css:
    app.css.append_css({"external_url": css})

app.scripts.append_script({
    'external_url': [
                     'https://cdn.bootcss.com/react/15.6.2/react.min.js',
                     'https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js',                   
                     'https://cdn.bootcss.com/semantic-ui/2.3.1/semantic.min.js',
                     'static/js/custom.js',
     ]
})

@app.server.route('/static/js/<path:path>')
def static_js(path):
    static_folder = os.path.join(os.getcwd(), 'static/js')
    return send_from_directory(static_folder, path)

@app.server.route('/static/css/<path:path>')
def static_css(path):
    static_folder = os.path.join(os.getcwd(), 'static/css')
    return send_from_directory(static_folder, path)
    
@app.server.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.server.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')    
    
if __name__ == '__main__':
    app.run_server(debug=True)