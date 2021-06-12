from plotly.subplots import make_subplots
import charts.member_spending as ms
import charts.book_issues as bu
import plotly.graph_objects as go

def final_plots(members, spend, books, issues):
    fig1 = ms.member_bar_plot(members, spend)
    fig2 = ms.member_pie_plot(members, spend)
    
    fig3 = bu.book_pie_plot(books, issues)
    fig4 = bu.book_line_plot(books, issues)
    
    with open('templates/chart.html', 'w') as f:
        f.close()
    
    with open('templates/chart.html', 'a') as f:
        f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
    
