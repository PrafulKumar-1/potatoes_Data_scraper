from scraper.exporters.csv_exporter import save_csv
from scraper.exporters.json_exporter import save_json

def export_leads(leads, csv_path, json_path):
    save_csv(leads, csv_path)
    save_json(leads, json_path)
