const httpUtil = require('../util/http-util');
const config = process.env.NODE_ENV === 'production' ? require('../config.json') : require('../config.dev.json');
const validations = require('../validator');

const SEARCH_ENGINE_URL = `${config.search_engine_host}:${config.search_engine_port}`;
const AUTOCOMPLETE_ENGINE_URL = `${config.autocomplete_engine_host}:${config.autocomplete_engine_port}`;

module.exports = (app) => {
    app.get('/', async (req, res, next) => {
        res.status(200).render('index');
    });

    app.get('/data', async (req, res, next) => {
        res.status(200).render('data');
    });

    app.get('/demo', async (req, res, next) => {
        res.status(200).render('demo');
    });

    app.get('/populate',
        [validations.checkSearchTerm],
        validations.validate,
        async (req, res, next) => {
            try {
                let prefix = req.query.term;
                const populateResp = await httpUtil.requestUrl(`${AUTOCOMPLETE_ENGINE_URL}/populate?term=${prefix}`, 'GET', req);
                res.json(populateResp.data);
            } catch (err) {
                next(err);
            }
        });

    app.get('/search',
        [validations.checkSearchId],
        validations.validate,
        async (req, res, next) => {
            try {
                let id = req.query.q;
                const searchResp = await httpUtil.requestUrl(`${SEARCH_ENGINE_URL}/search?id=${id}&is_random=False`, 'GET', req);
                res.json(searchResp.data)
            } catch (err) {
                next(err);
            }
        });

    app.get('/search-random', async (req, res, next) => {
        try {
            const searchResp = await httpUtil.requestUrl(`${SEARCH_ENGINE_URL}/search?is_random=True`, 'GET', req);
            res.json(searchResp.data);
        } catch (err) {
            next(err);
        }
    });

    app.get('/health', (req, res, next) => {
        res.status(200).json({status: 'healthy'});
    });
}
