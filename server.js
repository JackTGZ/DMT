const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

let counts = {
  dengue: 0,
  malaria: 0,
};

app.use(bodyParser.json());

app.get('/api/counts', (req, res) => {
  res.json(counts);
});

app.post('/api/update-count', (req, res) => {
  const { type, value } = req.body;
  if (type && value !== undefined && !isNaN(value)) {
    counts[type] = Number(value);
    res.json({ success: true });
  } else {
    res.status(400).json({ success: false, error: 'Invalid data' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
