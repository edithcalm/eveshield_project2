const express = require('express');
const morgan = require('morgan');
const app = express();
const PORT = 5000;

app.use(morgan('dev'));
app.use(express.static('public')); // Serves index.html, CSS, JS

app.listen(PORT, () => {
  console.log(`EveShield frontend running at http://localhost:${PORT}`);
});
