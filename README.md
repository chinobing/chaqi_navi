# chaqi.net 

This navigation website was initially designed by [BYR-Navi](https://byr-navi.com/ ) with [jekyll](https://jekyllrb.com/).
I use it as my personal navigation website and I really like its design concept. But I am not familiar with Jekyll and feel like I need a website more than just a static HTML navigation website. Thus, I modified it with Pyhton and [Plotly DASH](https://dash.plot.ly/).

In general, I use Plotly DASH for data visualization only. But I really want to know what else Dash can do beside it. So here is the one.

#
You may notice ```the header,footer and layout``` will be created dynamically with page load. The reason is that the data for  ``` header,footer and layout``` will be generated and updated with page refresh without restarting the whole DASH app again.

# Demo
Link:  [ChaQi.net](http://www.chaqi.net)

![](https://raw.githubusercontent.com/fundviz/chaqi_navi/master/demo.png)

# BUG
- [ ] The DASH app wont interact with custom JS for Semantic UI Popup.
- [ ] Using html.Form as ```enter key```will trigger the callback even with empty value of dcc.Input.
- [ ] Favicon and Meta wont be added or displayed on VPS.
