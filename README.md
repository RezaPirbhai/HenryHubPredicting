# HenryHubPredicting
First Full ML Project

I began this at 6am on the 26th June and finished it at 11pm on the 26th of June. 
I would say a couple things - by no means is this perfect - but for a days effort I'm okay with it and will seek to improve this model after familiarisng myself further with machine leanring.

I wanted to look at commodities and I after researching I decided to use the Henry Hub Price as what I would aim to predict and using features of WTI, HDD and CDD which represent the energy required to heat and cool to try and quantify the amount of energy needed. 

Getting the Henry Hub (HH) and West Texan Intermediate (WTI) data was fairly easy - just needed to sign up for API keys and then import.
Getting the HDD and CDD weather was more of a pain, I first had to find where the information was available and then I had to web-scrape it, however making the webscraper was far easier done through using AI - and I now have a solid template for how to do webscraping from that. 

From here we had to clean the data, drop rows which didn't have Henry hall data and set data as our index, we also had to change the weather data from txt to csv and also aggregate the data as the txt files had the data for all regions so take the mean of this to get one tangible metric for the HDD and CDD. 

# Post finding the results - I'm starting to query whether this was a bad idea, we found weather to be incredibly insignificant which felt surprising but maybe we need more different types of data or better outlier detection both of which I can work on, or see if specific regions provide far more important data - e.g. regions of high pop density.

Moving on after cleaning the data, we did an initial EDA. 
We plot the HH and WTI prices to see what type of movement they have - notably Henry Hub does not have a generally positive trend but follows periods of multiple years with high volatility spikes.

# When I next come back to this, I want to do a bit more research into what specifically causes all the outliers - WTI's outliers are easy being covid and the 08 crash.

To confirm the lack of trend we did a seasonal decomposition plot and observed very little trend, but we did observe seasonality which makes sense. High nat gas is required in Jul-Aug for cooling and in the Winter months for heating.

I was then highly confused after plotting rolling correlation and CCF plots, but the conclusion I came to was just that there wasn't significant correlation between HDD and HH and CDD and HH but more research could be done into this. 

We then plotted ACF and PACF graphs - and this gave the most useful information so far, whilst the ACF graph showed stickiness the PACF graph showed 90+% of the movement could be attributed to a one day lag of the HH price - so we took this on as a feature. To confirm this we ran a quick hypothesis test and found strong evidence to support using the day before data to predict the next day data. At this point I started wondering about whether I could model this using stochastic calculus and markov chains - and quickly discovered an AR(1) is just a first order Markov process.
# This did highlight I need to learn more theory i.e. ARIMA theory and do a bit more time series analysis / econometrics knowledge. 

Then did a quick correlation matrix to confirm what I had though so far, no major conclusions were found WTI and HH some weak + correlation and CDD and HDD some -ve correlation. Neither of which was overly surprising.

I then spent about half an hour trying to figure ot how to use the weather data I had tried so hard to find and didn't find that much success, but decided to put it into the XGBoost model anyway with some more features using rolling lags and anomalies of the CDD and HDD.

Finally we start designing our XGBoost model and features we choose mostly weather features but also a HH_lag1 and WTI. We then train with 80% of the data and we downgraded to XGB 1.7.6 for early stopping rounds since I could not figure our how to get it otherwise. I also randomly chose my estimators, learning rate, depth, and tree samples.

# However, I think it would be a good idea to experiment with these and see what works best!

We then find our RMSE and get a score of 0.6575 which seems okay, but means nothing on its owns we compare to other models. We also plot our feature importance and find HH_lag1 unsurprisngly is most important but WTI AND HDD_anom seem fairly significant. 
Model comparison shows our model is more accurate than the others with lag-1 being closest but our model thankfully is better than that.

We tested against an AR(1) model and the RMSE was 1.9733, showing our model has a 66.7% improvement upon a basic AR(1) model. 

# Although on that I forgot what the measurement to find whether this is overfit or something - so I could probs check that. 

After plotting permutation importance on the other hand, we find HH_lag1 is the onlt one that has highly signficant importance - so maybe WTI and HDD are less important than the feature importance suggests.

# Again, in my learning journey not yet sure how to interpret this but I'll learn soon and will report back to this read me when I do.

We also make some shap plots which just further show HH_lag1 being the dominant feature but it does support WTI having an effect. 

So, to conclude the model seems fairly accurate from the RMSE and how the model performed compared to the actual dates:
![image](https://github.com/user-attachments/assets/e42f50d2-09e6-4e7d-90cd-8106c27a121c)

But there is definately more work to be done... 








