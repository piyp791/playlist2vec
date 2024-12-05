const winston = require('winston');
const fs = require('fs');
const ecsFormat = require('@elastic/ecs-winston-format');
require('winston-daily-rotate-file');

const logDir = 'src/logs';

// Set up Logging==========================================
// Create the log directory if it does not exist
if (!fs.existsSync(logDir)) { fs.mkdirSync(logDir); }
const tsFormat = () => (new Date()).toLocaleTimeString();

const addSourceFormat = winston.format((info) => {
  info.source_application = 'web-server';
  return info;
})();

const fileTransport = new winston.transports.DailyRotateFile({
  filename: `${logDir}/webserver.-%DATE%.log`,
  datePattern: 'YYYY-MM-DD-HH',
  maxSize: '5m',
  timestamp: tsFormat,
  colorize: true,
  level: 'debug',
});

const logger = winston.createLogger({
  format: winston.format.combine(
    addSourceFormat,
    ecsFormat(),
  ),
  transports: [
    new (winston.transports.Console)({
      timestamp: tsFormat,
      colorize: true,
      level: 'debug',
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple(),
      ),
    }),
    fileTransport,
  ],
});

module.exports = logger;