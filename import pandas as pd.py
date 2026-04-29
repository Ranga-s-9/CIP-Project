import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# LOAD OR GENERATE DATA
# =========================
csv_file = "sales_data.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    print(f"'{csv_file}' not found. Generating sample data...\n")
    data = {
        'Date': [
            '2024-01-05', '2024-01-20', '2024-02-10', '2024-02-25',
            '2024-03-08', '2024-03-22', '2024-04-14', '2024-04-28',
            '2024-05-05', '2024-05-19', '2024-06-11', '2024-06-30',
            '2024-07-03', '2024-07-18', '2024-08-09', '2024-08-24',
            '2024-09-06', '2024-09-21', '2024-10-10', '2024-10-29',
            '2024-11-07', '2024-11-23', '2024-12-05', '2024-12-20',
        ],
        'Region':   ['North','South','East','West','North','East','South','West',
                     'East','North','West','South','North','East','South','West',
                     'North','South','East','West','North','South','East','West'],
        'Product':  ['Laptop','Phone','Tablet','Laptop','Phone','Tablet','Laptop','Phone',
                     'Tablet','Laptop','Phone','Tablet','Laptop','Phone','Tablet','Laptop',
                     'Phone','Tablet','Laptop','Phone','Tablet','Laptop','Phone','Tablet'],
        'Category': ['Electronics','Electronics','Electronics','Electronics',
                     'Electronics','Electronics','Electronics','Electronics',
                     'Electronics','Electronics','Electronics','Electronics',
                     'Electronics','Electronics','Electronics','Electronics',
                     'Electronics','Electronics','Electronics','Electronics',
                     'Electronics','Electronics','Electronics','Electronics'],
        'Sales':    [1500, 800, 600, 1700, 950, 500, 1800, 870,
                     620, 1600, 910, 540, 1750, 830, 580, 1650,
                     990, 510, 1720, 860, 560, 1780, 920, 530],
        'Profit':   [300, 160, 90, 340, 190, 75, 360, 174,
                     93, 320, 182, 81, 350, 166, 87, 330,
                     198, 76, 344, 172, 84, 356, 184, 79],
        'Quantity': [10, 20, 15, 12, 22, 14, 11, 19,
                     16, 13, 21, 18, 10, 20, 15, 12,
                     23, 14, 11, 18, 16, 10, 21, 13],
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"Sample data saved to '{csv_file}'.\n")

# Convert Date column
df['Date'] = pd.to_datetime(df['Date'])

# Add Month column
df['Month'] = df['Date'].dt.month

# =========================
# BASIC ANALYSIS
# =========================
total_sales    = df['Sales'].sum()
total_profit   = df['Profit'].sum()
total_quantity = df['Quantity'].sum()

print("=" * 35)
print("        BASIC ANALYSIS")
print("=" * 35)
print(f"Total Sales    : {total_sales:,.2f}")
print(f"Total Profit   : {total_profit:,.2f}")
print(f"Total Quantity : {total_quantity}")

# =========================
# GROUP ANALYSIS
# =========================
sales_by_region   = df.groupby('Region')['Sales'].sum()
sales_by_product  = df.groupby('Product')['Sales'].sum()
monthly_sales     = df.groupby('Month')['Sales'].sum()
profit_by_category = df.groupby('Category')['Profit'].sum()

print("\n--- Sales by Region ---")
print(sales_by_region.to_string())

print("\n--- Sales by Product ---")
print(sales_by_product.to_string())

print("\n--- Monthly Sales ---")
print(monthly_sales.to_string())

print("\n--- Profit by Category ---")
print(profit_by_category.to_string())

# =========================
# VISUALIZATION
# =========================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Sales Dashboard", fontsize=16, fontweight='bold')

# --- Bar Chart: Sales by Product ---
sales_by_product.plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
axes[0].set_title("Sales by Product")
axes[0].set_xlabel("Product")
axes[0].set_ylabel("Sales")
axes[0].tick_params(axis='x', rotation=45)

# --- Line Chart: Monthly Sales Trend ---
monthly_sales.plot(kind='line', marker='o', ax=axes[1], color='darkorange')
axes[1].set_title("Monthly Sales Trend")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Sales")
axes[1].set_xticks(range(1, 13))

# --- Pie Chart: Sales by Region ---
sales_by_region.plot(kind='pie', autopct='%1.1f%%', ax=axes[2],
                     startangle=90, ylabel='')
axes[2].set_title("Sales by Region")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150)
print("\nChart saved as 'sales_dashboard.png'")
plt.show()
print("\nDone!")