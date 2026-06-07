import plotly.graph_objects as go

go.Figure(go.Bar(y=[1, 3, 2])).show()
go.Figure(go.Scatter(y=[1, 3, 2], mode='lines')).show()