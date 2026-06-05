# Mutual Fund Analytics

A comprehensive platform for analyzing and tracking mutual fund performance.

## Project Structure

```
mutual-fund-analytics/
├── data/                  # Data storage
│   ├── raw/              # Raw data files
│   └── processed/        # Processed data
├── notebooks/            # Jupyter notebooks for analysis
├── sql/                  # SQL queries and scripts
├── dashboard/            # Dashboard application
├── reports/              # Generated reports
├── data_ingestion.py     # Data ingestion module
├── live_nav_fetch.py     # Live NAV fetching module
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Ingestion
```bash
python data_ingestion.py
```

### Fetch Live NAV
```bash
python live_nav_fetch.py
```

## Project Features

- Real-time mutual fund NAV tracking
- Historical data analysis
- Performance reporting
- Interactive dashboard
- Data processing pipelines

## Contributing

Guidelines for contributing to this project.

## License

MIT License
