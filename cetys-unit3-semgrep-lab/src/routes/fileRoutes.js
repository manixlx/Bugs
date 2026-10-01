const express = require("express");
const fs = require("fs");
const path = require("path");

const router = express.Router();
const DOCUMENT_ROOT = path.join(__dirname, "..", "..", "documents");

router.get("/download", (req, res, next) => {
    try {
        const requested = String(req.query.name || "");
        if (!requested) return res.status(400).json({ error: "name query parameter is required" });

        const fullPath = path.join(DOCUMENT_ROOT, requested);
        if (!fs.existsSync(fullPath)) return res.status(404).json({ error: "File not found" });

        const data = fs.readFileSync(fullPath);
        res.setHeader("Content-Disposition", `attachment; filename="${path.basename(fullPath)}"`);
        res.send(data);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
