# Data Structure Planning

## Tables

### User
- user_id
- email
- first_name
- last_name
- user_type
- password_hash

### Mood
- user_id
- mood_id (primary,unique)
- app_name
- app_type
- time_spent
- mood (emoji unicode)
  
### Hours
- user_id (foreign)
- procrastination_hours (view, sum of mood.time_spent group by app_type)
- gaming_hours (view, sum of mood.time_spent group by app_type)
- productive_hours (view, sum of mood.time_spent group by app_type)

### Receipts
Does not query/link to other table so it becomes a "snapshot" of the past.
- receipt_id
- author_id (foreign, user_id)
- procrastination_spent
- gaming_spent
- productive_spent

### ReceiptsShared
- author_id (foreign)
- receiver_id (foreign)
- receipt_id (foreign)

# Redundancy Zone
Held off for later. Pray to god they see the light again.

- uid (foreign key)
- event_id (primary unique)
- event_name (string)
- time_start (unix time? datetime?)
- time_end (for 1-hour blocks,etc, can be null)
- is_due (boolean)
- priority(?) (maybe ID 1=low 2=medium 3=high?)
