import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
def get_dates(N_ofyears,formatD):

    ano_final = datetime.datetime.now()
    ano_inicial = (datetime.datetime.now() - relativedelta(years=N_ofyears))
    dateRange=pd.date_range(ano_inicial,(ano_final-timedelta(days=1)).strftime('%d/%m/%Y'),freq='d').strftime('%b %d, %Y')
    if(formatD=="/"):
        ano_final = ano_final.strftime('%m/%d/%Y')
        ano_inicial=ano_inicial.strftime('%m/%d/%Y')
    else:
        ano_final = ano_final.strftime('%Y-%m-%d')
        ano_inicial=ano_inicial.strftime('%Y-%m-%d')
    return ano_inicial, ano_final,dateRange
