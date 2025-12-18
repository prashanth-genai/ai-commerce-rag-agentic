@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping("/{userId}")
    public Map<String, Object> getOrder(@PathVariable String userId) {
        return Map.of(
            "orderId", "ORD12345",
            "status", "SHIPPED",
            "deliveryDate", "2025-10-25"
        );
    }
}

