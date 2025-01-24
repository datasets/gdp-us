<a className="gh-badge" href="https://datahub.io/core/gdp-us"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Gross Domestic Product (GDP) of the United States (US) both nominal and real on
an annual and quarterly basis. Annual data is provided since 1930 and quarterly
data since 1947. Both total GDP (levels) and annualized percentage change in
GDP are provided. Both levels and changes are available both in current dollars
(nominal GDP) and in chained 2017 dollars (real GDP). Data is sourced from US
Government's Bureau of Economic Analysis (BEA) and provided in standardized
CSV.

## Data

The calculation of GDP and, in particular, chained measures of GDP involves
some complexities. You can read more about the benefits and issues of BEA's
Chain Indexes in the [BEA's 1997 Survey of Current Business][bea-1997].

[bea-1997]: http://www2.econ.iastate.edu/classes/econ302/vandewetering/BEA.html

## Preparation

Requires Python. Install the requirements:

    pip install -r scripts/requirements.txt

Then run the script to get the data:

    python scripts/process.py

## Automation
Up-to-date (auto-updates every month) gdp-us dataset could be found on the datahub.io: https://datahub.io/core/gdp-us

## License

Public Domain Dedication and License.

Note we assume source data is public domain as US Federal Government.

