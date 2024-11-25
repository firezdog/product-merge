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

**Generated with the help of OpenAI's ChatGPT.**
