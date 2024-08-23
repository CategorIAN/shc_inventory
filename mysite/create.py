import pandas as pd
import os
from polls.models import Department, Item, Employee

def insert_values(table, model):
    df = pd.read_csv("\\".join([os.getcwd(), "tables", "{}.csv".format(table)]))
    fields = df.columns
    for i in df.index:
        values = df.loc[i, :]
        d = dict(list(zip(fields, values)))
        entry = model(**d)
        entry.save()

def fill_tables():
    for table, model in zip(["department", "item", "employee"], [Department, Item, Employee]):
        insert_values(table, model)