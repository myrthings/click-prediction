# Click-through Prediction For a Company With 28M MAU
This project is the summary code of my team capstone project at IE Datascience Bootcamp. My team and I worked in a click-through prediction for a company with 28M MAU to **improve the ad allocation of the company**. The data is propietary and not available but I leave here a summary of all the analysis we did.

## Context 🧭
Programmatic advertising is the automated transaction of buying and selling advertising online. Ads are displayed with banners in a website and their performance is measured with CTR (Click Throught Rate). Banners holders get paid by number of clicks and by number of impressions (a lot less than for clicks). The way to monetize the banners is by selling them in ad auctions where advertisers bid for the banners. 60% of our company revenue comes from its website banners. Our problem is to increase that revenue as much as possible.

## Process 🚶‍♀️🚶‍♂️
The process we followed is more iterative and circular than linear. However, we've ordered the notebook in the following steps:
- **The problem:** Explanation of the business problem and how the challenge was approached.
- **Import the libraries and the data:** The libraries needed and *ourtools.py* file included for custom auxiliar functions. Also an explanation of the data.
- **Data Visualization:** What visualizations we did that weere more important for our process. Made with Matplotlib and Seaborn.
- **Feature Engineering:** How we cleaned and prepared the data.
- **Model Preparation:** The division of the sample sets in test and train.
- **Model Building and Evaluation:** The different algorithms we used to fit our data and its evaluation. We compared them using *AUC* and at the end chose *Lightgbm* as the best model.
- **More about the perfomance of *Lightgbm*:** The results of our analysis with the final model.
- **Model for Revenue:** An evaluation of the Economic Impact of the model. Our model duplicated the revenue of not having any model.
- **Conclusions:** How much time we spent on each task.

## Development ⚙️
The whole analysis is displayed in a Jupyter Notebook. We also include a Python file with some auxiliar functions. At the begining of the notebook you can find all the libraries needed. On the model part, there's some other libraries for the algorithms.

## How to use it 👩‍💻
*You can't use it as it is* uploaded because the data is propietary and not available. BUT, you can download the notebook and reuse the functions for your own data. The more useful and original parts are:
- **Visualizations:** We did a prety good job thinking how to display the time, maybe you're interested in that. (You can improve their appearance for sure :blush:)
- **Undersample:** We created our own function to undersample the data an divide it in train and test with the less possible lose of data points.
- **Economic model:** This part is completely ours because we didn't find any information on the internet. The model is just an application of probability distributions over a lift measure given ad prices (fixed in our example). It's quite useful if you want need to explain your results to a non-technical client.

## Authors
- [Manuel Alvarez](https://www.linkedin.com/in/manuelalvrod/)
- [Myriam Barnés (me)](https://www.linkedin.com/in/myriambarnes/)
- [Isaque Campinho](https://www.linkedin.com/in/isaque-campinho-72362521/)
- [Tarik Jebbari](https://www.linkedin.com/in/tarik-jebbari/)
