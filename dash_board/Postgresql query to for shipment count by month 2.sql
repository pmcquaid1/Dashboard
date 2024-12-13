SELECT * FROM dash_board_shipment;
SELECT EXTRACT('MONTH' FROM actual_delivery) AS actual_delivery,
COUNT(shipment_id) AS shipment_count
FROM dash_board_shipment
GROUP BY EXTRACT('MONTH' FROM actual_delivery);

