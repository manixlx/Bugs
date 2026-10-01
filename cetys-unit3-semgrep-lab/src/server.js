const express = require("express");
const accountRoutes = require("./routes/accountRoutes");
const searchRoutes = require("./routes/searchRoutes");
const projectRoutes = require("./routes/projectRoutes");
const diagnosticsRoutes = require("./routes/diagnosticsRoutes");
const fileRoutes = require("./routes/fileRoutes");
const reportRoutes = require("./routes/reportRoutes");

const app = express();
app.use(express.json());
app.use("/api/accounts", accountRoutes);
app.use("/api/search", searchRoutes);
app.use("/api/projects", projectRoutes);
app.use("/api/diagnostics", diagnosticsRoutes);
app.use("/api/files", fileRoutes);
app.use("/api/reports", reportRoutes);

app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({ error: "Unexpected server error", detail: err.message });
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Lab API listening on port ${port}`));
