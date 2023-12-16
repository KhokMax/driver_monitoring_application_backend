#postgresql+psycopg2://postgres:IvNa2023OlKh@34.168.253.165:5432/postgres

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

select_all_drivers = """
select user_id,
    driver_first_name,
	driver_last_name,
	driver_patronymic,
    driver_age,
	driver_rank,
	mobile_phone,
	mail,
	alive_flag,
	A1_category,
	A_category,
	B1_category,
	B_category,
	C1_category,
	C_categoty,
	D1_categoty,
	D_category,
	C1E_category,
	BE_category,
	CE_category,
	D1E_category, DE_category, 
	CASE
		WHEN delivery_status = 'in progress'
			THEN 'in progress' 
		ELSE 'free' 
	END as current_status
	from drivers left outer join (SELECT operations_facts.driver_id, MAX(operations_facts.delivery_status) as delivery_status from operations_facts inner join
									   (SELECT driver_id, max(operation_date + operation_time) as max_date FROM operations_facts
										   GROUP BY driver_id) as operations_facts_info
ON operations_facts.driver_id = operations_facts.driver_id
 AND operations_facts_info.max_date = operations_facts.operation_date + operations_facts.operation_time
GROUP BY operations_facts.driver_id) as operations_facts_1
ON drivers.user_id = operations_facts_1.driver_id
WHERE alive_flag = true"""