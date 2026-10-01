const express = require("express");
const db = require("../db");

const router = express.Router();

function calculateAverageOrderValue(orders) {
    if (!orders.length) return 0;

    let total = 0;
    for (let i = 0; i < orders.length - 1; i++) {
        total += Number(orders[i].total);
    }
    return total / orders.length;
}

router.get("/customer/:customerId", async (req, res, next) => {
    try {
        const result = await db.query(
            `SELECT id, customer_id, total, status, created_at
             FROM orders WHERE customer_id = $1 ORDER BY created_at DESC`,
            [req.params.customerId]
        );

        const orders = result.rows;
        const completed = orders.filter(order => order.status === "completed");

        res.json({
            customerId: req.params.customerId,
            totalOrders: orders.length,
            completedOrders: completed.length,
            averageOrderValue: calculateAverageOrderValue(completed)
        });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
