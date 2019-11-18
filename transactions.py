#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas

path = '/usr/local/data/transactions.txt'
data = pandas.read_csv(path, header=None, names = ['index','id','transaction','segment'])


# ### 1. Количество клиентов для каждого из сегментов, совершавших транзакции.

# In[13]:


segments_groups = data.groupby('segment')
r_segment = segments_groups.get_group('R')
af_segment = segments_groups.get_group('AF')
r_segment_len = len(r_segment)
af_segment_len = len(af_segment)

print('Количество клиентов для сегмента R: ',  r_segment_len)
print('Количество клиентов для сегмента AF: ', af_segment_len)


# ### 2. Cредний объем отдельной транзакции в каждом из сегментов.

# In[17]:


r_mean_transaction = round(r_segment['transaction'].mean())
af_mean_transaction = round(af_segment['transaction'].mean())

print('Cредний объем отдельной транзакции для сегмента R: ',  r_mean_transaction)
print('Cредний объем отдельной транзакции для сегмента AF: ', af_mean_transaction)


# ### 3. 90% доверительный интервал для среднего объема отдельной транзакции в каждом из сегментов.

# In[21]:


import math


def getInterval(df, const_t = 1.65):
    """
    Находит границу доверительного интервала для датафрейма df.
    const_t - аргумент функции Лапласа (F(t) = 0.90/2)
    """
    var = df.var() # дисперсия
    mean = df.mean()
    n = len(df)
    
    left_bound = mean - const_t*math.sqrt(var/n)
    right_bound = mean + const_t*math.sqrt(var/n)
    
    return round(left_bound),round(right_bound)
    
    
r_interval, af_interval = map(getInterval,(r_segment['transaction'],af_segment['transaction']))

print('Доверительный интервал для сегмента R: ', r_interval)
print('Доверительный интервал для сегмента AF: ', af_interval)


# ### 4. Проверка гипотезы о равенстве средних объемов отдельных транзакций между сегментами при уровне значимости 10%.

# In[23]:


quantile = 1.65 # аргумент функции Лапласа (F(z) = 1/2*(1 - 0.1))


def checkHypothesis(df1, df2):
    """
    Проверяет гипотезу равенства средних в выборках df1 и df2.
    H0: mean1 == mean2
    H1: mean1 != mean2
    """
    mean1, mean2 = df1.mean(), df2.mean()
    var1, var2 = df1.var(), df2.var()
    n1, n2 = len(df1),len(df2)
    
    z = (mean1 - mean2)/math.sqrt(var1/n1 + var2/n2)
    
    if abs(z) > quantile:
        return False
    
    return True


# In[24]:


if checkHypothesis(r_segment['transaction'], af_segment['transaction']):
    print('Гипотеза не отвергается')
else:
    print('Гипотеза отвергается')

