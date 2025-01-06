const axios = require('axios');
const url = require('url');
const logger = require('./log-util');
const ConnectionError = require('../errors/connection-error');
const APIError = require('../errors/api-error');

module.exports = {
  async requestUrl(resourceLocator, method, req, data) {

    const metaInfo = {
      endpoint: url.parse(req.url).pathname,
      requestid: req.requestId,
    };

    const config = {
      headers: metaInfo,
    };

    const userAgent = req.headers['user-agent'];
    const recEnginePayload = {
      ...metaInfo,
      ...(data ?? {}),
      ...{ user_agent: { original: userAgent } },
    };
    logger.info(`Sending request to URL : ${resourceLocator} with payload ${JSON.stringify(recEnginePayload)}`);
    return axios.get(resourceLocator, config)
    .catch((err) => {
      // possible error codes: 400, 500
      if (err.response && (err.response.status === 500 || err.response.status === 400)) {
        throw new APIError(`API call failed with error code: ${err.response.code} :: ${JSON.stringify(err.response.data)}`);
      }
      else {
        const statusCode = err?.response?.status ?? 0;
        throw new ConnectionError(`Error in sending request to URL : ${resourceLocator} :: Error code: ${statusCode} :: Payload ${JSON.stringify(recEnginePayload)}`);
      }
    });
  },
};