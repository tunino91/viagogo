# Purpose
This repo is looking to investigate the results of an A/B test after a hypothetical UI change on the home page of a company. You can find all the requested analysis with the description of the metrics in experiment.pdf file.
Metrics that have been considered are:
- Conversion Rate: percentage of visitors to our website who subsequently make a purchase.
- Bounce Rate: percentage of visitors to our website who navigate away from the site after viewing only one page.
- Date: date of user’s visit.
- User Types: new or returning visitor to the website
- Land (Boolean): 0: user navigated to home page from another page on our site, 1: user landed directly on the home page.
- Bounce (Boolean): 0: user navigated to another page on our website after landing, 1: user left our website after landing.
- Purchase (Boolean): 0: user did not make a purchase, 1: user made a purchase.
- Visitors_Control: number of visitors in the control group that meet the criteria of the preceding columns.
- Visitors_Variant: number of visitors in the variant group that meet the criteria of the preceding columns.

## Installation
It is higly recommended to start a virtual environment for development.
You can follow <a href="https://gist.github.com/simonw/4835a22c79a8d3c29dd155c716b19e16" target="_top">this page</a> to set up a virtual environment.
```sh
cd code
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Usage
```sh
cd code
source venv/bin/activate
python main.py
```
