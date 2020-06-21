import pandas as pd, numpy as np
import random,requests
from bs4 import BeautifulSoup
from faker import Faker
#initialize Faker
fake=Faker()

names=[]
address=[]
company=[]
n_names=200000

for n in range(n_names):
    names.append(fake.name())
    address.append(fake.address())
    company.append(fake.company())
    
claim_reason=["Medical","Travel","Phone","Other"]
Confidentiality_level=["High","Low","Medium","Very low"]

claim_confidentiality_dict=dict(zip(claim_reason,Confidentiality_level))

claim_reasons=np.random.choice(claim_reason,n_names, p=[.55,.15,.15,.15])
claim_confidentiality_levels=[claim_confidentiality_dict[claim_reasons[i]] for i in range(len(claim_reasons))]

variables=[names,address,company,claim_reasons,claim_confidentiality_levels]

df=pd.DataFrame(variables).transpose()
df.columns=["Customer Name","Customer Address","Company Name","Claim Reason","Data confidentiality"]
df["Customer Address"]=df["Customer Address"].str.replace("\n",",")
df.head()

URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

countries_list = list()
pop_list = list()
res = requests.get(URL).text
soup = BeautifulSoup(res,'html.parser')
for items in soup.find('table', class_='wikitable').find_all('tr')[1::1]:
    data = items.find_all(['th','td'])
    try:
        country = data[1].a.text
        pop = int(data[2].get_text().replace(",", ""))
        

    except AttributeError:pass
    countries_list.append(country)
    pop_list.append(pop)
 
 
 
 
countries_list = countries_list[:100]
pop_list = pop_list[:100]
norm_pop_list = [float(i)/sum(pop_list) for i in pop_list]

df["Country"]=np.random.choice(countries_list,n_names, p=norm_pop_list)

claim_manager=["James","Rodrigo","Elena","Yao","Rick"]
df["Claim_manager"]=np.random.choice(claim_manager,n_names)


df["Claim Amount"]=0

for i in range(len(df)):
    if df["Claim Reason"][i]=="Medical":
        df["Claim Amount"][i]=np.random.randint(1300,2300)
    elif df["Claim Reason"][i]=="Travel":
        df["Claim Amount"][i]=np.random.randint(300,900)
    elif df["Claim Reason"][i]=="Phone":
        df["Claim Amount"][i]=np.random.randint(200,270)
    else:
        df["Claim Amount"][i]=np.random.randint(1,100)
        
df.groupby("Claim Reason")["Claim Amount"].mean()
average_category_premiums=list(round(df.groupby("Claim Reason")["Claim Amount"].mean()*8,0))

df["Category Premium"]=0

for i in range(len(df)):
    if df["Claim Reason"][i]=="Medical":
        df["Category Premium"][i]=average_category_premiums[0]                                              
    elif df["Claim Reason"][i]=="Other":
        df["Category Premium"][i]=average_category_premiums[1]
    elif df["Claim Reason"][i]=="Phone":
        df["Category Premium"][i]=average_category_premiums[2]
    else:
        df["Category Premium"][i]=average_category_premiums[3]
        
df["Premium/Amount Ratio"]=df["Claim Amount"]/df["Category Premium"]
round(df.groupby("Claim Reason")["Premium/Amount Ratio"].min(),2)*100

df["Claim Request output"]=np.where(df["Premium/Amount Ratio"]<0.06,"Yes","No")
