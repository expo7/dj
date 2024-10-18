from django.db import models

from django.db import models

class StockInfo(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    longName = models.CharField(max_length=255, null=True, blank=True)
    marketCap = models.BigIntegerField(null=True, blank=True)
    enterpriseValue = models.BigIntegerField(null=True, blank=True)
    trailingPE = models.FloatField(null=True, blank=True)
    forwardPE = models.FloatField(null=True, blank=True)
    pegRatio = models.FloatField(null=True, blank=True)
    priceToSalesTrailing12Months = models.FloatField(null=True, blank=True)
    priceToBook = models.FloatField(null=True, blank=True)
    enterpriseToRevenue = models.FloatField(null=True, blank=True)
    enterpriseToEbitda = models.FloatField(null=True, blank=True)
    fiftyTwoWeekHigh = models.FloatField(null=True, blank=True)
    fiftyTwoWeekLow = models.FloatField(null=True, blank=True)
    fiftyDayAverage = models.FloatField(null=True, blank=True)
    twoHundredDayAverage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.ticker
    
class StockAnalysis(models.Model):
    ticker1 = models.CharField(max_length=10)
    ticker2 = models.CharField(max_length=10)
    analysis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis of {self.ticker1} vs {self.ticker2}"