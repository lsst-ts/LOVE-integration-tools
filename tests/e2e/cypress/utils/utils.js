export const login = () => {
  cy.visit('/');
  cy.url().should('include', '/login');
  cy.get('#id_username').type('test');
  cy.get('#id_password').type('test_linode');
  cy.get('button').contains('Login').click();
  cy.url().should('not.include', 'login');
  return cy
    .root()
    .should('contain', 'Create new view')
    .then(() => {
      expect(localStorage.getItem('LOVE-TOKEN')).to.not.equal(null);
      return localStorage.getItem('LOVE-TOKEN');
    });
};

export const requestToken = (callback) => {
  const url = '/manager/api/get-token/';
  const data = {
    username: 'test',
    password: 'test_linode',
  };
  return fetch(url, {
    method: 'POST',
    headers: new Headers({
      Accept: 'application/json',
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((response) => {
      const { token } = response;
      callback(token);
      return token;
    });
};

export const getViews = (callback) => {
  const data = {
    username: 'test',
    password: 'test_linode',
  };
  cy.request({
    url: '/manager/api/get-token/',
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .its('body')
    .then((body) => body.token)
    .then((token) => {
      console.log('token', token);
      return cy.request({
        url: '/manager/ui_framework/views/summary/',
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
      });
    })
    .its('body')
    .then((views) => {
      console.log('views', views);
      views = views;
      callback(views);
      return views;
    });
};
