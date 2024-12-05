const logger = require('../util/log-util');

module.exports = (err, req, res, next) => {
    const errStatus = err.statusCode || err.response?.status || 500;
    const errMsg = err.message || err.response?.data.detail || 'Something went wrong';
    logger.error(`Some error occurred: ${errMsg}`);
    logger.error(err.stack);

    if (err.name === 'APIError') {
      return res.status(500).json({
        STATUS: 'FAIL',
        STATUSCODE: 500,
        message: 'Something went wrong. Please try again later.',
      });
    } else if (err.name === 'ConnectionError') {
      return res.status(500).json({
        STATUS: 'FAIL',
        STATUSCODE: 500,
        message: 'Something went wrong. Please try again later.',
      });
    }
  
    res.status(errStatus).json({
      STATUS: 'FAIL',
      STATUSCODE: errStatus,
      message: errMsg,
    });
  };