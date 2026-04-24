# Race Condition Filter — LLM Analysis Report
*2026-04-24 13:34  |  Model: GitHub Models*

## Summary
| Verdict | Count |
|---------|-------|
| 🔴 REAL races | **455** |
| ✅ False Positives | 134 |
| 🟡 Uncertain | 15 |
| Total analysed | 604 |

---
## 🔴 Real Races — sorted by risk score

### 1. `PriceConfig` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/priceservice/prices (PriceController.create)`
- **Endpoint 2:** `DELETE /api/v1/priceservice/prices/pricesId (PriceController.delete)`
- **File:** `./examples/train-ticket/ts-price-service/src/main/java/price/controller/PriceController.java` line 60
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 2. `PriceConfig` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/priceservice/prices (PriceController.create)`
- **Endpoint 2:** `PUT /api/v1/priceservice/prices (PriceController.update)`
- **File:** `./examples/train-ticket/ts-price-service/src/main/java/price/controller/PriceController.java` line 60
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 3. `PriceConfig` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/priceservice/prices/pricesId (PriceController.delete)`
- **Endpoint 2:** `PUT /api/v1/priceservice/prices (PriceController.update)`
- **File:** `./examples/train-ticket/ts-price-service/src/main/java/price/controller/PriceController.java` line 66
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 4. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 5. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 6. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 7. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 8. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 9. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 10. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 11. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 12. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 13. `Order` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 14. `Order` — HIGH | risk 10/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** createNewOrder + payOrder on Order entity

### 15. `Order` — HIGH | risk 10/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** createNewOrder + payOrder on Order entity

### 16. `Order` — HIGH | risk 10/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** createNewOrder + payOrder on Order entity

### 17. `User` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/userservice/users/register (UserController.registerUser)`
- **Endpoint 2:** `DELETE /api/v1/userservice/users/userId (UserController.deleteUserById)`
- **File:** `./examples/train-ticket/ts-user-service/src/main/java/user/controller/UserController.java` line 55
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 18. `User` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/userservice/users/register (UserController.registerUser)`
- **Endpoint 2:** `PUT /api/v1/userservice/users (UserController.updateUser)`
- **File:** `./examples/train-ticket/ts-user-service/src/main/java/user/controller/UserController.java` line 55
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 19. `User` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/userservice/users/userId (UserController.deleteUserById)`
- **Endpoint 2:** `PUT /api/v1/userservice/users (UserController.updateUser)`
- **File:** `./examples/train-ticket/ts-user-service/src/main/java/user/controller/UserController.java` line 64
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 20. `User` — HIGH | risk 10/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/userservice/users/id/userId (UserController.getUserByUserId)`
- **Endpoint 2:** `PUT /api/v1/userservice/users (UserController.updateUser)`
- **File:** `./examples/train-ticket/ts-user-service/src/main/java/user/controller/UserController.java` line 49
- **Why it's real:** Read operation followed by write operation on same entity

### 21. `ConsignRecord` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/consignservice/consigns (ConsignController.insertConsign)`
- **Endpoint 2:** `PUT /api/v1/consignservice/consigns (ConsignController.updateConsign)`
- **File:** `./examples/train-ticket/ts-consign-service/src/main/java/consign/controller/ConsignController.java` line 37
- **Why it's real:** Write-Write on same entity with no lock

### 22. `TrainType` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/trainservice/trains (TrainController.create)`
- **Endpoint 2:** `PUT /api/v1/trainservice/trains (TrainController.update)`
- **File:** `./examples/train-ticket/ts-train-service/src/main/java/train/controller/TrainController.java` line 37
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 23. `TrainType` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/trainservice/trains (TrainController.create)`
- **Endpoint 2:** `DELETE /api/v1/trainservice/trains/id (TrainController.delete)`
- **File:** `./examples/train-ticket/ts-train-service/src/main/java/train/controller/TrainController.java` line 37
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 24. `TrainType` — CRITICAL | risk 10/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/trainservice/trains (TrainController.update)`
- **Endpoint 2:** `DELETE /api/v1/trainservice/trains/id (TrainController.delete)`
- **File:** `./examples/train-ticket/ts-train-service/src/main/java/train/controller/TrainController.java` line 85
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 25. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 26. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 27. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 28. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 29. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 30. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 31. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 32. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 33. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 34. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 35. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 36. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 37. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 38. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 39. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 40. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 41. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 42. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 43. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 44. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 45. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 46. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 47. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 48. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 49. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 50. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 51. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 52. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 53. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 54. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 55. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 56. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 57. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 58. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 59. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 60. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 61. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 62. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 63. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 64. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 65. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 66. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 67. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 68. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 69. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 70. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 71. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 72. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 73. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 74. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 75. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 76. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 77. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 78. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 79. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 80. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 81. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 82. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 83. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 84. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 85. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 86. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 94
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 87. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 94
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 88. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 94
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 89. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 110
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 90. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 110
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 91. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 110
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 92. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 129
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 93. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 129
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 94. `Order` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 137
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 95. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock and high severity

### 96. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock and high severity

### 97. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity Order

### 98. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write on same entity Order with no lock

### 99. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read before Write on same entity Order

### 100. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write on same entity Order with no lock

### 101. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write on same entity Order with no lock

### 102. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** High severity Write-Write conflict on Order entity with potential for data corruption/lost updates

### 103. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write conflict on Order entity with high severity and potential for data corruption/lost updates

### 104. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, high severity

### 105. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, high severity

### 106. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 107. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 108. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 109. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 110. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 111. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 112. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 113. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 114. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 115. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 116. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 117. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 118. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Read-check before Write (TOCTOU) on same entity Order

### 119. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Read-check before Write (TOCTOU) on same entity Order

### 120. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability and data corruption

### 121. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability and data corruption

### 122. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability and data corruption

### 123. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability and data corruption

### 124. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity with high severity

### 125. `Order` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 47
- **Why it's real:** CreateNewOrder and queryOrders on Order entity with high severity

### 126. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 127. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 128. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 129. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 130. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 131. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 132. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 133. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 134. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 135. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 136. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 137. `Trip` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 138. `Trip` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left (TravelController.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Read-check before Write (TOCTOU) on Trip entity with high severity

### 139. `Trip` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left_parallel (TravelController.queryInfoInparallel)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Read-check before Write (TOCTOU) on Trip entity with high severity

### 140. `Trip` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/left (Travel2Controller.queryInfo)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 116
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 141. `Trip` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/left (Travel2Controller.queryInfo)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 116
- **Why it's real:** Read-check before Write (TOCTOU) on Trip entity with high severity

### 142. `Trip` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trip_detail (Travel2Controller.getTripAllDetailInfo)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 130
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 143. `Trip` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trip_detail (Travel2Controller.getTripAllDetailInfo)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 130
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 144. `Assurance` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/assuranceservice/assurances/assuranceid/assuranceId (AssuranceController.deleteAssurance)`
- **Endpoint 2:** `DELETE /api/v1/assuranceservice/assurances/orderid/orderId (AssuranceController.deleteAssuranceByOrderId)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 50
- **Why it's real:** Two DELETE endpoints on same entity with no lock

### 145. `Assurance` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/assuranceservice/assurances/assuranceid/assuranceId (AssuranceController.deleteAssurance)`
- **Endpoint 2:** `PATCH /api/v1/assuranceservice/assurances/assuranceId/orderId/typeIndex (AssuranceController.modifyAssurance)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 50
- **Why it's real:** Two endpoints with one DELETE and one PATCH on same entity

### 146. `Assurance` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/assuranceservice/assurances/assuranceid/assuranceId (AssuranceController.deleteAssurance)`
- **Endpoint 2:** `GET /api/v1/assuranceservice/assurances/typeIndex/orderId (AssuranceController.createNewAssurance)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 147. `Assurance` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/assuranceservice/assurances/orderid/orderId (AssuranceController.deleteAssuranceByOrderId)`
- **Endpoint 2:** `PATCH /api/v1/assuranceservice/assurances/assuranceId/orderId/typeIndex (AssuranceController.modifyAssurance)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 57
- **Why it's real:** Two endpoints with one DELETE and one PATCH on same entity

### 148. `Assurance` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE /api/v1/assuranceservice/assurances/orderid/orderId (AssuranceController.deleteAssuranceByOrderId)`
- **Endpoint 2:** `GET /api/v1/assuranceservice/assurances/typeIndex/orderId (AssuranceController.createNewAssurance)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 57
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 149. `Assurance` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PATCH /api/v1/assuranceservice/assurances/assuranceId/orderId/typeIndex (AssuranceController.modifyAssurance)`
- **Endpoint 2:** `GET /api/v1/assuranceservice/assurances/typeIndex/orderId (AssuranceController.createNewAssurance)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 67
- **Why it's real:** Two GET endpoints on same entity

### 150. `Assurance` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PATCH /api/v1/assuranceservice/assurances/assuranceId/orderId/typeIndex (AssuranceController.modifyAssurance)`
- **Endpoint 2:** `GET /api/v1/assuranceservice/assurances/assuranceid/assuranceId (AssuranceController.getAssuranceById)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 67
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 151. `Assurance` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PATCH /api/v1/assuranceservice/assurances/assuranceId/orderId/typeIndex (AssuranceController.modifyAssurance)`
- **Endpoint 2:** `GET /api/v1/assuranceservice/assurance/orderid/orderId (AssuranceController.findAssuranceByOrderId)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 67
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 152. `User` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/userservice/users/id/userId (UserController.getUserByUserId)`
- **Endpoint 2:** `DELETE /api/v1/userservice/users/userId (UserController.deleteUserById)`
- **File:** `./examples/train-ticket/ts-user-service/src/main/java/user/controller/UserController.java` line 49
- **Why it's real:** Read operation followed by delete operation on same entity

### 153. `Config` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/configservice/configs (ConfigController.createConfig)`
- **Endpoint 2:** `PUT api/v1/configservice/configs (ConfigController.updateConfig)`
- **File:** `./examples/train-ticket/ts-config-service/src/main/java/config/controller/ConfigController.java` line 46
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 154. `Config` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/configservice/configs (ConfigController.createConfig)`
- **Endpoint 2:** `DELETE api/v1/configservice/configs/configName (ConfigController.deleteConfig)`
- **File:** `./examples/train-ticket/ts-config-service/src/main/java/config/controller/ConfigController.java` line 46
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 155. `Config` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT api/v1/configservice/configs (ConfigController.updateConfig)`
- **Endpoint 2:** `DELETE api/v1/configservice/configs/configName (ConfigController.deleteConfig)`
- **File:** `./examples/train-ticket/ts-config-service/src/main/java/config/controller/ConfigController.java` line 53
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 156. `FoodOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/foodservice/orders (FoodController.createFoodOrder)`
- **Endpoint 2:** `POST /api/v1/foodservice/createOrderBatch (FoodController.createFoodBatches)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 59
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 157. `FoodOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/foodservice/orders (FoodController.createFoodOrder)`
- **Endpoint 2:** `PUT /api/v1/foodservice/orders (FoodController.updateFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 59
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 158. `FoodOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/foodservice/orders (FoodController.createFoodOrder)`
- **Endpoint 2:** `DELETE /api/v1/foodservice/orders/orderId (FoodController.deleteFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 59
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 159. `FoodOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/foodservice/createOrderBatch (FoodController.createFoodBatches)`
- **Endpoint 2:** `PUT /api/v1/foodservice/orders (FoodController.updateFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 65
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 160. `FoodOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/foodservice/createOrderBatch (FoodController.createFoodBatches)`
- **Endpoint 2:** `DELETE /api/v1/foodservice/orders/orderId (FoodController.deleteFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 65
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 161. `FoodOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/foodservice/orders (FoodController.updateFoodOrder)`
- **Endpoint 2:** `DELETE /api/v1/foodservice/orders/orderId (FoodController.deleteFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 72
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 162. `Station` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/stationservice/stations (StationController.create)`
- **Endpoint 2:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 41
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 163. `Station` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/stationservice/stations (StationController.create)`
- **Endpoint 2:** `DELETE /api/v1/stationservice/stations/stationsId (StationController.delete)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 41
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 164. `Station` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **Endpoint 2:** `DELETE /api/v1/stationservice/stations/stationsId (StationController.delete)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 47
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 165. `Money` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment/money (PaymentController.addMoney)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 41
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 166. `Money` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment/money (PaymentController.addMoney)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/userId/money (InsidePaymentController.addMoney)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 41
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 167. `Money` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment/money (PaymentController.addMoney)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/drawback/userId/money (InsidePaymentController.drawBack)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 41
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 168. `Money` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/userId/money (InsidePaymentController.addMoney)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 40
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 169. `Money` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/drawback/userId/money (InsidePaymentController.drawBack)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 40
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 170. `Money` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment/money (PaymentController.addMoney)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 41
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 171. `Money` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment/money (PaymentController.addMoney)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 41
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 172. `Money` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 34
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 173. `Money` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/userId/money (InsidePaymentController.addMoney)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 34
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 174. `Money` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.queryAccount)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 40
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 175. `Payment` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/paymentservice/payment (PaymentController.pay)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 35
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 176. `Payment` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/paymentservice/payment (PaymentController.pay)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 35
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 177. `Payment` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 34
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 178. `Contacts` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/contactservice/contacts (ContactsController.createNewContacts)`
- **Endpoint 2:** `DELETE api/v1/contactservice/contacts/contactsId (ContactsController.deleteContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 46
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 179. `Contacts` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/contactservice/contacts/admin (ContactsController.createNewContactsAdmin)`
- **Endpoint 2:** `DELETE api/v1/contactservice/contacts/contactsId (ContactsController.deleteContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 54
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 180. `Contacts` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `DELETE api/v1/contactservice/contacts/contactsId (ContactsController.deleteContacts)`
- **Endpoint 2:** `PUT api/v1/contactservice/contacts (ContactsController.modifyContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 61
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 181. `SecurityConfig` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/securityservice/securityConfigs (SecurityController.create)`
- **Endpoint 2:** `PUT /api/v1/securityservice/securityConfigs (SecurityController.update)`
- **File:** `./examples/train-ticket/ts-security-service/src/main/java/security/controller/SecurityController.java` line 42
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 182. `SecurityConfig` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/securityservice/securityConfigs (SecurityController.create)`
- **Endpoint 2:** `DELETE /api/v1/securityservice/securityConfigs/id (SecurityController.delete)`
- **File:** `./examples/train-ticket/ts-security-service/src/main/java/security/controller/SecurityController.java` line 42
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 183. `SecurityConfig` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `PUT /api/v1/securityservice/securityConfigs (SecurityController.update)`
- **Endpoint 2:** `DELETE /api/v1/securityservice/securityConfigs/id (SecurityController.delete)`
- **File:** `./examples/train-ticket/ts-security-service/src/main/java/security/controller/SecurityController.java` line 49
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 184. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `DELETE /api/v1/fooddeliveryservice/orders/d/orderId (FoodDeliveryController.deleteFoodDeliveryOrder)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 185. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/tripid (FoodDeliveryController.updateTripId)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 186. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/seatno (FoodDeliveryController.updateSeatNo)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 187. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/dtime (FoodDeliveryController.updateDeliveryTime)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 188. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/fooddeliveryservice/orders/d/orderId (FoodDeliveryController.deleteFoodDeliveryOrder)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/tripid (FoodDeliveryController.updateTripId)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 43
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 189. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/fooddeliveryservice/orders/d/orderId (FoodDeliveryController.deleteFoodDeliveryOrder)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/seatno (FoodDeliveryController.updateSeatNo)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 43
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 190. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/fooddeliveryservice/orders/d/orderId (FoodDeliveryController.deleteFoodDeliveryOrder)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/dtime (FoodDeliveryController.updateDeliveryTime)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 43
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 191. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/fooddeliveryservice/orders/tripid (FoodDeliveryController.updateTripId)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/seatno (FoodDeliveryController.updateSeatNo)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 67
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 192. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/fooddeliveryservice/orders/tripid (FoodDeliveryController.updateTripId)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/dtime (FoodDeliveryController.updateDeliveryTime)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 67
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 193. `FoodDeliveryOrder` — CRITICAL | risk 9/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/fooddeliveryservice/orders/seatno (FoodDeliveryController.updateSeatNo)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/dtime (FoodDeliveryController.updateDeliveryTime)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 73
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 194. `FoodDeliveryOrder` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/fooddeliveryservice/orders/d/orderId (FoodDeliveryController.deleteFoodDeliveryOrder)`
- **Endpoint 2:** `GET /api/v1/fooddeliveryservice/orders/orderId (FoodDeliveryController.getFoodDeliveryOrderById)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 43
- **Why it's real:** Read-check before Write (TOCTOU) on FoodDeliveryOrder entity

### 195. `ConsignPrice` — HIGH | risk 9/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/consignpriceservice/consignprice/config (ConsignPriceController.getPriceConfig)`
- **Endpoint 2:** `POST /api/v1/consignpriceservice/consignprice (ConsignPriceController.modifyPriceConfig)`
- **File:** `./examples/train-ticket/ts-consign-price-service/src/main/java/consignprice/controller/ConsignPriceController.java` line 48
- **Why it's real:** Write operation on ConsignPrice entity without lock

### 196. `PriceConfig` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/priceservice/prices/routeId/trainType (PriceController.query)`
- **Endpoint 2:** `POST /api/v1/priceservice/prices (PriceController.create)`
- **File:** `./examples/train-ticket/ts-price-service/src/main/java/price/controller/PriceController.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 197. `PriceConfig` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/priceservice/prices/routeId/trainType (PriceController.query)`
- **Endpoint 2:** `DELETE /api/v1/priceservice/prices/pricesId (PriceController.delete)`
- **File:** `./examples/train-ticket/ts-price-service/src/main/java/price/controller/PriceController.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 198. `PriceConfig` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/priceservice/prices/routeId/trainType (PriceController.query)`
- **Endpoint 2:** `PUT /api/v1/priceservice/prices (PriceController.update)`
- **File:** `./examples/train-ticket/ts-price-service/src/main/java/price/controller/PriceController.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 199. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 200. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 201. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 202. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 203. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 204. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 205. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 206. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write on same entity Order with no lock

### 207. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write on same entity Order with no lock

### 208. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Write-Write on same entity Order with no lock

### 209. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read before Write on same entity Order

### 210. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 50
- **Why it's real:** Read-check before Write (TOCTOU) on same entity Order

### 211. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 212. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 213. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 214. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 215. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 216. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 217. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 218. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 219. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 220. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 57
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 221. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 222. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 223. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 224. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 225. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 226. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 227. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 228. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 229. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/query (OrderOtherController.queryOrders)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 65
- **Why it's real:** Write-Write on same entity, no lock

### 230. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 231. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 232. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 233. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/travelDate/trainNumber (OrderOtherController.calculateSoldTicket)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 83
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 234. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 235. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 236. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 237. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 238. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/price/orderId (OrderOtherController.getOrderPrice)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 90
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 239. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 240. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 241. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 242. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderPay/orderId (OrderOtherController.payOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 97
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 243. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 244. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 245. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Write-Write conflict on same entity Order

### 246. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Write-Write conflict on same entity Order

### 247. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Write-Write conflict on same entity Order

### 248. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Write-Write conflict on same entity Order

### 249. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Write-Write conflict on same entity Order

### 250. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.getOrderById)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 104
- **Why it's real:** Write-Write conflict on same entity Order

### 251. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Write operation on Order entity with no lock

### 252. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 253. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Write operation on Order entity with no lock

### 254. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 255. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 256. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 257. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 258. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `POST /api/v1/orderservice/order (OrderController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 259. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 260. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 261. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write operation on Order entity with no lock

### 262. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 263. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 264. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/security/checkDate/accountId (OrderOtherController.securityInfoCheck)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 119
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 265. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 266. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 267. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 268. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 269. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 270. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 271. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 272. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther (OrderOtherController.saveOrderInfo)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 128
- **Why it's real:** Read-Write conflict on Order entity with no lock

### 273. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 274. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 275. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 276. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 277. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 278. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 279. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/orderOtherService/orderOther/admin (OrderOtherController.updateOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 135
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 280. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 281. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 282. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 283. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write-Write conflict on Order entity with no lock

### 284. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 285. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 286. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/orderOtherService/orderOther/orderId (OrderOtherController.deleteOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 142
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 287. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 288. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 289. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 290. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 291. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther (OrderOtherController.findAllOrder)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 151
- **Why it's real:** Write operation on Order entity followed by a read operation on the same entity, potential for TOCTOU vulnerability

### 292. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 293. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 294. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 295. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/tickets (OrderController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 40
- **Why it's real:** Write-Write conflict on Order entity with high severity

### 296. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 297. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Read-check before Write (TOCTOU) on same entity 'Order'

### 298. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 299. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Read-check before Write (TOCTOU) on same entity 'Order'

### 300. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/admin (OrderController.addcreateNewOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order (OrderController.findAllOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 53
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 301. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 61
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 302. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 61
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 303. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 61
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 304. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 61
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 305. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderservice/order/query (OrderController.queryOrders)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 61
- **Why it's real:** Write-Write conflict on same entity 'Order'

### 306. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 77
- **Why it's real:** Write operation on Order entity without lock

### 307. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 77
- **Why it's real:** Write operation on Order entity without lock

### 308. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/travelDate/trainNumber (OrderController.calculateSoldTicket)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 77
- **Why it's real:** Write operation on Order entity without lock

### 309. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 85
- **Why it's real:** Write operation on Order entity without lock

### 310. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 85
- **Why it's real:** Write operation on Order entity without lock

### 311. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 85
- **Why it's real:** Write operation on Order entity without lock

### 312. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 102
- **Why it's real:** Write operation on Order entity without lock

### 313. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 102
- **Why it's real:** Write operation on Order entity without lock

### 314. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/orderId (OrderController.getOrderById)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 102
- **Why it's real:** Write operation on Order entity without lock

### 315. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order (OrderController.saveOrderInfo)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 119
- **Why it's real:** Write operation on Order entity without lock

### 316. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **Endpoint 2:** `PUT /api/v1/orderservice/order/admin (OrderController.updateOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 119
- **Why it's real:** Write operation on Order entity without lock

### 317. `Order` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/security/checkDate/accountId (OrderController.securityInfoCheck)`
- **Endpoint 2:** `DELETE /api/v1/orderservice/order/orderId (OrderController.deleteOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 119
- **Why it's real:** Write operation on Order entity without lock

### 318. `Trip` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 71
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 319. `Trip` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 71
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 320. `Trip` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 94
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 321. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/routes/tripId (Travel2Controller.getRouteByTripId)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 48
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 322. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/routes/tripId (Travel2Controller.getRouteByTripId)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 48
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 323. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/routes/tripId (Travel2Controller.getRouteByTripId)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 48
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 324. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/routes (Travel2Controller.getTripsByRouteId)`
- **Endpoint 2:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 56
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 325. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/routes (Travel2Controller.getTripsByRouteId)`
- **Endpoint 2:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 56
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 326. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/routes (Travel2Controller.getTripsByRouteId)`
- **Endpoint 2:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 56
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 327. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/routes (Travel2Controller.getTripsByRouteId)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 56
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 328. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/routes (Travel2Controller.getTripsByRouteId)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 56
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 329. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/routes (Travel2Controller.getTripsByRouteId)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 56
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 330. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `GET /api/v1/travel2service/trips (Travel2Controller.queryAll)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent read operation

### 331. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/train_types/tripId (TravelController.getTrainTypeByTripId)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent read operation

### 332. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/routes/tripId (TravelController.getRouteByTripId)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent read operation

### 333. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/routes (TravelController.getTripsByRouteId)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent POST operation

### 334. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/trips/tripId (TravelController.retrieve)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent read operation

### 335. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left (TravelController.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent POST operation

### 336. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left_parallel (TravelController.queryInfoInparallel)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent POST operation

### 337. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trip_detail (TravelController.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 64
- **Why it's real:** Write operation on Trip entity with concurrent POST operation

### 338. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips/tripId (Travel2Controller.retrieve)`
- **Endpoint 2:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 79
- **Why it's real:** Concurrent write operation on Trip entity

### 339. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips/tripId (Travel2Controller.retrieve)`
- **Endpoint 2:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 79
- **Why it's real:** Write-Write conflict between GET and DELETE endpoints on the same entity

### 340. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips/tripId (Travel2Controller.retrieve)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 79
- **Why it's real:** Write-Write conflict between GET and POST endpoints on the same entity

### 341. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips/tripId (Travel2Controller.retrieve)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 79
- **Why it's real:** Read-check before Write (TOCTOU) on the same entity

### 342. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips/tripId (Travel2Controller.retrieve)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 79
- **Why it's real:** Write-Write conflict between GET and DELETE endpoints on the same entity

### 343. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/trips/tripId (TravelController.retrieve)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Write-Write conflict between GET and PUT endpoints on the same entity

### 344. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left (TravelController.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 345. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left_parallel (TravelController.queryInfoInparallel)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 346. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trip_detail (TravelController.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 347. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/trips (TravelController.queryAll)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 87
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 348. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travel2service/trips/left (Travel2Controller.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 349. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travel2service/trip_detail (Travel2Controller.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 350. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/routes (TravelController.getTripsByRouteId)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 351. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/trips/tripId (TravelController.retrieve)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 352. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trip_detail (TravelController.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 95
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 353. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trips/left (Travel2Controller.queryInfo)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 116
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 354. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travel2service/trip_detail (Travel2Controller.getTripAllDetailInfo)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 130
- **Why it's real:** Write-Write conflict on Trip entity with high severity

### 355. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips (Travel2Controller.queryAll)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 138
- **Why it's real:** Write-Write endpoint on same entity

### 356. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips (Travel2Controller.queryAll)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 138
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 357. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/trips (Travel2Controller.queryAll)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 138
- **Why it's real:** Write-Write endpoint on same entity

### 358. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/admin_trip (Travel2Controller.adminQueryAll)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 146
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 359. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/admin_trip (Travel2Controller.adminQueryAll)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 146
- **Why it's real:** Write-Write endpoint on same entity

### 360. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips/routes (TravelController.getTripsByRouteId)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 63
- **Why it's real:** Write-Write conflict on same entity

### 361. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips/routes (TravelController.getTripsByRouteId)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 63
- **Why it's real:** Write-Write conflict on same entity

### 362. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips/routes (TravelController.getTripsByRouteId)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 63
- **Why it's real:** Write-Write conflict on same entity

### 363. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/trips/tripId (TravelController.retrieve)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 71
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 364. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left (TravelController.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 71
- **Why it's real:** Write-Write conflict on same entity

### 365. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left_parallel (TravelController.queryInfoInparallel)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 71
- **Why it's real:** Write-Write conflict on same entity

### 366. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/travelservice/trips (TravelController.createTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trip_detail (TravelController.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 71
- **Why it's real:** Write-Write conflict on same entity

### 367. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travelservice/trips/tripId (TravelController.retrieve)`
- **Endpoint 2:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 86
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 368. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travelservice/trips/tripId (TravelController.retrieve)`
- **Endpoint 2:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 86
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 369. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left (TravelController.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 94
- **Why it's real:** Write-Write conflict on same entity

### 370. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left_parallel (TravelController.queryInfoInparallel)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 94
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 371. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trip_detail (TravelController.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 94
- **Why it's real:** Read-check before Write (TOCTOU) on Trip entity

### 372. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/trips (TravelController.queryAll)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 94
- **Why it's real:** Write-Read conflict on Trip entity with no lock

### 373. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/travelservice/trips (TravelController.updateTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/admin_trip (TravelController.adminQueryAll)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 94
- **Why it's real:** Write-Read conflict on Trip entity with no lock

### 374. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left (TravelController.queryInfo)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 102
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 375. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trips/left_parallel (TravelController.queryInfoInparallel)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 102
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 376. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **Endpoint 2:** `POST /api/v1/travelservice/trip_detail (TravelController.getTripAllDetailInfo)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 102
- **Why it's real:** Write-Write conflict on Trip entity with no lock

### 377. `Trip` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/travelservice/trips/tripId (TravelController.deleteTrip)`
- **Endpoint 2:** `GET /api/v1/travelservice/admin_trip (TravelController.adminQueryAll)`
- **File:** `./examples/train-ticket/ts-travel-service/src/main/java/travel/controller/TravelController.java` line 102
- **Why it's real:** Write-Read conflict on Trip entity with no lock

### 378. `Assurance` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/assuranceservice/assurances/orderid/orderId (AssuranceController.deleteAssuranceByOrderId)`
- **Endpoint 2:** `GET /api/v1/assuranceservice/assurances/assuranceid/assuranceId (AssuranceController.getAssuranceById)`
- **File:** `./examples/train-ticket/ts-assurance-service/src/main/java/assurance/controller/AssuranceController.java` line 57
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 379. `User` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/users/login (UserController.getToken)`
- **Endpoint 2:** `POST /api/v1/userservice/users/register (UserController.registerUser)`
- **File:** `./examples/train-ticket/ts-auth-service/src/main/java/auth/controller/UserController.java` line 45
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 380. `User` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/users/login (UserController.getToken)`
- **Endpoint 2:** `DELETE /api/v1/userservice/users/userId (UserController.deleteUserById)`
- **File:** `./examples/train-ticket/ts-auth-service/src/main/java/auth/controller/UserController.java` line 45
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 381. `User` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/users/login (UserController.getToken)`
- **Endpoint 2:** `PUT /api/v1/userservice/users (UserController.updateUser)`
- **File:** `./examples/train-ticket/ts-auth-service/src/main/java/auth/controller/UserController.java` line 45
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 382. `User` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/userservice/users/id/userId (UserController.getUserByUserId)`
- **Endpoint 2:** `POST /api/v1/userservice/users/register (UserController.registerUser)`
- **File:** `./examples/train-ticket/ts-user-service/src/main/java/user/controller/UserController.java` line 49
- **Why it's real:** Write operation on different entity, but same entity is being read and written concurrently

### 383. `Config` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/configservice/configs (ConfigController.queryAll)`
- **Endpoint 2:** `POST api/v1/configservice/configs (ConfigController.createConfig)`
- **File:** `./examples/train-ticket/ts-config-service/src/main/java/config/controller/ConfigController.java` line 39
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 384. `Config` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/configservice/configs (ConfigController.queryAll)`
- **Endpoint 2:** `PUT api/v1/configservice/configs (ConfigController.updateConfig)`
- **File:** `./examples/train-ticket/ts-config-service/src/main/java/config/controller/ConfigController.java` line 39
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 385. `Config` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/configservice/configs (ConfigController.queryAll)`
- **Endpoint 2:** `DELETE api/v1/configservice/configs/configName (ConfigController.deleteConfig)`
- **File:** `./examples/train-ticket/ts-config-service/src/main/java/config/controller/ConfigController.java` line 39
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 386. `ConsignRecord` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/consignservice/consigns (ConsignController.insertConsign)`
- **Endpoint 2:** `GET /api/v1/consignservice/consigns/account/id (ConsignController.findByAccountId)`
- **File:** `./examples/train-ticket/ts-consign-service/src/main/java/consign/controller/ConsignController.java` line 37
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 387. `ConsignRecord` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/consignservice/consigns (ConsignController.updateConsign)`
- **Endpoint 2:** `GET /api/v1/consignservice/consigns/account/id (ConsignController.findByAccountId)`
- **File:** `./examples/train-ticket/ts-consign-service/src/main/java/consign/controller/ConsignController.java` line 43
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 388. `ConsignRecord` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/consignservice/consigns (ConsignController.updateConsign)`
- **Endpoint 2:** `GET /api/v1/consignservice/consigns/order/id (ConsignController.findByOrderId)`
- **File:** `./examples/train-ticket/ts-consign-service/src/main/java/consign/controller/ConsignController.java` line 43
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 389. `ConsignRecord` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/consignservice/consigns (ConsignController.updateConsign)`
- **Endpoint 2:** `GET /api/v1/consignservice/consigns/consignee (ConsignController.findByConsignee)`
- **File:** `./examples/train-ticket/ts-consign-service/src/main/java/consign/controller/ConsignController.java` line 43
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 390. `FoodOrder` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/foodservice/orders (FoodController.updateFoodOrder)`
- **Endpoint 2:** `GET /api/v1/foodservice/orders/orderId (FoodController.findFoodOrderByOrderId)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 72
- **Why it's real:** Write-Write conflict on FoodOrder entity with no lock, high severity

### 391. `Station` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **Endpoint 2:** `GET /api/v1/stationservice/stations/name/stationIdForName (StationController.queryById)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 47
- **Why it's real:** Write-Write endpoint on same entity without lock

### 392. `Station` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **Endpoint 2:** `POST /api/v1/stationservice/stations/namelist (StationController.queryForNameBatch)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 47
- **Why it's real:** Write-Write endpoint on same entity without lock

### 393. `Station` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/stationservice/stations/stationsId (StationController.delete)`
- **Endpoint 2:** `POST /api/v1/stationservice/stations/idlist (StationController.queryForIdBatch)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 53
- **Why it's real:** Write-Write endpoint on same entity without lock

### 394. `Station` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/stationservice/stations/stationsId (StationController.delete)`
- **Endpoint 2:** `GET /api/v1/stationservice/stations/name/stationIdForName (StationController.queryById)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 53
- **Why it's real:** Write-Write endpoint on same entity without lock

### 395. `Station` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/stationservice/stations/stationsId (StationController.delete)`
- **Endpoint 2:** `POST /api/v1/stationservice/stations/namelist (StationController.queryForNameBatch)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 53
- **Why it's real:** Write-Write endpoint on same entity without lock

### 396. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/drawback/userId/money (InsidePaymentController.drawBack)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 34
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 397. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 40
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 398. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.createAccount)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/money (InsidePaymentController.queryAddMoney)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 40
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 399. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/inside_pay_service/inside_payment/userId/money (InsidePaymentController.addMoney)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 47
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 400. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/inside_pay_service/inside_payment/userId/money (InsidePaymentController.addMoney)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/money (InsidePaymentController.queryAddMoney)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 47
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 401. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/inside_pay_service/inside_payment/drawback/userId/money (InsidePaymentController.drawBack)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 65
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 402. `Money` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/inside_pay_service/inside_payment/drawback/userId/money (InsidePaymentController.drawBack)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/money (InsidePaymentController.queryAddMoney)`
- **File:** `./examples/train-ticket/ts-inside-payment-service/src/main/java/inside_payment/controller/InsidePaymentController.java` line 65
- **Why it's real:** Write-Write conflict on same entity 'Money'

### 403. `Contacts` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/contactservice/contacts (ContactsController.createNewContacts)`
- **Endpoint 2:** `POST api/v1/contactservice/contacts/admin (ContactsController.createNewContactsAdmin)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 46
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 404. `Contacts` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/contactservice/contacts (ContactsController.createNewContacts)`
- **Endpoint 2:** `PUT api/v1/contactservice/contacts (ContactsController.modifyContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 46
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 405. `Contacts` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST api/v1/contactservice/contacts/admin (ContactsController.createNewContactsAdmin)`
- **Endpoint 2:** `PUT api/v1/contactservice/contacts (ContactsController.modifyContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 54
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 406. `Contacts` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST api/v1/contactservice/contacts/admin (ContactsController.createNewContactsAdmin)`
- **Endpoint 2:** `GET api/v1/contactservice/contacts/account/accountId (ContactsController.findContactsByAccountId)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 54
- **Why it's real:** Write operation on admin endpoint and read operation on account endpoint can cause data corruption/lost updates

### 407. `Contacts` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST api/v1/contactservice/contacts/admin (ContactsController.createNewContactsAdmin)`
- **Endpoint 2:** `GET api/v1/contactservice/contacts/id (ContactsController.getContactsByContactsId)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 54
- **Why it's real:** Write operation on admin endpoint and read operation on specific contact endpoint can cause data corruption/lost updates

### 408. `Contacts` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT api/v1/contactservice/contacts (ContactsController.modifyContacts)`
- **Endpoint 2:** `GET api/v1/contactservice/contacts/account/accountId (ContactsController.findContactsByAccountId)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 69
- **Why it's real:** Write operation on contacts endpoint and read operation on account endpoint can cause data corruption/lost updates

### 409. `Contacts` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT api/v1/contactservice/contacts (ContactsController.modifyContacts)`
- **Endpoint 2:** `GET api/v1/contactservice/contacts/id (ContactsController.getContactsByContactsId)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 69
- **Why it's real:** Write operation on contacts endpoint and read operation on specific contact endpoint can cause data corruption/lost updates

### 410. `SecurityConfig` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/securityservice/securityConfigs (SecurityController.findAllSecurityConfig)`
- **Endpoint 2:** `POST /api/v1/securityservice/securityConfigs (SecurityController.create)`
- **File:** `./examples/train-ticket/ts-security-service/src/main/java/security/controller/SecurityController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 411. `SecurityConfig` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/securityservice/securityConfigs (SecurityController.findAllSecurityConfig)`
- **Endpoint 2:** `PUT /api/v1/securityservice/securityConfigs (SecurityController.update)`
- **File:** `./examples/train-ticket/ts-security-service/src/main/java/security/controller/SecurityController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 412. `SecurityConfig` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/securityservice/securityConfigs (SecurityController.findAllSecurityConfig)`
- **Endpoint 2:** `DELETE /api/v1/securityservice/securityConfigs/id (SecurityController.delete)`
- **File:** `./examples/train-ticket/ts-security-service/src/main/java/security/controller/SecurityController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 413. `FoodDeliveryOrder` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `GET /api/v1/fooddeliveryservice/orders/store/storeId (FoodDeliveryController.getFoodDeliveryOrderByStoreId)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Write operation on FoodDeliveryOrder entity without lock

### 414. `FoodDeliveryOrder` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/fooddeliveryservice/orders/d/orderId (FoodDeliveryController.deleteFoodDeliveryOrder)`
- **Endpoint 2:** `GET /api/v1/fooddeliveryservice/orders/store/storeId (FoodDeliveryController.getFoodDeliveryOrderByStoreId)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 43
- **Why it's real:** Write operation on FoodDeliveryOrder entity without lock

### 415. `FoodDeliveryOrder` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/fooddeliveryservice/orders/orderId (FoodDeliveryController.getFoodDeliveryOrderById)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/tripid (FoodDeliveryController.updateTripId)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 49
- **Why it's real:** Read-check before Write (TOCTOU) on FoodDeliveryOrder entity

### 416. `FoodDeliveryOrder` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/fooddeliveryservice/orders/orderId (FoodDeliveryController.getFoodDeliveryOrderById)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/seatno (FoodDeliveryController.updateSeatNo)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 49
- **Why it's real:** Read-check before Write (TOCTOU) on FoodDeliveryOrder entity

### 417. `FoodDeliveryOrder` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/fooddeliveryservice/orders/orderId (FoodDeliveryController.getFoodDeliveryOrderById)`
- **Endpoint 2:** `PUT /api/v1/fooddeliveryservice/orders/dtime (FoodDeliveryController.updateDeliveryTime)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 49
- **Why it's real:** Read-check before Write (TOCTOU) on FoodDeliveryOrder entity

### 418. `TrainType` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/trainservice/trains (TrainController.create)`
- **Endpoint 2:** `GET /api/v1/trainservice/trains/id (TrainController.retrieve)`
- **File:** `./examples/train-ticket/ts-train-service/src/main/java/train/controller/TrainController.java` line 37
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 419. `TrainType` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/trainservice/trains (TrainController.create)`
- **Endpoint 2:** `GET /api/v1/trainservice/trains/byName/name (TrainController.retrieveByName)`
- **File:** `./examples/train-ticket/ts-train-service/src/main/java/train/controller/TrainController.java` line 37
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 420. `TrainType` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/trainservice/trains (TrainController.create)`
- **Endpoint 2:** `GET /api/v1/trainservice/trains (TrainController.query)`
- **File:** `./examples/train-ticket/ts-train-service/src/main/java/train/controller/TrainController.java` line 37
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 421. `Route` — CRITICAL | risk 8/10
- **Type:** WRITE_WRITE
- **Confidence:** CRITICAL
- **Endpoint 1:** `POST /api/v1/routeservice/routes (RouteController.createAndModifyRoute)`
- **Endpoint 2:** `DELETE /api/v1/routeservice/routes/routeId (RouteController.deleteRoute)`
- **File:** `./examples/train-ticket/ts-route-service/src/main/java/route/controller/RouteController.java` line 36
- **Why it's real:** Two WRITE endpoints on same entity with no lock

### 422. `ConsignPrice` — HIGH | risk 8/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/consignpriceservice/consignprice/weight/isWithinRegion (ConsignPriceController.getPriceByWeightAndRegion)`
- **Endpoint 2:** `POST /api/v1/consignpriceservice/consignprice (ConsignPriceController.modifyPriceConfig)`
- **File:** `./examples/train-ticket/ts-consign-price-service/src/main/java/consignprice/controller/ConsignPriceController.java` line 35
- **Why it's real:** Write operation on ConsignPrice entity without lock

### 423. `Order` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `POST /api/v1/orderOtherService/orderOther (OrderOtherController.createNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** CreateNewOrder and payOrder on Order entity with high severity

### 424. `Order` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/orderOtherService/orderOther/tickets (OrderOtherController.getTicketListByDateAndTripId)`
- **Endpoint 2:** `POST /api/v1/orderOtherService/orderOther/admin (OrderOtherController.addcreateNewOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 43
- **Why it's real:** CreateNewOrder and payOrder on Order entity with high severity

### 425. `FoodOrder` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/foodservice/orders (FoodController.findAllFoodOrder)`
- **Endpoint 2:** `POST /api/v1/foodservice/orders (FoodController.createFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 53
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 426. `FoodOrder` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/foodservice/orders (FoodController.findAllFoodOrder)`
- **Endpoint 2:** `POST /api/v1/foodservice/createOrderBatch (FoodController.createFoodBatches)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 53
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 427. `FoodOrder` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/foodservice/orders (FoodController.findAllFoodOrder)`
- **Endpoint 2:** `PUT /api/v1/foodservice/orders (FoodController.updateFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 53
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 428. `FoodOrder` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/foodservice/orders (FoodController.findAllFoodOrder)`
- **Endpoint 2:** `DELETE /api/v1/foodservice/orders/orderId (FoodController.deleteFoodOrder)`
- **File:** `./examples/train-ticket/ts-food-service/src/main/java/foodsearch/controller/FoodController.java` line 53
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 429. `Station` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/stationservice/stations (StationController.query)`
- **Endpoint 2:** `POST /api/v1/stationservice/stations (StationController.create)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 430. `Station` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/stationservice/stations (StationController.query)`
- **Endpoint 2:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 431. `Station` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/stationservice/stations (StationController.query)`
- **Endpoint 2:** `DELETE /api/v1/stationservice/stations/stationsId (StationController.delete)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 432. `Station` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **Endpoint 2:** `GET /api/v1/stationservice/stations/id/stationNameForId (StationController.queryForStationId)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 47
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 433. `Station` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `PUT /api/v1/stationservice/stations (StationController.update)`
- **Endpoint 2:** `POST /api/v1/stationservice/stations/idlist (StationController.queryForIdBatch)`
- **File:** `./examples/train-ticket/ts-station-service/src/main/java/fdse/microservice/controller/StationController.java` line 47
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 434. `Payment` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment (PaymentController.pay)`
- **Endpoint 2:** `GET /api/v1/paymentservice/payment (PaymentController.query)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 435. `Payment` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment (PaymentController.pay)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/payment (InsidePaymentController.queryPayment)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 436. `Payment` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/paymentservice/payment (PaymentController.pay)`
- **Endpoint 2:** `GET /api/v1/inside_pay_service/inside_payment/account (InsidePaymentController.queryAccount)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 35
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 437. `Payment` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/paymentservice/payment (PaymentController.query)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment (InsidePaymentController.pay)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 47
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 438. `Payment` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/paymentservice/payment (PaymentController.query)`
- **Endpoint 2:** `POST /api/v1/inside_pay_service/inside_payment/difference (InsidePaymentController.payDifference)`
- **File:** `./examples/train-ticket/ts-payment-service/src/main/java/com/trainticket/controller/PaymentController.java` line 47
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 439. `Route` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/routeservice/routes (RouteController.createAndModifyRoute)`
- **Endpoint 2:** `GET /api/v1/routeservice/routes/routeId (RouteController.queryById)`
- **File:** `./examples/train-ticket/ts-route-service/src/main/java/route/controller/RouteController.java` line 36
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 440. `Route` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `POST /api/v1/routeservice/routes (RouteController.createAndModifyRoute)`
- **Endpoint 2:** `POST /api/v1/routeservice/routes/byIds (RouteController.queryByIds)`
- **File:** `./examples/train-ticket/ts-route-service/src/main/java/route/controller/RouteController.java` line 36
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 441. `Route` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/routeservice/routes/routeId (RouteController.deleteRoute)`
- **Endpoint 2:** `GET /api/v1/routeservice/routes/routeId (RouteController.queryById)`
- **File:** `./examples/train-ticket/ts-route-service/src/main/java/route/controller/RouteController.java` line 42
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 442. `Route` — HIGH | risk 7/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `DELETE /api/v1/routeservice/routes/routeId (RouteController.deleteRoute)`
- **Endpoint 2:** `POST /api/v1/routeservice/routes/byIds (RouteController.queryByIds)`
- **File:** `./examples/train-ticket/ts-route-service/src/main/java/route/controller/RouteController.java` line 42
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 443. `Order` — CRITICAL | risk 6/10
- **Type:** WRITE_WRITE
- **Confidence:** MEDIUM
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 444. `Order` — CRITICAL | risk 6/10
- **Type:** WRITE_WRITE
- **Confidence:** MEDIUM
- **Endpoint 1:** `GET /api/v1/orderOtherService/orderOther/status/orderId/status (OrderOtherController.modifyOrder)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-other-service/src/main/java/other/controller/OrderOtherController.java` line 111
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 445. `Order` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/orderPay/orderId (OrderController.payOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 85
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 446. `Order` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/orderservice/order/price/orderId (OrderController.getOrderPrice)`
- **Endpoint 2:** `GET /api/v1/orderservice/order/status/orderId/status (OrderController.modifyOrder)`
- **File:** `./examples/train-ticket/ts-order-service/src/main/java/order/controller/OrderController.java` line 85
- **Why it's real:** Read-check before Write (TOCTOU) on Order entity

### 447. `Trip` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/train_types/tripId (Travel2Controller.getTrainTypeByTripId)`
- **Endpoint 2:** `POST /api/v1/travel2service/trips (Travel2Controller.createTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 448. `Trip` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/train_types/tripId (Travel2Controller.getTrainTypeByTripId)`
- **Endpoint 2:** `PUT /api/v1/travel2service/trips (Travel2Controller.updateTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 449. `Trip` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET /api/v1/travel2service/train_types/tripId (Travel2Controller.getTrainTypeByTripId)`
- **Endpoint 2:** `DELETE /api/v1/travel2service/trips/tripId (Travel2Controller.deleteTrip)`
- **File:** `./examples/train-ticket/ts-travel2-service/src/main/java/travel2/controller/Travel2Controller.java` line 40
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 450. `Contacts` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/contactservice/contacts (ContactsController.getAllContacts)`
- **Endpoint 2:** `POST api/v1/contactservice/contacts (ContactsController.createNewContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 38
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 451. `Contacts` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/contactservice/contacts (ContactsController.getAllContacts)`
- **Endpoint 2:** `POST api/v1/contactservice/contacts/admin (ContactsController.createNewContactsAdmin)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 38
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 452. `Contacts` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/contactservice/contacts (ContactsController.getAllContacts)`
- **Endpoint 2:** `DELETE api/v1/contactservice/contacts/contactsId (ContactsController.deleteContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 38
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 453. `Contacts` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** HIGH
- **Endpoint 1:** `GET api/v1/contactservice/contacts (ContactsController.getAllContacts)`
- **Endpoint 2:** `PUT api/v1/contactservice/contacts (ContactsController.modifyContacts)`
- **File:** `./examples/train-ticket/ts-contacts-service/src/main/java/contacts/controller/ContactsController.java` line 38
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 454. `FoodDeliveryOrder` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** MEDIUM
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `GET /api/v1/fooddeliveryservice/orders/orderId (FoodDeliveryController.getFoodDeliveryOrderById)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

### 455. `FoodDeliveryOrder` — HIGH | risk 6/10
- **Type:** READ_WRITE
- **Confidence:** MEDIUM
- **Endpoint 1:** `POST /api/v1/fooddeliveryservice/orders (FoodDeliveryController.createFoodDeliveryOrder)`
- **Endpoint 2:** `GET /api/v1/fooddeliveryservice/orders/all (FoodDeliveryController.getAllFoodDeliveryOrders)`
- **File:** `./examples/train-ticket/ts-food-delivery-service/src/main/java/food_delivery/controller/FoodDeliveryController.java` line 37
- **Why it's real:** Read-check before Write (TOCTOU) on same entity

---
## 🟡 Uncertain — needs manual review

- `Order` [CRITICAL] `OrderOtherController.updateOrder` ↔ `OrderController.createNewOrder` — *Admin config endpoint rarely called concurrently*
- `Order` [CRITICAL] `OrderOtherController.updateOrder` ↔ `OrderController.addcreateNewOrder` — *Admin config endpoint rarely called concurrently*
- `Order` [HIGH] `OrderOtherController.addcreateNewOrder` ↔ `OrderOtherController.queryOrders` — *Admin config endpoints rarely called concurrently*
- `Order` [HIGH] `OrderOtherController.addcreateNewOrder` ↔ `OrderOtherController.calculateSoldTicket` — *Admin config endpoints rarely called concurrently*
- `Order` [HIGH] `OrderController.addcreateNewOrder` ↔ `OrderController.queryOrders` — *Admin config endpoints rarely called concurrently, insufficient information to decide*
- `Order` [HIGH] `OrderController.payOrder` ↔ `OrderController.securityInfoCheck` — *Admin config endpoint rarely called concurrently*
- `Order` [HIGH] `OrderController.payOrder` ↔ `OrderController.findAllOrder` — *Admin config endpoint rarely called concurrently*
- `Trip` [HIGH] `Travel2Controller.updateTrip` ↔ `Travel2Controller.adminQueryAll` — *Admin config endpoint rarely called concurrently*
- `Trip` [HIGH] `Travel2Controller.updateTrip` ↔ `TravelController.adminQueryAll` — *Admin config endpoints rarely called concurrently*
- `Trip` [HIGH] `Travel2Controller.deleteTrip` ↔ `Travel2Controller.adminQueryAll` — *Admin config endpoints rarely called concurrently*
- `Trip` [HIGH] `Travel2Controller.adminQueryAll` ↔ `TravelController.createTrip` — *Admin config endpoint rarely called concurrently*
- `Trip` [HIGH] `TravelController.createTrip` ↔ `TravelController.adminQueryAll` — *Admin config endpoints rarely called concurrently*
- `FoodDeliveryOrder` [HIGH] `FoodDeliveryController.getFoodDeliveryOrderByStoreId` ↔ `FoodDeliveryController.updateDeliveryTime` — *parse error*
- `TrainType` [HIGH] `TrainController.update` ↔ `TrainController.query` — *Admin config endpoints rarely called concurrently*
- `TrainType` [HIGH] `TrainController.delete` ↔ `TrainController.query` — *Admin config endpoints rarely called concurrently*

---
## ✅ False Positives — filtered out

- ~~`PriceConfig`~~ `PriceController.queryAll` ↔ `PriceController.create` — *Endpoints partitioned by different path param*
- ~~`PriceConfig`~~ `PriceController.queryAll` ↔ `PriceController.delete` — *Endpoints partitioned by different path param*
- ~~`PriceConfig`~~ `PriceController.queryAll` ↔ `PriceController.update` — *Endpoints partitioned by different path param*
- ~~`Order`~~ `OrderOtherController.addcreateNewOrder` ↔ `OrderController.payOrder` — *Read-only endpoint on Order entity*
- ~~`Order`~~ `OrderOtherController.addcreateNewOrder` ↔ `OrderController.modifyOrder` — *Read-only endpoint on Order entity*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderController.payOrder` — *Endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderController.modifyOrder` — *Endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.modifyOrder` ↔ `OrderController.saveOrderInfo` — *Endpoints partitioned by different user/orderId path param*
- ~~`Order`~~ `OrderOtherController.updateOrder` ↔ `OrderOtherController.deleteOrder` — *Endpoints partitioned by different admin path param*
- ~~`Order`~~ `OrderController.payOrder` ↔ `OrderController.modifyOrder` — *Both endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.getTicketListByDateAndTripId` ↔ `OrderOtherController.payOrder` — *Read-only endpoint and partitioned by order ID*
- ~~`Order`~~ `OrderOtherController.getTicketListByDateAndTripId` ↔ `OrderOtherController.modifyOrder` — *Read-only endpoint and partitioned by order ID*
- ~~`Order`~~ `OrderOtherController.getTicketListByDateAndTripId` ↔ `OrderOtherController.saveOrderInfo` — *Read-only endpoint and partitioned by order ID*
- ~~`Order`~~ `OrderOtherController.createNewOrder` ↔ `OrderOtherController.queryOrders` — *Endpoints are partitioned by different path param*
- ~~`Order`~~ `OrderOtherController.createNewOrder` ↔ `OrderOtherController.calculateSoldTicket` — *Endpoints are partitioned by different path param*
- ~~`Order`~~ `OrderOtherController.createNewOrder` ↔ `OrderOtherController.getOrderPrice` — *Endpoints are partitioned by different path param*
- ~~`Order`~~ `OrderOtherController.calculateSoldTicket` ↔ `OrderOtherController.payOrder` — *Read-only endpoints on different paths*
- ~~`Order`~~ `OrderOtherController.getOrderPrice` ↔ `OrderOtherController.payOrder` — *Both endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderOtherController.getOrderById` — *Endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderOtherController.findAllOrder` — *Both endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderController.calculateSoldTicket` — *Endpoints partitioned by different path param*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderController.securityInfoCheck` — *Endpoints partitioned by different path param*
- ~~`Order`~~ `OrderOtherController.payOrder` ↔ `OrderController.findAllOrder` — *Both endpoints are GET/read-only on same entity*
- ~~`Order`~~ `OrderOtherController.modifyOrder` ↔ `OrderOtherController.securityInfoCheck` — *Read-only endpoints on different entity OrderOther*
- ~~`Order`~~ `OrderOtherController.modifyOrder` ↔ `OrderOtherController.findAllOrder` — *Read-only endpoints on different entity OrderOther*
- ~~`Order`~~ `OrderOtherController.modifyOrder` ↔ `OrderController.getTicketListByDateAndTripId` — *Read-only endpoints on different entity OrderOther*
- ~~`Order`~~ `OrderOtherController.modifyOrder` ↔ `OrderController.queryOrders` — *Read-only endpoints on different entity OrderOther*
- ~~`Order`~~ `OrderOtherController.modifyOrder` ↔ `OrderController.getOrderById` — *Both endpoints are GET on Order entity*
- ~~`Order`~~ `OrderOtherController.updateOrder` ↔ `OrderOtherController.findAllOrder` — *Endpoints are partitioned by different path param (admin) and are idempotent*
- ~~`Order`~~ `OrderOtherController.deleteOrder` ↔ `OrderOtherController.findAllOrder` — *DELETE and GET endpoints are on different Order entities*
- ~~`Order`~~ `OrderController.createNewOrder` ↔ `OrderController.calculateSoldTicket` — *Endpoints are GET/read-only on Order entity with different path parameters*
- ~~`Order`~~ `OrderController.createNewOrder` ↔ `OrderController.getOrderPrice` — *Endpoints are GET/read-only on Order entity with different path parameters*
- ~~`Order`~~ `OrderController.createNewOrder` ↔ `OrderController.getOrderById` — *Endpoints are GET/read-only on Order entity with different path parameters*
- ~~`Order`~~ `OrderController.createNewOrder` ↔ `OrderController.securityInfoCheck` — *Endpoints are GET/read-only on Order entity with different path parameters*
- ~~`Order`~~ `OrderController.createNewOrder` ↔ `OrderController.findAllOrder` — *Endpoints are GET/read-only on Order entity with different path parameters*
- ~~`Order`~~ `OrderController.calculateSoldTicket` ↔ `OrderController.payOrder` — *Read-only endpoints on different paths*
- ~~`Order`~~ `OrderController.calculateSoldTicket` ↔ `OrderController.modifyOrder` — *Read-only endpoints on different paths*
- ~~`Order`~~ `OrderController.payOrder` ↔ `OrderController.getOrderById` — *Endpoints are partitioned by different path parameters*
- ~~`Order`~~ `OrderController.getOrderById` ↔ `OrderController.modifyOrder` — *Endpoints are partitioned by different path parameters*
- ~~`Order`~~ `OrderController.modifyOrder` ↔ `OrderController.securityInfoCheck` — *Read and write operations on different Order entity fields*
- ~~`Order`~~ `OrderController.modifyOrder` ↔ `OrderController.findAllOrder` — *Read and write operations on different Order entity fields*
- ~~`Order`~~ `OrderController.saveOrderInfo` ↔ `OrderController.findAllOrder` — *Read operation on Order entity*
- ~~`Order`~~ `OrderController.updateOrder` ↔ `OrderController.findAllOrder` — *Read operation on Order entity*
- ~~`Order`~~ `OrderController.deleteOrder` ↔ `OrderController.findAllOrder` — *Read operation on Order entity*
- ~~`Trip`~~ `Travel2Controller.getTrainTypeByTripId` ↔ `TravelController.createTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.getTrainTypeByTripId` ↔ `TravelController.updateTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.getTrainTypeByTripId` ↔ `TravelController.deleteTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.getRouteByTripId` ↔ `Travel2Controller.createTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.getRouteByTripId` ↔ `Travel2Controller.updateTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.getRouteByTripId` ↔ `Travel2Controller.deleteTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.createTrip` ↔ `Travel2Controller.retrieve` — *Read and write endpoints are on different paths*
- ~~`Trip`~~ `Travel2Controller.createTrip` ↔ `Travel2Controller.queryInfo` — *Read and write endpoints are on different paths*
- ~~`Trip`~~ `Travel2Controller.createTrip` ↔ `Travel2Controller.getTripAllDetailInfo` — *Read and write endpoints are on different paths*
- ~~`Trip`~~ `Travel2Controller.createTrip` ↔ `Travel2Controller.adminQueryAll` — *Admin endpoint rarely called concurrently*
- ~~`Trip`~~ `Travel2Controller.createTrip` ↔ `TravelController.queryAll` — *Concurrent read operations on Trip entity*
- ~~`Trip`~~ `Travel2Controller.createTrip` ↔ `TravelController.adminQueryAll` — *Admin endpoint rarely called concurrently*
- ~~`Trip`~~ `Travel2Controller.updateTrip` ↔ `Travel2Controller.queryInfo` — *Endpoints are not directly related to the same entity*
- ~~`Trip`~~ `Travel2Controller.updateTrip` ↔ `Travel2Controller.getTripAllDetailInfo` — *Endpoints are not directly related to the same entity*
- ~~`Trip`~~ `Travel2Controller.updateTrip` ↔ `Travel2Controller.queryAll` — *Endpoints are not directly related to the same entity*
- ~~`Trip`~~ `Travel2Controller.updateTrip` ↔ `TravelController.getTrainTypeByTripId` — *Endpoints are not directly related to the same entity*
- ~~`Trip`~~ `Travel2Controller.updateTrip` ↔ `TravelController.getRouteByTripId` — *Endpoints are not directly related to the same entity*
- ~~`Trip`~~ `Travel2Controller.updateTrip` ↔ `TravelController.getTripsByRouteId` — *Endpoints are not directly related to the same entity*
- ~~`Trip`~~ `Travel2Controller.deleteTrip` ↔ `Travel2Controller.queryAll` — *Both endpoints are GET/read-only on same entity*
- ~~`Trip`~~ `Travel2Controller.deleteTrip` ↔ `TravelController.getTrainTypeByTripId` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.deleteTrip` ↔ `TravelController.getRouteByTripId` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `Travel2Controller.deleteTrip` ↔ `TravelController.queryAll` — *Read-only endpoints on Trip entity*
- ~~`Trip`~~ `Travel2Controller.deleteTrip` ↔ `TravelController.adminQueryAll` — *Read-only endpoints on Trip entity*
- ~~`Trip`~~ `TravelController.getTrainTypeByTripId` ↔ `TravelController.createTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `TravelController.getTrainTypeByTripId` ↔ `TravelController.updateTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `TravelController.getTrainTypeByTripId` ↔ `TravelController.deleteTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `TravelController.getRouteByTripId` ↔ `TravelController.createTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `TravelController.getRouteByTripId` ↔ `TravelController.updateTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `TravelController.getRouteByTripId` ↔ `TravelController.deleteTrip` — *Endpoints partitioned by different path param*
- ~~`Trip`~~ `TravelController.createTrip` ↔ `TravelController.queryAll` — *Endpoints are GET/read-only on same entity*
- ~~`Trip`~~ `TravelController.deleteTrip` ↔ `TravelController.queryAll` — *Read-only endpoint*
- ~~`Assurance`~~ `AssuranceController.getAllAssurances` ↔ `AssuranceController.deleteAssurance` — *Read-only endpoint and DELETE endpoint on different path parameters*
- ~~`Assurance`~~ `AssuranceController.getAllAssurances` ↔ `AssuranceController.deleteAssuranceByOrderId` — *Read-only endpoint and DELETE endpoint on different path parameters*
- ~~`Assurance`~~ `AssuranceController.getAllAssurances` ↔ `AssuranceController.modifyAssurance` — *Read-only endpoint and PATCH endpoint on different path parameters*
- ~~`Assurance`~~ `AssuranceController.getAllAssurances` ↔ `AssuranceController.createNewAssurance` — *Read-only endpoint and GET endpoint on different path parameters*
- ~~`Assurance`~~ `AssuranceController.deleteAssurance` ↔ `AssuranceController.getAssuranceById` — *Read-only endpoint and GET endpoint on same entity but different path parameters*
- ~~`Assurance`~~ `AssuranceController.deleteAssurance` ↔ `AssuranceController.findAssuranceByOrderId` — *Read-only endpoint and GET endpoint on same entity but different path parameters*
- ~~`Assurance`~~ `AssuranceController.deleteAssuranceByOrderId` ↔ `AssuranceController.findAssuranceByOrderId` — *Endpoints partitioned by different path parameters*
- ~~`Assurance`~~ `AssuranceController.createNewAssurance` ↔ `AssuranceController.getAssuranceById` — *Both endpoints are GET/read-only on same entity*
- ~~`Assurance`~~ `AssuranceController.createNewAssurance` ↔ `AssuranceController.findAssuranceByOrderId` — *Both endpoints are GET/read-only on same entity*
- ~~`User`~~ `UserController.getAllUser` ↔ `UserController.registerUser` — *Both endpoints are GET/read-only on same entity*
- ~~`User`~~ `UserController.getAllUser` ↔ `UserController.deleteUserById` — *Both endpoints are GET/read-only on same entity*
- ~~`User`~~ `UserController.getAllUser` ↔ `UserController.updateUser` — *Both endpoints are GET/read-only on same entity*
- ~~`User`~~ `UserController.getUserByUserName` ↔ `UserController.registerUser` — *Both endpoints are GET/read-only on same entity*
- ~~`User`~~ `UserController.getUserByUserName` ↔ `UserController.deleteUserById` — *Both endpoints are GET/read-only on same entity*
- ~~`User`~~ `UserController.getUserByUserName` ↔ `UserController.updateUser` — *Both endpoints are GET/read-only on same entity*
- ~~`Config`~~ `ConfigController.createConfig` ↔ `ConfigController.retrieve` — *Endpoints partitioned by different path param*
- ~~`Config`~~ `ConfigController.updateConfig` ↔ `ConfigController.retrieve` — *Endpoints partitioned by different path param*
- ~~`Config`~~ `ConfigController.deleteConfig` ↔ `ConfigController.retrieve` — *Endpoints partitioned by different path param*
- ~~`ConsignRecord`~~ `ConsignController.insertConsign` ↔ `ConsignController.findByOrderId` — *Endpoints partitioned by different path param (order/id)*
- ~~`ConsignRecord`~~ `ConsignController.insertConsign` ↔ `ConsignController.findByConsignee` — *Endpoints partitioned by different path param (consignee)*
- ~~`FoodOrder`~~ `FoodController.createFoodOrder` ↔ `FoodController.findFoodOrderByOrderId` — *Endpoints partitioned by different path param (orderId)*
- ~~`FoodOrder`~~ `FoodController.createFoodBatches` ↔ `FoodController.findFoodOrderByOrderId` — *Endpoints partitioned by different path param (orderId)*
- ~~`FoodOrder`~~ `FoodController.deleteFoodOrder` ↔ `FoodController.findFoodOrderByOrderId` — *Read-only GET endpoint on FoodOrder entity, partitioned by orderId path param*
- ~~`Station`~~ `StationController.create` ↔ `StationController.queryForStationId` — *Endpoints partitioned by different path param*
- ~~`Station`~~ `StationController.create` ↔ `StationController.queryForIdBatch` — *Endpoints partitioned by different path param*
- ~~`Station`~~ `StationController.create` ↔ `StationController.queryById` — *Endpoints partitioned by different path param*
- ~~`Station`~~ `StationController.create` ↔ `StationController.queryForNameBatch` — *Endpoints partitioned by different path param*
- ~~`Station`~~ `StationController.delete` ↔ `StationController.queryForStationId` — *Read endpoint is idempotent and does not modify data*
- ~~`Money`~~ `InsidePaymentController.addMoney` ↔ `InsidePaymentController.drawBack` — *Both endpoints are GET/read-only on same entity*
- ~~`Money`~~ `PaymentController.addMoney` ↔ `InsidePaymentController.queryAccount` — *Endpoints partitioned by different path param*
- ~~`Money`~~ `PaymentController.addMoney` ↔ `InsidePaymentController.queryAddMoney` — *Endpoints partitioned by different path param*
- ~~`Money`~~ `InsidePaymentController.addMoney` ↔ `InsidePaymentController.queryAccount` — *Read-only endpoints on different paths*
- ~~`Money`~~ `InsidePaymentController.queryAccount` ↔ `InsidePaymentController.drawBack` — *Read-only endpoints on different paths*
- ~~`Payment`~~ `InsidePaymentController.pay` ↔ `InsidePaymentController.queryPayment` — *Endpoints partitioned by different path param*
- ~~`Payment`~~ `InsidePaymentController.pay` ↔ `InsidePaymentController.queryAccount` — *Endpoints partitioned by different path param*
- ~~`Payment`~~ `InsidePaymentController.queryPayment` ↔ `InsidePaymentController.payDifference` — *Endpoints partitioned by different path param*
- ~~`Payment`~~ `InsidePaymentController.queryAccount` ↔ `InsidePaymentController.payDifference` — *Endpoints partitioned by different path param*
- ~~`Contacts`~~ `ContactsController.createNewContacts` ↔ `ContactsController.findContactsByAccountId` — *Endpoints partitioned by different path param*
- ~~`Contacts`~~ `ContactsController.createNewContacts` ↔ `ContactsController.getContactsByContactsId` — *Endpoints partitioned by different path param*
- ~~`Contacts`~~ `ContactsController.deleteContacts` ↔ `ContactsController.findContactsByAccountId` — *Delete operation and read operation on account endpoint are not concurrent writes*
- ~~`Contacts`~~ `ContactsController.deleteContacts` ↔ `ContactsController.getContactsByContactsId` — *Delete operation and read operation on specific contact endpoint are not concurrent writes*
- ~~`SecurityConfig`~~ `SecurityController.create` ↔ `SecurityController.check` — *Endpoints partitioned by different path param*
- ~~`SecurityConfig`~~ `SecurityController.update` ↔ `SecurityController.check` — *Endpoints partitioned by different path param*
- ~~`SecurityConfig`~~ `SecurityController.delete` ↔ `SecurityController.check` — *Endpoints partitioned by different path param*
- ~~`FoodDeliveryOrder`~~ `FoodDeliveryController.deleteFoodDeliveryOrder` ↔ `FoodDeliveryController.getAllFoodDeliveryOrders` — *GET /api/v1/fooddeliveryservice/orders/all is a read-only endpoint*
- ~~`FoodDeliveryOrder`~~ `FoodDeliveryController.getAllFoodDeliveryOrders` ↔ `FoodDeliveryController.updateTripId` — *GET /api/v1/fooddeliveryservice/orders/all is a read-only endpoint*
- ~~`FoodDeliveryOrder`~~ `FoodDeliveryController.getAllFoodDeliveryOrders` ↔ `FoodDeliveryController.updateSeatNo` — *GET /api/v1/fooddeliveryservice/orders/all is a read-only endpoint*
- ~~`FoodDeliveryOrder`~~ `FoodDeliveryController.getAllFoodDeliveryOrders` ↔ `FoodDeliveryController.updateDeliveryTime` — *GET /api/v1/fooddeliveryservice/orders/all is a read-only endpoint*
- ~~`FoodDeliveryOrder`~~ `FoodDeliveryController.getFoodDeliveryOrderByStoreId` ↔ `FoodDeliveryController.updateTripId` — *Endpoints are partitioned by different path param (storeId)*
- ~~`FoodDeliveryOrder`~~ `FoodDeliveryController.getFoodDeliveryOrderByStoreId` ↔ `FoodDeliveryController.updateSeatNo` — *Endpoints are partitioned by different path param (storeId)*
- ~~`TrainType`~~ `TrainController.retrieve` ↔ `TrainController.update` — *Endpoints are GET/read-only on same entity*
- ~~`TrainType`~~ `TrainController.retrieve` ↔ `TrainController.delete` — *Endpoints are GET/read-only on same entity*
- ~~`TrainType`~~ `TrainController.retrieveByName` ↔ `TrainController.update` — *Endpoints are GET/read-only on same entity*
- ~~`TrainType`~~ `TrainController.retrieveByName` ↔ `TrainController.delete` — *Endpoints are GET/read-only on same entity*
- ~~`Route`~~ `RouteController.createAndModifyRoute` ↔ `RouteController.queryAll` — *Both endpoints are GET/read-only on same entity*
- ~~`Route`~~ `RouteController.createAndModifyRoute` ↔ `RouteController.queryByStartAndTerminal` — *Both endpoints are GET/read-only on same entity*
- ~~`Route`~~ `RouteController.deleteRoute` ↔ `RouteController.queryAll` — *Both endpoints are GET/read-only on same entity*
- ~~`Route`~~ `RouteController.deleteRoute` ↔ `RouteController.queryByStartAndTerminal` — *Both endpoints are GET/read-only on same entity*
- ~~`ConsignPrice`~~ `ConsignPriceController.getPriceInfo` ↔ `ConsignPriceController.modifyPriceConfig` — *GET and POST endpoints are on different paths, GET is read-only*

---
## Fix Recommendations

| Race Type | Recommended Fix |
|-----------|----------------|
| WRITE_WRITE on Order/Payment | Optimistic locking (`@Version`) + retry |
| WRITE_WRITE on config entities | Pessimistic lock or admin serialisation |
| READ_WRITE (TOCTOU) | Atomic compare-and-swap or DB constraint |
| Any unprotected critical path | Redis distributed lock (Redisson) |