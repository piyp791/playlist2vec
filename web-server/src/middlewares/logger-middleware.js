const logger = require('../util/log-util');
const url = require('url');

const ENDPOINTS_EXCLUDED = ['.js', '.map', '.woff', 'woff?v=3.2.1',
  '.png', '.jpeg', '.jpg', '.ico', '.css', '.svg', '.webp'];

module.exports = (req, res, next) => {
  if (!!req.url && !ENDPOINTS_EXCLUDED.some((ext) => req.url.endsWith(ext))) {
    const randomId = (Math.random() + 1).toString(36).substring(2);
    req.requestId = randomId;
    logger.info(`Endpoint hit  ${req.url}  ${req.method} -- ${new Date()}`, {
      requestid: req.requestId,
      endpoint: url.parse(req.url).pathname,
      user_agent: { original: req.headers['user-agent'] },
    });
  }
  next();
};