const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
app.use(cors());
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'html')));
const markdownDir = path.join(__dirname, 'markdown');

app.get('/files', (req, res) => {
    fs.readdir(markdownDir, (err, files) => {
        res.json({files});
    });
});

app.listen(PORT,()=>{
    console.log("Servidor en el puerto 3000");
});
