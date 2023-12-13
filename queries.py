get_all_deliveries = """
SELECT *,
	CASE 
		WHEN delivery_id IN (SELECT delivery_id
							 FROM operations_facts 
							 WHERE delivery_status = 'end')
			THEN 'end'
		WHEN delivery_id IN (SELECT delivery_id
							 FROM operations_facts 
							 WHERE delivery_status = 'in progress')
			THEN 'in progress' 
		ELSE 'up to next' 
	END 
	AS delivery_status
FROM deliveries
"""

post_new_driver = """
INSERT INTO drivers(
	user_id, driver_first_name, driver_last_name, driver_patronymic, driver_age, driver_rank, mobile_phone, mail, a1_category, a_category, b1_category, b_category, c1_category, c_categoty, d1_categoty, d_category, c1e_category, be_category, ce_category, d1e_category, de_category)
VALUES (:driver_first_name, :driver_last_name:, :driver_patronymic, :driver_age, :driver_rank:, :mobile_phone, :mail, :a1_category, :a_category, :b1_category, :b_category, :c1_category, :c_categoty, :d1_categoty, :d_category, :c1e_category, :be_category:, :ce_category, :d1e_category, :de_category, :user_id)
"""