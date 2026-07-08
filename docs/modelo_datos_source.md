# Modelo de datos fuente

Este documento describe el modelo relacional inicial que uso para simular la operacion transaccional de RetailMax.

## Convencion de nombres

Para el codigo propio uso nombres en espanol, especialmente en funciones, variables de control y argumentos de ejecucion. En cambio, en las tablas fuente mantengo nombres fisicos de columnas en ingles, como `sale_id`, `product_id`, `store_id` y `net_amount`.

Tome esta decision porque esas columnas representan el contrato tecnico de la fuente simulada. En un proyecto real es comun recibir sistemas origen con nombres en ingles, y lo importante para el pipeline es documentarlos, validarlos y transformarlos de forma consistente.

## Entidades principales

### `source.mstr_proveedores`

Representa proveedores de productos.

Campos principales:

- `supplier_id`: identificador del proveedor.
- `supplier_name`: nombre del proveedor.
- `country`: pais de origen.
- `category_specialty`: categoria principal que abastece.
- `lead_time_days`: tiempo promedio de entrega.
- `reliability_score`: indicador sintetico de confiabilidad.

### `source.mstr_articulos`

Representa el catalogo de productos.

Campos principales:

- `product_id`: identificador del producto.
- `sku`: codigo comercial.
- `product_name`: nombre del producto.
- `category` y `subcategory`: clasificacion comercial.
- `supplier_id`: proveedor asociado.
- `unit_cost`: costo unitario.
- `unit_price`: precio de venta.

Relacion principal:

- `supplier_id` se relaciona con `source.mstr_proveedores`.

### `source.mstr_tiendas`

Representa tiendas fisicas, canales digitales y puntos omnicanal.

Campos principales:

- `store_id`: identificador de la tienda o canal.
- `store_name`: nombre del punto de venta.
- `city`: ciudad.
- `region`: region comercial.
- `store_format`: tipo de operacion: tienda fisica, ecommerce u omnicanal.

### `source.crm_miembros`

Representa clientes registrados en el programa de fidelizacion.

Campos principales:

- `customer_id`: identificador del cliente.
- `member_code`: codigo de membresia.
- `email`: correo sintetico.
- `gender`: genero declarado.
- `birth_date`: fecha de nacimiento.
- `loyalty_segment`: segmento de fidelizacion.
- `registration_date`: fecha de registro.

### `source.trans_ventas`

Representa transacciones de venta.

Campos principales:

- `sale_id`: identificador de venta.
- `sale_date`: fecha de venta.
- `store_id`: punto o canal de venta.
- `customer_id`: cliente asociado, puede ser nulo en compras de invitado.
- `product_id`: producto vendido.
- `quantity`: cantidad vendida.
- `unit_price`: precio unitario.
- `discount_rate`: descuento aplicado.
- `net_amount`: valor neto de la venta.
- `order_status`: estado de la orden.

Relaciones principales:

- `store_id` se relaciona con `source.mstr_tiendas`.
- `customer_id` se relaciona con `source.crm_miembros`, cuando existe.
- `product_id` se relaciona con `source.mstr_articulos`.

### `source.inv_stock_diario`

Representa inventario diario por tienda y producto.

Campos principales:

- `inventory_id`: identificador del registro de inventario.
- `snapshot_date`: fecha del corte.
- `store_id`: tienda o canal.
- `product_id`: producto.
- `stock_on_hand`: unidades disponibles.
- `reorder_point`: punto de reorden.
- `stock_status`: estado del inventario.

Relaciones principales:

- `store_id` se relaciona con `source.mstr_tiendas`.
- `product_id` se relaciona con `source.mstr_articulos`.

### `source.post_devoluciones`

Representa devoluciones posteriores a una venta.

Campos principales:

- `return_id`: identificador de la devolucion.
- `sale_id`: venta original.
- `return_date`: fecha de devolucion.
- `product_id`: producto devuelto.
- `returned_quantity`: cantidad devuelta.
- `return_reason`: motivo de devolucion.
- `refund_amount`: valor devuelto al cliente.

Relacion principal:

- `sale_id` se relaciona con `source.trans_ventas`.

## Decisiones relevantes

- El modelo separa maestros, transacciones e inventario para simular una fuente operativa realista.
- Algunas ventas tienen `customer_id` nulo para representar compras de invitado.
- Algunas ventas incluyen anomalias controladas, como cantidades invalidas o descuentos extremos, para probar reglas de calidad en Silver.
- Los datos personales son sinteticos y no representan personas reales.
