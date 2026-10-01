const express = require("express");
const db = require("../db");

const router = express.Router();

router.get("/customers", async (req, res, next) => {
    try {
        const term = String(req.query.q || "").trim();
        if (term.length < 2) return res.status(400).json({ error: "Search term must contain at least two characters" });

        const result = await db.query(
            `SELECT id, email, full_name, status
             FROM customers
             WHERE full_name ILIKE $1
             ORDER BY full_name
             LIMIT 50`,
            [`%${term}%`]
        );

        res.json({ count: result.rows.length, results: result.rows });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
