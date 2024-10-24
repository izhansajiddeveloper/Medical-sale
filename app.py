import streamlit as st
import pandas as pd
from datetime import datetime

# Sample products with additional medicines
products = {
    'Product Name': [
        'Paracetamol', 'Ibuprofen', 'Cough Syrup', 'Antibiotic', 'Aspirin', 
        'Antihistamine', 'Loperamide', 'Naproxen', 'Metformin', 'Simvastatin', 
        'Omeprazole', 'Levothyroxine', 'Amoxicillin', 'Ciprofloxacin', 
        'Citalopram', 'Sertraline', 'Venlafaxine', 'Doxycycline', 'Gabapentin', 
        'Clonazepam', 'Fluoxetine', 'Lorazepam', 'Ranitidine', 'Cetirizine', 
        'Diphenhydramine', 'Hydrochlorothiazide', 'Furosemide', 'Atorvastatin', 
        'Rosuvastatin', 'Bupropion', 'Hydrocodone', 'Tramadol', 
        'Metoprolol', 'Insulin'  # Additional medicines
    ],
    'Price': [
        5, 8, 12, 15, 4, 10, 9, 14, 7, 18, 
        11, 20, 6, 10, 13, 12, 16, 19, 10, 14, 
        9, 17, 15, 8, 7, 13, 11, 12, 18, 5, 
        9, 14, 11, 22  # Updated to 32 prices
    ],
    'Quantity': [
        50, 30, 20, 10, 40, 25, 15, 60, 45, 35, 
        55, 20, 10, 5, 25, 30, 15, 8, 22, 27, 
        12, 18, 28, 40, 35, 30, 25, 50, 30, 20, 
        18, 10, 5, 3  # Updated to 32 quantities
    ],
    'Reorder Level': [
        10, 5, 5, 3, 10, 5, 5, 10, 10, 5, 
        5, 3, 5, 3, 5, 5, 5, 3, 5, 5, 
        5, 5, 5, 10, 10, 10, 5, 3, 10, 5, 
        5, 5, 7, 8  # Updated to 32 reorder levels
    ]
}

# Create a DataFrame
df_products = pd.DataFrame(products)

# Initialize monthly sales in session state
if 'monthly_sales' not in st.session_state:
    st.session_state.monthly_sales = []  # To track sales for the current month

# Title
st.title("Medical Store Sales & Inventory Management")

# Display available products
st.subheader("Available Products in Store")
st.write(df_products[['Product Name', 'Price', 'Quantity']])

# Sales Form
st.subheader("Enter Sale")
product_name = st.selectbox("Product", df_products['Product Name'])
quantity_sold = st.number_input("Quantity", min_value=1)

# Add sale and update stock
if st.button("Add Sale"):
    product_row = df_products[df_products['Product Name'] == product_name]
    
    # Check if enough stock is available
    current_stock = product_row['Quantity'].values[0]
    
    if quantity_sold > current_stock:
        st.error(f"Insufficient stock for {product_name}. Only {current_stock} left.")
    else:
        total_price = product_row['Price'].values[0] * quantity_sold
        new_stock = current_stock - quantity_sold
        
        # Update stock in DataFrame
        df_products.loc[df_products['Product Name'] == product_name, 'Quantity'] = new_stock
        
        # Display total bill
        st.success(f"Total Bill for {quantity_sold} {product_name}: ${total_price:.2f}")
        
        # Check if stock is below reorder level
        reorder_level = product_row['Reorder Level'].values[0]
        if new_stock <= reorder_level:
            st.warning(f"Stock for {product_name} is low! Only {new_stock} left. Consider restocking.")
        
        # Record sale in session state
        sale_entry = {
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Format the date
            'Product': product_name,
            'Quantity': quantity_sold,
            'Total': total_price
        }
        st.session_state.monthly_sales.append(sale_entry)

# Show updated product data
st.subheader("Updated Inventory")
st.write(df_products[['Product Name', 'Price', 'Quantity']])

# Check for any low stock items
st.subheader("Stock Alerts")
low_stock = df_products[df_products['Quantity'] <= df_products['Reorder Level']]
if not low_stock.empty:
    st.warning("The following items are low on stock and need restocking:")
    st.write(low_stock[['Product Name', 'Quantity']])
else:
    st.success("All medicines are sufficiently stocked.")

# Monthly Sales Summary
if st.session_state.monthly_sales:
    df_sales = pd.DataFrame(st.session_state.monthly_sales)
    st.subheader("Monthly Sales Summary")
    st.write(df_sales)
    
    # Calculate total sales
    total_sales = df_sales['Total'].sum()
    st.success(f"Total Sales for the Month: ${total_sales:.2f}")
else:
    st.info("No sales recorded yet for this month.")
