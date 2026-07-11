# Modelo entidad-relación y modelo analítico

Este documento resume las relaciones principales del modelo fuente y cómo esas relaciones se convierten en un modelo analítico en Gold.

## Modelo relacional fuente

```mermaid
erDiagram
    MSTR_PROVEEDORES ||--o{ MSTR_ARTICULOS : abastece
    MSTR_ARTICULOS ||--o{ TRANS_VENTAS : vendido_en
    MSTR_TIENDAS ||--o{ TRANS_VENTAS : registra
    CRM_MIEMBROS ||--o{ TRANS_VENTAS : realiza
    TRANS_VENTAS ||--o{ POST_DEVOLUCIONES : genera
    MSTR_ARTICULOS ||--o{ INV_STOCK_DIARIO : tiene_stock
    MSTR_TIENDAS ||--o{ INV_STOCK_DIARIO : controla_stock

    MSTR_PROVEEDORES {
        string supplier_id PK
        string supplier_name
        string country
        double reliability_score
    }

    MSTR_ARTICULOS {
        string product_id PK
        string sku
        string supplier_id FK
        double unit_cost
        double unit_price
    }

    MSTR_TIENDAS {
        string store_id PK
        string store_name
        string city
        string region
    }

    CRM_MIEMBROS {
        string customer_id PK
        string member_code
        string email
        string loyalty_segment
    }

    TRANS_VENTAS {
        string sale_id PK
        date sale_date
        string store_id FK
        string customer_id FK
        string product_id FK
        double net_amount
    }

    INV_STOCK_DIARIO {
        string inventory_id PK
        date snapshot_date
        string store_id FK
        string product_id FK
        int stock_on_hand
    }

    POST_DEVOLUCIONES {
        string return_id PK
        string sale_id FK
        date return_date
        double refund_amount
    }
```

## Relaciones principales

| Relación | Explicación |
|---|---|
| Proveedor a producto | Un proveedor puede abastecer varios productos |
| Producto a venta | Un producto puede aparecer en muchas ventas |
| Tienda a venta | Una tienda o canal registra muchas ventas |
| Cliente a venta | Un cliente puede realizar muchas compras; también existen compras invitadas |
| Venta a devolución | Una venta puede generar una o varias devoluciones |
| Producto y tienda a inventario | El inventario se controla por producto, tienda y fecha |

## Modelo analítico Gold

En Gold uso un modelo orientado a análisis. La tabla central es `gold_fact_ventas`, y alrededor de ella quedan dimensiones para producto, tienda y cliente.

```mermaid
erDiagram
    GOLD_DIM_PRODUCTO ||--o{ GOLD_FACT_VENTAS : describe_producto
    GOLD_DIM_TIENDA ||--o{ GOLD_FACT_VENTAS : describe_tienda
    GOLD_DIM_CLIENTE ||--o{ GOLD_FACT_VENTAS : describe_cliente

    GOLD_DIM_PRODUCTO {
        string product_id PK
        string sku
        string product_name
        string category
        string supplier_id
        string supplier_name
    }

    GOLD_DIM_TIENDA {
        string store_id PK
        string store_name
        string city
        string region
        string store_format
    }

    GOLD_DIM_CLIENTE {
        string customer_id PK
        string member_code
        string loyalty_segment
        string email_hash
    }

    GOLD_FACT_VENTAS {
        string sale_id PK
        date sale_date
        string store_id FK
        string customer_id FK
        string product_id FK
        double net_amount_analitico
        double net_amount_after_returns
    }
```

## KPIs derivados

Además del modelo de dimensiones y hechos, construí tablas agregadas para facilitar el análisis:

- `gold_kpi_ventas_diarias`: ventas, descuentos y devoluciones por fecha y canal.
- `gold_kpi_inventario_diario`: productos agotados y en riesgo de quiebre por tienda y fecha.
- `gold_kpi_clientes_rfm`: recencia, frecuencia y valor monetario de clientes.

Estas tablas no reemplazan la tabla de hechos, sino que resumen preguntas de negocio frecuentes para que el consumo analítico sea más directo.
