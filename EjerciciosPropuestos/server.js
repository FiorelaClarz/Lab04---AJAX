const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");
const cors = require("cors");
const app = express();
app.use(cors());
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname,"html")));
const markdownDir = path.join(__dirname,"markdown");

app.get("/files",(req,res) => {
    fs.readdir(markdownDir,(err,files) => {
        res.json({files});
    });
});

app.get("/file/:name",(req,res) => {
    const fileName = req.params.name;
    const filePath = path.join(markdownDir,fileName);
    fs.readFile(filePath,"utf8",(err,data) => {
        res.json({content:data});
    });
});

app.post('/crear', (req, res) => {
    const {name,txt } = req.body;
    const filePath = path.join(markdownDir, name);

    fs.writeFile(filePath,txt, (err) => {
    });
});


app.listen(PORT,()=>{
    console.log("Servidor en el puerto 3000");
});
