# importing pandas library
import pandas as pd
df = pd.read_csv(r"C:\Users\raman\Documents\data.csv", encoding='iso-8859-1')

# displays the first few rows of our dataset
print(df.head(10))

#data cleaning
missing_values = df.isnull().sum()

print(missing_values)

# this code replaces any null values in description column with no description
df['Description'].fillna('No Description', inplace=True)

df = df.dropna(subset=['CustomerID'])

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# remove any rows where quantity or unitprice is less than or equal to 0
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# exploratory data analysis
summary_statistics = df.describe()
print(summary_statistics)

# count unique items sold
unique_items_count = df['Description'].nunique()
print(unique_items_count)

# What are the total sales
df['Sales'] = df['Quantity'] * df['UnitPrice']

top_items = df.groupby('Description')['Sales'].sum().sort_values(ascending = False).head(10)
print(top_items)

# Product Popularity: determine the most popular products based on sold quantity
# Product Popularity: determine the most popular products based on sold quantity
# Product trends over time: analyzing how popular a product was over time
# Stock code analysis: investigate if certain types of stock codes are associated with higher sales or revenue
# product description analysis

# group by description to aggregate data by product 
# sum the quantity column to get the total quantity sold of each product 
# sort the result in descending order to get the mostt popular products

product_sales = df.groupby('Description').agg(Total_Quantity_Sold=('Quantity','sum')).reset_index()
product_sales_sorted = product_sales.sort_values(by='Total_Quantity_Sold', ascending=False)

# display the top 10 most popular products
top_10_products = product_sales_sorted.head(10)

plt.figure(figsize=(12,8))
plt.barh(top_10_products['Description'], top_10_products['Total_Quantity_Sold'])
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Description')
plt.title('Top 10 Most Popular Products')
plt.gca().invert_yaxis() # To have highest value at the top
plt.show()


# convert InvoiceDate to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
# filter the dataframe for POPCORN HOLDER
holder_data = df[df['Description'] == 'POPCORN HOLDER']
# group the data by invoicce date and sum up quantities
holder_sales_over_time = holder_data.groupby(holder_data['InvoiceDate'].dt.to_period('M'))['Quantity'].sum().reset_index()
# convert the invoicedate from period to timestamp for plotting
holder_sales_over_time['InvoiceDate'] = holder_sales_over_time['InvoiceDate'].dt.to_timestamp()

# plot the time-series for the quantity of gliders sold
plt.figure(figsize=(14,7))
plt.plot(holder_sales_over_time['InvoiceDate'], holder_sales_over_time['Quantity'], marker='o')
plt.xlabel('Date')
plt.ylabel('Qunatity Sold')
plt.title('QUANTITY of POPCORN HOLDER SOLD OVER TIME')
plt.grid(True)
plt.show()

# is there a significant different in sales during the holidays months (november) to march
from scipy import stats
november_sales = df[(df['InvoiceDate'].dt.month == 11) & (df['InvoiceDate'].dt.year == 2011)]['Quantity']
march_sales = df[(df['InvoiceDate'].dt.month == 3) & (df['InvoiceDate'].dt.year == 2011)]['Quantity']

print(stats.shapiro(november_sales))
print(stats.shapiro(march_sales))

# check for variances
print(stats.levene(november_sales, march_sales))

t_stat, p_value = stats.ttest_ind(november_sales, march_sales, equal_var= False)

print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

# interpret the results
if p_value < 0.05:
    print("The difference in means between November sales and March sales is statistically significant.")
else:
    print("There is no statistically significant differnce in means between November sales and March sales.") 
