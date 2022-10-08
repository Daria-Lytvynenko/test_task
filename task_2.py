"""
Here's an example of database structures:
FRUITS_EXPORT (Schema):
seller_info (table):
- seller_id
- fruit_id
- fruit_weight (tons)
consumption_info (table):
- fruit_id
- seller_id
- client_id
- quantity_purchased_fruit (tons)
"""

#How many tons worth of fruit does an average seller have?

SELECT 
    AVG(avg_amount) 
FROM 
    (select sum(fruit_weight (tons)) AS avg_amount 
FROM 
    seller_info 
GROUP BY 
    seller_id) AS result_avg;
    
#How many sellers have at least one client who purchased their fruit?  

SELECT
    COUNT(DISTINCT(seller_id))
FROM 
    consumption_info
WHERE 
    quantity_purchased_fruit (tons) > 0
