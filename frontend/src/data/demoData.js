export const demoProducts = [
  { id: 1, name: "Espresso Beans", current_stock: 18, unit: "kg", unit_cost: 520 },
  { id: 2, name: "House Blend Beans", current_stock: 15, unit: "kg", unit_cost: 480 },
  { id: 3, name: "Colombia Beans", current_stock: 12, unit: "kg", unit_cost: 540 },
  { id: 4, name: "Ethiopia Beans", current_stock: 10, unit: "kg", unit_cost: 560 },
  { id: 5, name: "Whole Milk", current_stock: 30, unit: "liter", unit_cost: 32 },
  { id: 6, name: "Oat Milk", current_stock: 22, unit: "liter", unit_cost: 45 },
  { id: 7, name: "Caramel Syrup", current_stock: 14, unit: "bottle", unit_cost: 85 },
  { id: 8, name: "Matcha Powder", current_stock: 7, unit: "kg", unit_cost: 650 },
];

export const demoAnalyses = {
  1: {
    product_name: "Espresso Beans",
    current_stock: 18,
    average_daily_sales: 6.5,
    recommendation:
      "Current stock is acceptable, but espresso demand should be monitored closely during peak days.",
  },
  2: {
    product_name: "House Blend Beans",
    current_stock: 15,
    average_daily_sales: 5.8,
    recommendation:
      "House Blend Beans show stable movement. Consider restocking soon to avoid falling below the comfort level.",
  },
  3: {
    product_name: "Colombia Beans",
    current_stock: 12,
    average_daily_sales: 4.9,
    recommendation:
      "Colombia Beans are moving steadily. A small replenishment is recommended in the next cycle.",
  },
  4: {
    product_name: "Ethiopia Beans",
    current_stock: 10,
    average_daily_sales: 4.2,
    recommendation:
      "Ethiopia Beans have lower remaining stock. It would be safer to prepare a restock plan soon.",
  },
  5: {
    product_name: "Whole Milk",
    current_stock: 30,
    average_daily_sales: 9.4,
    recommendation:
      "Whole Milk stock is currently sufficient, but weekend consumption may increase noticeably.",
  },
  6: {
    product_name: "Oat Milk",
    current_stock: 22,
    average_daily_sales: 8.7,
    recommendation:
      "Oat Milk demand is relatively high. Consider placing a new order before weekend demand increases.",
  },
  7: {
    product_name: "Caramel Syrup",
    current_stock: 14,
    average_daily_sales: 3.1,
    recommendation:
      "Caramel Syrup is in a comfortable range. No urgent action is required right now.",
  },
  8: {
    product_name: "Matcha Powder",
    current_stock: 7,
    average_daily_sales: 2.6,
    recommendation:
      "Matcha Powder stock is limited compared to recent movement. Early replenishment is recommended.",
  },
};