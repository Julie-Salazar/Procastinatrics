# Data Structure Planning

## Tables

### User
> user_id
> email
> first_name
> last_name
> user_type
> password_hash

### Events
There might be redundancy violations here - to be refined and adjusted.

> uid (foreign key)
> event_id (primary unique)
> event_name (string)
> time_start (unix time? datetime?)
> time_end (for 1-hour blocks,etc, can be null)
> is_due (boolean)
> priority(?) (maybe ID 1=low 2=medium 3=high?)

## Classes

### User
- db-facing object(?)

### Events
> ``Events.__init__()``
> ``Events.function()``

### Assignment
Extends ``Events``
> ``Assignment.__init__()``


