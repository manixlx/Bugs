const express = require("express");
const db = require("../db");

const router = express.Router();

router.get("/customers", async (req, res, next) => {
    try {
        const term = String(req.query.q || "").trim();
        const activeOnly = req.query.active === "true";

        if (term.length < 2) {
            return res.status(400).json({ error: "Search term must contain at least two characters" });
        }

        let sql =
            "SELECT id, email, full_name, status " +
            "FROM customers " +
            "WHERE full_name ILIKE '%" + term + "%'";

        if (activeOnly) sql += " AND status = 'active'";
        sql += " ORDER BY full_name LIMIT 50";

        const result = await db.query(sql);
        res.json({ count: result.rows.length, results: result.rows });
    } catch (err) {
        next(err);
    }
});

router.get("/orders", async (req, res, next) => {
    try {
        const customerId = req.query.customerId;
        const result = await db.query(
            "SELECT id, customer_id, total, status, created_at " +
            "FROM orders WHERE customer_id = $1 ORDER BY created_at DESC",
            [customerId]
        );
        res.json(result.rows);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
