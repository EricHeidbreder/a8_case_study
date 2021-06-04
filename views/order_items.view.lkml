

view: order_items {
  sql_table_name: "PUBLIC"."ORDER_ITEMS" ;;
  drill_fields: [id] 
  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}."ID" ;;
    label: "SOMETHING NEW" 
  }
  dimension: inventory_item_id { type: number  sql: ${TABLE}."INVENTORY_ITEM_ID" ;; }
  dimension: order_id { type: number  sql: ${TABLE}."ORDER_ID" ;; }
  dimension: sale_price { type: number  sql: ${TABLE}."SALE_PRICE" ;; }
  dimension: status { type: string  sql: ${TABLE}."STATUS" ;; }
  dimension: user_id { type: number  sql: ${TABLE}."USER_ID" ;; } 
  dimension_group: created {
    type: time
    timeframes: [
      raw, 
      time, 
      date, 
      week, 
      month, 
      quarter, 
      year
      ]
    sql: ${TABLE}."CREATED_AT" ;; 
  }
  dimension_group: delivered {
    type: time
    timeframes: [
      raw, 
      time, 
      date, 
      week, 
      month, 
      quarter, 
      year
      ]
    sql: ${TABLE}."DELIVERED_AT" ;; 
  }
  dimension_group: returned {
    type: time
    timeframes: [
      raw, 
      time, 
      date, 
      week, 
      month, 
      quarter, 
      year
      ]
    sql: ${TABLE}."RETURNED_AT" ;; 
  }
  dimension_group: shipped {
    type: time
    timeframes: [
      raw, 
      time, 
      date, 
      week, 
      month, 
      quarter, 
      year
      ]
    sql: ${TABLE}."SHIPPED_AT" ;; 
  } 
  measure: count { type: count  drill_fields: [detail*] } 
  set: detail {  fields: [
      id, 
      inventory_items.product_name, 
      inventory_items.id, 
      users.last_name, 
      users.first_name, 
      users.id
      ] } 
}
