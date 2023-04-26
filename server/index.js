/* This is a Node.js code that creates a server using the Express framework and listens to port 3000.
It also uses the `cors` middleware to enable cross-origin resource sharing and the `pg` library to
connect to a PostgreSQL database. The `app.get()` method defines a route for the root URL and
executes a SQL query to retrieve data from the database. The retrieved data is then sent as a JSON
response to the client. */
const express = require("express");
const app = express();
const cors = require("cors");
const { Pool } = require("pg");
app.use(express.json());
app.use(cors());

/* This code creates a new instance of the `Pool` class from the `pg` library, which is used to connect
to a PostgreSQL database. The `Pool` class manages a pool of client connections to the database,
allowing multiple clients to execute queries simultaneously. The object passed to the `Pool`
constructor contains the configuration options for connecting to the database, including the
username, host, password, port, and database name. */
const pool = new Pool({
    user: "postgres",
    host: "localhost",
    password: "kalam",
    port: 5432,
    database: "mydatabase",
});

/* This code defines a route for the root URL ("/") using the `app.get()` method of the Express
framework. When a client makes a GET request to the root URL, the code executes an asynchronous
function that queries a PostgreSQL database using the `pool.query()` method of the `pg` library. The
SQL query retrieves the `name` and `max(time)` columns from a table named `mytable`, groups the
results by `name`, and returns the result set as an array of objects. The retrieved data is then
sent as a JSON response to the client using the `res.json()` method of the Express framework. If an
error occurs during the execution of the function, the error is logged to the console using the
`console.log()` method. */
app.get("/", async (req, res) => {
    try {
        const data = await pool.query("select name,max(time) as time from mytable group by name");
        res.json(data.rows);
    } catch (err) {
        console.log(err);
    }
});
/* `app.listen(3000, (req, res) => { console.log("Server is listening to port 3000..."); });` is
starting the server and listening to incoming requests on port 3000. When the server starts
successfully, it logs a message to the console indicating that it is listening to port 3000. */
app.listen(3000, (req, res) => {
    console.log("Server is listening to port 3000...");
});
