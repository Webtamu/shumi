from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from plotly_calplot import calplot
import pandas as pd
import os

class Heatmap(QWidget):
    def __init__(self) -> None:

        super().__init__()

        # Load sales data
        file_path = "resources/sales_data.xlsx"  
        sales_data = pd.read_excel(file_path)

        # Create the Plotly figure
        fig = calplot(sales_data, x="date", y="sales", dark_theme=True)
        # Save the figure to an HTML file
        fig.write_html("heatmap.html")

        # Get the absolute path to the HTML file
        html_path = os.path.abspath("heatmap.html")

        # Set up the QWebEngineView to display the heatmap
        self.webView = QWebEngineView()

        # Use QUrl to load the HTML file
        file_url = QUrl.fromLocalFile(html_path)  # Convert the file path to a QUrl
        self.webView.setUrl(file_url)
      