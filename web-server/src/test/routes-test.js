const chai = require('chai');
const chaiHttp = require('chai-http');
const { expect } = require('chai');
const supertest = require('supertest');
const server = require('../index');

const request = supertest(server);

chai.use(chaiHttp);

describe('/populate', () => {
  const inValidTests = [
    { q: '', expected: 500 },
    { q: 'term=  ', expected: 500 },
    { q: 'term=1111111321312312312312313123123123123123123123123123123123123123123123123123asdasdasdasdewdcsacasxasa', expected: 500 },
  ];

  inValidTests.forEach(({ q, expected }) => {
    it(`should return 500 error when query is: ${q}`, async () => {
      const response = await request.get(`/populate?${q}`);
      const jsonResp = JSON.parse(response.text);
      expect(response.statusCode).to.equal(expected);
      expect(jsonResp.message).contains('Validation Error');
    });
  });

  it('should return valid results given proper input', async () => {
    const response = await request.get('/populate?term=indie');
    const jsonResp = JSON.parse(response.text);
    expect(response.statusCode).to.equal(200);
    expect(jsonResp.count).to.greaterThan(0);
  });


  it('should return valid results given proper input with no results', async () => {
    const response = await request.get('/populate?term=dasdasdasdasdasdasda');
    const jsonResp = JSON.parse(response.text);
    console.log(JSON.stringify(jsonResp));
    expect(response.statusCode).to.equal(200);
    expect(jsonResp.count).to.equal(0);
  });
});

describe('/search', () => {
  const inValidTests = [
    { q: '123123123', expected: 500 },
    { q: 'q=  ', expected: 500 },
    { q: 'q=-1231231231', expected: 500 },
    { q: 'q=bryan adams', expected: 500 },
  ];

  inValidTests.forEach(({ q, expected }) => {
    it(`should return 500 error when invalid input ${q}`, async () => {
      const response = await request.get(`/search?${q}`);
      const jsonResp = JSON.parse(response.text);
      expect(response.statusCode).to.equal(expected);
      expect(jsonResp.message).contains('Validation Error');
    });
  });

  it('should return 200 when proper input', async () => {
    const response = await request.get('/search?q=34');
    expect(response.statusCode).to.equal(200);
  });
});


describe('/search-random', () => {
  it(`should return valid results`, async () => {
    const response = await request.get(`/search-random/`);
    expect(response.statusCode).to.equal(200);
  });
});
