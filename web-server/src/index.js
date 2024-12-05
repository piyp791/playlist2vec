const express = require('express');
const bodyParser = require('body-parser');
const compression = require('compression');

const logger = require('./util/log-util');
const errorHandlerMiddleware = require('./middlewares/error-middleware');
const loggerMiddleware = require('./middlewares/logger-middleware');

const environment = process.env.NODE_ENV;
const config = environment === 'production' ? require('./config.json') : require('./config.dev.json');
const cacheTime = config.static_resource_cache_time;

const FOLDER = environment === 'production' ? 'dist' : 'src/public';

const shouldCompress = (req, res) => {
  if (req.headers['x-no-compression']) { return false; }
  return compression.filter(req, res);
};

const app = express();
const port = process.env.PORT || config.default_port;

app.use(loggerMiddleware);
app.use(compression({ filter: shouldCompress }));

if (environment !== 'production') {
  app.use(express.static(FOLDER)), { maxAge: cacheTime };
}

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

app.set('views', `${__dirname}/views/`);
app.set('view engine', 'ejs');

require('./routes/routes')(app);

app.use(errorHandlerMiddleware);
app.listen(port);
logger.info(`App server started at port ${port}. Environment: ${environment}.`);

module.exports = app;