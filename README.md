# API SOS Contador - Descarga Masiva de Papeles de Trabajo

Aplicación de escritorio para la descarga masiva y automatizada de papeles de trabajo de IVA desde la plataforma SOS Contador, diseñada específicamente para facilitar la realización del formulario F2002.

## 📋 Descripción

Esta herramienta permite a contadores y profesionales del área tributaria automatizar el proceso de descarga de papeles de trabajo de IVA para múltiples contribuyentes desde la API de SOS Contador. La aplicación cuenta con una interfaz gráfica intuitiva desarrollada en Tkinter que simplifica el proceso de autenticación, gestión de contribuyentes y descarga masiva de documentación.

## ✨ Características

- **Interfaz gráfica amigable** con diseño moderno y navegación intuitiva
- **Autenticación automática** con la API de SOS Contador
- **Gestión de múltiples contribuyentes** mediante archivo CSV
- **Descarga masiva concurrente** de papeles de trabajo para optimizar el tiempo
- **Tokens de acceso individuales** por cada CUIT registrado
- **Organización automática** de archivos JSON por contribuyente, año y mes
- **Actualización semanal** de credenciales (los tokens se reinician cada lunes)

## 🚀 Instalación

### Requisitos Previos

- Python 3.7 o superior
- Cuenta activa en [SOS Contador](https://www.sos-contador.com/)
- Sistema operativo Windows (optimizado para Windows)

### Instalación de Dependencias

1. Clone o descargue este repositorio:
```bash
git clone https://github.com/usuario/API-SOS-público.git
cd API-SOS-público
```

2. Cree un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Active el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale las dependencias:
```bash
pip install -r requirements.txt
```

## 🔧 Configuración

### 1. Configurar Credenciales

Edite el archivo `bin/Login.json` con sus credenciales de SOS Contador:

```json
{
    "usuario": "su-email@ejemplo.com",
    "password": "su-contraseña"
}
```

**Nota de Seguridad:** No comparta este archivo ni lo suba a repositorios públicos con sus credenciales reales.

### 2. Configurar Contribuyentes

El archivo `contribuyentes.csv` se genera automáticamente al obtener los tokens de acceso. Este archivo contiene la siguiente estructura:

```
id|cuit|razon_social|año|mes|F2002|jwt
```

- **id**: Identificador interno del contribuyente
- **cuit**: Número de CUIT del contribuyente
- **razon_social**: Razón social del contribuyente
- **año**: Año del período a consultar
- **mes**: Mes del período a consultar
- **F2002**: Indicador SI/NO para procesar la descarga
- **jwt**: Token de autorización individual

## 📖 Uso

### Modo Interfaz Gráfica (Recomendado)

1. Ejecute la aplicación:
```bash
python app.py
```

2. Siga estos pasos en orden:

   **a) Configurar Credenciales**
   - Haga clic en "Abrir Credenciales"
   - Edite el archivo JSON con sus datos de acceso
   - Guarde y cierre el archivo

   **b) Obtener Tokens de Acceso**
   - Haga clic en "Obtener Tokens de Acceso"
   - El sistema generará automáticamente el archivo `contribuyentes.csv`
   - Los tokens individuales se guardarán en la carpeta `Token/`

   **c) Editar Lista de Contribuyentes (Opcional)**
   - Haga clic en "Editar CSV"
   - Modifique los períodos (año/mes) si es necesario
   - Cambie "SI" a "NO" en la columna F2002 para excluir contribuyentes

   **d) Descargar Papeles de Trabajo**
   - Haga clic en "Descarga Masiva de Papeles de Trabajo"
   - Los archivos se descargarán en la carpeta `F2002/`

   **e) Acceder a los Resultados**
   - Haga clic en "Abrir Carpeta F2002" para ver los archivos descargados

### Modo Línea de Comandos

Para usuarios avanzados que prefieran ejecutar el script directamente:

```bash
python bin/sos_api.py
```

Este comando ejecutará el proceso completo: obtención de tokens y descarga de papeles de trabajo.

## 📁 Estructura del Proyecto

```
API-SOS-público/
├── app.py                      # Punto de entrada principal
├── APPui.py                    # Interfaz gráfica de usuario
├── GUI.ui                      # Diseño de la interfaz (Qt Designer)
├── requirements.txt            # Dependencias del proyecto
├── contribuyentes.csv          # Lista de contribuyentes (auto-generado)
├── response.json              # Respuesta del login (auto-generado)
├── LICENSE                    # Licencia del proyecto
├── bin/
│   ├── sos_api.py            # Módulo principal de la API
│   ├── Login.json            # Credenciales de acceso
│   ├── ABP-blanco-sin-fondo.png
│   ├── ABP-blanco-en-fondo-negro.ico
│   └── sos-contador_-small.png
├── Token/                     # Tokens individuales (auto-generado)
│   └── response_[CUIT]_[ID]_[RAZON_SOCIAL].json
├── F2002/                     # Papeles de trabajo descargados
│   └── F2002_[CUIT]_[RAZON_SOCIAL]_[AÑO]_[MES].json
└── Ejecutable/                # Versión compilada (opcional)
```

## 🔄 Flujo de Trabajo

1. **Autenticación**: El sistema se conecta a la API de SOS Contador con las credenciales del usuario
2. **Obtención de CUITs**: Se recuperan todos los contribuyentes asociados a la cuenta
3. **Generación de Tokens**: Se genera un token JWT individual para cada contribuyente
4. **Almacenamiento**: Los tokens se guardan tanto en archivos JSON como en el CSV
5. **Consulta**: Se realiza una consulta GET por cada contribuyente para obtener el listado de IVA
6. **Descarga Concurrente**: Se descargan múltiples papeles de trabajo simultáneamente
7. **Organización**: Los archivos se guardan con nomenclatura estándar para fácil identificación

## ⚙️ Dependencias

- **requests** (2.32.3): Manejo de peticiones HTTP a la API
- **certifi** (2024.8.30): Validación de certificados SSL
- **charset-normalizer** (3.4.0): Detección de codificación de caracteres
- **idna** (3.10): Soporte para dominios internacionalizados
- **urllib3** (2.2.3): Cliente HTTP de bajo nivel
- **tkinter**: Interfaz gráfica (incluido en Python estándar)

## 🐛 Solución de Problemas

### Error de Autenticación
- Verifique que sus credenciales en `bin/Login.json` sean correctas
- Asegúrese de tener conexión a internet
- Compruebe que su cuenta de SOS Contador esté activa

### Tokens Expirados
- Los tokens de SOS Contador se reinician cada lunes
- Vuelva a ejecutar "Obtener Tokens de Acceso" para renovarlos

### Descarga Incompleta
- Verifique que el campo "F2002" esté en "SI" para los contribuyentes deseados
- Compruebe que los períodos (año/mes) sean válidos
- Revise su conexión a internet durante el proceso

### Error al Abrir la Carpeta F2002
- Asegúrese de que existan archivos descargados en la carpeta
- Verifique los permisos de escritura en el directorio del proyecto

## 📝 Notas Importantes

- **Seguridad**: Nunca comparta sus credenciales o tokens de acceso
- **Actualización**: Los tokens deben renovarse semanalmente (cada lunes)
- **Período**: Por defecto, se consulta el mes anterior a la fecha actual
- **Formato**: Los archivos se descargan en formato JSON para máxima compatibilidad
- **Rendimiento**: La descarga concurrente optimiza el tiempo de ejecución

## 📜 Licencia

Este proyecto está bajo una **Licencia Pública con Restricciones Comerciales** (versión 1.0). Puntos clave:

- ✅ Distribución gratuita obligatoria
- ✅ Código abierto con acceso completo al código fuente
- ✅ Permitidas modificaciones y redistribución (gratuitas)
- ✅ Uso personal permitido
- ❌ Prohibida la venta o intercambio monetario del software

Ver archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Agustín Bustos Piasentini**

- Sitio web: [www.Agustin-Bustos-Piasentini.com.ar](https://www.Agustin-Bustos-Piasentini.com.ar/)
- Email: bustos-agustin@hotmail.com

## ☕ Donaciones

Si esta herramienta te ha sido útil y deseas apoyar su desarrollo, puedes hacer una donación en:

**[Cafecito.app/abustos](https://cafecito.app/abustos)**

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haga fork del repositorio
2. Cree una rama para su característica (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades, por favor abra un issue en el repositorio o contacte al autor directamente.

## 🔗 Enlaces Útiles

- [SOS Contador](https://www.sos-contador.com/) - Plataforma oficial
- [API SOS Contador](https://api.sos-contador.com/) - Documentación de la API
- [AFIP](https://www.afip.gob.ar/) - Administración Federal de Ingresos Públicos

---

**Nota**: Este proyecto no está afiliado oficialmente con SOS Contador. Es una herramienta independiente desarrollada para facilitar el trabajo de profesionales contables.
