
from scrap import getData
from model import mlModel2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

years=1

consider=["divida/pib eua","Relacao divida/pib Brasil","dxy","brent",'gold','bovespa','vix','usd_cny','usd_cop','usd_mxn','usd_brl',"Fed interest rate decisions","Selic"]
df=getData(years,consider)

gm_cv,betspar,r2,mse,coef,intercept,residual,estimator,norm=mlModel2(df)

sevendaysdf=df.loc[df.index >= len(df.index)-40, df.columns!="usd_brl"]
sevendaysdfY=df.loc[df.index >= len(df.index)-40, df.columns=="usd_brl"]
sevendaysPredict=gm_cv.predict(sevendaysdf)
print(coef)
print(sevendaysPredict)

norm__classifier_type=betspar["norm__classifier_type"]

sevendaysdf = norm.transform(sevendaysdf)

x = list(range(len(sevendaysdf)))
plt.figure(figsize=(12,8))

for m in estimator.estimators_:
    print("IN")
    print(m.predict(sevendaysdf))
    plt.plot(x, m.predict(sevendaysdf), color='grey', alpha=0.2, zorder=1)

plt.scatter(x,sevendaysdfY, marker='o', color='orange', zorder=4)

# "Bagging model" prediction
plt.plot(x,sevendaysPredict, color='red', zorder=5)


plt.savefig('testplot.png')