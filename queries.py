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



get_all_deliveries_by_driver = """
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
WHERE driver_id = '{}'
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



select_all_vehicles = """select vehicles.vehicle_id, vehicle_name, operations_facts_1.vehicle_status, max_distance, fuel_per_100_km, capacity_kg, license_category, vehicle_category, 
	CASE
		WHEN delivery_status = 'in progress'
			THEN 'in progress' 
		ELSE 'free' 
	END as current_status
	from vehicles left outer join (SELECT operations_facts.vehicle_id, MAX(operations_facts.delivery_status) as delivery_status, MAX(operations_facts.vehicle_status) as vehicle_status
								   from operations_facts inner join
									   (SELECT vehicle_id, max(operation_date + operation_time) as max_date FROM operations_facts
										   GROUP BY vehicle_id) as operations_facts_info
ON operations_facts.vehicle_id = operations_facts.vehicle_id
 AND operations_facts_info.max_date = operations_facts.operation_date + operations_facts.operation_time
GROUP BY operations_facts.vehicle_id) as operations_facts_1
ON vehicles.vehicle_id = operations_facts_1.vehicle_id
WHERE alive_flag = true"""



change_delivery_status = """
INSERT INTO operations_facts (vehicle_id, vehicle_status, driver_id, delivery_id, delivery_status, operation_date, operation_time)
SELECT vehicle_id, 'Good', driver_id, delivery_id, '{}', CURRENT_DATE + INTERVAL '2 hours', CURRENT_TIME + INTERVAL '2 hours'
FROM deliveries
WHERE delivery_id = '{}'"""


select_last_vehicle_location = """
SELECT * FROM vehicle_locations
WHERE vehicle_id = '{}'
ORDER BY loc_time DESC
LIMIT 1
"""