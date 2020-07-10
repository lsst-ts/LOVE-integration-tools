describe('Given the user just submitted its credentials', function () {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      // browser with a 720p monitor
      cy.viewport(1920, 1080);
    });

    it('When accepted it should display the Component Index screen', function () {
      cy.visit('/');
      cy.url().should('include', '/login');
      cy.get('#id_username').type('test');
      cy.get('#id_password').type('test_linode');
      cy.get('button').contains('Login').click();
      cy.url().should('not.include', 'login');
      cy.root().should('contain', 'Create new view');
      cy.document().toMatchImageSnapshot({
        threshold: 0.001,
      });
    });
  });

  it('When rejected it should display a warning message', async function () {
    cy.visit('/');
    cy.url().should('include', '/login');
    cy.get('#id_username').type('asdf');
    cy.get('#id_password').type('asdf');
    cy.get('button').contains('Login').click();
    cy.root().should(
      'contain',
      'Your username and password did not match, please try again'
    );
    cy.document().toMatchImageSnapshot({
      threshold: 0.001,
    });
  });
  it('Logout works', function () {
    cy.visit('/');
    cy.get('#id_username').type('test');
    cy.get('#id_password').type('test_linode');
    cy.get('button').contains('Login').click();

    cy.url().should('not.include', 'login');
    cy.get('button').get('[title=Settings]').click();
    cy.get('button').contains('Logout').click();
    cy.visit('/auxiliary-telescope');
    cy.url().should('include', '/login');
    cy.document().toMatchImageSnapshot({
      threshold: 0.001,
    });
  });

  it('If the token expired before logging in it should display a warning message', function () {
    localStorage.setItem('LOVE-TOKEN', 'asdf');
    cy.visit('/auxiliary-telescope');
    cy.root().should(
      'contain',
      'Your session has expired, you have been logged out'
    );
    cy.document().toMatchImageSnapshot({
      threshold: 0.001,
    });
  });
});
