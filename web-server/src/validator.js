const {
  query, validationResult,
} = require('express-validator');

const checkSearchTerm = query('term').trim().notEmpty().isLength({ max: 50 });
const checkSearchId = query('q')
                      .trim()
                      .notEmpty()
                      .matches(/^[0-9]+$/)
                      .isInt({ min: 0 })
                      .isLength({ min: 1, max: 10 });

const validate = (req, res, next) => {
  const result = validationResult(req);
  if (!result.isEmpty()) throw new Error(`Validation Error::${JSON.stringify({ errors: result.array() })}`);

  return next();
};

module.exports = {
  validate,
  checkSearchTerm,
  checkSearchId,
};