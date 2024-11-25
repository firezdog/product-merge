# Repository Overview

This repository provides a **Proof of Concept (POC)** for processing and updating supplier information from JSON lines files efficiently. The process is designed to minimize database round trips and avoid calculating differences in code, focusing on bulk inserts and database-level merging.

## Process Description

### 1. Seeding Initial Data
- A seed file initializes the `products` table with sample data.
- Each product includes the following fields: `id`, `supplier_id`, `price`, `created_at`, and `updated_at`.

### 2. Processing Update Files
- A file with product updates is read, and the updates are inserted into two temporary tables:
  1. **Full Updates Table**:
     - Contains updates where a `supplier_id` and a `price` are provided, but the `id` field is not required.
     - These updates fully replace the product information for the given `supplier_id`.
  2. **Partial Updates Table**:
     - Contains updates where an `id` is provided, representing updates to known internal products.
     - Additional fields (e.g., `supplier_id`, `price`) may be specified for update, but only non-null values will overwrite the corresponding fields in the database.

### 3. Merging Updates
- **Full Updates**:
  - Products matching the `supplier_id` are fully updated with all fields from the full updates table.
- **Partial Updates**:
  - Products matching the `id` are updated only for the fields provided in the partial updates table.
  - Fields with `NULL` values in the partial updates table are not overwritten.

### 4. Efficiency Goals
- Updates are performed in bulk by merging the temporary tables with the main `products` table.
- The process avoids excessive database round trips and reduces the need for in-memory calculations.

---

## Test Files

We create the following products:

id | supplier_id  | price \
-------------------------- \
1  | SUPPLIER-1-1 | 199.99 \
2  | SUPPLIER-1-2 | 299.99 \
3  | SUPPLIER-1-3 | 399.99 \
4  | SUPPLIER-2-1 | 499.99 \
5  | SUPPLIER-2-2 | 599.99

We then do the following vendor updates

1. update SUPPLIER-1-1's price to 1099.99
2. update SUPPLIER-1-2's price to 2099.99
3. update SUPPLIER-1-3's price to 5099.99
4. insert SUPPLIER-NEW-1 with price 25.52
5. insert SUPPLIER-NEW-2 with price 3.14
6. update product 4 (SUPPLIER-2-1) with new supplier_id SUPPLIER-NEW-3
7. update product 5 (SUPPLIER-2-2) with new supplier_id SUPPLIER-NEW-4 and new price 3.14 (notice here we supply an updated price and above we do not)

Final state should be

id | supplier_id  | price \
-------------------------- \
1  | SUPPLIER-1-1 | 1099.99 \
2  | SUPPLIER-1-2 | 2099.99 \
3  | SUPPLIER-1-3 | 5099.99 \
4  | SUPPLIER-NEW-3 | 499.99 \
5  | SUPPLIER-NEW-4 | 3.14 \
6  | SUPPLIER-NEW-1 | 25.52 \
7  | SUPPLIER-NEW-2 | 3.14

**Generated with the help of OpenAI's ChatGPT.**
