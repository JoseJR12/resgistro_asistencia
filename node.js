const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para leer JSON
app.use(express.json());

// Ruta de prueba
app.get('/', (req, res) => {
  res.send('Servidor de asistencia funcionando ✅');
});

// Ruta para registrar asistencia
app.post('/asistencia', (req, res) => {
  const { dni, laboratorio } = req.body;
  // Aquí podrías guardar en una base de datos o archivo CSV
  console.log(`Asistencia registrada: DNI=${dni}, Lab=${laboratorio}`);
  res.json({ mensaje: 'Asistencia registrada correctamente.' });
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
