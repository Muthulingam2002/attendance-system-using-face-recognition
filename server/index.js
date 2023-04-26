const express = require("express");
const app = express();
const cors = require("cors");
const { Pool } = require("pg");
app.use(express.json());
app.use(cors());

const pool = new Pool({
    user: "postgres",
    host: "localhost",
    password: "kalam",
    port: 5432,
    database: "mydatabase",
});

app.get("/", async (req, res) => {
    try {
        const data = await pool.query("select name,max(time) as time from mytable group by name");
        res.json(data.rows);
    } catch (err) {
        console.log(err);
    }
});
app.listen(3000, (req, res) => {
    console.log("Server is listening to port 3000...");
});
